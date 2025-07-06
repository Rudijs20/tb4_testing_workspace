#!/usr/bin/env python3

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