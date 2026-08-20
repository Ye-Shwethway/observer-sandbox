# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, live repo/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Real World and Creation Sandbox mutable state remain isolated.
- Reuse established semantics; design universal systems as expandable sockets rather than family-specific switchboards.
- `canonical_state_fingerprint()` remains a high-value zero-canonical-mutation invariant.

---

## Current checkpoint

Fresh current-schema Item Edit is now **live-confirmed working** by Creator after PR #358.

Latest accepted implementation:

### PR #360 — Universal Grading Sockets + Item Coverage v1

Merged commit:
`9155a94bc75b800d4a10f2a39993647c78d11d9c`

CI **#1195** ✅ targeted regression + CLI smoke.

Canonical contract:
`docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

Core architecture:
`authoritative raw state + registered grading sockets + universe policy -> derived GradePlan -> deterministic GradeProfile`.

Implemented extension points:
- evaluator registry / `EvaluatorSpec`;
- dimension registry / `DimensionSpec`;
- reference-profile registry;
- universe grading policy;
- rebuildable GradePlan;
- deterministic GradeProfile resolver.

Acceptance proves a synthetic new Item evaluator/dimension can be plugged into a fresh registry without changing resolver core.

Default realistic policy is explicit/fail-closed: current legitimate `resistance_load` is allowed; newly-registered supernatural dimensions are not automatically admitted; current load grading ceiling is S.

Current Item UI coverage:
- training resistance reuses `item-resistance-load-v1` and preserves existing thresholds;
- 55 lb-equivalent resistance -> S;
- draft review + approved Item detail display `Resistance Load: S · Expert`;
- ordinary uncovered Items display `No registered grading dimensions apply to this Item yet.`;
- no fabricated overall grade;
- raw draft `.txt` export stays technical/non-authoritative;
- no DB migration or new persisted GradePlan/grade authority.

Deployment/live rendering of #360 remains a separate evidence gate until runtime/Creator verification.

---

## Universal grading direction

Canonical vocabulary:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Shared vocabulary does not mean shared raw scales.

Rules:
1. raw authoritative facts remain independent of grades;
2. grades require explicit registered dimensions/evaluators;
3. unknown numeric fields are not automatically gradeable;
4. missing reference/evidence yields ungraded, not invented precision;
5. overall grade requires an explicit composite evaluator/scheme;
6. universe policy decides which dimensions/evaluators/references/ceilings are legitimate;
7. **Item Grade describes the item; Requirement Grade describes the interaction**;
8. Location grade is not access authorization;
9. AI may later propose applicability, but registry + policy + evidence + deterministic evaluator remain authority;
10. future domain additions should use sockets rather than central family switches.

Extension pattern:
`EvaluatorSpec + DimensionSpec + optional ReferenceProfile + UniverseGradingPolicy allowance`.

---

## Completed Creator foundation — retained

I5.2–I5.10 remain complete:
- I5.2 Creation Contract Reuse Map;
- I5.3 Universal Quantity / Measurement;
- I5.4 Universal Cross-Domain Grading;
- I5.5 Requirements / Access;
- I5.6 Universal Item Schema v1;
- I5.7 Single Sandbox Item materialization;
- I5.8 Atomic heterogeneous Item Batch;
- I5.9 Item / Container Operations;
- I5.10 Universal Location Schema v1.

Item Creator Studio/Telegram retains strict Single/Batch creation, AI/manual convergence, realism/self-correction, human review + raw export, approved details/economics, Item Edit parity/diagnostics, batch cleanup and human-friendly value presentation.

Locked Item ontology:
`Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations retain separate `contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by` semantics. Ownership is orthogonal to physical location/storage.

---

# CURRENT DEVELOPMENT FAMILY — Item Grading Coverage expansion

The socket foundation is accepted, but Item grading is **not exhaustively complete**. V1 has one real registered Item dimension (`resistance_load`) plus extension proofs.

Next bounded work should expand coverage without hard-coding item families.

Priority sequence:
1. verify deployed PR #360 Item grading UI when available;
2. identify additional Item raw properties/modules that already have defensible grading semantics or can support evidence-backed reference profiles;
3. add reusable evaluator/dimension/reference registrations rather than `if backpack / flashlight / sword` logic;
4. where generation-time classification helps, introduce a strict structured AI applicability-plan proposal whose ids must already resolve through the registries and current universe policy;
5. final grade letters remain deterministic, never AI authority;
6. Items with no defensible registered dimension remain valid/ungraded;
7. defer overall Item grade until a defensible explicit composite exists, including critical-dimension/missing-evidence behavior.

Do not invent durability, quality, efficiency or category baselines unless their underlying raw representation and evaluator/reference authority exist.

---

# NEXT AFTER Item Grading Coverage checkpoint

### I5.11 — Sandbox Location Creation + Embedded Contents

Required semantics remain:
- strict I5.10 Location materialization;
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 contracts;
- movable Items normally use `located_at`, or exact `stored_in` typed containers;
- validate whole Location + contents graph before writes;
- atomic apply/rollback;
- no automatic runtime readiness;
- no autonomous execution;
- no canonical writes.

Then I5.12 Location Contents Operations -> I5.13 Character/Location Binding & Runtime Readiness -> I5.14 Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

---

## Transmigration / Character locks

Nothing transmigrates automatically. I6 remains planning/validation only unless Creator expands scope. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Existing Character Manual/AI/profile/edit/grade-target parity stays locked. Full Sandbox autonomous ticking remains separately unauthorized.

---

## Exact resume point

**Creator live-confirmed fresh Item Edit works after PR #358. PR #360 merged at `9155a94bc75b800d4a10f2a39993647c78d11d9c`; CI #1195 is green. Universal Grading Socket v1 now provides evaluator/dimension/reference/universe-policy sockets, a rebuildable GradePlan and deterministic GradeProfile, with current Item resistance-load coverage plus explicit ungraded handling and draft/approved UI. Continue evidence-backed Item Grading Coverage through socket registrations and constrained AI applicability planning where useful; do not hard-code item families or fabricate baselines. Resume I5.11 after the intended grading-coverage checkpoint.**
