#include <chrono>
#include <map>
#include <memory>
#include <string>
#include <vector>

#include "ament_index_cpp/get_package_share_directory.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "lifecycle_msgs/msg/transition.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"
#include "plansys2_executor/ActionExecutorClient.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "yaml-cpp/yaml.h"

using namespace std::chrono_literals;

class NavigateAction : public plansys2::ActionExecutorClient
{
public:
  using NavigateToPose = nav2_msgs::action::NavigateToPose;
  using GoalHandleNavigate = rclcpp_action::ClientGoalHandle<NavigateToPose>;

  NavigateAction()
  : plansys2::ActionExecutorClient("navigate_action_node", 500ms)
  {
    declare_parameter<std::string>("action", "navigate");
    declare_parameter<std::string>("waypoints_file", "");
    declare_parameter<std::string>("map_frame", "map");
  }

protected:
  CallbackReturnT on_configure(const rclcpp_lifecycle::State & state) override
  {
    auto result = plansys2::ActionExecutorClient::on_configure(state);
    if (result != CallbackReturnT::SUCCESS) {
      return result;
    }

    nav_client_ = rclcpp_action::create_client<NavigateToPose>(
      shared_from_this(), "navigate_to_pose");

    map_frame_ = get_parameter("map_frame").as_string();
    auto waypoints_file = get_parameter("waypoints_file").as_string();
    if (waypoints_file.empty()) {
      waypoints_file = ament_index_cpp::get_package_share_directory("plansys2_waypoint_nav") +
        "/config/waypoints.yaml";
    }

    try {
      load_waypoints(waypoints_file);
    } catch (const std::exception & ex) {
      RCLCPP_ERROR(get_logger(), "Failed to load waypoints: %s", ex.what());
      return CallbackReturnT::FAILURE;
    }

    RCLCPP_INFO(get_logger(), "Waypoints loaded from %s", waypoints_file.c_str());
    return CallbackReturnT::SUCCESS;
  }

  CallbackReturnT on_activate(const rclcpp_lifecycle::State & state) override
  {
    reset_goal_state();
    return plansys2::ActionExecutorClient::on_activate(state);
  }

  void do_work() override
  {
    if (!goal_sent_) {
      start_navigation_goal();
      return;
    }

    if (!goal_result_received_) {
      send_feedback(last_completion_, last_status_);
      return;
    }

    const auto status = result_success_ ? "Navigate completed" : "Navigate failed";
    finish(result_success_, result_success_ ? 1.0f : last_completion_, status);
    reset_goal_state();
  }

private:
  void load_waypoints(const std::string & waypoints_file)
  {
    auto yaml = YAML::LoadFile(waypoints_file);
    waypoints_.clear();

    for (const auto & entry : yaml) {
      const auto name = entry.first.as<std::string>();
      const auto data = entry.second;

      geometry_msgs::msg::PoseStamped pose;
      pose.header.frame_id = map_frame_;
      pose.pose.position.x = data["x"].as<double>();
      pose.pose.position.y = data["y"].as<double>();
      pose.pose.position.z = data["position_z"] ? data["position_z"].as<double>() : 0.0;
      pose.pose.orientation.x = data["qx"] ? data["qx"].as<double>() : 0.0;
      pose.pose.orientation.y = data["qy"] ? data["qy"].as<double>() : 0.0;
      pose.pose.orientation.z = data["z"].as<double>();
      pose.pose.orientation.w = data["w"].as<double>();

      waypoints_[name] = pose;
    }
  }

  void start_navigation_goal()
  {
    const auto & args = get_arguments();
    if (args.size() != 3) {
      finish(false, 0.0, "navigate expects args: robot origin destination");
      return;
    }

    const auto & target = args[2];
    const auto waypoint_it = waypoints_.find(target);
    if (waypoint_it == waypoints_.end()) {
      finish(false, 0.0, "Waypoint not found: " + target);
      return;
    }

    if (!nav_client_->wait_for_action_server(1s)) {
      send_feedback(0.0, "Waiting for navigate_to_pose server");
      return;
    }

    NavigateToPose::Goal goal;
    goal.pose = waypoint_it->second;
    goal.pose.header.stamp = now();

    RCLCPP_INFO(
      get_logger(), "Navigating to %s: x=%.2f y=%.2f",
      target.c_str(), goal.pose.pose.position.x, goal.pose.pose.position.y);

    auto send_goal_options = rclcpp_action::Client<NavigateToPose>::SendGoalOptions();
    send_goal_options.goal_response_callback =
      [this](GoalHandleNavigate::SharedPtr goal_handle) {
        if (!goal_handle) {
          goal_result_received_ = true;
          result_success_ = false;
          last_status_ = "Nav2 rejected goal";
          return;
        }
        last_status_ = "Nav2 accepted goal";
      };

    send_goal_options.feedback_callback =
      [this](
      GoalHandleNavigate::SharedPtr,
      const std::shared_ptr<const NavigateToPose::Feedback> feedback) {
        if (feedback == nullptr) return;
        const auto distance = feedback->distance_remaining;
        last_completion_ = distance <= 0.05 ? 0.95f : 0.5f;
        last_status_ = "Distance remaining: " + std::to_string(distance) + " m";
      };

    send_goal_options.result_callback =
      [this](const GoalHandleNavigate::WrappedResult & result) {
        goal_result_received_ = true;
        result_success_ = result.code == rclcpp_action::ResultCode::SUCCEEDED;
        last_completion_ = result_success_ ? 1.0f : last_completion_;
        last_status_ = result_success_ ? "Nav2 goal reached" : "Nav2 goal failed";
      };

    nav_client_->async_send_goal(goal, send_goal_options);
    goal_sent_ = true;
    goal_result_received_ = false;
    result_success_ = false;
    last_completion_ = 0.05f;
    last_status_ = "Navigate running";
    send_feedback(last_completion_, last_status_);
  }

  void reset_goal_state()
  {
    goal_sent_ = false;
    goal_result_received_ = false;
    result_success_ = false;
    last_completion_ = 0.0f;
    last_status_.clear();
  }

  std::map<std::string, geometry_msgs::msg::PoseStamped> waypoints_;
  rclcpp_action::Client<NavigateToPose>::SharedPtr nav_client_;
  bool goal_sent_ {false};
  bool goal_result_received_ {false};
  bool result_success_ {false};
  float last_completion_ {0.0f};
  std::string last_status_;
  std::string map_frame_ {"map"};
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<NavigateAction>();
  node->set_parameter(rclcpp::Parameter("action", "navigate"));
  node->set_parameter(rclcpp::Parameter("action_name", "navigate"));
  node->trigger_transition(lifecycle_msgs::msg::Transition::TRANSITION_CONFIGURE);
  node->trigger_transition(lifecycle_msgs::msg::Transition::TRANSITION_ACTIVATE);
  rclcpp::spin(node->get_node_base_interface());
  rclcpp::shutdown();
  return 0;
}
