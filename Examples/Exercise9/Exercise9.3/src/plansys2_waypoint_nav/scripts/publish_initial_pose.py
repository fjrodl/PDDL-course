#!/usr/bin/env python3
"""Publish initial pose to AMCL so localization starts without manual 2D Pose Estimate."""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped


def main():
    rclpy.init()
    node = Node("initial_pose_publisher")
    node.set_parameters([rclpy.Parameter("use_sim_time", rclpy.Parameter.Type.BOOL, True)])

    node.declare_parameter("x", -2.0)
    node.declare_parameter("y", -0.5)
    node.declare_parameter("yaw", 0.0)
    node.declare_parameter("covariance_position", 0.25)
    node.declare_parameter("covariance_yaw", 0.068)

    x = node.get_parameter("x").value
    y = node.get_parameter("y").value
    yaw = node.get_parameter("yaw").value
    cov_pos = node.get_parameter("covariance_position").value
    cov_yaw = node.get_parameter("covariance_yaw").value

    qz = math.sin(yaw / 2.0)
    qw = math.cos(yaw / 2.0)

    publisher = node.create_publisher(PoseWithCovarianceStamped, "/initialpose", 1)

    # Wait briefly for /clock so sim time is valid
    for _ in range(20):
        now = node.get_clock().now()
        if now.nanoseconds > 0:
            break
        node.get_logger().info("Waiting for /clock...")
        rclpy.spin_once(node, timeout_sec=0.5)

    msg = PoseWithCovarianceStamped()
    msg.header.frame_id = "map"
    msg.header.stamp = node.get_clock().now().to_msg()
    msg.pose.pose.position.x = x
    msg.pose.pose.position.y = y
    msg.pose.pose.position.z = 0.0
    msg.pose.pose.orientation.x = 0.0
    msg.pose.pose.orientation.y = 0.0
    msg.pose.pose.orientation.z = qz
    msg.pose.pose.orientation.w = qw
    msg.pose.covariance = [
        cov_pos, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, cov_pos, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 1e-9, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 1e-9, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 1e-9, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, cov_yaw,
    ]

    node.get_logger().info(f"Publishing initial pose: x={x}, y={y}, yaw={yaw:.3f} rad")
    publisher.publish(msg)
    rclpy.spin_once(node, timeout_sec=1.0)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
