# Universal Grading Socket Architecture v1

Status: **APPROVED IMPLEMENTATION CONTRACT — SOCKET FOUNDATION + ITEM COVERAGE V1**  
Date: 2026-08-20

## Purpose

Extend the existing Universal Cross-Domain Grading Contract without enumerating every possible Item, Location, Quest, Technology or future universe element.

Core invariant:

`authoritative raw state + registered grading sockets + universe policy -> derived GradePlan -> deterministic GradeProfile`

The system defines **how evidence becomes a grade**, not a hard-coded catalog of every entity that can exist.

Grades remain derived interpretation. Raw represented facts remain authority.

---

## Non-goals

V1 does **not**:
- let AI author authoritative grade letters;
- let AI invent arbitrary thresholds or evaluator code;
- require every possible Item family to be pre-registered;
- persist grade letters as a second source of truth;
- make Item grade a Character interaction requirement;
- make Location grade an access authorization;
- require a DB schema migration;
- activate supernatural capabilities in the Real World.

Unknown/uncovered dimensions remain ungraded rather than receiving fabricated precision.

---

## Shared vocabulary

Reuse the existing canonical vocabulary and comparison semantics:

`E < D < C < B < A < S < SS < SSS < X < XX`

A scheme/evaluator may expose only the subset justified by its domain and universe policy.

The same grade letter across domains does not imply the same raw quantity, risk, capability, access or requirement.

---

# Socket model

## 1. Evaluator Registry

Stable evaluator ids map deterministic input evidence to a `GradeResult`.

An evaluator registration declares at minimum:
- stable evaluator id;
- evaluator family;
- domain compatibility;
- supported grades;
- deterministic evaluation callable/adapter.

V1 evaluator families may include registered forms such as:
- monotonic;
- ordinal;
- target-range;
- ratio;
- reference-relative;
- composite.

The registry is expandable. Adding a new evaluator must not require changes to the grade-plan resolver core.

V1 reuses existing `item-resistance-load-v1` through this socket rather than duplicating its thresholds.

## 2. Dimension Registry

A `DimensionSpec` declares one meaningfully gradeable dimension.

Required metadata:
- stable dimension id;
- domain;
- human label;
- evaluator id;
- authoritative source paths;
- applicability predicate/requirements;
- optional reference-profile id;
- optional criticality/composite metadata;
- supported universe-policy constraints.

Examples:
- `item / resistance_load`;
- future `item / durability`;
- future `item / storage_capacity`;
- `location / completeness`;
- future `technology / capability`;
- future universe-specific `item / magical_potency`.

Dimensions are registered independently of individual entity families. There must be no central `if backpack / elif flashlight / elif sword` catalog.

## 3. Reference Profile Registry

Some evaluators need category- or universe-relative reference data instead of universal absolute thresholds.

A reference profile may define:
- stable reference id;
- domain/dimension;
- universe or universe-family scope;
- optional semantic category scope;
- deterministic bands/targets/distribution metadata;
- source/provenance/version metadata.

No reference profile means no reference-relative grade. The system must fail closed to `ungraded` rather than ask AI to invent a baseline.

## 4. Universe Grading Policy

A universe policy controls which grading semantics are legitimate in that universe.

It may restrict:
- allowed dimensions;
- allowed evaluators;
- allowed reference profiles;
- supported grade ceiling/subset;
- future compatibility/capability constraints.

The default realistic Sandbox/Real-World-compatible policy must not silently admit supernatural grading dimensions.

Future universes may register their own policy/reference extensions without changing base Item schema code.

## 5. Grade Plan

A `GradePlan` is a deterministic/read-time description of which registered dimensions apply to one represented entity.

Each plan row records stable metadata such as:
- dimension id;
- evaluator id;
- source paths;
- reference profile if any.

The plan is rebuildable from authoritative facts + registries + universe policy. It is **not persistence authority**.

AI may later propose a structured plan mapping during creation, but every proposed dimension/evaluator/reference must resolve through registered sockets before use. V1 does not require AI-authored plan entries; deterministic applicability is sufficient to prove the architecture.

## 6. Grade Profile

The resolver evaluates every valid plan dimension and returns the existing `GradeProfile`/`GradeResult` semantics.

Rules:
- zero applicable dimensions is valid and means `ungraded / no registered grading dimension applies`;
- dimension results are deterministic;
- overall grade is optional;
- overall exists only through an explicit registered composite evaluator/scheme;
- missing critical evidence may block a composite instead of being silently averaged away;
- display units never change grade.

---

# Item Grading Coverage v1

## Goal

Prove the socket architecture against the current Item system while preserving the established Item schema and creation/materialization/edit flows.

V1 Item behavior:
1. normalized Item facts remain authority;
2. Item validation/build stage asks the grading socket resolver for applicable registered Item dimensions;
3. current `resistance_training.resistance_load` resolves through registered `item / resistance_load` dimension;
4. its evaluator reuses existing deterministic `item-resistance-load-v1` grading;
5. unrelated ordinary Items receive no fabricated grade when no dimension currently applies;
6. derived grade output remains compatible with the existing `derived.grades` representation;
7. Telegram review/detail may expose a human-readable Grading section without internal scheme ids;
8. technical exports may retain canonical derived metadata where already present.

This v1 intentionally proves **extensibility**, not exhaustive world coverage. Later dimensions such as durability, capacity, efficiency, technological capability or supernatural properties are added by registering sockets/reference profiles, not by rewriting Item creation logic.

---

# Creation-time relationship

The universal creation pipeline remains:

`Creator intent -> strict type schema -> AI/raw fact fill -> deterministic normalization/validation -> grading plan resolution -> deterministic derived grades -> preview -> explicit approval -> Sandbox-only materialization`

AI owns neither grade thresholds nor final grade letters.

If a future AI planner proposes applicability, the deterministic boundary remains:

`AI proposal -> registry resolution -> universe-policy validation -> evidence validation -> deterministic evaluator`.

---

# Item grade vs interaction requirement

Preserve the existing rule:

> **Item Grade describes the item. Requirement Grade describes the interaction.**

A 55 lb dumbbell may derive an S resistance-load Item grade. The Character requirement for a curl, carry, squat or other action is a separate requirement/action calculation.

No automatic `Item grade -> Character minimum grade` mapping is permitted.

---

# Extension contract

A new gradeable concept should normally be addable through one or more registrations:

`EvaluatorSpec + DimensionSpec + optional ReferenceProfile + optional UniversePolicy allowance`

without editing:
- Item family switch statements;
- creation/materialization core;
- Telegram navigation core;
- grade vocabulary core.

A new domain may reuse the same sockets by supplying its authoritative source adapter and registered dimensions.

---

# Acceptance for first implementation slice

The first implementation must prove:
- existing resistance-load Item grades remain unchanged;
- grading plan discovery is registry-driven rather than hard-coded in Item schema;
- a synthetic new registered Item dimension/evaluator can be added in tests without editing resolver core;
- an ordinary Item with no registered dimension remains ungraded and receives no fabricated grade;
- unknown evaluator/dimension/reference ids fail closed;
- universe policy can reject a dimension not allowed by policy;
- display-unit conversion does not change a grade;
- `derived.grades` remains compatible with current Item persistence/edit behavior;
- no DB migration and no canonical Real World mutation.

After this socket + Item coverage slice is accepted, additional Item grading dimensions can be added incrementally from evidence-backed evaluator/reference definitions. Location and other universal domains can reuse the same architecture later.
