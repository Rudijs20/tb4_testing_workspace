#!/usr/bin/env python3

# Copyright 2022 Clearpath Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @author Roni Kreinin (rkreinin@clearpathrobotics.com)

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

        self.clock_subscription = self.create_subscription(
            Clock,
            '/clock',
            self.clock_callback,
            10)
        self.latest_time = None
        self.first_time_received = False

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
        # self.local_sub = self.create_subscription(
        #     PointStamped,
        #     '/lookahead_point',  # use this for RPP
        #     self.local_callback,
        #     10
        # )
        self.local_sub = self.create_subscription(
            Path,
            '/optimal_trajectory',    # Use this for modified MPPI 
            self.local_callback,
            10
        )

    def clock_callback(self, msg):
        self.latest_time = msg.clock.sec + msg.clock.nanosec * 1e-9
        if not self.first_time_received:
            self.first_time_received = True

    def global_callback(self, msg):
        self.global_count += 1

    def local_callback(self, msg):
        self.local_count += 1

    # def get_time(self):
    #     if not self.first_time_received:
    #         self.get_logger().info('Waiting for first clock message...')
    #         while rclpy.ok() and not self.first_time_received:
    #             rclpy.spin_once(self, timeout_sec=0.1)
    #     return self.latest_time

    # def reset_counts(self):
    #     self.global_count = 0
    #     self.local_count = 0

def run_script(command):
    return subprocess.Popen(command, shell=True)

def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()

    cpu_proc = run_script("python3 /home/rudolfs/ros2_ws/nav2_cpu_logger.py")
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

    # def local_plan_callback(msg):
    #     if navigator.tracking_active:
    #         navigator.local_planner_changes += 1

    navigator.create_subscription(Odometry, '/odom', odom_callback, 10)
    # navigator.create_subscription(Path, '/controller_server/local_plan', local_plan_callback, 10)

    if not navigator.getDockedStatus():
        navigator.info('Docking before initializing pose')
        navigator.dock()

    initial_pose = navigator.getPoseStamped([1.7502, -0.2405], TurtleBot4Directions.NORTH_WEST)
    navigator.setInitialPose(initial_pose)
    navigator.waitUntilNav2Active()

    goal_pose = navigator.getPoseStamped([31.2465, -7.9053], TurtleBot4Directions.NORTH_WEST)
    # goal_pose = navigator.getPoseStamped([2.3, -1.5], TurtleBot4Directions.NORTH_WEST)

    navigator.undock()

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

    while metrics_monitor.latest_time is None:
        time.sleep(0.1)

    start_time = metrics_monitor.latest_time
    # metrics_monitor.reset_counts()

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

    end_time = metrics_monitor.latest_time
    global_count = metrics_monitor.global_count
    local_count = metrics_monitor.local_count
    execution_time = end_time - start_time if start_time and end_time else 0.0

    print("End time:", end_time)
    print("Execution time:", execution_time)

    navigator.tracking_active = False

    cpu_proc.terminate()
    battery_proc.terminate()
    cmd_vel_proc.terminate()

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