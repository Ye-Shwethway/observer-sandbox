# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-21**

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

A rebuilt world requires represented space before Characters and Items can become runnable. Therefore the immediate feature family is modern Sandbox Location Creation.

---

# Current authorized feature family — Location Creation

Canonical detailed implementation plan:

`docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`

Kickoff contract:

`docs/LOCATION_CREATION_KICKOFF_V1.md`

Existing foundation:

- `docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`;
- `src/observer_sandbox/location_creation_schema.py`;
- `docs/WORLD_LOCATION_NODE_MODEL.md`;
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`;
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`;
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

## Schema evolution rule

Do **not** create a competing second Location ontology.

The existing `location-v1` foundation must first be refined. If the exact payload can remain compatible, keep its version. If the approved refinement changes exact required/top-level/nested structure incompatibly, create an explicit successor version such as `location-v2` rather than silently changing `location-v1` semantics.

No Location UI/AI/materialization work begins until that refined exact versioned schema is locked.

## Approved refinement scope

1. optional Geography;
2. explicit Boundary semantics;
3. registry-backed interface kinds;
4. registry-backed functional classes/facility/resource/capability vocabulary;
5. stable definition/configuration vs initial/live runtime-state separation;
6. minimal control/ownership semantics;
7. Location-specific universal grading evidence/profile.

---

# Location grading direction

Location grading reuses:

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived Location GradeProfile`

Retain current `location-completeness-v1` as the mandatory representation-completeness dimension.

Planned/evidence-gated dimensions:

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

## L11.0 — Schema Refinement + Grading Contract

Lock the refined exact versioned payload, Geography/Boundary/Control modules, interface kinds, registry vocabulary, definition-vs-runtime ownership map, grading evidence matrix and GradeProfile contract. Validate at least property/building and room/outdoor-zone examples.

## L11.1 — Exact Validator + Registry/Grading Foundation

Implement exact validator/canonicalizer compatibility, registry-backed vocabulary, readback/revalidation safety, completeness grade retention and justified evidence-gated Location grading sockets.

## L11.2 — Sandbox Persistence + Graph Materializer

Register the Location Creation adapter; materialize isolated normalized Location state with stable IDs, same-Sandbox parent checks, acyclic hierarchy, topology/local-ref resolution and one atomic graph apply. No canonical writes; no runtime activation.

## L11.3 — Manual Full-Schema Creation

Complete Creator-facing Manual authoring, Preview, raw `.txt`, Cancel/no-write, explicit Sandbox approval and actionable diagnostics using the exact same validator/materializer.

## L11.4 — AI Full-Schema Creation

Complete provider-facing structured fill, strong Location system authoring contract, natural prompts, safe canonicalization, bounded repair, Telegram typing and the same Preview/export/Approve path as Manual.

## L11.5 — Nested Composition + Embedded Items

Support child Locations and exact Item-schema embedding with local refs, structural/storage/placement distinctions, whole dependency validation and one atomic success/rollback boundary. No generic `contents` bag.

## L11.6 — Detail/Browse + Edit Parity

Expose hierarchy/topology/facility/environment/economic facts and derived Location GradeProfile. Edit reuses exact schema/validator with stale guard, Preview/Apply/Done, audit and exact pause restoration where needed.

## L11.7 — Full Location Vertical Acceptance

Prove representative property/building and room/outdoor graphs, explicit topology, unknown geography without fabrication, boundary semantics, facilities/resources, grading, nested Locations, embedded Items, Manual/AI parity, atomic approval, failure/no-write behavior, Edit parity, Real World fingerprint stability and non-activation after approval.

Only after L11.7 closes does the Genesis transition begin.

---

# Completed foundation — retain

Completed reusable foundations include:

- universal Creation proposal/socket and isolated Sandbox lifecycle;
- Character Creation/Edit parity;
- Item Single/Batch Creation/Edit parity;
- Universal Quantity/Measurement;
- Universal Grading Socket Architecture;
- Requirements/Access;
- Universal Item Schema and Item/container operations;
- current Universal Location Schema v1 foundation;
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

**Begin L11.0 from `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`: refine the existing Location foundation and lock its exact versioned schema before any Location UI/AI/materialization. Add Geography, Boundary, registry-backed interface/functional/facility/resource semantics, definition-vs-runtime ownership, minimal control/ownership and the Location grading evidence/profile contract. Use an explicit successor schema version if the exact payload breaks compatibility. Then proceed L11.1 through L11.7. Only after full Location acceptance begin the approved prototype Real World reset and Genesis transmigration transition.**
