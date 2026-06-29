# PlanSys2 Exercises — Symbolic Planning in ROS 2

These progressive exercises introduce **PlanSys2**, the ROS 2 bridge between PDDL-based symbolic planning and real robot execution. By the end you will be able to:

- Write a PDDL domain and problem from scratch
- Launch PlanSys2, load a problem via the terminal or a Python client, and retrieve a plan
- Extend a domain with resource constraints (battery)
- Connect PlanSys2 to Nav2 so a real (simulated) robot executes the plan in Gazebo

### Learning Objectives

| # | Exercise | PDDL Concepts | PlanSys2 / ROS 2 Skills |
|---|----------|---------------|------------------------|
| 0 | **Getting Started** | Understand PDDL domain structure (types, predicates, actions with typed parameters); understand problem structure (objects, init, goal) | Launch PlanSys2 with `model_file` and `problem_file` arguments; use `plansys2_terminal` to set instances, predicates, and goals interactively; inspect problem state with `get problem` commands |
| 1 | **Basic Transport** | Write a STRIPS domain (types, predicates, actions); write a problem (objects, initial state, goal); understand action preconditions and effects | Launch PlanSys2 with a domain file; use `plansys2_terminal` to set instances, predicates, and goals; request a plan; load a problem programmatically via ROS 2 services from Python |
| 2 | **Battery-Aware Planning** | Add resource predicates (`battery_high`, `battery_low`); model a new action (`recharge`) with preconditions that depend on resources; understand how constraints force the planner to insert extra steps | Compare two domain versions; observe how changing preconditions changes the plan; experiment by modifying the problem (moving the charger, removing it, adding rooms) |
| 3 | **Waypoint Navigation + Nav2** | Write a domain with durative actions and temporal planning (POPF); use ordering predicates (`next`) to enforce visitation sequences; map symbolic names to geometric coordinates | Build a custom ROS 2 package with an `ActionExecutorClient` node; integrate PlanSys2 with Nav2's `NavigateToPose` action; run a full simulation (Gazebo + Nav2 + PlanSys2); execute a plan end-to-end with feedback |

### Progressive Difficulty

```
Exercise 9.0          Exercise 9.1          Exercise 9.2          Exercise 9.3
  PlanSys2 basics   ─────►  PDDL basics   ─────►  Resource constraints ─────►  Real robot execution
  Launch + Terminal       Terminal + Python       Extended domain              Nav2 + Gazebo integration
  No execution            No execution            No execution                 Full simulation
```

---

## Prerequisites

- **Ubuntu 22.04** (or 24.04 with ROS 2 Jazzy)
- **ROS 2 Humble** (or Jazzy)
- **PlanSys2** packages
- A working terminal and basic familiarity with PDDL (types, predicates, actions, goals)

### Install PlanSys2

```bash
# ROS 2 Humble
sudo apt update
sudo apt install -y ros-humble-plansys2-*

# ROS 2 Jazzy
sudo apt update
sudo apt install -y ros-jazzy-plansys2-*
```

Verify the installation:

```bash
source /opt/ros/humble/setup.bash   # or jazzy
ros2 pkg list | grep plansys2
```

You should see packages such as:

```
plansys2_bringup
plansys2_core
plansys2_domain_expert
plansys2_executor
plansys2_planner
plansys2_problem_expert
plansys2_terminal
```

### Install a Standalone Planner (Optional — for offline validation)

You can validate any PDDL domain + problem pair **without ROS 2** using a planner like **VHPOP**, **Fast Downward**, or **POPF**. This is useful to catch modelling errors before launching ROS 2.

```bash
# Example with VHPOP (if available in your PDDL-course/Planners/ folder)
~/PDDL-course/Planners/vhpop domain.pddl problem.pddl
```

#### Installing POPF

POPF is the **default planner inside PlanSys2**. It supports temporal (durative) actions, which makes it the only planner among the three exercises capable of solving Exercise 9.3. You can also run POPF standalone to validate your PDDL files outside ROS 2.

```bash
# Clone POPF
git clone https://github.com/KCL-Planning/POPF.git
```

**Option A — Standalone build (CMake):**

```bash
cd POPF

# Install Python dependencies
pip3 install --user -r requirements.txt

# Build the C++ components
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_VERBOSE_MAKEFILE=ON ..
make -j$(nproc)
```

After building, the executable is at `POPF/build/popf`.

**Option B — Build with colcon (ROS 2 workspace):**

```bash
mkdir -p popf_ws/src
cp -r POPF popf_ws/src/

cd popf_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build \
  --packages-select popf \
  --cmake-args \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_VERBOSE_MAKEFILE=ON
source install/setup.bash
```

The executable is available as `ros2 run popf popf`.

```bash
./POPF/build/popf <domain.pddl> <problem.pddl>
```

Or add it to your PATH:

```bash
export PATH="$HOME/POPF/build:$PATH"
popf <domain.pddl> <problem.pddl>
```

**Note:** POPF requires Python 3.8+ and a C++17 compiler. On Ubuntu 22.04 these are available by default.

---

## PlanSys2 Architecture

PlanSys2 splits planning into four ROS 2 nodes:

| Node              | Role                                                                 |
|-------------------|----------------------------------------------------------------------|
| **Domain Expert** | Loads and maintains the PDDL domain (types, predicates, actions)     |
| **Problem Expert**| Stores the current problem: objects, facts, and goal                 |
| **Planner**       | Generates a plan using POPF (or another solver)                      |
| **Executor**      | Executes each action by calling the registered action performer nodes|

```
Domain Expert  ← PDDL domain
Problem Expert ← PDDL problem (instances, predicates, goal)
       ↓
    Planner  →  Plan (ordered list of actions)
       ↓
    Executor →  Action Performer Nodes (ROS 2 actions / services)
```

---

## Quick Start — Running the Official Example

Before the exercises, verify your installation with the bundled example:

```bash
source /opt/ros/humble/setup.bash

# Terminal 1 — launch PlanSys2
ros2 launch plansys2_bringup plansys2_bringup_launch_distributed.py \
  model_file:=/opt/ros/humble/share/plansys2_simple_example/pddl/domain.pddl \
  problem_file:=empty_problem.pddl

# Terminal 2 — interactive terminal
ros2 run plansys2_terminal plansys2_terminal
```

In the terminal type:

```
set instance room1 location
set instance room2 location
set predicate (robot_at room1)
set predicate (connected room1 room2)
set predicate (connected room2 room1)
set goal (and (robot_at room2))
get plan
```

Expected plan:

```
0: (move room1 room2) [0.001]
```

---

## Exercise 9.0 — Getting Started with PlanSys2

**Goal:** Launch PlanSys2 for the first time, load a domain and empty problem, then build a problem interactively through the terminal.

**Scenario:** A robot (`robot1`) is in the `kitchen` and needs to pick up a `coke` object and move it to the `livingroom`.

### Files

```
Exercise9.0/
├── robot_domain.pddl              # PDDL domain with typed parameters
├── empty_problem.pddl             # Minimal problem file (required for launch)
├── problem_setting.commands       # Terminal commands to set up the problem
└── tutorial.commands              # Extended tutorial with multiple rooms
```

### Step 1 — Understand the Domain

Open `robot_domain.pddl` and identify:

- **Types:** `robot`, `room`, `object`
- **Predicates:** `robot_at`, `object_at`, `gripper_empty`, `holding`
- **Actions:** `move`, `pick`, `place`

Notice that predicates and actions use **typed parameters** (e.g., `?r - robot`, `?rm - room`). This is more expressive than the simple untyped version.

### Step 2 — Launch PlanSys2

```bash
source /opt/ros/humble/setup.bash

# From the Exercise9.0 directory:
cd Exercise9.0

# Terminal 1 — launch PlanSys2 with domain and empty problem
ros2 launch plansys2_bringup plansys2_bringup_launch_distributed.py \
  model_file:=$(pwd)/robot_domain.pddl \
  problem_file:=empty_problem.pddl
```

The `problem_file:=empty_problem.pddl` argument loads a minimal problem so the system starts with valid state. You will then modify the problem interactively through the terminal.

Check that the nodes started correctly:

```bash
# Terminal 3 — verify
ros2 node list
ros2 service list | grep -E "domain_expert|problem_expert|planner"
```

You should see `domain_expert`, `problem_expert`, `planner`, and `executor` nodes.

### Step 3 — Set Up the Problem via Terminal

```bash
# Terminal 2 — interactive terminal
ros2 run plansys2_terminal plansys2_terminal
```

Then paste the commands from `problem_setting.commands`:

```
set instance robot1 robot
set instance kitchen room
set instance livingroom room
set instance coke object
set predicate (robot_at robot1 kitchen)
set predicate (object_at coke kitchen)
set predicate (gripper_empty robot1)

get problem instances
get problem predicates
```

### Step 4 — Set the Goal and Get a Plan

In the terminal, continue:

```
set goal (and (object_at coke livingroom))
get problem goal
get plan
```

Expected plan:

```
0:      (pick robot1 coke kitchen)        [0.001]
0.001:  (move robot1 kitchen livingroom)  [0.001]
0.002:  (place robot1 coke livingroom)    [0.001]
```

**Explanation:** The robot picks the coke in the kitchen, moves to the livingroom, and places the coke.

### Step 5 — Extended Tutorial

Try the extended scenario from `tutorial.commands` — it sets up a multi-room environment with a robot named `leia`:

```
set instance leia robot
set instance entrance room
set instance kitchen room
set instance bedroom room
set instance dinning room
set instance bathroom room
set instance chargingroom room

set predicate (connected entrance dinning)
set predicate (connected dinning entrance)
set predicate (connected dinning kitchen)
set predicate (connected kitchen dinning)
set predicate (connected dinning bedroom)
set predicate (connected bedroom dinning)
set predicate (connected bathroom bedroom)
set predicate (connected bedroom bathroom)
set predicate (connected chargingroom kitchen)
set predicate (connected kitchen chargingroom)

set predicate (charging_point_at chargingroom)
set predicate (battery_low leia)
set predicate (robot_at leia entrance)

set goal (and (robot_at leia bathroom))
get plan
```

This sets up a house with six rooms and asks the robot to navigate from `entrance` to `bathroom`.

**Note:** If you source `tutorial.commands` directly (e.g., `source tutorial.commands`), you may see warnings like:

```
getExpr: Error parsing expresion [ (and(robot_at leia bathroom))]
getExpr: Error parsing expresion [(robot_at leia bathroom)]
```

These are **harmless warnings** — the system is still working correctly. The `plansys2_terminal` parser accepts the commands without issue when pasted interactively. The warning only appears when the file is sourced as a shell script.

### Useful Commands

See the [Common Commands Cheat Sheet](#common-commands-cheat-sheet) below.

---

## Exercise 9.1 — Basic Transport with PlanSys2

**Goal:** Load a simple robot-transport domain into PlanSys2, set up a problem interactively through the terminal, and obtain a plan.

**Scenario:** A robot must move a box from `room1` to `room2`. The robot can `move`, `pick`, and `place`.

### Files

```
Exercise9.1/
├── pddl/
│   ├── robot_domain.pddl              # PDDL domain
│   ├── robot_problem.pddl             # PDDL problem (for offline validation)
│   ├── test_basic_transport.pddl      # Test: basic box transport
│   ├── test_same_room_goal.pddl       # Test: goal already satisfied
│   ├── test_two_objects.pddl          # Test: two boxes to move
│   ├── test_three_rooms.pddl          # Test: three-room chain
│   └── test_unreachable.pddl          # Test: no path between rooms
├── scripts/
│   ├── load_problem_and_plan.py       # Python client to load problem + get plan
│   └── test_planner.py                # Automated test suite (vhpop or popf)
└── problem_terminal.commands          # Commands for plansys2_terminal
```

### Step 1 — Understand the Domain

Open `pddl/robot_domain.pddl` and identify:

- **Types:** `location`, `object`
- **Predicates:** `robot_at`, `connected`, `object_at`, `holding`, `hand_empty`
- **Actions:** `move`, `pick`, `place`

### Step 2 — Validate with a Standalone Planner

Run the problem through VHPOP and POPF to compare the results:

```bash
# VHPOP
vhpop pddl/robot_domain.pddl pddl/robot_problem.pddl

# POPF
popf pddl/robot_domain.pddl pddl/robot_problem.pddl
```

Expected output (VHPOP):

```
1:(pick box room1)
2:(move room1 room2)
3:(place box room2)
```

Expected output (POPF):

```
Plan found
Plan length: 3

0.000: (pick box room1) [0.001]
0.001: (move room1 room2) [0.001]
0.002: (place box room2) [0.001]
```

**POPF vs VHPOP:** Both planners find the same sequence of actions. VHPOP prints actions as a numbered list, while POPF prints each action with its start time and duration in brackets. POPF's output format is the same format you will see inside PlanSys2, because POPF is PlanSys2's default solver.

### Step 3 — Launch PlanSys2

```bash
source /opt/ros/humble/setup.bash

# Terminal 1 — launch PlanSys2 with the domain
ros2 launch plansys2_bringup plansys2_bringup_launch_distributed.py \
  model_file:=$(pwd)/pddl/robot_domain.pddl \
  problem_file:=empty_problem.pddl
```

Check that the nodes started correctly:

```bash
# Terminal 3 — verify
ros2 node list
ros2 service list | grep -E "domain_expert|problem_expert|planner"
```

You should see `domain_expert`, `problem_expert`, `planner`, and `executor` nodes.

### Step 4 — Load the Problem via Terminal

```bash
# Terminal 2 — interactive terminal
ros2 run plansys2_terminal plansys2_terminal
```

Then paste the commands from `problem_terminal.commands`:

```
set instance room1 location
set instance room2 location
set instance box object
set predicate (robot_at room1)
set predicate (object_at box room1)
set predicate (connected room1 room2)
set predicate (connected room2 room1)
set predicate (hand_empty)
set goal (and (object_at box room2))
get problem instances
get problem predicates
get problem goal
get plan
```

Expected plan:

```
0:      (pick box room1)        [0.001]
0.001:  (move room1 room2)      [0.001]
0.002:  (place box room2)       [0.001]
```

**Explanation:** The robot picks the box in room1, moves to room2, and places the box.

### Step 5 — Load the Problem via Python

```bash
# Terminal 2 (after closing the terminal)
python3 load_problem_and_plan.py
```

Expected output:

```
Plan generated from Python:
0.000: (pick box room1) [0.001]
0.001: (move room1 room2) [0.001]
0.002: (place box room2) [0.001]
```

### Step 6 — Run the Test Suite

The `scripts/test_planner.py` script runs five test problems and verifies the results automatically:

| Test | Description | Expected |
|------|-------------|----------|
| Basic transport | Move box from room1 to room2 | 3 actions: pick, move, place |
| Same room goal | Box already at goal | Empty plan (0 actions) |
| Two objects | Move two boxes to room2 | 7 actions (pick→move→place→move→pick→move→place) |
| Three rooms | Move box through room1 → room2 → room3 | 4 actions |
| Unreachable | No connection between rooms | No plan possible |

#### Running with VHPOP

```bash
# If vhpop is in your PATH or at PDDL-course/Planners/vhpop (auto-detected):
python3 scripts/test_planner.py

# Or specify the path explicitly:
python3 scripts/test_planner.py vhpop
python3 scripts/test_planner.py ~/PDDL-course/Planners/vhpop
```

#### Running with POPF

```bash
# If popf is in your PATH (auto-detected):
python3 scripts/test_planner.py

# Or specify the path explicitly:
python3 scripts/test_planner.py popf
python3 scripts/test_planner.py ~/POPF/build/popf
```

#### Running with a Custom Planner

Any planner that accepts `planner domain.pddl problem.pddl` and prints actions in a numbered format can be used:

```bash
python3 scripts/test_planner.py /path/to/your/planner
```

#### Expected Output (VHPOP)

```
Running tests with VHPOP
Domain: .../Exercise9.1/pddl/robot_domain.pddl
============================================================

Test 1: Basic transport
  Description: Move box from room1 to room2
  Problem: test_basic_transport.pddl
  OK: Plan length 3
  OK: Actions match expected set

Test 2: Same room goal
  Description: Box already at goal — plan should be empty (0 actions)
  Problem: test_same_room_goal.pddl
  OK: Empty plan (goal already satisfied)

Test 3: Two objects
  Description: Move two boxes from room1 to room2 (pick→move→place→move→pick→move→place)
  Problem: test_two_objects.pddl
  OK: Plan length 7
  OK: Actions match expected set

Test 4: Three rooms
  Description: Move box through three rooms (room1 -> room2 -> room3)
  Problem: test_three_rooms.pddl
  OK: Plan length 4
  OK: Actions match expected set

Test 5: Unreachable
  Description: No connection between rooms — no plan possible
  Problem: test_unreachable.pddl
  OK: Planner timed out (as expected for unsolvable problem)

============================================================
SUMMARY
============================================================
  [PASS] Basic transport
  [PASS] Same room goal
  [PASS] Two objects
  [PASS] Three rooms
  [PASS] Unreachable

5/5 tests passed
All tests passed!
```

#### Expected Output (POPF)

```
Running tests with POPF
Domain: .../Exercise9.1/pddl/robot_domain.pddl
============================================================

Test 1: Basic transport
  Description: Move box from room1 to room2
  Problem: test_basic_transport.pddl
  OK: Plan length 3
  OK: Actions match expected set

Test 2: Same room goal
  Description: Box already at goal — plan should be empty (0 actions)
  Problem: test_same_room_goal.pddl
  OK: Empty plan (goal already satisfied)

Test 3: Two objects
  Description: Move two boxes from room1 to room2 (pick→move→place→move→pick→move→place)
  Problem: test_two_objects.pddl
  OK: Plan length 7
  OK: Actions match expected set

Test 4: Three rooms
  Description: Move box through three rooms (room1 -> room2 -> room3)
  Problem: test_three_rooms.pddl
  OK: Plan length 4
  OK: Actions match expected set

Test 5: Unreachable
  Description: No connection between rooms — no plan possible
  Problem: test_unreachable.pddl
  OK: No plan found (as expected)

============================================================
SUMMARY
============================================================
  [PASS] Basic transport
  [PASS] Same room goal
  [PASS] Two objects
  [PASS] Three rooms
  [PASS] Unreachable

5/5 tests passed
All tests passed!
```

**Note:** The unreachable test behaves differently between planners. VHPOP times out (it keeps searching), while POPF detects the problem is unsolvable immediately. Both outcomes are accepted by the test script.

### Useful Commands

See the [Common Commands Cheat Sheet](#common-commands-cheat-sheet) below.

### ROS 2 Services Used by the Python Client

| Service                                    | Purpose                                      |
|--------------------------------------------|----------------------------------------------|
| `/problem_expert/clear_problem_knowledge`  | Clear the current problem state              |
| `/problem_expert/add_problem`              | Load a full PDDL problem file as text        |
| `/planner/get_plan`                        | Request a plan given domain + problem text   |

---

## Exercise 9.2 — Battery-Aware Planning

**Goal:** Extend the domain with a battery constraint so the robot must recharge before it can continue moving.

**Scenario:** The robot must move a box from `room1` to `room2`, but there is an intermediate room `room_mid` with a charger. Each `move` action drains the battery from `high` to `low`. The robot can only move when the battery is `high`, and must `recharge` at a location with a charger.

### Files

```
Exercise9.2/
├── pddl/
│   ├── robot_domain_energy.pddl           # Extended domain with battery + recharge
│   ├── robot_problem_energy.pddl          # Problem with 3 rooms and charger
│   ├── test_energy_basic.pddl             # Test: basic recharge scenario
│   ├── test_energy_charger_at_start.pddl  # Test: charger at room1
│   ├── test_energy_no_charger.pddl        # Test: no charger — unreachable
│   ├── test_energy_four_rooms.pddl        # Test: four rooms, two chargers
│   └── test_energy_start_low.pddl         # Test: start with low battery
├── scripts/
│   ├── load_problem_and_plan.py           # Python client to load problem + get plan
│   └── test_planner.py                    # Automated test suite (vhpop or popf)
└── problem_terminal.commands              # Terminal commands for the energy problem
```

### Step 1 — Compare Domains

Compare `robot_domain_energy.pddl` with `robot_domain.pddl` from Exercise 9.1. Identify the differences:

**New predicates:**
- `battery_high` — robot has enough battery to move
- `battery_low` — robot needs to recharge
- `charger_at ?l` — there is a charger at location `l`

**Modified action `move`:**
- Now requires `(battery_high)` as precondition
- Effect includes `(not (battery_high))` and `(battery_low)`

**New action `recharge`:**
- Requires robot at a location with a charger and battery low
- Restores battery to high

### Step 2 — Validate with a Standalone Planner

```bash
# VHPOP
vhpop pddl/robot_domain_energy.pddl pddl/robot_problem_energy.pddl

# POPF
popf pddl/robot_domain_energy.pddl pddl/robot_problem_energy.pddl
```

Expected output (VHPOP):

```
1:(pick box room1)
2:(move room1 room_mid)
3:(recharge room_mid)
4:(move room_mid room2)
5:(place box room2)
```

Expected output (POPF):

```
Plan found
Plan length: 5

0.000: (pick box room1) [0.001]
0.001: (move room1 room_mid) [0.001]
0.002: (recharge room_mid) [0.001]
0.003: (move room_mid room2) [0.001]
0.004: (place box room2) [0.001]
```

Notice how both planners insert `recharge room_mid` between the two moves. The battery constraint forces the planner to find a plan that includes recharging. POPF's output format matches what PlanSys2 will produce, since POPF is PlanSys2's built-in solver.

### Step 3 — Launch PlanSys2 with the Energy Domain

```bash
source /opt/ros/humble/setup.bash

# Terminal 1 — from the Exercise9.2 directory:
cd Exercise9.2
ros2 launch plansys2_bringup plansys2_bringup_launch_distributed.py \
  model_file:=$(pwd)/pddl/robot_domain_energy.pddl \
  problem_file:=empty_problem.pddl
```

### Step 4 — Load the Problem via Terminal

```bash
# Terminal 2
ros2 run plansys2_terminal plansys2_terminal
```

Paste the commands from `problem_terminal.commands`:

```
set instance room1 location
set instance room_mid location
set instance room2 location
set instance box object
set predicate (robot_at room1)
set predicate (object_at box room1)
set predicate (connected room1 room_mid)
set predicate (connected room_mid room1)
set predicate (connected room_mid room2)
set predicate (connected room2 room_mid)
set predicate (charger_at room_mid)
set predicate (battery_high)
set predicate (hand_empty)
set goal (and (object_at box room2))
get problem instances
get problem predicates
get problem goal
get plan
```

Expected plan:

```
0:      (pick box room1)        [0.001]
0.001:  (move room1 room_mid)   [0.001]
0.002:  (recharge room_mid)     [0.001]
0.003:  (move room_mid room2)   [0.001]
0.004:  (place box room2)       [0.001]
```

### Step 5 — Run the Test Suite

The `scripts/test_planner.py` script runs five test problems and verifies the results:

| Test | Description | Expected |
|------|-------------|----------|
| Energy basic | Box from room1 to room2 via room_mid | 5 actions, includes `recharge` |
| Charger at start | Charger at room1 instead of room_mid | 5 actions, still needs recharge |
| No charger | No charger anywhere | No plan possible |
| Four rooms | Four rooms with two chargers | 7 actions, recharges twice |
| Start low battery | Robot starts with `battery_low` | 6 actions, must recharge first |

#### Running with VHPOP

```bash
# Auto-detect (if vhpop is in PATH or at PDDL-course/Planners/vhpop):
python3 scripts/test_planner.py

# Or specify explicitly:
python3 scripts/test_planner.py vhpop
python3 scripts/test_planner.py ~/PDDL-course/Planners/vhpop
```

#### Running with POPF

```bash
# Auto-detect (if popf is in PATH):
python3 scripts/test_planner.py

# Or specify explicitly:
python3 scripts/test_planner.py popf
python3 scripts/test_planner.py ~/POPF/build/popf
```

#### Running with a Custom Planner

Any planner that accepts `planner domain.pddl problem.pddl` and prints actions in a numbered format can be used:

```bash
python3 scripts/test_planner.py /path/to/your/planner
```

#### Expected Output (VHPOP)

```
Running tests with VHPOP
Domain: .../Exercise9.2/pddl/robot_domain_energy.pddl
============================================================

Test 1: Energy basic (recharge required)
  Description: Box from room1 to room2 via room_mid with recharge
  Problem: test_energy_basic.pddl
  OK: Plan length 5
  OK: Plan contains required actions: ['recharge']

Test 2: Charger at start
  Description: Charger at room1 — robot must still recharge between moves
  Problem: test_energy_charger_at_start.pddl
  OK: Plan length 5
  OK: Plan contains required actions: ['recharge']

Test 3: No charger (unreachable)
  Description: No charger anywhere — cannot recharge, no plan possible
  Problem: test_energy_no_charger.pddl
  OK: Planner timed out (as expected for unsolvable problem)

Test 4: Four rooms with two chargers
  Description: Four rooms, two chargers — robot recharges twice
  Problem: test_energy_four_rooms.pddl
  OK: Plan length 7
  OK: Plan contains required actions: ['recharge']

Test 5: Start with low battery
  Description: Robot starts with low battery — must recharge first
  Problem: test_energy_start_low.pddl
  OK: Plan length 6
  OK: Plan contains required actions: ['recharge']

============================================================
SUMMARY
============================================================
  [PASS] Energy basic (recharge required)
  [PASS] Charger at start
  [PASS] No charger (unreachable)
  [PASS] Four rooms with two chargers
  [PASS] Start with low battery

5/5 tests passed
All tests passed!
```

#### Expected Output (POPF)

```
Running tests with POPF
Domain: .../Exercise9.2/pddl/robot_domain_energy.pddl
============================================================

Test 1: Energy basic (recharge required)
  Description: Box from room1 to room2 via room_mid with recharge
  Problem: test_energy_basic.pddl
  OK: Plan length 5
  OK: Plan contains required actions: ['recharge']

Test 2: Charger at start
  Description: Charger at room1 — robot must still recharge between moves
  Problem: test_energy_charger_at_start.pddl
  OK: Plan length 5
  OK: Plan contains required actions: ['recharge']

Test 3: No charger (unreachable)
  Description: No charger anywhere — cannot recharge, no plan possible
  Problem: test_energy_no_charger.pddl
  OK: Planner timed out (as expected for unsolvable problem)

Test 4: Four rooms with two chargers
  Description: Four rooms, two chargers — robot recharges twice
  Problem: test_energy_four_rooms.pddl
  OK: Plan length 7
  OK: Plan contains required actions: ['recharge']

Test 5: Start with low battery
  Description: Robot starts with low battery — must recharge first
  Problem: test_energy_start_low.pddl
  OK: Plan length 6
  OK: Plan contains required actions: ['recharge']

============================================================
SUMMARY
============================================================
  [PASS] Energy basic (recharge required)
  [PASS] Charger at start
  [PASS] No charger (unreachable)
  [PASS] Four rooms with two chargers
  [PASS] Start with low battery

5/5 tests passed
All tests passed!
```

**Note:** The no-charger test is genuinely unsolvable — the robot cannot reach room2 without recharging, and there is no charger. Both VHPOP and POPF will timeout on this problem (POPF's static analysis cannot detect this case without search). The test script accepts timeout as a valid result for this test.

### Step 6 — Experiment

Try modifying the problem:

1. **Move the charger to `room1` instead of `room_mid`** — does the plan change?
2. **Remove the charger entirely** — what happens when you request a plan?
3. **Add a fourth room** — how does the planner handle longer chains?

---

## Exercise 9.3 — Waypoint Navigation with Nav2 Integration

**Goal:** Connect PlanSys2 to Nav2 so a simulated TurtleBot3 executes a waypoint navigation plan in Gazebo.

**Scenario:** A robot must visit five waypoints (`wp1` → `wp2` → `wp3` → `wp4` → `wp5`) in order. PlanSys2 generates the symbolic plan, and a custom action performer node translates each `navigate` action into a Nav2 `NavigateToPose` goal.

### Architecture

```
PDDL Domain + Problem
       ↓
PlanSys2 (Domain Expert → Problem Expert → Planner)
       ↓  Plan: (navigate turtlebot start wp1) ...
navigate_action_node (ActionExecutorClient)
       ↓  NavigateToPose action
Nav2 (move_base)
       ↓
TurtleBot3 in Gazebo
```

### Files

```
Exercise9.3/
├── problem_terminal.commands               # Commands for plansys2_terminal
└── src/plansys2_waypoint_nav/              # ROS 2 package (single source of truth)
    ├── CMakeLists.txt
    ├── package.xml
    ├── config/
    │   └── waypoints.yaml                  # Maps symbolic names to (x, y, z, w) poses
    ├── launch/
    │   └── simulation.launch.py  # Launches Gazebo + Nav2 + PlanSys2
    ├── pddl/
    │   ├── domain_waypoint_mission.pddl    # PDDL domain with durative actions
    │   └── problem_waypoint_mission.pddl   # PDDL problem with 5 waypoints
    ├── scripts/
    │   ├── execute_plan.py  # Python client: load + plan + execute
    │   └── publish_initial_pose.py             # Publishes initial pose for Nav2
    └── src/
        └── navigate_action_node.cpp        # Action performer: PDDL → Nav2
```

### Step 1 — Understand the Domain

Open `src/plansys2_waypoint_nav/pddl/domain_waypoint_mission.pddl`:

- **Types:** `robot`, `waypoint`
- **Predicates:** `robot_at`, `connected`, `next`, `visited`
- **Durative action `navigate`:** moves the robot between connected waypoints in 1 time unit

The `next` predicate enforces the visitation order. Without it, the planner could visit waypoints in any order.

**Important:** This domain uses `:durative-actions`, which means actions have a duration. VHPOP does **not** support durative actions — only POPF can solve this problem. This is why POPF is the default planner in PlanSys2.

### Step 2 — Validate with POPF

```bash
# POPF (required — VHPOP cannot handle durative actions)
popf src/plansys2_waypoint_nav/pddl/domain_waypoint_mission.pddl \
  src/plansys2_waypoint_nav/pddl/problem_waypoint_mission.pddl
```

Expected output:

```
1:(navigate turtlebot start wp1)
2:(navigate turtlebot wp1 wp2)
3:(navigate turtlebot wp2 wp3)
4:(navigate turtlebot wp3 wp4)
5:(navigate turtlebot wp4 wp5)
```

### Step 3 — Build the ROS 2 Package

```bash
# Create a workspace
mkdir -p plansys2_ws/src
cp -r Exercise9.3/src/plansys2_waypoint_nav plansys2_ws/src/

cd plansys2_ws

# Install dependencies
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build --symlink-install
source install/setup.bash
```

Verify the executables:

```bash
ros2 pkg executables plansys2_waypoint_nav
```

Expected:

```
plansys2_waypoint_nav execute_plan.py
plansys2_waypoint_nav navigate_action_node
```

### Step 4 — Run the Full Simulation

You need **TurtleBot3 Gazebo**, **Nav2**, and **PlanSys2** installed:

```bash
sudo apt install -y ros-humble-turtlebot3-* ros-humble-nav2-*
```

**Terminal 1 — Launch Gazebo + Nav2 + PlanSys2:**

```bash
source install/setup.bash
ros2 launch plansys2_waypoint_nav simulation.launch.py
```

This single launch file starts:
- Gazebo with the TurtleBot3 warehouse world
- Nav2 with AMCL, planner, and controller
- PlanSys2 with the waypoint domain loaded
- The `navigate_action_node` action performer

**Terminal 2 — Execute the Plan:**

```bash
source install/setup.bash
ros2 run plansys2_waypoint_nav execute_plan.py
```

Expected output:

```
Waiting for service /problem_expert/clear_problem_knowledge...
Waiting for service /problem_expert/add_problem...
Waiting for service /planner/get_plan...
Waiting for action /execute_plan...
Plan generated by PlanSys2:
0.000: (navigate turtlebot start wp1) [1.000]
1.001: (navigate turtlebot wp1 wp2) [1.000]
2.002: (navigate turtlebot wp2 wp3) [1.000]
3.003: (navigate turtlebot wp3 wp4) [1.000]
4.004: (navigate turtlebot wp4 wp5) [1.000]
Sending plan to PlanSys2 executor...
Executing (navigate turtlebot start wp1): 0.50 - Navigate running
...
Execution result: success
```

**Terminal 3 (Optional) — Interactive Terminal:**

```bash
source /opt/ros/humble/setup.bash
ros2 run plansys2_terminal plansys2_terminal
```

Useful commands:
- `get plan` — request a plan
- `execute plan` — send the plan to the executor
- `get knowledge` — show current predicates

### Step 5 — Understand the Action Performer

The file `navigate_action_node.cpp` is the bridge between PlanSys2 and Nav2:

1. It inherits from `plansys2::ActionExecutorClient`
2. It registers as the performer for the `navigate` PDDL action
3. When PlanSys2 dispatches `(navigate turtlebot wp2 wp3)`, the node:
   - Extracts the third argument (`wp3`)
   - Looks up `wp3`'s coordinates in `waypoints.yaml`
   - Sends a `NavigateToPose` action goal to Nav2
   - Reports feedback and completion back to PlanSys2

### Step 6 — Experiment

1. **Modify `waypoints.yaml`** — change a waypoint's coordinates and re-run
2. **Add a sixth waypoint** — update the domain, problem, and YAML file
3. **Change the visitation order** — modify the `next` predicates in the problem

---

## Common Commands Cheat Sheet

### Launch PlanSys2

```bash
# Distributed (separate nodes)
ros2 launch plansys2_bringup plansys2_bringup_launch_distributed.py \
  model_file:=<path-to-domain.pddl> \
  problem_file:=empty_problem.pddl

# Monolithic (single process)
ros2 launch plansys2_bringup plansys2_bringup_launch_monolithic.py \
  model_file:=<path-to-domain.pddl> \
  problem_file:=empty_problem.pddl
```

The `problem_file` argument is required — use `empty_problem.pddl` to start with an empty problem that you can fill interactively through the terminal.

### Terminal

```bash
ros2 run plansys2_terminal plansys2_terminal

# Or pipe commands from a file
ros2 run plansys2_terminal plansys2_terminal < problem_terminal.commands
```

### Inspect the System

```bash
ros2 node list
ros2 service list
ros2 topic list
ros2 action list
```

### Python Client Pattern

```python
import rclpy
from rclpy.node import Node
from plansys2_msgs.srv import AddProblem, ClearProblemKnowledge, GetPlan

class PlanSys2Client(Node):
    def __init__(self):
        super().__init__("plansys2_client")
        self.clear_cli = self.create_client(ClearProblemKnowledge, "/problem_expert/clear_problem_knowledge")
        self.add_cli   = self.create_client(AddProblem, "/problem_expert/add_problem")
        self.plan_cli  = self.create_client(GetPlan, "/planner/get_plan")

    def wait_for_services(self):
        for cli, name in [(self.clear_cli, "clear"), (self.add_cli, "add"), (self.plan_cli, "plan")]:
            self.get_logger().info(f"Waiting for {name}...")
            cli.wait_for_service()
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `No problem file specified` in terminal | Normal — the problem is loaded interactively with `set` commands |
| Planner returns no plan | Check that preconditions can be satisfied; verify `connected` predicates are bidirectional |
| `Could not contact planner` | Make sure PlanSys2 is launched and `ros2 node list` shows `/planner` |
| Action performer not found | The node must be running and registered with the correct action name |
| `ros-humble-test-msgs` error during build | Run `sudo apt install ros-humble-test-msgs` then rebuild |
| `getExpr: Error parsing expresion` warnings | Harmless — occurs when sourcing `.commands` files with `source`. The system works correctly. Paste commands interactively instead. |

---

## Further Reading

- [PlanSys2 Documentation](https://intelligentroboticslab.github.io/PlanSys2/)
- [PDDL Specification](http://metatheory.matthewtdavis.com/pddl/)
- [ROS 2 Nav2 Documentation](https://docs.nav2.org/)
- [POPF Planner](https://www.robots.ox.ac.uk/~avigad/teaching/Planning/POPF/)
