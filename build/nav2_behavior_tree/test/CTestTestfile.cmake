# CMake generated Testfile for 
# Source directory: /home/rudolfs/ros2_ws/src/navigation2/nav2_behavior_tree/test
# Build directory: /home/rudolfs/ros2_ws/build/nav2_behavior_tree/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(test_bt_utils "/usr/bin/python3" "-u" "/opt/ros/jazzy/share/ament_cmake_test/cmake/run_test.py" "/home/rudolfs/ros2_ws/build/nav2_behavior_tree/test_results/nav2_behavior_tree/test_bt_utils.gtest.xml" "--package-name" "nav2_behavior_tree" "--output-file" "/home/rudolfs/ros2_ws/build/nav2_behavior_tree/ament_cmake_gtest/test_bt_utils.txt" "--command" "/home/rudolfs/ros2_ws/build/nav2_behavior_tree/test/test_bt_utils" "--gtest_output=xml:/home/rudolfs/ros2_ws/build/nav2_behavior_tree/test_results/nav2_behavior_tree/test_bt_utils.gtest.xml")
set_tests_properties(test_bt_utils PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/rudolfs/ros2_ws/build/nav2_behavior_tree/test/test_bt_utils" TIMEOUT "60" WORKING_DIRECTORY "/home/rudolfs/ros2_ws/build/nav2_behavior_tree/test" _BACKTRACE_TRIPLES "/opt/ros/jazzy/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/jazzy/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;95;ament_add_test;/opt/ros/jazzy/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/rudolfs/ros2_ws/src/navigation2/nav2_behavior_tree/test/CMakeLists.txt;1;ament_add_gtest;/home/rudolfs/ros2_ws/src/navigation2/nav2_behavior_tree/test/CMakeLists.txt;0;")
subdirs("../gtest")
subdirs("plugins/condition")
subdirs("plugins/decorator")
subdirs("plugins/control")
subdirs("plugins/action")
