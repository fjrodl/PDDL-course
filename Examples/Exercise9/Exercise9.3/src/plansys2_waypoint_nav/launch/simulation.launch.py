from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo, TimerAction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_rviz = LaunchConfiguration("use_rviz")
    use_sim_time = LaunchConfiguration("use_sim_time")
    headless = LaunchConfiguration("headless")
    x_pose = LaunchConfiguration("x_pose")
    y_pose = LaunchConfiguration("y_pose")
    z_pose = LaunchConfiguration("z_pose")
    roll = LaunchConfiguration("roll")
    pitch = LaunchConfiguration("pitch")
    yaw = LaunchConfiguration("yaw")

    nav2_dir = FindPackageShare("nav2_bringup")
    plansys2_bringup_dir = FindPackageShare("plansys2_bringup")
    plansys2_nav_dir = FindPackageShare("plansys2_waypoint_nav")

    return LaunchDescription([
        DeclareLaunchArgument("use_rviz", default_value="True", description="Launch RViz2"),
        DeclareLaunchArgument("use_sim_time", default_value="True", description="Use Gazebo simulation time"),
        DeclareLaunchArgument("headless", default_value="False", description="Run Gazebo headless"),
        DeclareLaunchArgument("x_pose", default_value="-2.00", description="Initial X position"),
        DeclareLaunchArgument("y_pose", default_value="-0.50", description="Initial Y position"),
        DeclareLaunchArgument("z_pose", default_value="0.01", description="Initial Z position"),
        DeclareLaunchArgument("roll", default_value="0.00", description="Initial roll"),
        DeclareLaunchArgument("pitch", default_value="0.00", description="Initial pitch"),
        DeclareLaunchArgument("yaw", default_value="0.00", description="Initial yaw"),

        LogInfo(msg="=== Starting PlanSys2 + Nav2 + TurtleBot3 simulation ==="),

        IncludeLaunchDescription(
            PathJoinSubstitution([nav2_dir, "launch", "tb3_simulation_launch.py"]),
            launch_arguments={
                "use_sim_time": use_sim_time,
                "headless": headless,
                "use_rviz": use_rviz,
                "use_namespace": "False",
                "x_pose": x_pose,
                "y_pose": y_pose,
                "z_pose": z_pose,
                "roll": roll,
                "pitch": pitch,
                "yaw": yaw,
            }.items(),
        ),

        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package="plansys2_waypoint_nav",
                    executable="publish_initial_pose.py",
                    name="initial_pose_publisher",
                    output="screen",
                    parameters=[{
                        "x": x_pose,
                        "y": y_pose,
                        "yaw": yaw,
                    }],
                ),
            ],
        ),

        IncludeLaunchDescription(
            PathJoinSubstitution([plansys2_bringup_dir, "launch", "plansys2_bringup_launch_monolithic.py"]),
            launch_arguments={
                "model_file": PathJoinSubstitution([plansys2_nav_dir, "pddl", "domain_waypoint_mission.pddl"]),
            }.items(),
        ),

        Node(
            package="plansys2_waypoint_nav",
            executable="navigate_action_node",
            name="navigate_action_node",
            output="screen",
            parameters=[{
                "waypoints_file": PathJoinSubstitution([plansys2_nav_dir, "config", "waypoints.yaml"]),
                "map_frame": "map",
            }],
        ),
    ])
