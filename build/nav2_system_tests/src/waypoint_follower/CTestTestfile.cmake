# CMake generated Testfile for 
# Source directory: /home/rudolfs/ros2_ws/src/navigation2/nav2_system_tests/src/waypoint_follower
# Build directory: /home/rudolfs/ros2_ws/build/nav2_system_tests/src/waypoint_follower
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(test_waypoint_follower "/usr/bin/python3" "-u" "/opt/ros/jazzy/share/ament_cmake_test/cmake/run_test.py" "/home/rudolfs/ros2_ws/build/nav2_system_tests/test_results/nav2_system_tests/test_waypoint_follower.xml" "--package-name" "nav2_system_tests" "--generate-result-on-success" "--env" "TEST_DIR=/home/rudolfs/ros2_ws/src/navigation2/nav2_system_tests/src/waypoint_follower" "BT_NAVIGATOR_XML=navigate_to_pose_w_replanning_and_recovery.xml" "--command" "/home/rudolfs/ros2_ws/src/navigation2/nav2_system_tests/src/waypoint_follower/test_case_py.launch")
set_tests_properties(test_waypoint_follower PROPERTIES  TIMEOUT "180" WORKING_DIRECTORY "/home/rudolfs/ros2_ws/build/nav2_system_tests/src/waypoint_follower" _BACKTRACE_TRIPLES "/opt/ros/jazzy/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/home/rudolfs/ros2_ws/src/navigation2/nav2_system_tests/src/waypoint_follower/CMakeLists.txt;1;ament_add_test;/home/rudolfs/ros2_ws/src/navigation2/nav2_system_tests/src/waypoint_follower/CMakeLists.txt;0;")
