#!/usr/bin/env python3
"""Shared test planner utilities for Exercise9."""

import shutil
import subprocess
import sys
from pathlib import Path


def run_planner(planner_cmd, domain, problem_path, timeout=30):
    result = subprocess.run(
        [planner_cmd, str(domain), str(problem_path)],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.stdout + result.stderr


def parse_vhpop_output(output):
    actions = []
    for line in output.strip().splitlines():
        line = line.strip()
        if line and line[0].isdigit() and "(" in line:
            parts = line.split(":")
            if len(parts) >= 2:
                action_str = parts[1].strip()
                if action_str.startswith("("):
                    action_name = action_str[1:].split()[0]
                    actions.append(action_name)
    return actions


def parse_popf_output(output):
    if "unsolvable" in output:
        return []
    actions = []
    for line in output.strip().splitlines():
        line = line.strip()
        if ":" in line and "(" in line and "[" in line:
            action_str = line.split(":")[1].strip() if ":" in line else line
            if action_str.startswith("("):
                action_name = action_str[1:].split()[0]
                actions.append(action_name)
    return actions


def find_planner(name):
    """Find planner executable in PATH or common locations."""
    found = shutil.which(name)
    if found:
        return found
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    candidate = repo_root / "Planners" / name
    if candidate.exists():
        return str(candidate)
    return None


def print_summary(results):
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total = len(results)
    passed = sum(1 for _, p in results if p)

    for name, p in results:
        status = "PASS" if p else "FAIL"
        print(f"  [{status}] {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("All tests passed!")
        sys.exit(0)
    else:
        print(f"{total - passed} test(s) failed.")
        sys.exit(1)
