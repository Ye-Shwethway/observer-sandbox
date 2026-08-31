# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-31**

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

Before any Creator Creation planning/coding/review/debugging, read:

`docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`

Core vertical:

`versioned schema -> registered socket/reuse map -> Manual full-schema + AI full-schema -> canonicalize -> strict validate -> dependency/graph validate -> write-free preview + .txt -> explicit approval -> atomic Sandbox materialization -> approved detail -> Edit Preview/Apply/Done -> cleanup`

A new domain must not be built as bespoke CRUD.

---

# Current strategic direction — Location first, then Genesis

The current Real World Darian/Thorne Estate/legacy Item world is explicitly prototype-era exemplar content. It is not a preservation constraint.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

Canonical Genesis plan:

`docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`

Decision record:

`docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`

The destructive reset is **not authorized yet**.

A rebuilt world requires represented space before Characters and Items can become runnable. Therefore the immediate feature family remains modern Sandbox Location Creation.

---

# Current authorized feature family — Location Creation

Canonical detailed implementation plan:

`docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`

Current refined schema authority:

- `docs/UNIVERSAL_LOCATION_SCHEMA_V2.md`;
- `src/observer_sandbox/location_creation_schema_v2.py`;
- `src/observer_sandbox/location_schema_registry_v2.py`;
- `src/observer_sandbox/sandbox_location_v2.py`;
- `docs/WORLD_LOCATION_NODE_MODEL.md`;
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`;
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`;
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

The v2 schema is an explicit successor to the retained v1 foundation, not a competing ontology.

---

# Location grading direction

Location grading reuses:

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived Location GradeProfile`

Retain `location-completeness-v1` as the mandatory representation-completeness dimension.

Evidence/reference-gated dimensions remain:

- completeness — mandatory;
- spatial scale — magnitude only, kind/reference aware;
- infrastructure/facility capability — registry evidence based;
- connectivity/mobility — graph evidence based and separate from access;
- asset value — economy/reference gated;
- security/protection — deferred until authoritative raw security evidence exists.

AI/Creator forms do not author grade letters, evaluator ids, thresholds or reference profiles.

No automatic overall Location grade without an explicit approved composite semantic.

---

# Location implementation slices

## ✅ L11.0 — Schema Refinement + Grading Contract

Closed. `location-v2` is locked with Geography, Boundary, typed interfaces, registry-backed functional/facility/resource/capability semantics, definition-vs-runtime state separation, minimal control/ownership and Location grading evidence contracts.

## ✅ L11.1 — Exact Validator + Registry/Grading Foundation

Closed. Exact v2 validation/canonicalization and registry foundations are executable; derived completeness grading remains non-authored and read-time derived.

## ✅ L11.2 — Sandbox Persistence + Graph Materializer

Closed. Validated v2 Locations materialize into isolated Sandbox persistence with stable IDs, same-Sandbox graph checks, acyclic structural hierarchy, typed graph projection, atomic materialization, no runtime activation and canonical isolation.

## ✅ L11.3 — Manual Full-Schema Creation

Closed through PR #380 / CI #1225.

Current Manual Location authoring provides:

- **Guided Build** from a sparse valid `location-v2` draft;
- all 13 supported sections: Identity, Structure, Geography, Spatial, Boundary, Access, Operations, Topology, Facilities, Environment, Control, Economics, Provenance;
- one-section-at-a-time replacement with whole-payload revalidation and revision increment;
- advanced Exact JSON path retained;
- write-free Preview and `.txt` export;
- Cancel/no materialization;
- revision-bound explicit approval into Sandbox;
- same validator/materializer as all other Location paths.

Invalid section updates leave the previous draft revision intact and create no Location rows.

## ▶ L11.4 — AI Full-Schema Creation — CURRENT NEXT SLICE

Existing foundation already supports natural-language AI Location proposals, v2 registry-aware prompting, exact validation, reroll, shared Preview/export/Approve, no AI-authored grades, no fake Sandbox refs and no runtime/canonical activation.

Remaining contract-completion work:

1. replace loose provider output schema `{type: object}` with a complete provider-facing structured `location-v2` fill schema aligned to authoritative registries;
2. add **at most one bounded deterministic repair attempt** for deterministic representation errors only;
3. add Telegram `typing` feedback during Location AI generation/reroll;
4. retain the exact same validator, draft revision, Preview/export/approval and L11.2 materializer boundaries;
5. prove invalid AI output cannot create draft/materialized state unless the bounded repair produces an exact valid payload.

Do not broaden this slice into nested composition or runtime activation.

## L11.5 — Nested Composition + Embedded Items

Support child Locations and exact Item-schema embedding with local refs, structural/storage/placement distinctions, whole dependency validation and one atomic success/rollback boundary. No generic `contents` bag.

## L11.6 — Detail/Browse + Edit Parity

Expose hierarchy/topology/facility/environment/economic facts and derived Location GradeProfile. Edit reuses exact schema/validator with stale guard, Preview/Apply/Done, audit and exact pause restoration where needed.

## L11.7 — Full Location Vertical Acceptance

Prove representative property/building and room/outdoor graphs, explicit topology, unknown geography without fabrication, boundary semantics, facilities/resources, grading, nested Locations, embedded Items, Manual/AI parity, atomic approval, failure/no-write behavior, Edit parity, Real World fingerprint stability and non-activation after approval.

Only after L11.7 closes does the Genesis transition begin.

---

# Recent UX parity addition

Approved Sandbox Characters now expose a read-only **Full Profile `.txt` export** from both Character detail and Profile menu.

The export reads the current approved Sandbox profile snapshot, including current edited profile values plus Skills, Preferences, Hobbies and Habits, while intentionally excluding live runtime-owned changing state. It reuses the existing Telegram text-document delivery path and does not mutate Sandbox or Real World state.

Closed through PR #379 / CI #1223.

---

# Completed foundation — retain

Completed reusable foundations include:

- universal Creation proposal/socket and isolated Sandbox lifecycle;
- Character Creation/Edit parity + approved full-profile text export;
- Item Single/Batch Creation/Edit parity;
- Universal Quantity/Measurement;
- Universal Grading Socket Architecture;
- Requirements/Access;
- Universal Item Schema and Item/container operations;
- Universal Location v1 foundation + explicit `location-v2` successor;
- Location v2 exact validator, registry and Sandbox materializer;
- human review + raw export;
- provider schema/canonicalizer/validator compatibility patterns;
- Sandbox clock/pause/readiness/AI binding;
- canonical isolation proofs.

Item representative post-rollback acceptance is explicitly approved and closed. Do not restart fine-grained Item realism gating without Creator authorization.

---

# After Location acceptance — Genesis transition

Sequence:

1. **G1 — Prototype Content Reset Audit & Contract**  
   Define exact keep/wipe sets and dependency-safe cleanup order.

2. **G2 — Remove legacy reseeding authority**  
   Remove/disable/generalize Darian/Thorne Estate/legacy Item bootstrap paths so restart/deploy cannot resurrect retired content.

3. **G3 — Controlled Real World content reset**  
   Retire prototype Characters, Locations, Items/fixtures/inventory and content-bound relations while preserving reusable infrastructure.

4. **G4 — Transmigration Foundation**  
   Use `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`: freeze Sandbox revision -> schema/dependency validation -> target-universe compatibility -> conflict/id resolution -> Creator preview -> explicit approval -> atomic canonical materialization -> provenance.

5. **G5 — Genesis Transmigration**  
   Dependency order: Locations/root topology -> Items/fixtures/containers + placement -> Characters + valid starting Location -> readiness/affordances -> explicit activation.

A Character cannot be activated without a valid represented Location.

Preserve reusable time/clock, weather/environment, economy/money, AI/provider, generic event/action/runtime, physiology/effects, Mind/Memory, grading/requirements/quantity/economic-value and Creation infrastructure.

---

# Future Reincarnation / Renewal

Reincarnation is for modern-to-modern canonical renewal, not for preserving prototype-era content:

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
- until the future reset is actually implemented and verified, current Real World prototype content still exists.

## Exact resume point

**Begin L11.4 contract completion. Keep the existing AI Location foundation, but replace its loose provider schema with the complete authoritative `location-v2` structured fill schema, add at most one bounded deterministic repair attempt, add Telegram typing feedback, and prove all AI outputs still converge on the same exact validator/draft/Preview/export/revision-bound approval/L11.2 materializer. Do not start L11.5 nested composition until L11.4 is green and merged.**
