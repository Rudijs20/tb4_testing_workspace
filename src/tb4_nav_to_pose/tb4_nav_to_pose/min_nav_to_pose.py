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

import rclpy
import time
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator


def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()

    initial_pose = navigator.getPoseStamped([1.7502, -0.2405], TurtleBot4Directions.NORTH_WEST)
    navigator.setInitialPose(initial_pose)

    navigator.waitUntilNav2Active()
    print("Navigatoinr is active.")

    goal_pose = navigator.getPoseStamped([31.2465, -7.9053], TurtleBot4Directions.NORTH_WEST)

    print("Goal pose is set")

    navigator.undock()

    navigator.goToPose(goal_pose)

    time.sleep(3000)

    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()