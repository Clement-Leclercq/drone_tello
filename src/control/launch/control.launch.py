from launch import LaunchDescription
import launch_ros.actions

def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
            package = 'control', 
            executable = 'control', 
            name = 'control',
            remappings=[
                ('/control', '/secure_cmd')
            ]
            ),
        launch_ros.actions.Node(
            package = 'control', 
            executable = 'tello_behavior', 
            name = 'tello_behavior'
            ),
        launch_ros.actions.Node(
            namespace = 'rqt_gui',
            package='rqt_gui',
            executable='rqt_gui',
            ),
        launch_ros.actions.Node(
            package = 'joy', 
            executable = 'joy_node', 
            name = 'joy'
            ),        
        launch_ros.actions.Node(
            package = 'zbar_ros', 
            executable = 'barcode_reader', 
            name = 'barcode_reader',
            remappings=[
                ('/image', '/image_raw')
            ]
            ),

        ])