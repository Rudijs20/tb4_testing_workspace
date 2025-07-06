# !/usr/bin/env python3
# !/bin/bash

import subprocess
import rclpy
import time
import csv
import os
from nav_msgs.msg import Odometry, Path
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator
from builtin_interfaces.msg import Time
from rclpy.task import Future
from rclpy.node import Node
from rosgraph_msgs.msg import Clock
from datetime import datetime
import threading
from rclpy.executors import SingleThreadedExecutor
from geometry_msgs.msg import PointStamped

class MetricsMonitor(Node):
    def __init__(self):
        super().__init__('metrics_monitor')

        self.global_count = 0
        self.local_count = 0
        self.global_sub = self.create_subscription(
            Path,
            '/plan',
            self.global_callback,
            10
        )
        # self.local_sub = self.create_subscription(
        #     Path,
        #     '/local_plan',          # use this for DWB
        #     self.local_callback,
        #     10
        # )
        self.local_sub = self.create_subscription(
            PointStamped,
            '/lookahead_point',  # use this for RPP
            self.local_callback,
            10
        )
        # self.local_sub = self.create_subscription(
        #     Path,
        #     '/optimal_trajectory',    # Use this for modified MPPI 
        #     self.local_callback,
        #     10
        # )

    def clock_callback(self, msg):
        self.latest_time = msg.clock.sec + msg.clock.nanosec * 1e-9
        if not self.first_time_received:
            self.first_time_received = True

    def global_callback(self, msg):
        self.global_count += 1

    def local_callback(self, msg):
        self.local_count += 1


def run_script(command):
    return subprocess.Popen(command, shell=True)

def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()
    # rviz_proc = subprocess.Popen(["ros2", "launch", "turtlebot4_viz", "view_navigation.launch.py"])
    battery_proc = subprocess.Popen(["ros2", "run", "battery_logger", "log_battery"])
    cmd_vel_proc = subprocess.Popen(["ros2", "run", "cmd_vel_tracker", "cmd_vel_logger"])

    filename = f"navigation_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    navigator.path_length = 0.0
    navigator.previous_position = None
    navigator.local_planner_changes = 0
    navigator.tracking_active = False

    def odom_callback(msg):
        if navigator.tracking_active:
            current_position = msg.pose.pose.position
            if navigator.previous_position is not None:
                dx = current_position.x - navigator.previous_position.x
                dy = current_position.y - navigator.previous_position.y
                navigator.path_length += (dx**2 + dy**2)**0.5
            navigator.previous_position = current_position
            
    navigator.create_subscription(Odometry, '/odom', odom_callback, 10)

    if navigator.getDockedStatus():
        navigator.info('Undocking before initializing pose')
        navigator.undock()

    initial_pose = navigator.getPoseStamped([3.36,-0.242], 200.45) 

    navigator.setInitialPose(initial_pose)
    navigator.waitUntilNav2Active()
    print("Navigatoinr is active.")

    # Different goal poses can be used to test the navigation in the 11th floor office:
    # goal_pose = navigator.getPoseStamped([32.111, -8.418], TurtleBot4Directions.EAST) # FAR LOCATOIN
    goal_pose = navigator.getPoseStamped([21.19, -13.18], TurtleBot4Directions.EAST) # MIDDLE LOCATOIN
    # goal_pose = navigator.getPoseStamped([2.2, -1.23], TurtleBot4Directions.EAST) # NEAR LOCATION

    navigator.path_length = 0.0
    navigator.previous_position = None
    navigator.local_planner_changes = 0
    navigator.tracking_active = True

    metrics_monitor = MetricsMonitor()
    executor = SingleThreadedExecutor()
    executor.add_node(metrics_monitor)
    executor.add_node(navigator)

    monitor_thread = threading.Thread(target=executor.spin, daemon=True)
    monitor_thread.start()

    start_time = time.time()

    print("Start time:", start_time)

    navigator.goToPose(goal_pose)

    i = 0
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print('ETA: {:.0f} seconds.'.format(
                feedback.estimated_time_remaining.sec +
                feedback.estimated_time_remaining.nanosec / 1e9), end='\r')
        i += 1
        time.sleep(0.1)

    result = navigator.getResult()
    if result == 0:
        navigator.info('Goal succeeded!')
    elif result == 1:
        navigator.info('Goal was canceled!')
    elif result == 2:
        navigator.info('Goal failed!')
    else:
        navigator.info('Goal has an invalid return status!')

    end_time = time.time()
    global_count = metrics_monitor.global_count
    local_count = metrics_monitor.local_count
    execution_time = end_time - start_time if start_time and end_time else 0.0

    print("End time:", end_time)
    print("Execution time:", execution_time)

    navigator.tracking_active = False

    battery_proc.terminate()
    cmd_vel_proc.terminate()
    # rviz_proc.terminate()

    results_dir = os.path.expanduser("~/ros2_ws/results")
    os.makedirs(results_dir, exist_ok=True)

    file_path = os.path.join(results_dir, filename)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Execution Time (s)', 'Path Length (m)', 'Local Planner Changes', 'Global Planner Changes'])
        writer.writerow([
            execution_time,
            navigator.path_length,
            local_count,
            global_count
        ])

    subprocess.run("pkill -f 'battery_logger|nav2_cpu_logger|cmd_vel_tracker'", shell=True)
    navigator.destroy_node()
    metrics_monitor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()