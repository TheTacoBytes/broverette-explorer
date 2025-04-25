#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Get paths to package directories
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    params_file_slam = os.path.join(
        get_package_share_directory('broverette_slam'), 'config', 'params.yaml'
    )
    params_file_nav2 = os.path.join(
        get_package_share_directory('broverette_nav2_bringup'), 'config', 'nav2_params.yaml'
    )
    
    # Paths to the SLAM Toolbox and Nav2 launch files
    slam_toolbox_launch = os.path.join(slam_toolbox_dir, 'launch', 'online_sync_launch.py')
    nav2_bringup_launch = os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')

    # Create the launch description
    ld = LaunchDescription()

    # 1) Include SLAM Toolbox launch file
    #    - This example uses online_sync; replace with your desired SLAM mode
    slam_toolbox_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_toolbox_launch),
        launch_arguments={
            'use_sim_time': 'False',
            'slam_params_file': params_file_slam
        }.items()
    )
    ld.add_action(slam_toolbox_include)

    # 2) Include Nav2 bringup launch file in SLAM mode (slam:=true)
    nav2_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_bringup_launch),
        launch_arguments={
            'slam': 'True',         # Tells Nav2 to skip the static map server
            'use_sim_time': 'False',
            'map': '',
            'params_file': params_file_nav2
        }.items()
    )
    ld.add_action(nav2_include)

    return ld
