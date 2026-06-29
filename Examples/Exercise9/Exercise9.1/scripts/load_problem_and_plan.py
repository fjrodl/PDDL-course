#!/usr/bin/env python3
"""Load a PDDL problem into PlanSys2 and request a plan."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))

import rclpy

from plansys2_client import PlanSys2ProblemLoader


def main():
    base_path = Path(__file__).resolve().parent.parent
    domain_path = base_path / "pddl" / "robot_domain.pddl"
    problem_path = base_path / "pddl" / "robot_problem.pddl"

    rclpy.init()
    node = PlanSys2ProblemLoader()

    try:
        node.wait_for_services()
        node.load_problem(problem_path)
        plan_items = node.get_plan(domain_path, problem_path)

        print("Plan generated from Python:")
        for item in plan_items:
            print(f"{item.time:.3f}: {item.action} [{item.duration:.3f}]")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()