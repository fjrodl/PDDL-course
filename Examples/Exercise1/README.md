# Basic Planning Exercise with Robots and Objects

This basic exercise shows how robots can be coordinated to move objects between locations using classical planning techniques. The domain uses actions with preconditions and effects to achieve a specified goal state.

## 🧠 Key Concepts

This scenario helps compare how different planners handle features such as action expressivity, ADL constructs, and execution constraints. It is particularly useful to analyze limitations or capabilities of each planner with respect to `:adl` features.

---

## 🗂️ Domain Overview

### ✅ Requirements Used

- `:strips` – Standard requirement for basic planning.
- `:typing` – Allows the use of types for parameters.
- `:negative-preconditions` – Enables `not` in preconditions.
- `:disjunctive-preconditions` – Enables `or` in preconditions.
- `:equality` – Enables use of `=` and `/=` in conditions.

> **Note**: Some planners only support `:strips`. Others like VHPOP or SMTPlan support `:adl`, but with limitations.

### 🧩 Types

- `robot`
- `location`
- `object`

### 🔧 Predicates

- `(at-robot ?r - robot ?loc - location)`  
- `(at-object ?o - object ?loc - location)`  
- `(holding ?r - robot ?o - object)`

### ⚙️ Actions

- `move`: Moves a robot between two different locations.
- `pick_up`: Allows a robot to pick up an object from a location.
- `put_down`: Allows a robot to put down an object at a location.
- `visit`: Demonstrates a disjunctive precondition; **comment this action for compatibility** with STRIPS-only planners.

---

## 📌 Problem Instance

### Objects

- Robots: `robot1`, `robot2`
- Locations: `loc1`, `loc2`, `loc3`
- Objects: `box1`, `box2`

### Initial State

- `robot1` at `loc1`
- `robot2` at `loc2`
- `box1` at `loc1`
- `box2` at `loc3`

### Goal State

- `robot1` at `loc2`
- `box1` at `loc2`
- `box2` at `loc1`

---

## 🚀 Execution Examples

### With FF (supports STRIPS only):

```bash
../../Planners/ff -o domain.pddl -f problem.pddl
```

### With SMTPlan (supports ADL):

```bash
../../Planners/SMTPlan domain.pddl problem.pddl
```


---

### ⚠️ VHPOP Compatibility Note

The original domain definition used the predicate:

```lisp
(at ?obj - (either robot object) ?loc - location)
```

This syntax, while valid in PDDL, is **not supported by VHPOP**, which does not handle `either` type declarations in predicates.

To ensure compatibility, we replaced it with two separate predicates:

```lisp
(at-robot ?r - robot ?loc - location)
(at-object ?o - object ?loc - location)
```



---

## 🧪 Suggested Experiments

Use different versions of the domain with:
- Only `:strips` → test with FF, Fast Downward
- Full `:adl` with disjunctions and conditionals → test with VHPOP, SMTPlan
- Try triggering unsupported features (e.g., `or`, `when`) in STRIPS-only planners

Compare:
- Planning time
- Number of steps
- Plan quality
- Error messages

---

## 📁 Files

- `Exercise1_G` – ADL-style domain with typed predicates and complex actions
- `Exercise1_N` – This version is not compatible with vhpop
