import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/victorcai/ros2_ws/install/vehicle_detection_pkg'
