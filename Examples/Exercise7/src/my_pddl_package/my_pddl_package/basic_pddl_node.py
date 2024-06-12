
#It is missed if everything is used, TODO:check
import subprocess
import os
import time 
import yaml


# ROS 2 related 
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration

# NAV2 related
from nav2_msgs.action import NavigateToPose
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

from rclpy.action import ActionClient

from geometry_msgs.msg import PoseStamped




# You should be ussing ROS 2 parameters here. 

# SOLVER_PATH = "<ROUTE_TO_YOUR_PLANNER>/SMTPlan"
# Example 
SOLVER_PATH = "/home/odiseo/PDDL-course/Planners/SMTPlan"

# PATH_PDDL_FILES = "ROUTE TO YOUR FOLDER WITH DOMAIN AND SOLVER"
# PATH_PDDL_FILES = "/home/odiseo/cognitive_pddl/src/Robotica_cognitiva/waypoints_with_pddl/waypoints_with_pddl"
PATH_PDDL_FILES = "/home/odiseo/PDDL-course/Examples/Exercise7/src/my_pddl_package/domains_and_problems"


#These are just examples, double check with the domain and problem that you want to use
DOMAIN_PDDL_FILE = "domain.pddl"
PROBLEM_PDDL_FILE = "problem.pddl"



class PlannerPath(Node):
    """
    Class in charge of loading and sending waypoints
    """
    def __init__(self):
        super().__init__("planer_path")
        self.nav_pose_client = ActionClient(self, NavigateToPose, "navigate_to_pose")

        with open(os.path.join(PATH_PDDL_FILES, DOMAIN_PDDL_FILE), encoding="utf-8") as f:
            read_data = f.read()
            self.get_logger().info(f"PDDL Domain File Content:\n{read_data}")

        # Launch the planner
        solver = subprocess.Popen(
            args=[
                SOLVER_PATH,
                os.path.join(PATH_PDDL_FILES, DOMAIN_PDDL_FILE),
                os.path.join(PATH_PDDL_FILES, PROBLEM_PDDL_FILE),
            ],
            stdout=subprocess.PIPE,
        )

        # Load waypoints while the solver is running
        waypoints = self.load_waypoints(
            os.path.join(PATH_PDDL_FILES, "../waypoints/waypoints.yaml")
        )

        solver.wait()
        self.get_logger().info("Finished PDDL solving step")

        # Parse the output from the solver
        path = []
        for line in solver.stdout.readlines():
            self.get_logger().info(f"Solver output: {line.strip()}")
            path.append(str(line).split(" ")[2][:-1])

        navigator = BasicNavigator()

        # Send the path
        self.nav_pose_client.wait_for_server()
        for point in path:
            # Get the waypoint to go to
            waypoint = waypoints[point]
            print (">>>>>>>>>>> "+point)
            print (waypoint)

            # Set our demo's initial pose
            # initial_pose = PoseStamped()
            # initial_pose.header.frame_id = 'map'
            # initial_pose.header.stamp = navigator.get_clock().now().to_msg()
            # initial_pose.pose.position.x = 0.0
            # initial_pose.pose.position.y = 0.0
            # initial_pose.pose.orientation.z = 0.0
            # initial_pose.pose.orientation.w = 1.0
            # navigator.setInitialPose(initial_pose)



            # If autostart, you should `waitUntilNav2Active()` instead.
            # navigator.lifecycleStartup()

            # # Wait for navigation to fully activate, since autostarting nav2
            # navigator.waitUntilNav2Active()
            # Go to our demos first goal pose
            goal_pose = PoseStamped()
            goal_pose.header.stamp = navigator.get_clock().now().to_msg()
            goal_pose.header.frame_id = waypoint["frame_id"]
            goal_pose.pose.position.x = waypoint["position"]["x"]
            goal_pose.pose.position.y = waypoint["position"]["y"]
            goal_pose.pose.position.z = waypoint["position"]["z"]
            goal_pose.pose.orientation.x = waypoint["orientation"]["x"]
            goal_pose.pose.orientation.y = waypoint["orientation"]["y"]
            goal_pose.pose.orientation.w = waypoint["orientation"]["w"]
            goal_pose.pose.orientation.z = waypoint["orientation"]["z"]
            # sanity check a valid path exists
            # path = navigator.getPath(initial_pose, goal_pose)

            navigator.goToPose(goal_pose)

            i = 0
            while not navigator.isTaskComplete():
                ################################################
                #
                # Implement some code here for your application!
                #
                ##############################################
                # Do something with the feedback
                i = i + 1
                feedback = navigator.getFeedback()
                if feedback and i % 5 == 0:
                    print('Estimated time of arrival: ' + '{0:.0f}'.format(
                        Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9)
                        + ' seconds.')

                    # Some navigation timeout to demo cancellation
                    if Duration.from_msg(feedback.navigation_time) > Duration(seconds=600.0):
                        navigator.cancelTask()

                    # Some navigation request change to demo preemption
                    if Duration.from_msg(feedback.navigation_time) > Duration(seconds=18.0):
                        goal_pose.pose.position.x = -3.0
                        navigator.goToPose(goal_pose)

            # Do something depending on the return code
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                self.get_logger().info('Goal succeeded!')
            elif result == TaskResult.CANCELED:
                self.get_logger().info('Goal was canceled!')
            elif result == TaskResult.FAILED:
                self.get_logger().info('Goal failed!')
            else:
                self.get_logger().info('Goal has an invalid return status!')

            self.get_logger().info("Arrived at the destination")

        # Check lifecycle and how to use it
        navigator.lifecycleShutdown()


    def load_waypoints(self, file_path):
        """
        Load waypoints from a yaml file.
        """
        with open(file_path, "r") as file:
            return yaml.safe_load(file)



def main(args=None):
    """
    Main function
    """
    rclpy.init(args=args)
    node = PlannerPath()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
