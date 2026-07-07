# Session: Cognitive Architectures, Task Planning, and PDDL

**Summer School for Software Engineering in Robotics**

**Francisco J. Rodriguez Lera**

---

## Outline

1. Introduction & Cognitive Architectures
2. What is AI Planning?
3. PDDL History & Versions
4. PDDL Fundamentals
5. Actions Deep Dive
6. Worked Example
7. Planning Algorithms & Sussman Anomaly
8. Plan Validity & Type Correctness
9. Temporal & Advanced PDDL
10. Planners & Tools
11. PDDL in Robotics
12. Exercises
13. References & Resources

---

## 1. Introduction & Cognitive Architectures

### The Robot Decision Problem

A robot must decide **what to do** and **in what order** to accomplish a task. This is not just about low-level control (motors, sensors) but about high-level reasoning:

- Which actions should I perform?
- In what sequence?
- What if something goes wrong?
- How do I know when I'm done?

This is the domain of **task planning**.

### Cognitive Architectures

A cognitive architecture provides the overall structure for how an autonomous agent perceives, reasons, and acts. Three main paradigms:

| Architecture | Approach | Representative |
|---|---|---|
| **Deliberative** | SENSE → PLAN → ACT | Fikes, STRIPS |
| **Reactive** | Stimulus → Response (no explicit plan) | Brooks, Subsumption |
| **Hybrid** | Deliberative layer + Reactive layer | Arkin, GAT (Three-Layer) |

**Deliberative architectures** build an explicit model of the world, search for a plan, then execute it step by step. This is where PDDL fits in.

**Reactive architectures** bypass planning entirely — behavior emerges from layered reflexes. Fast but limited in long-horizon tasks.

**Hybrid architectures** combine both: a deliberative layer handles long-term goals and planning, while a reactive layer handles real-time responses to unexpected events.

> **References:**
> - Ingrand & Ghallab (2017). *Deliberation for autonomous robots: A survey.* Artificial Intelligence, 247, 10-44.
> - Kotseruba & Tsotsos (2020). *40 years of cognitive architectures.* Artif Intell Rev 53, 17-94.

### The SENSE-PLAN-ACT Cycle

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  SENSE   │────▶│  PLAN    │────▶│  ACT     │
└─────────┘     └─────────┘     └─────────┘
      ▲                            │
      │                            │
      └────────────────────────────┘
```

1. **SENSE**: Perceive the current state of the world
2. **PLAN**: Given the current state and a goal, generate a sequence of actions
3. **ACT**: Execute the first action, then loop

This cycle is the foundation of deliberative robot architectures. PDDL provides the language to formalize the PLAN step.

---

## 2. What is AI Planning?

### Formal Definition

**Automated planning** is the process of finding a sequence of actions that transforms an initial state into a goal state, given a model of what actions are available and how they change the world.

Formally, a planning problem is a tuple **Σ = (S, A, E, γ)**:

- **S**: A recursively enumerable set of states
- **A**: A recursively enumerable set of actions (controlled by the planner, may include a "no-op")
- **E**: A recursively enumerable set of events (uncontrolled by the planner, may include a neutral event "e")
- **γ**: A transition function mapping (state, action, event) → 2^S (a subset of possible next states)

### Planning System vs. Planner

| Term | Meaning |
|---|---|
| **Planning System** | The complete pipeline: model formalization + search + solution extraction |
| **Planner** | The algorithm that takes a formalized problem and produces a plan |

The planner is **domain-independent**: it doesn't need to know what the domain represents. It operates purely on the formal structure — predicates, actions, preconditions, effects.

However, **not every planner can solve every problem**. Planners differ in:
- Which PDDL features they support
- Search strategies (forward, backward, SAT-based, etc.)
- Trade-offs between completeness and efficiency

### Why Planning Matters in Robotics

Planning enables robots to:
- Handle complex multi-step tasks without hardcoding every scenario
- Adapt to new goals by re-planning rather than reprogramming
- Reason about resource constraints, time, and dependencies
- Integrate with perception and execution systems through formal interfaces

---

## 3. PDDL History & Versions

### Origins

PDDL (Planning Domain Definition Language) was created for the **1998 International Planning Competition (IPC)** to enable empirical comparison between planning systems. It has since become the de facto standard for classical planning benchmarks.

### Version Timeline

| Version | Year | Key Features |
|---|---|---|
| **PDDL 1.0** | 1998 | Basic STRIPS: predicates, actions, preconditions, effects |
| **PDDL 1.1** | 1998 | Added ADL: negative/disjunctive preconditions, quantifiers, conditional effects |
| **PDDL 1.2** | 2000 | Added typing, equality, ADL in effects |
| **PDDL 2.0** | 2002 | Added durative actions, numeric fluents, temporal constraints |
| **PDDL 2.1** | 2002 | Refined durative actions, duration inequalities, plan metrics |
| **PDDL 2.2** | 2004 | Added axioms, timed initial literals |
| **PDDL 3.0** | 2006 | Added trajectory constraints, preferences |
| **PDDL 3.1** | 2008 | Added object fluents |

### Notable Extensions

| Extension | Purpose |
|---|---|
| **PDDL+** | Continuous change, predictable exogenous events |
| **NDDL** | NASA's activity/constraint-based language |
| **MA-PDDL** | Multi-agent planning with communication |
| **PPDDL** | Probabilistic effects and observations |
| **MAPL** | Multi-agent planning language |
| **RDDL** | Relational Dynamic Influence Diagrams |

### The IPC Connection

Each IPC competition drives PDDL evolution:
- **IPC 1998**: STRIPS and ADL tracks
- **IPC 2000**: STRIPS, ADL, temporal, metric
- **IPC 2004**: Classical, satisficing, optimal, temporal, metric
- **IPC 2006**: Added continuous change, multi-modal
- **IPC 2008**: Deterministic, probabilistic, temporal
- **IPC 2011**: Deterministic, contingent, continuous-time
- **IPC 2014**: Sequential, multi-objective, temporal
- **IPC 2018**: Sequential, multi-objective, temporal, multi-agent

> **Reference:** [ICAPS Competitions](https://icaps-conference.org/index.php/Main/Competitions)

---

## 4. PDDL Fundamentals

### Two Files: Domain and Problem

Every PDDL planning problem consists of **two files**:

1. **Domain file** (`domain.pddl`): Defines what actions exist and how they work (the "physics" of the world)
2. **Problem file** (`problem.pddl`): Defines the specific instances, initial state, and goal (a specific "puzzle")

This separation allows the same domain to be reused across many different problem instances.

### Basic Structure

```pddl
;; Domain file
(define (domain <name>)
  (:requirements ...)
  (:types ...)
  (:predicates ...)
  (:functions ...)
  (:action <name>
    :parameters (...)
    :precondition (...)
    :effect (...)))

;; Problem file
(define (problem <name>)
  (:domain <domain-name>)
  (:objects ...)
  (:init ...)
  (:goal ...))
```

### Requirements

The `:requirements` section declares which PDDL features the domain uses:

| Requirement | Feature |
|---|---|
| `:strips` | Basic STRIPS operators (add/delete lists) |
| `:typing` | Typed object declarations |
| `:adl` | Action Description Language (negation, disjunction, quantifiers in preconditions) |
| `:negative-preconditions` | `not` in preconditions |
| `:disjunctive-preconditions` | `or` in preconditions |
| `:equality` | `=` and `/=` in conditions |
| `:conditional-effects` | `when` in effects |
| `:fluents` | Numeric functions that change over time |
| `:durative-actions` | Actions with duration, `at start`/`at end`/`over all` |
| `:duration-inequalities` | Duration constraints like `(/= ?duration 0)` |
| `:timed-initial-literals` | Facts that become true at specific times |
| `:axioms` | Derived predicates (functions of state) |

**Important:** Most planners do NOT fully support all PDDL features. Always check your planner's documentation.

### Types

Types organize objects into categories:

```pddl
(:types robot location object)
```

Types form a hierarchy — every type is a subtype of `object` (the implicit root). You can define subtypes:

```pddl
(:types
  (room building - location)
  (drone robot)
  (package object))
```

Here, `room` and `building` are subtypes of `location`; `drone` is a subtype of `robot`.

### Predicates

Predicates describe facts about the world:

```pddl
(:predicates
  (at ?r - robot ?loc - location)
  (holding ?r - robot ?obj - object)
  (connected ?l1 ?l2 - location))
```

Key points:
- Predicates have **no intrinsic meaning** — their meaning comes from how actions affect them and what's true in the initial state
- Parameters in predicate declarations only specify **arity** and **types** — the parameter names don't matter
- **Static predicates** are never changed by any action (e.g., `connected`)
- **Dynamic predicates** are modified by action effects (e.g., `at`, `holding`)

### Functions (Numeric Fluents)

Functions map objects to numeric values:

```pddl
(:functions
  (battery ?r - robot)
  (distance ?l1 ?l2 - location))
```

Functions can be **static** (constant throughout planning) or **fluents** (change via action effects).

---

## 5. Actions Deep Dive

### Action Structure

```pddl
(:action <name>
  :parameters (?x - type ?y - type ...)
  :precondition (<condition>)
  :effect (<effects>))
```

All parts except the name are technically optional, though most planners require at least preconditions and effects.

### Parameters

Parameters are typed variables that become concrete objects when an action is instantiated:

```pddl
:parameters (?r - robot ?from - location ?to - location)
```

When applied: `(move robot1 loc1 loc2)` — the parameters are **grounded** to specific objects.

### Preconditions: STRIPS vs. ADL

**STRIPS preconditions** (simplest):
```pddl
;; Atomic fact
(at ?r ?loc)

;; Conjunction
(and (at ?r ?loc) (at ?obj ?loc))
```

**ADL preconditions** (more expressive):
```pddl
;; Negation
(not (holding ?r ?obj))

;; Disjunction
(or (at ?r loc1) (at ?r loc2))

;; Equality
(not (= ?from ?to))

;; Universal quantifier
(forall (?x - object) (or (at ?x ?loc) (holding ?r ?x)))

;; Existential quantifier
(exists (?x - location) (and (at ?r ?x) (charging-station ?x)))
```

### Effects: STRIPS vs. ADL

**STRIPS effects** (add/delete):
```pddl
;; Add a fact
(at ?r ?to)

;; Delete a fact (negation in effect = delete)
(not (at ?r ?from))

;; Combined
(and (not (at ?r ?from)) (at ?r ?to))
```

**ADL effects** (conditional and quantified):
```pddl
;; Conditional effect
(when (and (at ?obj ?from) (= ?obj box1))
  (not (at ?obj ?from)))

;; Quantified effect
(forall (?x - object)
  (when (and (at ?x ?from) (fragile ?x))
    (broken ?x)))
```

### Complete Action Example

```pddl
(:action move
  :parameters (?r - robot ?from - location ?to - location)
  :precondition (and
    (at ?r ?from)
    (connected ?from ?to)
    (not (= ?from ?to)))
  :effect (and
    (not (at ?r ?from))
    (at ?r ?to)))
```

This action:
1. Requires the robot to be at `?from`
2. Requires `?from` and `?to` to be connected
3. Requires `?from` and `?to` to be different locations
4. Moves the robot from `?from` to `?to`

---

## 6. Worked Example: Logistics Domain

### Domain File

```pddl
(define (domain logistics)
  (:requirements :strips :typing :negative-preconditions)

  (:types
    robot
    location
    object)

  (:predicates
    (at ?obj - (either robot object) ?loc - location)
    (holding ?r - robot ?obj - object))

  (:action move
    :parameters (?r - robot ?from - location ?to - location)
    :precondition (and
      (at ?r ?from)
      (not (= ?from ?to)))
    :effect (and
      (not (at ?r ?from))
      (at ?r ?to)))

  (:action pick-up
    :parameters (?r - robot ?obj - object ?loc - location)
    :precondition (and
      (at ?r ?loc)
      (at ?obj ?loc))
    :effect (and
      (not (at ?obj ?loc))
      (holding ?r ?obj)))

  (:action put-down
    :parameters (?r - robot ?obj - object ?loc - location)
    :precondition (holding ?r ?obj)
    :effect (and
      (not (holding ?r ?obj))
      (at ?obj ?loc))))
```

### Problem File

```pddl
(define (problem logistics-01)
  (:domain logistics)
  (:objects
    robot1   - robot
    loc1 loc2 loc3 - location
    box1     - object)
  (:init
    (at robot1 loc1)
    (at box1 loc1))
  (:goal
    (at box1 loc2)))
```

### Step-by-Step Solution

**Initial State:**
```
(at robot1 loc1)
(at box1 loc1)
```

**Step 1: `(pick-up robot1 box1 loc1)`**
- Preconditions: `(at robot1 loc1)` ✓, `(at box1 loc1)` ✓
- Effects: delete `(at box1 loc1)`, add `(holding robot1 box1)`

**State after Step 1:**
```
(at robot1 loc1)
(holding robot1 box1)
```

**Step 2: `(move robot1 loc1 loc2)`**
- Preconditions: `(at robot1 loc1)` ✓, `(not (= loc1 loc2))` ✓
- Effects: delete `(at robot1 loc1)`, add `(at robot1 loc2)`

**State after Step 2:**
```
(at robot1 loc2)
(holding robot1 box1)
```

**Step 3: `(put-down robot1 box1 loc2)`**
- Preconditions: `(holding robot1 box1)` ✓
- Effects: delete `(holding robot1 box1)`, add `(at box1 loc2)`

**State after Step 3:**
```
(at robot1 loc2)
(at box1 loc2)
```

**Goal check:** `(at box1 loc2)` ✓ — **Goal satisfied!**

**Final Plan:**
```
1. (pick-up robot1 box1 loc1)
2. (move robot1 loc1 loc2)
3. (put-down robot1 box1 loc2)
```

---

## 7. Planning Algorithms & Sussman Anomaly

### Forward Search (Progression)

Start from the initial state, apply actions, and search toward the goal.

```
Initial State → apply actions → Successor States → ... → Goal State
```

**Algorithm:**
1. Start with the initial state as the root of the search tree
2. For each state, find all applicable actions (preconditions satisfied)
3. Apply each action to generate successor states
4. Check if any successor satisfies the goal
5. Repeat until goal found or search space exhausted

**Properties:**
- ✓ **Correct**: any returned plan is valid
- ✓ **Complete**: will find a plan if one exists
- ✗ **Expensive**: branching factor can be huge; not feasible for long plans

### Backward Search (Regression)

Start from the goal, work backward to find what conditions are needed.

```
Goal ← what action achieves this? ← what preconditions? ← ... ← Initial State
```

**Properties:**
- ✓ **Correct** and **Complete**
- ✗ Still exponential in worst case
- Often has lower branching factor than forward search (fewer actions achieve a given goal than are applicable in a given state)

### Search Strategies

| Strategy | Approach | Complete? | Optimal? |
|---|---|---|---|
| **BFS** | Explore level by level | Yes | Yes (by steps) |
| **DFS** | Go deep, then backtrack | Yes (finite space) | No |
| **IDS** | DFS with increasing depth limit | Yes | Yes (by steps) |
| **A*** | Heuristic-guided best-first | Yes | Yes (if h is admissible) |

### Heuristics

A heuristic function **h(s)** estimates the cost from state **s** to the goal. Good heuristics are:
- **Admissible**: never overestimate (guarantees optimality with A*)
- **Consistent**: h(s) ≤ cost(s, s') + h(s') for all successors s'

Common planning heuristics:
- **hmax**: Maximum heuristic value of subgoals
- **hadd**: Sum of heuristic values of subgoals
- **Pattern databases**: Precomputed exact costs for subsets of facts
- **Relaxation heuristics**: Solve a simplified version of the problem (e.g., ignore delete lists → STRIPS relaxation)

### The Sussman Anomaly

The **Sussman Anomaly** (Gerald Jay Sussman, 1973) demonstrates a fundamental challenge in planning:

**Problem:** Three blocks A, B, C on a table. Goal: A on B, B on C.

```
Initial:        Goal:
  A               A
  B               B
  C               C
table         table
```

**The anomaly:** The two subgoals (A on B, B on C) **interfere** with each other:
- If you solve "B on C" first, then placing "A on B" is fine
- If you solve "A on B" first, you must clear B to place it on C, which undoes "A on B"

**Why it matters:**
- Pure forward search may find a solution, but could waste effort exploring wrong orderings
- Pure backward search may solve subgoals independently, then fail to merge them
- **Partial-order planners** solve this by recognizing that some actions are independent and can be interleaved

**Resolution:** The key insight is that planning systems need to reason about **action ordering constraints** — some actions must precede others, while others can happen in any order. This led to the development of **partial-order planning** (NONAX, UCW) and **planning graph** methods (Graphplan, SATPLAN).

---

## 8. Plan Validity & Type Correctness

### What Makes a Plan Valid?

A plan is valid if and only if:

1. **Preconditions satisfied**: Each action's preconditions hold in the state at the point of execution
2. **Type correctness**: Objects used in grounded actions match the types declared for the action's parameters
3. **Goal achievement**: Executing the plan from the initial state reaches a state satisfying the goal
4. **No conflicts**: Actions don't produce contradictory states
5. **Resource constraints respected**: Time, energy, and other constraints are satisfied

### Type Correctness

When a domain uses typing, every grounded action must respect type constraints:

```pddl
(:action pick-up
  :parameters (?r - robot ?obj - object ?loc - location)
  ...)
```

Valid grounding: `(pick-up robot1 box1 loc1)` ✓
Invalid grounding: `(pick-up box1 robot1 loc1)` ✗ (wrong types)

Type hierarchy matters: if `drone` is a subtype of `robot`, then `(pick-up drone1 box1 loc1)` is valid.

### Closed-World Assumption

PDDL uses the **closed-world assumption**: any fact not listed in the initial state or added by an action effect is **false**. This is why delete effects are expressed as `(not <predicate>)` — they explicitly negate facts that were previously true.

### Non-Sequential Plans

Not all plans are strictly ordered sequences. **Partial-order plans** specify:
- A set of actions
- Ordering constraints between some pairs of actions
- Causal links between actions

This flexibility is important for:
- **Scheduling**: independent actions can run in parallel
- **Replanning**: fewer ordering constraints means easier adaptation
- **Multi-agent execution**: different agents can execute independent actions simultaneously

---

## 9. Temporal & Advanced PDDL

### Durative Actions

Durative actions take time to execute. Conditions and effects can be specified at different time points:

```pddl
(:durative-action move
  :parameters (?r - robot ?from - location ?to - location
                ?duration - number)
  :duration (= ?duration 5)
  :condition (and
    (at start (at ?r ?from))
    (over all (not (= ?from ?to))))
  :effect (and
    (at start (not (at ?r ?from)))
    (at end (at ?r ?to))))
```

**Time points:**
- `at start`: condition/effect at the beginning of the action
- `at end`: condition/effect at the end of the action
- `over all`: condition must hold throughout the entire duration

### Duration Inequalities

```pddl
:duration (and
  (>= ?duration 3)
  (<= ?duration 7))
```

This allows flexible timing — the action takes between 3 and 7 time units.

### Numeric Fluents

Functions whose values change over time:

```pddl
(:functions
  (battery ?r - robot)
  (speed ?r - robot))

(:durative-action drive
  :parameters (?r - robot ?from - location ?to - location)
  :duration (= ?duration (/ (distance ?from ?to) (speed ?r)))
  :condition (and
    (at start (at ?r ?from))
    (at start (> (battery ?r) 0)))
  :effect (and
    (at start (not (at ?r ?from)))
    (at end (at ?r ?to))
    (at end (decrease (battery ?r) (* ?duration 0.5)))))
```

### Plan Metrics

Metrics define what makes a plan "good":

```pddl
;; Minimize total execution time
(:metric minimize (total-time))

;; Minimize sum of step costs
(:metric minimize (step-count))

;; Minimize a specific fluent
(:metric minimize (total-cost))

;; Satisfice: any valid plan is acceptable
(:metric satisfice 1)
```

### Axioms (Derived Predicates)

Axioms define predicates that are **derived** from other facts (not directly modified by actions):

```pddl
(:axioms
  ;; A location is "reachable" if connected to the robot's current location
  (?x - location)
  (reachable ?x)
  (connected ?x ?current-location))
```

### Timed Initial Literals

Facts that become true at specific times, independent of actions:

```pddl
(:init
  (at robot1 loc1)
  (at 5.0 (emergency-stop))    ;; becomes true at time 5
  (at >= 10.0 (deadline-reached)))  ;; becomes true at time 10+
```

---

## 10. Planners & Tools

### Planner Categories

| Category | Characteristics | Examples |
|---|---|---|
| **Classical** | Fully observable, deterministic, instantaneous actions | FF, Fast Downward, Metric-FF |
| **Temporal** | Durative actions, numeric fluents, scheduling | POPF, TIMELINE, UniGOV |
| **Probabilistic** | Non-deterministic effects, observations | SymNeuron, PROST, PopFud |
| **SAT-based** | Encode planning as Boolean satisfiability | SATPLAN, MergeSAT |
| **Constraint-based** | Encode as constraint satisfaction | SMTPlan, OptiPlan |

### Satisficing vs. Optimizing

| Approach | Goal | Trade-off |
|---|---|---|
| **Satisficing** | Find *any* valid plan quickly | Fast, but plan quality varies |
| **Optimizing** | Find the *best* plan (by metric) | Slower, guarantees optimality |

Most practical robotics applications use **satisficing** planners — a good plan found quickly is better than an optimal plan that takes too long to compute.

### Notable Planners

| Planner | Type | Key Features |
|---|---|---|
| **FF** | Classical | Greedy heuristic, fast, STRIPS-only |
| **Fast Downward** | Classical | Pattern database heuristics, IPC winner |
| **POPF** | Temporal | Partial-order, temporal + metric planning |
| **VHPOP** | Classical/ADL | VH-fast heuristic, supports ADL |
| **SMTPlan** | Constraint-based | SMT solver backend, supports ADL + temporal |
| **Fast Downward (temporal)** | Temporal | Temporal adaptation of Fast Downward |

### Plan Validation Tools

| Tool | Purpose |
|---|---|
| **VAL** | PDDL syntax checker + plan validator |
| **INVAL** | Alternative plan validator |
| **Fast Downward (check mode)** | Validate plans against domain/problem |

**Why validate?** Planners are research prototypes — they can produce invalid plans due to bugs. Always validate plans before execution, especially in safety-critical robotics applications.

### Running a Planner

```bash
# Classical planner (FF)
ff -o domain.pddl -f problem.pddl

# Temporal planner (POPF)
popf domain.pddl problem.pddl

# SMT-based planner
SMTPlan domain.pddl problem.pddl

# Validate a plan with VAL
validate domain.pddl problem.pddl plan.siplan
```

---

## 11. PDDL in Robotics

### The Integration Challenge

PDDL produces abstract plans (sequences of action names and parameters). Robots need concrete execution (motor commands, sensor processing). The bridge between these worlds requires:

1. **State tracking**: Keeping the PDDL state synchronized with the real world
2. **Action execution**: Translating PDDL actions into robot behaviors
3. **Monitoring**: Detecting when execution deviates from the plan
4. **Replanning**: Generating new plans when things go wrong

### RosPlan (ROS 1)

RosPlan was the first major PDDL-ROS integration framework:

| Component | Role |
|---|---|
| **Knowledge Base** | Stores the PDDL domain model |
| **Problem Interface** | Generates PDDL problem files from current state |
| **Planner Interface** | Calls external planners, publishes plans |
| **Parsing Interface** | Converts PDDL plans to ROS messages |
| **Plan Dispatch** | Executes plans step by step |

### PlanSys2 (ROS 2)

PlanSys2 is the ROS 2 successor, with a more modular architecture:

| Component | Role |
|---|---|
| **Domain Expert** | PDDL model (types, predicates, functions, actions) |
| **Problem Expert** | Current instances, predicates, functions, goals |
| **Planner** | Generates plans from Domain + Problem Experts |
| **Executor** | Executes plans by activating **Action Performers** (ROS 2 nodes) |

**Action Performers** are ROS 2 nodes that implement individual PDDL actions. Each performer:
- Advertises which PDDL action it can execute
- Receives action parameters via ROS 2 interfaces
- Executes the behavior and reports success/failure

### MERLIN2: Hybrid Cognitive Architecture

MERLIN2 goes beyond pure planning by combining:

| Layer | Technology | Role |
|---|---|---|
| **Deliberative** | PDDL Planner | Long-term task planning |
| **Reactive** | YASMIN (FSM) | Real-time behavior, monitoring, recovery |
| **Knowledge** | ROS 2 Nav2, semantic maps | World representation |

MERLIN2 provides:
- Symbolic knowledge management
- Behavior scheduling and monitoring
- Hybrid architecture (planner + finite state machine)
- Full ROS 2 compatibility

> **References:**
> - [MERLIN2 Paper](https://www.softwareimpacts.com/article/S2665-9638(23)00014-3/fulltext)
> - [MERLIN2 Documentation](https://merlin2.readthedocs.io/en/latest/)
> - [PlanSys2 Tutorials](https://github.com/PlanSys2/ros2_planning_system_examples)

---

## 12. Exercises

See the `Examples/` directory for hands-on exercises. Each exercise includes a README with detailed instructions.

| Exercise | Topic | Difficulty | Key Concepts |
|---|---|---|---|
| [Exercise 1](Examples/Exercise1/) | Basic Planning | ★☆☆ | STRIPS, ADL, types, predicates, planner compatibility |
| [Exercise 2](Examples/Exercise2/) | Navigation & Fluents | ★☆☆ | Numeric fluents, durative actions, charging |
| [Exercise 3](Examples/Exercise3/) | Metrics in Planning | ★★☆ | IPC Rover benchmark, plan metrics, planner comparison |
| [Exercise 4](Examples/Exercise4/) | Comparing Planners | ★★☆ | Sussman anomaly, POPF vs VHPOP, timing analysis |
| [Exercise 5](Examples/Exercise5/) | Cybersecurity | ★★☆ | IPC 2012 domain, complexity, domain-specific planning |
| [Exercise 6](Examples/Exercise6/) | Durative Actions | ★★☆ | PDDL2.1 temporal planning, step-by-step walkthrough |
| [Exercise 7](Examples/Exercise7/) | ROS 2 Integration | ★★★ | SMTPlan + ROS 2, tiago_simulator, action performers |
| [Exercise 8](Examples/Exercise8/) | PlanSys2 & BTs | ★★★ | PlanSys2 framework, behavior trees, Doxygen documentation |

### Running Exercises

```bash
# Navigate to an exercise directory
cd Examples/Exercise1/

# Run with POPF
../../Planners/popf domain.pddl problem.pddl

# Run with SMTPlan
../../Planners/SMTPlan domain.pddl problem.pddl

# Validate a plan
validate domain.pddl problem.pddl plan.siplan
```

---

## 13. References & Resources

### Online Resources

- **[planning.wiki](https://planning.wiki/)** — Comprehensive PDDL reference, planner comparisons, tutorials
- **[planning.domains](http://planning.domains)** — Online PDDL editor with syntax highlighting and benchmark repository
- **[ICAPS Competitions](https://icaps-conference.org/index.php/Main/Competitions)** — IPC archives, planner source code, competition domains

### Tools

- **[VAL](https://github.com/KCL-Planning/VAL)** — PDDL syntax checker and plan validator
- **[INVAL](https://github.com/patrikhaslum/INVAL)** — Alternative plan validator
- **[PDDL4J](https://github.com/plan4j/pddl4j)** — Java PDDL library

### Key Papers

- Ghallab, Nau, Traverso. *Automated Planning: Theory and Practice.* Morgan Kaufmann, 2004.
- Pellier & Fiorino (2017). *PDDL4J: a planning domain description library for Java.* JETTA 30, 1-34.
- Hoffmann (2003). *The FF planner: The first systematic approach to fast heuristic planning.*
- Ingrand & Ghallab (2017). *Deliberation for autonomous robots: A survey.* AI 247, 10-44.
- Kotseruba & Tsotsos (2020). *40 years of cognitive architectures.* Artif Intell Rev 53, 17-94.

### Projects

- **[DMARCE](https://github.com/DMARCE-PROJECT)** — Decision Making in Autonomous Robots: Cybersecurity and Explainability
- **[SELF-AIR](https://github.com/shepherd-robot)** — Supporting Extensive Livestock Farming with Autonomous Intelligent Robots
- **[PlanSys2](https://plansys2.github.io/)** — ROS 2 Planning System
- **[MERLIN2](https://merlin2.readthedocs.io/)** — Hybrid Cognitive Architecture for ROS 2

---

*Summer School for Software Engineering in Robotics*
