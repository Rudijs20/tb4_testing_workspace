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

def run_script(command):
    return subprocess.Popen(command, shell=True)

def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()

    def odom_callback(msg):
        if navigator.tracking_active:
            current_position = msg.pose.pose.position
            if navigator.previous_position is not None:
                dx = current_position.x - navigator.previous_position.x
                dy = current_position.y - navigator.previous_position.y
                navigator.path_length += (dx**2 + dy**2)**0.5
            navigator.previous_position = current_position

    def local_plan_callback(msg):
        if navigator.tracking_active:
            navigator.local_planner_changes += 1

    navigator.create_subscription(Odometry, '/odom', odom_callback, 10)
    navigator.create_subscription(Path, '/controller_server/local_plan', local_plan_callback, 10)

    if not navigator.getDockedStatus():
        navigator.info('Docking before initializing pose')
        navigator.dock()

    initial_pose = navigator.getPoseStamped([1.7502, -0.2405], TurtleBot4Directions.NORTH_WEST)
    navigator.setInitialPose(initial_pose)
    navigator.waitUntilNav2Active()

    goal_pose = navigator.getPoseStamped([31.2465, -7.9053], TurtleBot4Directions.NORTH_WEST)

    navigator.undock()

    navigator.goToPose(goal_pose)

    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()