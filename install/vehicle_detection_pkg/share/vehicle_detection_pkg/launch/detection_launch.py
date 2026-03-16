from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['ros2', 'bag', 'play', '/home/victorcai/ros2_ws/data/converted_bag', '--loop', '--rate', '0.5'],
            output='screen'
        ),
        Node(
            package='vehicle_detection_pkg',
            executable='detection_node',
            name='vehicle_detector',
            output='screen'
        )
    ])
