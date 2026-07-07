#!/usr/bin/env bash
# Run all PlanSys2 tests for Exercise 9.
# Usage: ./run_all_tests.sh [standalone|plansys2|all]
#   standalone  - run VHPOP/POPF planner tests only (no ROS 2 needed)
#   plansys2    - run PlanSys2 integration tests (requires ROS 2 Jazzy + PlanSys2)
#   all         - run both (default)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-all}"

EXERCISE91="$SCRIPT_DIR/Exercise9.1/scripts"
EXERCISE92="$SCRIPT_DIR/Exercise9.2/scripts"

TOTAL_PASS=0
TOTAL_FAIL=0

run_test() {
    local label="$1"
    shift
    echo ""
    echo "=============================================="
    echo "  $label"
    echo "=============================================="
    if "$@"; then
        TOTAL_PASS=$((TOTAL_PASS + 1))
    else
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
    fi
}

echo "=============================================="
echo "  Exercise 9 — Test Runner"
echo "  Mode: $MODE"
echo "=============================================="

if [[ "$MODE" == "standalone" || "$MODE" == "all" ]]; then
    run_test "Exercise 9.1 — Standalone VHPOP" \
        python3 "$EXERCISE91/test_planner.py" vhpop

    run_test "Exercise 9.2 — Standalone VHPOP" \
        python3 "$EXERCISE92/test_planner.py" vhpop
fi

if [[ "$MODE" == "plansys2" || "$MODE" == "all" ]]; then
    run_test "Exercise 9.1 — PlanSys2 Integration" \
        python3 "$EXERCISE91/test_plansys2.py"

    run_test "Exercise 9.2 — PlanSys2 Integration" \
        python3 "$EXERCISE92/test_plansys2.py"
fi

echo ""
echo "=============================================="
echo "  FINAL RESULTS"
echo "=============================================="
echo "  PASSED: $TOTAL_PASS"
echo "  FAILED: $TOTAL_FAIL"
echo "=============================================="

if [[ $TOTAL_FAIL -gt 0 ]]; then
    exit 1
fi
exit 0
