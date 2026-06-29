#!/usr/bin/env python3
"""Run all test problems for Exercise 9.2 and verify the results."""

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
DOMAIN = BASE / "pddl" / "robot_domain_energy.pddl"

TESTS = [
    {
        "name": "Energy basic (recharge required)",
        "file": BASE / "pddl" / "test_energy_basic.pddl",
        "expect_plan": True,
        "must_contain": ["recharge"],
        "expected_length": 5,
        "description": "Box from room1 to room2 via room_mid with recharge",
    },
    {
        "name": "Charger at start",
        "file": BASE / "pddl" / "test_energy_charger_at_start.pddl",
        "expect_plan": True,
        "must_contain": ["recharge"],
        "expected_length": 5,
        "description": "Charger at room1 — robot must still recharge between moves",
    },
    {
        "name": "No charger (unreachable)",
        "file": BASE / "pddl" / "test_energy_no_charger.pddl",
        "expect_plan": False,
        "must_contain": None,
        "expected_length": None,
        "description": "No charger anywhere — cannot recharge, no plan possible",
        "allow_timeout": True,
    },
    {
        "name": "Four rooms with two chargers",
        "file": BASE / "pddl" / "test_energy_four_rooms.pddl",
        "expect_plan": True,
        "must_contain": ["recharge"],
        "expected_length": 7,
        "description": "Four rooms, two chargers — robot recharges twice",
    },
    {
        "name": "Start with low battery",
        "file": BASE / "pddl" / "test_energy_start_low.pddl",
        "expect_plan": True,
        "must_contain": ["recharge"],
        "expected_length": 6,
        "description": "Robot starts with low battery — must recharge first",
    },
]


def check_test(test, actions):
    passed = True
    details = []

    if test["expect_plan"]:
        if not actions:
            passed = False
            details.append("FAIL: Expected a plan but got none")
        else:
            if test["expected_length"] is not None:
                if len(actions) != test["expected_length"]:
                    passed = False
                    details.append(
                        f"FAIL: Expected {test['expected_length']} actions, got {len(actions)}"
                    )
                else:
                    details.append(f"OK: Plan length {len(actions)}")

            if test["must_contain"]:
                action_set = set(actions)
                missing = set(test["must_contain"]) - action_set
                if missing:
                    passed = False
                    details.append(
                        f"FAIL: Plan missing required actions: {missing}"
                    )
                else:
                    details.append(
                        f"OK: Plan contains required actions: {test['must_contain']}"
                    )
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
            timeout = 10 if test.get("allow_timeout") else 30
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