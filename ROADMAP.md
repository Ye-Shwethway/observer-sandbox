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

`versioned schema -> registered socket/reuse map -> Manual full-schema + AI full-schema -> canonicalize -> strict validate -> dependency/graph validate -> write-free preview + .txt -> explicit approval -> atomic Sandbox materialization -> approved detail -> Creator-friendly field Edit Preview/Apply/Done -> dependency-safe cleanup`

A new Creation domain must not be built as bespoke CRUD.

Approved-object Edit UX must not default to whole-section JSON replacement. The normal interaction is:

`Object Detail -> Edit -> Section -> Field -> friendly typed input/choice -> Preview -> Apply -> Continue/Done`

Raw/exact JSON may remain only as a clearly labeled advanced fallback where useful. Character/Profile Edit is the interaction-parity reference; typed field editors may vary by domain while the exact validator/materializer remains shared authority.

For canonical-isolation proofs around Sandbox mutation, fingerprint samples belong inside one writer transaction before commit:

`writer lock -> canonical before -> Sandbox writes -> canonical after -> rollback on mismatch / commit on match`.

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
- `src/observer_sandbox/telegram_sandbox_location_edit_adapter.py`;
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

## ✅ L11.6 — Detail/Browse + Edit + Cleanup Parity

**CLOSED after Creator production smoke.**

Implementation chain:

- PR #397 — guarded Sandbox Location update service;
- PR #398 — Telegram Edit Preview/Apply/Done backend parity;
- PR #399 — complete human detail/readback;
- PR #400 — dependency-aware cleanup;
- PR #402 — field-by-field Creator-friendly Location Edit UX;
- PR #404 — human-readable changed-field edit Preview;
- PR #405 — canonical-isolation race/atomic rollback fix for Apply/Delete.

Closed capabilities:

- approved Location browse/detail;
- readable hierarchy/geography, quantities, boundaries, access/control, environment, facilities/resources/capabilities, topology, economics and relationships;
- derived completeness GradeProfile presentation;
- exact-schema Edit with graph preflight and source-fingerprint stale guard;
- normal Edit is section -> field rather than complete-section JSON;
- scalar values use direct friendly input;
- enums use buttons;
- registry-backed lists such as Facilities capabilities/types/resources/utilities use multi-select toggles;
- same-Sandbox references use human-readable object pickers rather than raw IDs;
- physical quantities accept human units such as `12 ft`, `36 m`, `1800 ft2`;
- Topology has structured interface list/add/edit/delete controls;
- complete-section JSON is retained only as explicit `Advanced JSON` fallback;
- Preview shows human-readable changed fields instead of raw section JSON;
- Preview -> Apply -> Done remains mandatory;
- atomic projection rewrite and update audit event;
- canonical-isolation proof occurs inside one SQLite writer transaction before commit;
- legitimate concurrent Real World runtime writes cannot cause post-commit false alarms;
- actual canonical mutation during Sandbox update/delete rolls back atomically;
- no runtime pause because approved Location runtime is not running yet;
- dependency-aware Delete Location;
- active Character/Item relations, actor runtime placement and authoritative Location references block delete;
- no cascaded graph rewrite;
- safe delete requires fresh source-fingerprint review and explicit confirmation;
- blocked review arms no delete session and Cancel invalidates an armed review.

Verification:

- PR #402 / CI #1275 / deploy #386 ✅;
- PR #404 / CI #1278 / deploy #387 ✅;
- PR #405 / CI #1279 / deploy #388 ✅;
- Creator production smoke confirmed the field-level Edit, readable Preview and successful Apply path ✅.

## ▶ L11.7 — Full Location Vertical Acceptance

**NEXT. This is the final Location slice before Genesis.**

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
15. Creator-friendly Edit Preview/Apply/Done parity;
16. human-readable changed-field Preview;
17. dependency-safe cleanup;
18. canonical isolation under one transactional invariant;
19. approved Locations remain not runtime-active.

L11.7 should primarily be an **acceptance/hardening pass**, not a new feature-design phase. Any implementation work should be narrowly driven by acceptance failures.

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

**L11.6 is closed after Creator production smoke. Production is green through PR #405 / CI #1279 / deploy #388. Begin L11.7 Full Location Vertical Acceptance and only patch issues that the acceptance matrix actually exposes.**
