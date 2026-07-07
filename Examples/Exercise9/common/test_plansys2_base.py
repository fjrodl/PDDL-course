#!/usr/bin/env python3
"""Shared PlanSys2 integration test utilities.

Launches PlanSys2 as a subprocess, waits for services, runs tests, and cleans up.
"""

import signal
import subprocess
import sys
import time
from pathlib import Path

import rclpy
from rclpy.node import Node

from plansys2_msgs.srv import AddProblem, ClearProblemKnowledge, GetPlan


class PlanSys2TestHarness:
    """Launches PlanSys2 distributed, runs tests, then tears down."""

    def __init__(self, domain_path, empty_problem_path, timeout_sec=30):
        self.domain_path = Path(domain_path)
        self.empty_problem_path = Path(empty_problem_path)
        self.timeout_sec = timeout_sec
        self.launch_process = None

    def start(self):
        """Launch PlanSys2 distributed bringup."""
        cmd = [
            "ros2", "launch",
            "plansys2_bringup",
            "plansys2_bringup_launch_distributed.py",
            f"model_file:={self.domain_path}",
            f"problem_file:={self.empty_problem_path}",
        ]
        print(f"  Launching PlanSys2: {' '.join(cmd)}")
        self.launch_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            preexec_fn=os_setsid,
        )
        print(f"  PlanSys2 PID: {self.launch_process.pid}")

    def stop(self):
        """Kill the PlanSys2 process group."""
        if self.launch_process and self.launch_process.poll() is None:
            try:
                os_killpg(self.launch_process.pid, signal.SIGTERM)
                self.launch_process.wait(timeout=10)
            except Exception:
                try:
                    os_killpg(self.launch_process.pid, signal.SIGKILL)
                    self.launch_process.wait(timeout=5)
                except Exception:
                    pass
            print("  PlanSys2 stopped.")
        elif self.launch_process:
            print("  PlanSys2 already exited.")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


def os_setsid():
    import os
    os.setsid()


def os_killpg(pgid, sig):
    import os
    os.killpg(pgid, sig)


class PlanSys2Tester(Node):
    """ROS 2 node that communicates with PlanSys2 services for testing."""

    def __init__(self):
        super().__init__("plansys2_tester")
        self.clear_client = self.create_client(
            ClearProblemKnowledge, "/problem_expert/clear_problem_knowledge"
        )
        self.add_client = self.create_client(
            AddProblem, "/problem_expert/add_problem"
        )
        self.plan_client = self.create_client(
            GetPlan, "/planner/get_plan"
        )

    def wait_for_services(self, timeout_sec=60):
        import time as _time
        deadline = _time.monotonic() + timeout_sec
        for client, name in [
            (self.clear_client, "/problem_expert/clear_problem_knowledge"),
            (self.add_client, "/problem_expert/add_problem"),
            (self.plan_client, "/planner/get_plan"),
        ]:
            self.get_logger().info(f"Waiting for {name}...")
            while _time.monotonic() < deadline:
                if client.wait_for_service(timeout_sec=2.0):
                    break
            else:
                raise RuntimeError(f"Service {name} not available")

    def call_sync(self, client, request, retries=8, retry_delay=3.0, timeout=30.0):
        import time as _time
        last_error = None
        for attempt in range(retries):
            future = client.call_async(request)
            rclpy.spin_until_future_complete(self, future, timeout_sec=timeout)
            try:
                result = future.result()
                if result is not None:
                    return result
                last_error = RuntimeError("Service returned None")
            except Exception as e:
                last_error = e
            if attempt < retries - 1:
                self.get_logger().warn(
                    f"Service call failed (attempt {attempt+1}/{retries}): {last_error}. Retrying..."
                )
                _time.sleep(retry_delay)
        raise RuntimeError(f"Service call failed after {retries} attempts: {last_error}") from last_error

    def clear_problem(self):
        resp = self.call_sync(self.clear_client, ClearProblemKnowledge.Request())
        if resp is None or not resp.success:
            raise RuntimeError(f"Clear failed: {resp.error_info if resp else 'No response'}")

    def load_problem(self, problem_path):
        problem_text = Path(problem_path).read_text(encoding="utf-8")
        req = AddProblem.Request()
        req.problem = problem_text
        resp = self.call_sync(self.add_client, req)
        if resp is None or not resp.success:
            raise RuntimeError(f"Add problem failed: {resp.error_info if resp else 'No response'}")

    def get_plan(self, domain_path, problem_path, timeout=30.0):
        req = GetPlan.Request()
        req.domain = Path(domain_path).read_text(encoding="utf-8")
        req.problem = Path(problem_path).read_text(encoding="utf-8")
        resp = self.call_sync(self.plan_client, req, timeout=timeout)
        if resp is None or not resp.success:
            raise RuntimeError(f"Get plan failed: {resp.error_info if resp else 'No response'}")
        return resp.plan.items


def run_test_case(test, domain_path, node, test_num):
    """Run a single test case against the PlanSys2 services.

    Returns (passed: bool, details: list[str], crashed: bool).
    """
    name = test["name"]
    problem_path = Path(test["file"])
    expect_plan = test.get("expect_plan", True)
    expected_length = test.get("expected_length")
    expected_actions = test.get("expected_actions")
    must_contain = test.get("must_contain")
    allow_timeout = test.get("allow_timeout", False)

    print(f"\n  Test {test_num}: {name}")
    print(f"    Problem: {problem_path.name}")

    try:
        node.clear_problem()
        node.load_problem(problem_path)
        timeout = 10.0 if allow_timeout else 60.0
        plan_items = node.get_plan(domain_path, problem_path, timeout=timeout)

        actions = []
        for item in plan_items:
            action_str = item.action
            if "(" in action_str:
                action_name = action_str[1:].split()[0]
                actions.append(action_name)

        passed, details = check_result(
            test, actions, expect_plan, expected_length,
            expected_actions, must_contain,
        )
        return passed, details, False

    except subprocess.TimeoutExpired:
        if allow_timeout:
            return True, ["OK: Timed out (expected for unsolvable)"], True
        return False, ["FAIL: Timed out"], True
    except Exception as e:
        error_msg = str(e)
        if allow_timeout:
            return True, [f"OK: Exception (expected for unsolvable): {e}"], True
        if "Plan not found" in error_msg and expect_plan and expected_length == 0:
            return True, ["OK: Empty plan (goal already satisfied, PlanSys2 returns 'Plan not found')"], False
        return False, [f"FAIL: {e}"], True


def check_result(test, actions, expect_plan, expected_length,
                 expected_actions, must_contain):
    """Validate plan actions against expectations."""
    passed = True
    details = []

    if expect_plan:
        if not actions and expected_length != 0:
            passed = False
            details.append("FAIL: Expected a plan but got none")
        elif not actions and expected_length == 0:
            details.append("OK: Empty plan (goal already satisfied)")
        else:
            if expected_length is not None:
                if len(actions) != expected_length:
                    passed = False
                    details.append(
                        f"FAIL: Expected {expected_length} actions, got {len(actions)}"
                    )
                else:
                    details.append(f"OK: Plan length {len(actions)}")

            if expected_actions:
                expected_set = set(expected_actions)
                actual_set = set(actions)
                if expected_set != actual_set:
                    passed = False
                    details.append(
                        f"FAIL: Expected actions {expected_set}, got {actual_set}"
                    )
                else:
                    details.append("OK: Actions match expected set")

            if must_contain:
                action_set = set(actions)
                missing = set(must_contain) - action_set
                if missing:
                    passed = False
                    details.append(f"FAIL: Missing required actions: {missing}")
                else:
                    details.append(f"OK: Contains required actions: {must_contain}")
    else:
        if actions:
            passed = False
            details.append(
                f"FAIL: Expected no plan, got {len(actions)} actions"
            )
        else:
            details.append("OK: No plan (as expected)")

    return passed, details


def print_summary(results):
    """Print PASS/FAIL summary and exit with appropriate code."""
    print("\n" + "=" * 60)
    print("PLANSSYS2 INTEGRATION TEST SUMMARY")
    print("=" * 60)

    total = len(results)
    passed = sum(1 for _, p in results if p)

    for name, p in results:
        status = "PASS" if p else "FAIL"
        print(f"  [{status}] {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print(f"{total - passed} test(s) FAILED.")
        sys.exit(1)
