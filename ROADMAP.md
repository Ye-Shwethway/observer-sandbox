# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, live repo/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate, derive and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Universal systems use expandable registry/socket patterns rather than family-specific switchboards.
- `canonical_state_fingerprint()` remains a high-value zero-canonical-mutation invariant.
- Development velocity matters: do not turn optional realism polish into a creation-blocking treadmill without explicit Creator approval.

### Mandatory Creation implementation gate

`docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` is now the canonical implementation playbook for every current/future Creator Creation section.

Before planning, coding, reviewing, extending or debugging Character/Item/Location/Skill/Quest/System/Organization/Service/Event/world-element or future Creation sockets:

1. reread the Creation Implementation Standard;
2. identify the canonical versioned domain schema;
3. if no schema exists, **build/approve the schema first** before AI/UI/materialization work;
4. map existing reusable contracts/sockets;
5. follow the shared Creation vertical rather than creating a bespoke CRUD path.

Core vertical:

`versioned schema -> socket/reuse map -> full Manual form + full AI structured fill -> safe canonicalization -> strict structural/domain validation -> graph/dependency validation -> write-free review + .txt export -> explicit approval -> atomic Sandbox materialization -> approved detail -> Edit Preview/Apply/Done + pause restoration -> cleanup`.

Fine-grained realism is advisory/non-blocking by default unless a domain contract and explicit Creator authorization make it authoritative.

---

## Creation Implementation Standard v1 — completed meta-foundation

The standard was synthesized after detailed review of the completed Character Creation and Item Creation implementations and their failure history.

### Reused Character lessons

- exact schema instead of free-form prose properties;
- registry/schema-driven field vocabulary and presentation;
- Manual/AI parity through one authoritative validator/materializer;
- structured/paginated review for large profiles;
- explicit approval into isolated Sandbox state;
- Telegram as adapter, not semantic authority;
- Edit preflight, persistent edit-mode pause, Preview before Apply, stale guards and exact pre-edit pause-state restoration.

### Reused Item lessons

- Single and Batch reuse the same exact member schema;
- Batch validates the complete graph before one atomic apply;
- provider schema, canonicalizer and validator are separate contracts that require compatibility tests;
- provider schema/registries should share enum/module/metric sources;
- canonicalization may repair mechanical representation only, never invent semantic facts;
- validator normalized output must revalidate;
- strong system-side AI authoring contract keeps Creator prompts short/natural;
- one bounded self-correction attempt is recovery only, not the normal path;
- Telegram `typing` feedback for slow structured AI generation;
- human-facing review plus raw `.txt` technical audit export;
- safe actionable diagnostics;
- Cancel/no-write behavior before approval;
- Item Edit schema parity + pause restoration;
- repeated live errors require invariant-family audit rather than one-field whack-a-mole fixes;
- excessive realism gating is explicitly rejected as the default Creation policy.

`AGENTS.md` now carries a repository-level hard lock requiring this standard before any Creator Creation work.

---

## Current repository checkpoint — deliberate rollback baseline

Creator selected **`b59e632aa8e31647b85eeb244a4436c31e9e1e9d`** (`Fix Item nutrition basis semantics`, PR #369) as the acceptable Item Creation behavior after later realism checks caused repeated live rejection loops.

Rollback PR **#372** restored the full repository tree to that checkpoint while preserving history. It merged to `main` as:

`6fe07ec4fde0375b29477c026e4ace991f8834ce`

Intentionally rolled back:
- PR #370 luminous-efficacy blocking validation;
- PR #371 fixture-mobility reconciliation/tightening;
- interrupted later realism-simplification commits that had existed only on `test`.

**Policy lock:** do not reintroduce or further tighten fine-grained Item realism validation without explicit Creator authorization. The chosen `b59e632...` behavior is the current accepted baseline.

This baseline still retains earlier structural/schema safety, metric/grading foundations, AI canonicalization, schema-validator compatibility work, shared authoring guidance, metric coherence/evidence validation through PR #367, prompt refinement through PR #368, and nutrition-basis semantics through PR #369.

---

## Completed Creator foundation — retained

I5.2–I5.10 remain complete:
- I5.2 Creation Contract Reuse Map
- I5.3 Universal Quantity / Measurement
- I5.4 Universal Cross-Domain Grading
- I5.5 Requirements / Access
- I5.6 Universal Item Schema v1
- I5.7 Single Sandbox Item materialization
- I5.8 Atomic heterogeneous Item Batch
- I5.9 Item / Container Operations
- I5.10 Universal Location Schema v1

Additional accepted Item Creator work retained through the rollback baseline includes:
- strict Single/Batch AI/manual creation;
- atomic batch preview/apply;
- batch ref canonicalization;
- module/capability reconciliation;
- economic valuation + human-readable display;
- raw review export;
- approved Item detail parity;
- Item Edit with preview/apply/stale guard/pause restoration;
- Character/Item batch cleanup;
- schema/canonicalizer/validator compatibility audit;
- shared single+batch Creator AI authoring contract;
- nutrition-basis semantics.

Locked Item ontology:
`Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations remain distinct: `contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by`. Ownership is orthogonal to physical placement/storage.

---

## Universal grading foundation — retained

Universal Grading Socket v1 (PR #360) remains accepted.

Core invariant:
`authoritative raw state + registered grading sockets + universe policy -> derived GradePlan -> deterministic GradeProfile`.

Broad Item Grading Coverage Foundation (PR #362) remains retained:
- generic sparse `definition.modules.metrics` socket;
- registry-driven metric schema/unit normalization;
- performance metrics in draft/approved Item UI;
- deterministic named-dimension grading;
- Item Edit compatibility for nested metric fields.

Initial raw metrics include luminous flux, runtime, power, energy capacity, range, speed, data rate, digital storage, beam distance, water-resistance depth, charge time and payload capacity. Existing resistance load and container capacity remain dedicated-module evidence.

Grading locks:
1. raw represented facts remain authority;
2. arbitrary numeric fields are not automatically gradeable;
3. registered evaluator/dimension/reference/universe policy controls semantics;
4. missing evidence/reference -> ungraded, not invented precision;
5. realistic universes do not auto-admit supernatural dimensions;
6. AI does not own final grade letters/thresholds;
7. **Item Grade describes the Item; Requirement Grade describes the interaction**;
8. Location grade is not access authorization;
9. overall grade requires explicit composite semantics.

---

## Current Item acceptance policy

The previous goal of exhaustively polishing numeric realism before approval is **cancelled**. Creator-side prompts should remain short and natural; technical schema burden belongs to the system-side authoring/canonicalization path.

Creation blocking should prioritize:
- schema/type correctness;
- stable ids/refs/tokens;
- valid same-batch references;
- stack/instance/module structural consistency;
- hard module/capability contracts already present in the chosen baseline;
- atomic validation/materialization;
- Sandbox isolation and no canonical Real World mutation.

Do not block forward progress for every minor questionable real-world numeric ratio. Fine-grained realism can be revisited later as advisory/non-blocking quality work if desired.

---

# CURRENT ACCEPTANCE — one final representative Item pass

Do not mass-regenerate old Items yet.

After production is verified at rollback merge `6fe07ec4fde0...` or later:
1. create one small fresh multi-class batch using a very short natural Creator prompt;
2. verify preview succeeds without structural/schema rejection;
3. inspect that modules/metrics are broadly sensible without demanding microscopic realism;
4. approve the batch if structurally usable;
5. verify approved Item details retain expected metrics/grades;
6. live-edit one metric-bearing Item -> Preview -> Apply -> Done;
7. verify pre-edit pause-state restoration;
8. verify canonical Real World state remains unchanged.

If this passes, close the Item representative acceptance gate and resume feature development. Do not restart a chain of realism micro-fixes unless a genuine structural or runtime blocker appears.

---

# NEXT — I5.11 Sandbox Location Creation + Embedded Contents

**Mandatory kickoff:** reread `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` and follow its New Creation section checklist.

I5.11 already has the canonical schema `docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`. Therefore do **not** create a second Location schema. Map the existing schema into the shared Creation vertical.

Required implementation pattern:
- complete Manual/full-schema Location construction surface;
- complete provider-facing AI Location fill form generated/aligned from the exact Location schema;
- strong shared system-side authoring contract so natural Creator prompts are sufficient;
- safe canonicalization + exact Location validation;
- human preview + raw `.txt` technical export;
- AI `typing` feedback;
- Cancel/no-write semantics;
- explicit Creator approval;
- strict I5.10 Location materialization;
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 exact member schemas/contracts/storage;
- no arbitrary contents bag;
- movable Items normally use `located_at`, or exact `stored_in` typed containers;
- validate the whole Location + contents graph before writes;
- one atomic apply/rollback;
- approved Location detail/browse surface;
- Location Edit should reuse the same schema/validator and standard Preview/Apply/Done + pause-state-restoration semantics where runtime races matter;
- no automatic runtime readiness;
- no autonomous execution/ticking;
- no canonical writes.

Then:
I5.12 Location Contents Operations -> I5.13 Character/Location Binding & Runtime Readiness -> I5.14 Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

Every later Creation domain repeats the standard kickoff: **read standard -> schema exists/build first -> reuse/socket map -> full Manual/AI vertical -> acceptance**.

---

## Transmigration / Character locks

Nothing transmigrates automatically. Target-universe compatibility/policy validation precedes transmigration. I6 remains planning/validation only unless Creator expands scope. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed until later Mind + Relationship work. Existing Character creation/edit parity stays locked. Full Sandbox autonomous ticking remains separately unauthorized.

---

## Exact resume point

**`docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` is now mandatory before every Creator Creation domain and `AGENTS.md` enforces that high-level lock. The standard was synthesized from detailed Character + Item review and locks schema-first, expandable socket/registry design, full Manual/AI schema parity, strong system-side structured AI fill, schema/canonicalizer/validator compatibility, reusable Telegram typing/review/.txt/Cancel UX, explicit atomic Sandbox approval, canonical isolation, Edit Preview/Apply/Done with exact pause restoration, diagnostics and lifecycle cleanup. Item Creation remains deliberately rolled back to the `b59e632aa8e3` behavior; do not re-tighten fine realism without explicit authorization. Verify rollback merge `6fe07ec4fde0...` or later live, run one final short-prompt Item batch + Edit acceptance, then reread the Creation Standard and start I5.11 using the existing Universal Location Schema v1.**
