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

The current Real World Darian/Thorne Estate/legacy Item world is prototype-era exemplar content, not a preservation constraint. However it remains present until a later explicitly authorized destructive reset is actually executed and verified.

Canonical Genesis plan: `docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`  
Decision record: `docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`  
G1 reset audit contract: `docs/GENESIS_G1_PROTOTYPE_CONTENT_RESET_AUDIT_V1.md`

## 🟡 G1 — Prototype Content Reset Audit & Contract — REVIEW IN PROGRESS

**G1 is audit/contract only. It does not delete or mutate canonical Real World content.**

The repo-grounded G1 contract now inventories:

1. **KEEP set** — reusable universe infrastructure and canonical services/tables that survive;
2. **WIPE set** — prototype Characters, Locations, Items/fixtures/inventory and their prototype-owned runtime/state;
3. **RESEED-AUTHORITY REMOVE set** — bootstrap/seed/recovery paths that could recreate retired prototype content;
4. **DEPENDENCY / ORDER set** — graph and FK/reference ordering for safe later cleanup;
5. **BACKUP / ROLLBACK contract** — required pre-reset snapshot and abort criteria;
6. **POST-RESET verification contract** — prove prototype content absent while reusable infrastructure remains healthy;
7. **NO-TOUCH set** — Creation Sandbox and unrelated reusable systems that the reset must not damage.

Key G1 findings now locked for review:

- ordinary `runtime.status()` calls `_initialize_conn()`, so current status/health execution can invoke prototype seeders;
- `seed_home_and_darian()` can recreate the Thorne Estate graph and Darian after a DB-only deletion;
- Estate inventory, Darian economy, Estate media and several represented simulator seeders are content-bound bootstrap surfaces;
- generic Item definitions must be separated from Estate-specific stack materialization rather than wiped wholesale;
- current production Character seed directory contains Darian only; Quasi/Elias must not be assumed active without production DB evidence;
- the future clean Real World may contain zero canonical Characters, but current `status()` fails in that legitimate state because actor resolution is unconditional;
- therefore healthy empty-canonical-world semantics are a hard G2/G3 prerequisite;
- `world_observer_universe` is retained by default as the target universe/root identity while Estate/Character bootstrap assumptions are removed, unless a separate explicit universe-identity migration is later approved;
- the exact G3 row manifest remains production-DB-preflight-driven and must fail closed on unexpected dependencies.

G1 remains non-destructive until this contract is merged/reviewed. The current review vehicle is PR #409.

## G2 — Remove legacy reseeding authority + support healthy empty canonical world

After G1 approval:

- remove/generalize only the identified prototype reseed/bootstrap authority so retired Darian/Thorne Estate/legacy Items cannot return after reset;
- separate reusable definitions/contracts from Estate/Darian fixture materialization;
- make init/status/runtime health valid with zero canonical Characters and no synthetic default actor;
- prove normal init/status/restart does not recreate prototype content.

## G3 — Controlled Real World content reset

Execute the approved G1 wipe contract atomically/controllably only after G2 is production-green and the destructive reset is explicitly authorized. Preserve KEEP/NO-TOUCH sets, require verified backup/preflight, and prove post-restart no-reseed health.

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
- current Real World prototype content still exists until future reset is actually implemented and verified;
- **G1 is audit/contract only; destructive reset is not authorized merely by entering or merging G1**;
- do not make deploy/live claims without current evidence.

## Exact resume point

**G1 Prototype Content Reset Audit & Contract is under review in PR #409. Validate the docs-only security gate, merge the reviewed contract, then close G1 continuity and begin G2 reseed-authority removal/generalization plus healthy zero-Character canonical runtime. Do not perform destructive canonical reset in G1 or G2.**
