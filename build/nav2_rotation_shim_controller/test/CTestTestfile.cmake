# CMake generated Testfile for 
# Source directory: /home/rudolfs/ros2_ws/src/navigation2/nav2_rotation_shim_controller/test
# Build directory: /home/rudolfs/ros2_ws/build/nav2_rotation_shim_controller/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(test_shim_controller "/usr/bin/python3" "-u" "/opt/ros/jazzy/share/ament_cmake_test/cmake/run_test.py" "/home/rudolfs/ros2_ws/build/nav2_rotation_shim_controller/test_results/nav2_rotation_shim_controller/test_shim_controller.gtest.xml" "--package-name" "nav2_rotation_shim_controller" "--output-file" "/home/rudolfs/ros2_ws/build/nav2_rotation_shim_controller/ament_cmake_gtest/test_shim_controller.txt" "--command" "/home/rudolfs/ros2_ws/build/nav2_rotation_shim_controller/test/test_shim_controller" "--gtest_output=xml:/home/rudolfs/ros2_ws/build/nav2_rotation_shim_controller/test_results/nav2_rotation_shim_controller/test_shim_controller.gtest.xml")
set_tests_properties(test_shim_controller PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/rudolfs/ros2_ws/build/nav2_rotation_shim_controller/test/test_shim_controller" TIMEOUT "60" WORKING_DIRECTORY "/home/rudolfs/ros2_ws/build/nav2_rotation_shim_controller/test" _BACKTRACE_TRIPLES "/opt/ros/jazzy/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/jazzy/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;95;ament_add_test;/opt/ros/jazzy/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/rudolfs/ros2_ws/src/navigation2/nav2_rotation_shim_controller/test/CMakeLists.txt;4;ament_add_gtest;/home/rudolfs/ros2_ws/src/navigation2/nav2_rotation_shim_controller/test/CMakeLists.txt;0;")
subdirs("../gtest")
