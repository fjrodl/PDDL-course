cmake_minimum_required(VERSION 3.8)
project(plansys2_waypoint_nav)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_index_cpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(lifecycle_msgs REQUIRED)
find_package(nav2_msgs REQUIRED)
find_package(plansys2_executor REQUIRED)
find_package(plansys2_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(yaml-cpp REQUIRED)

add_executable(navigate_action_node src/navigate_action_node.cpp)
ament_target_dependencies(navigate_action_node
  ament_index_cpp
  geometry_msgs
  lifecycle_msgs
  nav2_msgs
  plansys2_executor
  plansys2_msgs
  rclcpp
  rclcpp_action
  rclcpp_lifecycle
)
target_link_libraries(navigate_action_node yaml-cpp)

install(TARGETS navigate_action_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY config launch pddl
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
   scripts/execute_plan.py
  scripts/publish_initial_pose.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
