import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/rudolfs/ros2_ws/install/tb4_nav_to_pose'
