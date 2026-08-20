# Universal Grading Socket Architecture v1

Status: **REPOSITORY-ACCEPTED — SOCKET FOUNDATION + ITEM COVERAGE V1**  
Date: 2026-08-20

## Purpose

Scale grading across arbitrarily many Items and future universal elements without predefining every entity family.

Core invariant:

`authoritative raw state + registered grading sockets + universe policy -> derived GradePlan -> deterministic GradeProfile`

The system defines **how evidence becomes a grade**, not a hard-coded catalog of everything that may exist. Raw represented facts remain authority; grades remain derived interpretation.

Repository acceptance:
- PR **#360** merged at `9155a94bc75b800d4a10f2a39993647c78d11d9c`;
- CI **#1195** passed targeted regression + CLI smoke;
- no DB migration;
- no persisted GradePlan/grade authority;
- no canonical Real World mutation.

Live Telegram deployment of #360 remains a separate evidence gate.

---

## Shared vocabulary

Reuse the canonical ordering:

`E < D < C < B < A < S < SS < SSS < X < XX`

A registered evaluator may expose only a justified subset. The same grade letter across domains does not imply the same raw scale, risk, access or capability.

---

# Socket model

## Evaluator Registry

`EvaluatorSpec` registers:
- stable evaluator id;
- evaluator family;
- domain;
- supported grades;
- deterministic evaluator implementation.

The resolver does not contain Item-family switches. A synthetic new evaluator is acceptance-tested without editing resolver core.

V1 reuses the existing deterministic `item-resistance-load-v1` evaluator rather than cloning its thresholds.

## Dimension Registry

`DimensionSpec` registers:
- stable dimension id;
- domain;
- human label;
- evaluator id;
- authoritative source paths;
- optional applicability predicate;
- optional reference profile;
- optional criticality metadata.

Current real Item dimension:
- `item / resistance_load`.

Future examples may include durability, storage capacity, efficiency, technological capability or universe-specific properties, but only after their evidence/evaluator/reference contracts are justified.

## Reference Profile Registry

`ReferenceProfile` is the socket for category- or universe-relative baselines.

A reference profile carries a stable id, domain/dimension binding and deterministic reference data. A dimension requiring a missing reference fails closed. AI must not fabricate a baseline merely to force a grade.

## Universe Grading Policy

`UniverseGradingPolicy` controls which grading semantics are legitimate in one universe context:
- allowed domains;
- allowed dimensions;
- allowed evaluators;
- allowed reference profiles;
- grade ceiling.

The default realistic policy explicitly allowlists the current `resistance_load` Item dimension/evaluator and caps it at S. Registering a synthetic `magical_potency` dimension does **not** silently make it valid in the realistic universe.

Future universes can register different policies/reference sets without changing Item-family code.

## Grade Plan

A `GradePlan` is a rebuildable description of which registered dimensions apply to represented facts under a universe policy.

It is not persistence authority. Unknown/uncovered dimensions are simply absent.

Future AI may propose applicability mappings, but any proposal must resolve through registered evaluator/dimension/reference sockets and universe policy before deterministic evaluation.

## Grade Profile

The resolver returns dimension `GradeResult`s grouped as a `GradeProfile`.

Rules:
- zero applicable dimensions is valid: `ungraded`;
- final dimension grades are deterministic;
- overall grade is optional and requires an explicit composite evaluator/scheme;
- missing critical evidence must not be silently averaged away;
- display units cannot change grade.

---

# Item Grading Coverage v1 — accepted behavior

Current Item integration is deliberately read-time/derived-first so existing creation/materialization/edit persistence remains stable.

Accepted behavior:
1. Item raw facts remain authority.
2. `item_grading.py` adapts full Creator draft payloads and already-normalized approved Item snapshots to the grading socket resolver.
3. Full Creator drafts are normalized through the existing strict Item validator before grading.
4. Approved Items use their persisted normalized facts directly.
5. `resistance_training.resistance_load` resolves through registered `resistance_load` -> `item-resistance-load-v1`.
6. Existing resistance-load grades remain unchanged; e.g. 55 lb -> S.
7. Ordinary Items with no registered applicable dimension show an explicit ungraded state rather than a fabricated grade.
8. Creator draft review and approved Sandbox Item detail expose human-facing grading, e.g. `Resistance Load: S · Expert`, without internal scheme ids.
9. Raw `.txt` draft export does not gain GradePlan authority fields and remains the technical authoring payload.
10. Existing persisted `derived.grades` compatibility remains untouched; the new socket is the extensible read-time path for future dimensions.

This v1 proves extensibility, not exhaustive Item coverage.

---

# Safety / semantic locks

- AI may propose raw facts or future applicability mappings; it does not author authoritative final grade letters when a deterministic evaluator exists.
- AI does not invent evaluator code or thresholds at runtime.
- Missing reference/evidence means ungraded, not hallucinated precision.
- Arbitrary numeric fields are not automatically gradeable.
- **Item Grade describes the item. Requirement Grade describes the interaction.**
- Item grade never automatically becomes a Character minimum requirement.
- Location grade never automatically becomes access authorization.
- No new universe-specific dimension is admitted without policy allowance.

---

# Extension contract

A new gradeable concept should normally be addable through:

`EvaluatorSpec + DimensionSpec + optional ReferenceProfile + UniverseGradingPolicy allowance`

without changing:
- Item-family switch statements;
- Item creation/materialization core;
- Telegram navigation core;
- universal grade vocabulary core;
- grading resolver core.

PR #360 acceptance proves this with a synthetic Item durability evaluator/dimension registered only in tests.

---

# Next grading expansion

Before claiming broad Item grading coverage, add evidence-backed reusable dimensions/reference profiles incrementally and, where useful, a structured AI applicability-plan proposal that remains registry/policy/evidence constrained.

Good candidate families include:
- measurable intrinsic capabilities with stable units;
- reference-relative capacity/efficiency where a defensible category reference exists;
- durability/condition only after a concrete raw durability representation exists;
- technology or supernatural dimensions only in universes whose policy explicitly allows them.

Do not block unrelated Item creation merely because no grading dimension applies yet.
