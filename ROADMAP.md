# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-09-03**

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

## Mandatory Creation gate

Before Creator Creation planning/coding/review/debugging, read:

`docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`

Core vertical:

`versioned schema -> registered socket/reuse map -> Manual full-schema + AI full-schema -> canonicalize -> strict validate -> dependency/graph validate -> write-free preview + .txt -> explicit approval -> atomic Sandbox materialization -> approved detail -> Edit Preview/Apply/Done -> dependency-safe cleanup`

A new Creation domain must not be built as bespoke CRUD.

---

# Current strategic direction — Location first, then Genesis

The current Real World Darian/Thorne Estate/legacy Item world is prototype-era exemplar content and is not a preservation constraint.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

Canonical Genesis plan: `docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`  
Decision record: `docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`

The destructive reset is **not authorized yet**. Full Location acceptance must close first.

---

# Current Location authority

Detailed plan: `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`

Primary executable contracts now include:

- `docs/UNIVERSAL_LOCATION_SCHEMA_V2.md`;
- `docs/LOCATION_GRADING_EVIDENCE_MATRIX_V1.md`;
- `src/observer_sandbox/location_creation_schema_v2.py`;
- `src/observer_sandbox/location_schema_registry_v2.py`;
- `src/observer_sandbox/location_ai_contract.py`;
- `src/observer_sandbox/sandbox_location_v2.py`;
- `src/observer_sandbox/sandbox_location_composition.py`;
- `src/observer_sandbox/sandbox_location_operations.py`;
- `src/observer_sandbox/sandbox_location_cleanup.py`;
- `src/observer_sandbox/telegram_sandbox_location_edit.py`;
- `src/observer_sandbox/telegram_sandbox_location_cleanup.py`;
- `docs/WORLD_LOCATION_NODE_MODEL.md`;
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`;
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`;
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

`location-v2` is an explicit successor to the retained v1 foundation, not a competing ontology.

## Grading lock

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived Location GradeProfile`

- completeness — mandatory;
- spatial scale — evidence/reference gated;
- infrastructure/facility capability — evidence/reference gated;
- connectivity — graph/context gated;
- asset value — economy/reference gated;
- security — deferred until raw security evidence exists;
- no AI/Creator-authored grade letters/thresholds/evaluator IDs;
- no automatic overall Location grade without explicit composite semantics.

---

# Location implementation slices

## ✅ L11.0 — Schema Refinement + Grading Contract

Closed. `location-v2` locks Geography, Boundary, typed interfaces, registry-backed functional/facility/resource/capability semantics, definition-vs-runtime state separation, minimal control/ownership and grading evidence contracts.

## ✅ L11.1 — Exact Validator + Registry/Grading Foundation

Closed. Exact v2 validation/canonicalization and registry foundations are executable; completeness grading is derived, not authored.

## ✅ L11.2 — Sandbox Persistence + Graph Materializer

Closed. Validated Locations materialize only into isolated Sandbox persistence with stable IDs, same-Sandbox graph checks, acyclic structural hierarchy, typed graph projection, atomic materialization, no runtime activation and canonical isolation.

## ✅ L11.3 — Manual Full-Schema Creation

Closed through PR #380 / CI #1225.

Manual Location authoring provides Guided Build over all 13 creation-owned sections, advanced Exact JSON, whole-payload revalidation, write-free Preview/export, Cancel/no-write and revision-bound Sandbox approval.

## ✅ L11.4 — AI Full-Schema Creation

Closed through PR #382 / CI #1226.

AI Location uses the complete strict provider-facing `location-v2` fill contract, exact deterministic validation, at most one bounded representation-only repair, reroll/typing feedback and the same Preview/export/approval/materializer as Manual.

## ✅ L11.5 — Nested Composition + Embedded Items

Closed by the subsequently verified production path and L11.6 progression.

Implemented authority includes:

- explicit `location-composition-v1` envelope;
- exact child `location-v2` and embedded `item-v1` members;
- deterministic `$ref` resolution;
- structural parent, topology, `located_at` and typed `stored_in` resolution;
- same-Sandbox validation and cycle/dependency rejection;
- whole-graph validation before writes;
- one atomic transaction and full rollback on failure;
- human whole-graph Preview + `.txt` export;
- revision-bound approval;
- no runtime activation or canonical mutation.

## ▶ L11.6 — Detail/Browse + Edit + Cleanup Parity — PRODUCTION GREEN, CREATOR SMOKE REMAINS

Implementation chain:

- PR #397 — guarded Sandbox Location update service;
- PR #398 — Telegram Edit Preview/Apply/Done parity;
- PR #399 — complete human detail/readback;
- PR #400 — dependency-aware cleanup.

Current capabilities:

- approved Location browse/detail;
- readable hierarchy/geography, quantities, boundaries, access/control, environment, facilities/resources/capabilities, topology, economics and relationships;
- derived completeness GradeProfile presentation;
- exact-schema Edit with graph preflight and source-fingerprint stale guard;
- Preview -> Apply -> Done;
- atomic projection rewrite and update audit event;
- no runtime pause because approved Location runtime is not running yet;
- dependency-aware Delete Location;
- active Character/Item relations, actor runtime placement and authoritative Location references block delete;
- no cascaded graph rewrite;
- safe delete requires fresh source-fingerprint review and explicit confirmation;
- blocked review arms no delete session and Cancel invalidates an armed review;
- canonical Real World fingerprint is verified unchanged.

Verification:

- PR #400 CI #1271 — targeted regression ✅, CLI init/status smoke ✅, full fallback correctly skipped;
- merge checkpoint `8fa1655bd97421ea6b3e99f200ae316d2eb0ff4c`;
- production deploy #385 — sync/install/cognition recovery/service entrypoint/restart/runtime health ✅.

Creator production smoke still required before marking this slice fully closed:

`Location detail -> Edit Preview/Apply/Done -> dependency-blocked Delete -> Cancel -> fresh review -> confirmed deletion of expendable unreferenced Location`

## L11.7 — Full Location Vertical Acceptance

**NEXT after L11.6 Creator smoke.**

Prove at least:

1. property/building hierarchy;
2. room/outdoor-zone hierarchy;
3. explicit interfaces/topology;
4. access policy distinct from operating state;
5. partial/unknown geography without fabrication;
6. boundary semantics;
7. facility/resource/capability evidence;
8. derived completeness + applicable grading dimensions;
9. nested child Locations;
10. embedded multi-class Items;
11. Manual and AI parity;
12. Preview/export write-free;
13. atomic approval;
14. invalid parent/cycle/cross-Sandbox/local-ref => zero writes;
15. Edit Preview/Apply/Done parity;
16. dependency-safe cleanup;
17. `canonical_state_fingerprint()` unchanged;
18. approved Locations remain not runtime-active.

Only after L11.7 closes does the Genesis transition begin.

---

# Recent Character UX parity

PR #379 / CI #1223 added read-only **Full Profile `.txt` export** for approved Sandbox Characters from both Character detail and Profile menu.

It exports current approved Sandbox profile values—including Creator edits—plus Skills, Preferences, Hobbies and Habits, while intentionally excluding live runtime-owned changing state.

---

# After Location acceptance — Genesis transition

1. **G1 — Prototype Content Reset Audit & Contract** — exact keep/wipe sets and cleanup order.
2. **G2 — Remove legacy reseeding authority** — Darian/Thorne Estate/legacy Item bootstrap cannot resurrect retired content.
3. **G3 — Controlled Real World content reset** — retire prototype content while preserving reusable infrastructure.
4. **G4 — Transmigration Foundation** — freeze Sandbox revision -> schema/dependency validation -> target-universe compatibility -> conflict/id resolution -> Creator preview -> explicit approval -> atomic canonical materialization -> provenance.
5. **G5 — Genesis Transmigration** — Locations/root topology -> Items/fixtures/containers + placement -> Characters + valid starting Location -> readiness/affordances -> explicit activation.

A Character cannot be activated without a valid represented Location.

Preserve reusable time/clock, weather/environment, economy/money, AI/provider, generic event/action/runtime, physiology/effects, Mind/Memory, grading/requirements/quantity/economic-value and Creation infrastructure.

---

# Future Reincarnation / Renewal

Reincarnation is modern-to-modern canonical renewal, not preservation of prototype-era content:

`modern canonical v1 -> Renew in Sandbox -> edit/regenerate/test -> compatibility + diff -> Creator approval -> canonical v2`

---

## Retained locks

- no automatic transmigration;
- target-universe compatibility before canonical promotion;
- `runtime_ready != running`;
- full autonomous Sandbox ticking remains separately unauthorized;
- missing grading evidence/reference => ungraded, not invented precision;
- Location grade never automatically becomes access authorization;
- overall grade requires explicit composite semantics;
- current Real World prototype content still exists until future reset is actually implemented and verified;
- do not make deploy/live claims without current evidence.

## Exact resume point

**Production is green through PR #400 / deploy #385. Perform the Creator Telegram smoke for Location Detail/Edit/Delete. If dependency blocking, Cancel invalidation, explicit safe deletion and post-delete navigation all pass, mark L11.6 closed and begin L11.7 Full Location Vertical Acceptance.**
