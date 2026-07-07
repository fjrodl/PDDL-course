#!/usr/bin/env python3
"""Shared PlanSys2 client for loading problems and requesting plans."""

from pathlib import Path

import rclpy
from rclpy.node import Node

from plansys2_msgs.srv import AddProblem, ClearProblemKnowledge, GetPlan


class PlanSys2ProblemLoader(Node):
    def __init__(self):
        super().__init__("plansys2_problem_loader")
        self.clear_problem_client = self.create_client(
            ClearProblemKnowledge,
            "/problem_expert/clear_problem_knowledge",
        )
        self.add_problem_client = self.create_client(
            AddProblem,
            "/problem_expert/add_problem",
        )
        self.get_plan_client = self.create_client(
            GetPlan,
            "/planner/get_plan",
        )

    def wait_for_services(self, timeout_sec=30):
        for client, name in (
            (self.clear_problem_client, "/problem_expert/clear_problem_knowledge"),
            (self.add_problem_client, "/problem_expert/add_problem"),
            (self.get_plan_client, "/planner/get_plan"),
        ):
            self.get_logger().info(f"Waiting for service {name}...")
            client.wait_for_service(timeout_sec=timeout_sec)

    def call(self, client, request):
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        try:
            return future.result()
        except Exception as e:
            raise RuntimeError(f"Service call failed: {e}") from e

    def load_problem(self, problem_path):
        problem_text = Path(problem_path).read_text(encoding="utf-8")

        clear_response = self.call(
            self.clear_problem_client,
            ClearProblemKnowledge.Request(),
        )
        if not clear_response.success:
            raise RuntimeError(clear_response.error_info)

        request = AddProblem.Request()
        request.problem = problem_text
        add_response = self.call(self.add_problem_client, request)
        if not add_response.success:
            raise RuntimeError(add_response.error_info)

    def get_plan(self, domain_path, problem_path):
        request = GetPlan.Request()
        request.domain = Path(domain_path).read_text(encoding="utf-8")
        request.problem = Path(problem_path).read_text(encoding="utf-8")

        response = self.call(self.get_plan_client, request)
        if not response.success:
            raise RuntimeError(response.error_info)
        return response.plan.items
