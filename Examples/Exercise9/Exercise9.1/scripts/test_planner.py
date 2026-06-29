#!/usr/bin/env python3
"""Run all test problems for Exercise 9.1 and verify the results."""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from test_planner_base import (
    find_planner,
    parse_popf_output,
    parse_vhpop_output,
    print_summary,
    run_planner,
)

BASE = Path(__file__).resolve().parent.parent
DOMAIN = BASE / "pddl" / "robot_domain.pddl"

TESTS = [
    {
        "name": "Basic transport",
        "file": BASE / "pddl" / "test_basic_transport.pddl",
        "expect_plan": True,
        "expected_actions": ["pick", "move", "place"],
        "expected_length": 3,
        "description": "Move box from room1 to room2",
    },
    {
        "name": "Same room goal",
        "file": BASE / "pddl" / "test_same_room_goal.pddl",
        "expect_plan": True,
        "expected_actions": [],
        "expected_length": 0,
        "description": "Box already at goal — plan should be empty (0 actions)",
    },
    {
        "name": "Two objects",
        "file": BASE / "pddl" / "test_two_objects.pddl",
        "expect_plan": True,
        "expected_actions": ["pick", "move", "place"],
        "expected_length": 7,
        "description": "Move two boxes from room1 to room2 (pick→move→place→move→pick→move→place)",
    },
    {
        "name": "Three rooms",
        "file": BASE / "pddl" / "test_three_rooms.pddl",
        "expect_plan": True,
        "expected_actions": ["pick", "move", "move", "place"],
        "expected_length": 4,
        "description": "Move box through three rooms (room1 -> room2 -> room3)",
    },
    {
        "name": "Unreachable",
        "file": BASE / "pddl" / "test_unreachable.pddl",
        "expect_plan": False,
        "expected_actions": None,
        "expected_length": None,
        "description": "No connection between rooms — no plan possible",
        "allow_timeout": True,
    },
]


def check_test(test, actions):
    passed = True
    details = []

    if test["expect_plan"]:
        if not actions and test["expected_length"] != 0:
            passed = False
            details.append(f"FAIL: Expected a plan but got none")
        elif not actions and test["expected_length"] == 0:
            details.append("OK: Empty plan (goal already satisfied)")
        else:
            if test["expected_length"] is not None:
                if len(actions) != test["expected_length"]:
                    passed = False
                    details.append(
                        f"FAIL: Expected {test['expected_length']} actions, got {len(actions)}"
                    )
                else:
                    details.append(f"OK: Plan length {len(actions)}")

            if test["expected_actions"]:
                expected_set = set(test["expected_actions"])
                actual_set = set(actions)
                if expected_set != actual_set:
                    passed = False
                    details.append(
                        f"FAIL: Expected actions {expected_set}, got {actual_set}"
                    )
                else:
                    details.append(f"OK: Actions match expected set")
    else:
        if actions:
            passed = False
            details.append(f"FAIL: Expected no plan, but got {len(actions)} actions")
        else:
            details.append("OK: No plan found (as expected)")

    return passed, details


def main():
    planner = None
    parser = None

    if len(sys.argv) > 1:
        planner = sys.argv[1]
    else:
        for candidate in ["vhpop", "popf"]:
            path = find_planner(candidate)
            if path:
                planner = path
                break

    if planner is None:
        print("ERROR: No planner found. Please install VHPOP or POPF.")
        print("Usage: python3 test_planner.py [vhpop|popf|<path-to-planner>]")
        sys.exit(1)

    planner_name = Path(planner).name
    if planner_name == "vhpop":
        parser = parse_vhpop_output
    else:
        parser = parse_popf_output

    print(f"Running tests with {planner.upper()}")
    print(f"Domain: {DOMAIN}")
    print("=" * 60)

    results = []
    for i, test in enumerate(TESTS, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"  Description: {test['description']}")
        print(f"  Problem: {test['file'].name}")

        try:
            timeout = 5 if test.get("allow_timeout") else 30
            output = run_planner(planner, DOMAIN, test["file"], timeout=timeout)
            actions = parser(output)
            passed, details = check_test(test, actions)

            for detail in details:
                print(f"  {detail}")

            results.append((test["name"], passed))

        except subprocess.TimeoutExpired:
            if test.get("allow_timeout"):
                print("  OK: Planner timed out (as expected for unsolvable problem)")
                results.append((test["name"], True))
            else:
                print("  FAIL: Planner timed out")
                results.append((test["name"], False))
        except Exception as e:
            print(f"  FAIL: {e}")
            results.append((test["name"], False))

    print_summary(results)


if __name__ == "__main__":
    main()