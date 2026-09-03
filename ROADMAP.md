# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-09-04**

## Operating principles

- Current Creator instruction, live repo/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate, derive and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Universal systems use expandable registry/socket patterns rather than family-specific switchboards.
- `canonical_state_fingerprint()` remains a high-value zero-canonical-mutation invariant.
- Development velocity matters: optional realism polish does not become a blocking treadmill without explicit Creator approval.

For canonical-isolation proofs around Sandbox mutation:

`writer lock -> canonical before -> Sandbox writes -> canonical after -> rollback on mismatch / commit on match`.

---

# ✅ Modern Sandbox Location Creation — FULLY ACCEPTED

Detailed implementation plan: `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`  
Final acceptance matrix: `docs/LOCATION_VERTICAL_ACCEPTANCE_V1.md`

## Location slices

- ✅ L11.0 — Schema Refinement + Grading Contract
- ✅ L11.1 — Exact Validator + Registry/Grading Foundation
- ✅ L11.2 — Sandbox Persistence + Graph Materializer
- ✅ L11.3 — Manual Full-Schema Creation
- ✅ L11.4 — AI Full-Schema Creation
- ✅ L11.5 — Nested Composition + Embedded Items
- ✅ L11.6 — Detail/Browse + Edit + Cleanup Parity
- ✅ **L11.7 — Full Location Vertical Acceptance**

### L11.7 final evidence

PR #407 added the explicit acceptance matrix plus representative cross-slice tests covering:

- property -> building -> room hierarchy;
- property -> outdoor-zone hierarchy;
- explicit room <-> outdoor topology;
- partial geography with unknown position/bounds preserved as null;
- enclosed indoor vs open outdoor boundary semantics;
- facilities/resources/capabilities/utilities through materialization;
- derived completeness GradeProfile with no invented overall grade;
- heterogeneous embedded `container` + `object` Items;
- local `located_at` and `stored_in` resolution;
- write-free preview;
- canonical fingerprint stability;
- no runtime activation.

Historical executable evidence for Manual/AI parity, atomic approval/rollback, invalid graph zero-writes, Creator-friendly Edit and dependency-safe cleanup is mapped in `docs/LOCATION_VERTICAL_ACCEPTANCE_V1.md`.

CI history:
- #1280 exposed an acceptance-test-only incorrect DB-column assumption; no product defect.
- #1281 passed after reading Item kind through approved materializer output.
- #1282 final acceptance rerun + CLI init/status smoke passed ✅.

PR #407 merged as `c3e8cbb556d0037c8310261398c19a0939bec09a`.

No production implementation patch was required by L11.7.

### Accepted Location boundaries

- `location-v2` is the current exact Location creation authority.
- `location-composition-v1` is the explicit nested Location + Item composition envelope.
- Manual and AI creation share exact validator/materializer authority.
- Preview/export remain write-free.
- Approval/materialization is explicit and Sandbox-only.
- Approved Location editing is field-friendly; whole-section raw JSON is Advanced fallback only.
- Cleanup is dependency-safe and non-cascading.
- Approved Locations remain not runtime-active.
- No automatic transmigration exists.

### Grading lock

Current active Location grading dimension is **completeness**.

- no AI/Creator-authored grades;
- no automatic overall grade;
- spatial scale, infrastructure/facility capability, connectivity and asset value remain evidence/reference gated;
- security remains deferred until raw security evidence exists;
- missing evidence/reference => ungraded.

---

# ▶ Current major phase — Genesis transition

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

The current Real World Darian/Thorne Estate/legacy Item world is prototype-era exemplar content, not a preservation constraint. It remains present until the later explicitly authorized destructive reset is actually executed and verified.

Canonical Genesis plan: `docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`  
Decision record: `docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`  
G1 reset audit contract: `docs/GENESIS_G1_PROTOTYPE_CONTENT_RESET_AUDIT_V1.md`

## ✅ G1 — Prototype Content Reset Audit & Contract — CLOSED

PR #409 merged the reviewed non-destructive G1 reset contract as `0dab6ca980510a8ef1553dd7d34fa86c5a0bc047` after Public Readiness Security Audit #236 passed.

G1 performed **no canonical Real World mutation** and authorized no destructive reset.

Locked G1 outputs:

1. **KEEP set** — reusable universe infrastructure and canonical services/tables that survive;
2. **WIPE set** — prototype Characters, Locations, Items/fixtures/inventory and prototype-owned runtime/state;
3. **RESEED-AUTHORITY REMOVE / GENERALIZE set** — startup paths that can recreate retired prototype content;
4. **DEPENDENCY / ORDER set** — graph/FK/reference cleanup ordering;
5. **BACKUP / ROLLBACK contract** — pre-reset snapshot and abort requirements;
6. **POST-RESET verification contract** — including post-restart no-reseed proof;
7. **NO-TOUCH set** — Creation Sandbox and unrelated reusable systems.

Key G1 findings:

- ordinary `runtime.status()` currently calls `_initialize_conn()`, so status/health can invoke content seeders;
- `seed_home_and_darian()` can recreate the Thorne Estate graph and Darian after DB-only deletion;
- Estate campus, Estate inventory, Darian economy, Estate media, and several represented simulator seeders are content-bound startup surfaces;
- generic Item definitions must be separated from Estate-specific stack/materialization rather than wiped wholesale;
- current production Character seed directory contains Darian only; Quasi/Elias are deletion candidates only if live DB preflight proves active prototype rows exist;
- `world_observer_universe` is retained by default as the target universe/root identity while Estate/Character bootstrap assumptions are removed, unless a separate explicit universe-identity migration is approved;
- exact G3 deletion rows remain production-DB-preflight-driven and fail closed on unexpected dependencies;
- a clean post-reset Real World may legitimately contain zero canonical Characters;
- current `status()` cannot represent that state healthily because `resolve_actor_id()` is unconditional;
- healthy empty-canonical-world semantics are therefore a hard prerequisite before destructive reset.

## ▶ G2 — Remove legacy reseeding authority + healthy empty canonical world — NEXT

G2 is implementation work, but remains **non-destructive to current canonical prototype content**.

Required G2 outcomes:

- remove/generalize `seed_home_and_darian()` from ordinary startup;
- remove/generalize `seed_estate_campus()` from ordinary startup;
- split generic Item definition registration from Estate-specific `seed_home_inventory()` materialization;
- remove Darian-specific `seed_initial_economy()` bootstrap while preserving generic economy infrastructure;
- generalize/remove the hard-coded Thorne Estate information-media seed;
- separate reusable technology/tactical/represented-skill action/task contracts from Thorne Estate simulator fixture materialization;
- preserve generic action vocabulary such as controlled H2H and field-medicine stabilization where it creates no live exemplar fixture;
- audit any remaining content-bound memory/familiarity/value/bootstrap path before declaring reseed authority removed;
- allow init/status/runtime health with zero canonical Characters;
- never create a synthetic/default Character merely for health;
- ensure actor-specific recovery/progression/migration only runs when a valid actor exists;
- prove ordinary init/status/restart cannot recreate Darian, Thorne Estate, Estate inventory/economy/media/simulator fixtures.

G2 must use focused/path-aware tests, PR/CI, merge, production deploy/runtime health, and post-deploy verification before G3 can be considered.

## G3 — Controlled Real World content reset

Only after G2 is production-green **and Creator explicitly authorizes destructive execution**:

- run live production DB preflight;
- create/verify backup and reset manifest;
- execute the approved bounded transaction;
- preserve KEEP/NO-TOUCH sets;
- pass FK/integrity/orphan checks;
- restart normally and prove retired content does not reseed;
- remain healthy with zero canonical Characters if Genesis Character transmigration has not yet occurred.

## G4 — Transmigration Foundation

`freeze Sandbox revision -> exact schema/dependency validation -> target-universe compatibility -> conflict/id resolution -> Creator preview -> explicit approval -> atomic canonical materialization -> provenance`

No automatic transmigration.

## G5 — Genesis Transmigration

Order:

`Locations/root topology -> Items/fixtures/containers + placement -> Characters + valid starting Location -> readiness/affordances -> explicit activation`

A Character cannot be activated without a valid represented Location.

---

# Mandatory Creation gate

Before Creator Creation planning/coding/review/debugging, read:

`docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`

Core vertical:

`versioned schema -> registered socket/reuse map -> Manual full-schema + AI full-schema -> canonicalize -> strict validate -> dependency/graph validate -> write-free preview + .txt -> explicit approval -> atomic Sandbox materialization -> approved detail -> Creator-friendly field Edit Preview/Apply/Done -> dependency-safe cleanup`

A new Creation domain must not be built as bespoke CRUD.

---

# Retained locks

- no automatic transmigration;
- target-universe compatibility before canonical promotion;
- `runtime_ready != running`;
- full autonomous Sandbox ticking remains separately unauthorized;
- missing grading evidence/reference => ungraded, not invented precision;
- Location grade never automatically becomes access authorization;
- overall grade requires explicit composite semantics;
- current Real World prototype content still exists until G3 is explicitly authorized, executed and verified;
- **G1 closure does not authorize destructive reset**;
- **G2 removes resurrection/bootstrap authority but must not delete current prototype canonical content**;
- do not make deploy/live claims without current evidence.

## Exact resume point

**G1 Prototype Content Reset Audit & Contract is closed through PR #409 / Public Readiness Security Audit #236 / merge `0dab6ca980510a8ef1553dd7d34fa86c5a0bc047`. Begin G2: remove/generalize prototype reseed authority and add healthy zero-canonical-Character init/status semantics, while leaving current Darian/Thorne Estate prototype rows untouched until separately authorized G3.**
