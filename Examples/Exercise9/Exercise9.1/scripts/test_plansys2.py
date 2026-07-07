#!/usr/bin/env python3
"""Integration tests for Exercise 9.1 using PlanSys2.

Launches PlanSys2, runs each test problem through the ROS 2 services,
and validates the plan results.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))

import rclpy

from test_plansys2_base import (
    PlanSys2TestHarness,
    PlanSys2Tester,
    check_result,
    print_summary,
    run_test_case,
)

BASE = Path(__file__).resolve().parent.parent
DOMAIN = BASE / "pddl" / "robot_domain.pddl"
EMPTY_PROBLEM = BASE / "pddl" / "empty_problem.pddl"

TESTS = [
    {
        "name": "Basic transport",
        "file": BASE / "pddl" / "test_basic_transport.pddl",
        "expect_plan": True,
        "expected_actions": ["pick", "move", "place"],
        "expected_length": 3,
    },
    {
        "name": "Same room goal",
        "file": BASE / "pddl" / "test_same_room_goal.pddl",
        "expect_plan": True,
        "expected_actions": [],
        "expected_length": 0,
    },
    {
        "name": "Two objects",
        "file": BASE / "pddl" / "test_two_objects.pddl",
        "expect_plan": True,
        "expected_actions": ["pick", "move", "place"],
        "expected_length": 7,
    },
    {
        "name": "Three rooms",
        "file": BASE / "pddl" / "test_three_rooms.pddl",
        "expect_plan": True,
        "expected_actions": ["pick", "move", "move", "place"],
        "expected_length": 4,
    },
    {
        "name": "Unreachable",
        "file": BASE / "pddl" / "test_unreachable.pddl",
        "expect_plan": False,
        "expected_actions": None,
        "expected_length": None,
        "allow_timeout": True,
    },
]


def main():
    print("=" * 60)
    print("Exercise 9.1 — PlanSys2 Integration Tests")
    print(f"Domain: {DOMAIN}")
    print("=" * 60)

    results = []

    with PlanSys2TestHarness(DOMAIN, EMPTY_PROBLEM) as harness:
        rclpy.init()
        node = PlanSys2Tester()

        try:
            node.wait_for_services(timeout_sec=60)
            print("  PlanSys2 services ready. Waiting for lifecycle activation...")
            import time
            time.sleep(10)
        except RuntimeError as e:
            print(f"  FAIL: Could not connect to PlanSys2: {e}")
            rclpy.shutdown()
            sys.exit(1)

        try:
            for i, test in enumerate(TESTS, 1):
                passed, details, crashed = run_test_case(
                    test, str(DOMAIN), node, i
                )
                for d in details:
                    print(f"    {d}")
                results.append((test["name"], passed))

                if crashed:
                    print("    Note: PlanSys2 may have crashed, restarting...")
                    harness.stop()
                    harness.start()
                    import time
                    time.sleep(15)
                    node = PlanSys2Tester()
                    try:
                        node.wait_for_services(timeout_sec=60)
                        print("    PlanSys2 restarted successfully.")
                    except RuntimeError as e:
                        print(f"    FAIL: Could not restart PlanSys2: {e}")
                        results.append(("Restart", False))
                        break
        finally:
            try:
                node.destroy_node()
            except Exception:
                pass
            try:
                rclpy.shutdown()
            except Exception:
                pass

    print_summary(results)


if __name__ == "__main__":
    main()
