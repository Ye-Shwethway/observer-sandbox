# Universal Cross-Domain Grading Contract v1

Status: **IMPLEMENTATION CANDIDATE — I5.4**  
Date: 2026-08-20

## Purpose

Generalize the proven profile-grading architecture so multiple domains can share one grade vocabulary without pretending they share one raw scale or one evaluator.

Core invariant:

`authoritative raw state + explicit named domain scheme -> derived grade metadata`

Grades remain interpretation, not a second source of truth.

---

## Shared vocabulary and ordering

Canonical vocabulary:

`E < D < C < B < A < S < SS < SSS < X < XX`

Labels remain:
- E — Beginner;
- D — Novice;
- C — Capable;
- B — Skilled;
- A — Advanced;
- S — Expert;
- SS — Elite;
- SSS — Master;
- X — Mythic;
- XX — Transcendent.

The vocabulary is universal. A scheme may expose only a legitimate subset.

Current Character RAPS/Skill schemes continue to expose E..S. Nothing in I5.4 compresses SS..XX into a 0..100 Character scale.

`grade_rank`, `compare_grades`, and `meets_minimum_grade` provide deterministic vocabulary comparison for later requirement/compatibility systems.

---

## Scheme metadata

`GradeScheme` now optionally declares:
- domain;
- dimension;
- supported grade subset.

Existing schemes are annotated rather than replaced.

Examples:
- Character RAPS -> `character / attribute_capability`;
- Character skill -> `character / skill_proficiency`;
- Body aesthetic proportion -> `body / aesthetic_proportion`;
- Item resistance load -> `item / resistance_load`;
- Location completeness -> `location / completeness`.

Same grade letter across two schemes does **not** imply equivalent raw quantities, risk, access or actor capability.

---

## Grade results and profiles

`GradeResult` retains its original fields:
- scheme id;
- grade;
- label;
- source/evaluated numeric value.

It now may also expose domain and dimension metadata.

`GradeProfile` is an optional read-time grouping:

`domain + dimension results + optional explicit composite overall result`.

Rules:
- at least one dimension is required;
- each dimension's registered scheme must belong to the profile domain when the scheme declares a domain;
- overall grade is optional;
- overall may only come from a registered `composite` scheme;
- grade profiles are not persistence authority.

---

## Existing Character compatibility

I5.4 preserves existing Character/Profile grading thresholds and scheme ids.

RAPS 0..100 remains:
- S >= 90;
- A >= 75;
- B >= 60;
- C >= 40;
- D >= 20;
- E >= 0.

Skill grading remains a distinct named scheme with the same current bands.

Body grading remains target-range/composite logic under its existing schemes.

The profile observer continues emitting its existing four-field grade payload; new domain/dimension metadata does not force Telegram/UI changes.

---

## Item exemplar — resistance load

Scheme:
`item-resistance-load-v1`

Domain/dimension:
`item / resistance_load`

Input authority:
`PhysicalQuantity(kind='mass')` from I5.3.

The evaluator consumes normalized kg truth, so pounds-versus-kilograms display cannot affect grade.

V1 project-defined load classification:
- E: < 5 lb;
- D: >= 5 lb;
- C: >= 10 lb;
- B: >= 20 lb;
- A: >= 35 lb;
- S: >= 50 lb.

These bands describe represented resistance load only. They are not a claim about product quality, exercise difficulty or the Character strength required to interact with the Item.

Therefore a 55 lb fixed dumbbell derives an S **Item resistance-load grade**, while a curl, goblet squat, carry or rack operation may each have a different actor requirement under I5.5+.

---

## Location exemplar — completeness

Scheme:
`location-completeness-v1`

Domain/dimension:
`location / completeness`

This reuses the existing spatial-container L0..L4 contract rather than inventing a new quality score:
- L0 Identity placeholder -> E;
- L1 Structural container -> D;
- L2 Traversable place -> C;
- L3 Usable place -> B;
- L4 Living place -> A.

S is intentionally not exposed by this scheme. Completeness is not prestige, danger, luxury or access authority.

A high completeness grade does not grant or deny entrance. Location access remains a separate I5.5 contract.

---

## Cross-domain rules

1. Grade vocabulary is shared; evaluators are domain-specific.
2. Raw authoritative state remains independently represented.
3. AI may provide raw facts but may not make derived grade letters authoritative when a deterministic scheme exists.
4. Numeric values are not gradeable unless a named scheme opts them in.
5. Item grade is not automatically a Character requirement.
6. Location grade is not authorization.
7. Display units cannot change grade.
8. Composite overall grade requires an explicit composite scheme.
9. Future universe/domain ceilings may consume deterministic grade ordering but are not activated by I5.4.
10. No DB schema migration or persisted grade state is introduced.

---

## Acceptance

`tests/test_cross_domain_grading_v1.py` proves:
- full vocabulary ordering through XX;
- existing Character RAPS semantics remain intact;
- equivalent 55 lb / metric Item load yields the same S resistance-load grade;
- Imperial/Metric display changes do not affect grade;
- Item load grade is explicitly not a Character requirement;
- Location L0..L4 maps through a separate registered scheme;
- domain-specific grade profiles validate;
- overall grade requires an explicit composite scheme.

Existing Character grading tests remain required targeted regression coverage.

Next slice after green CI:

**I5.5 — Universal Requirement & Access Contract.**
