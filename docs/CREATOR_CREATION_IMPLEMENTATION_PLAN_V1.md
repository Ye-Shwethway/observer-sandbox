# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — LOCATION CREATION ACTIVE**  
Date: 2026-08-21

## Objective

Build Creator Creation as one reusable schema-driven pipeline that can safely author arbitrary universe elements in isolated Sandbox state and later promote compatible approved content through explicit transmigration.

Core rules:

- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- AI proposes/fills structured facts; deterministic contracts validate, derive and mutate.
- Real World and Creation Sandbox mutable state remain isolated.
- every substantial domain uses a versioned exact schema and registered Creation socket;
- grading is derived from authoritative evidence through registered grading sockets; AI never authors final grade authority.

Mandatory implementation standard:

`docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`

---

## Completed Creator foundation — do not rebuild

The following foundations are accepted and reusable:

- I0 Creator authority hardening;
- I1 universal creation proposal/socket core;
- I2 isolated Creation Sandbox persistence/lifecycle;
- I2.5 Sandbox clock/speed/pause/readiness/AI binding;
- I3 Character + Location early representation proof;
- I4 Creator Studio proposal lifecycle;
- Character Manual/AI creation, review, approval, detail, Edit and grading parity;
- I5/I5.1 Sandbox observer foundations;
- I5.2 Creation Contract Reuse Map;
- I5.3 Universal Quantity / Measurement;
- I5.4 Cross-Domain Grading foundation;
- I5.5 Requirements / Access;
- I5.6 Universal Item Schema v1;
- I5.7 Single Sandbox Item materialization;
- I5.8 atomic heterogeneous Item Batch;
- I5.9 Item/container operations;
- I5.10 Universal Location Schema v1 foundation;
- Item Creator Studio Single/Batch Manual+AI flows;
- Item approved detail, Edit Preview/Apply/Done, pause restoration and cleanup;
- Universal Grading Socket Architecture v1;
- broad Item metric/grading coverage foundation;
- shared schema/canonicalizer/validator compatibility patterns;
- human review + raw `.txt` export;
- bounded AI repair/diagnostics;
- explicit atomic Sandbox approval and canonical isolation proofs.

Item representative post-rollback acceptance is explicitly approved and closed. Do not restart Item realism micro-gating unless Creator authorizes it.

Locked Item ontology:

`Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations remain distinct:

`contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by`.

---

# CURRENT FEATURE FAMILY — Modern Sandbox Location Creation

Canonical detailed plan:

`docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`

Kickoff contract:

`docs/LOCATION_CREATION_KICKOFF_V1.md`

Existing Location foundation:

- `docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`;
- `src/observer_sandbox/location_creation_schema.py`;
- `docs/WORLD_LOCATION_NODE_MODEL.md`;
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`;
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`.

The current Location foundation must be refined before UI/AI/materialization. Do not create a competing second ontology. If the exact payload changes incompatibly, use explicit versioned schema evolution rather than silently changing the meaning of `location-v1`.

Creator-approved refinement scope:

1. optional Geography module;
2. explicit Boundary module;
3. richer registry-backed interface kinds;
4. registry-backed functional/facility/resource/capability classifications;
5. stable definition/configuration vs initial/live runtime-state separation;
6. minimal control/ownership semantics;
7. Location-specific universal grading evidence/profile.

---

## Location grading direction

Reuse:

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived Location GradeProfile`

Retain current `location-completeness-v1` as the mandatory representation-completeness grade.

Planned/evidence-gated Location dimensions:

- completeness — mandatory;
- spatial scale — magnitude only, kind/reference aware;
- infrastructure/facility capability — registry evidence based;
- connectivity/mobility — graph evidence based, separate from access;
- asset value — economy/reference gated;
- security/protection — deferred until authoritative raw security evidence exists.

No authored grade fields. No automatic overall Location grade without an explicit composite semantic.

---

## Location implementation slices

### L11.0 — Schema Refinement + Grading Contract

Lock exact refined versioned payload, registry/enums, definition/runtime ownership map, Geography/Boundary/Control modules, interface improvements and Location Grading Evidence Matrix. Prove property/building and room/outdoor-zone examples before implementation proceeds.

### L11.1 — Exact Validator + Registry/Grading Foundation

Implement exact validator/canonicalizer compatibility, registry-backed vocabulary, revalidation/readback safety, completeness grading and justified Location grading sockets with fail-closed evidence/reference behavior.

### L11.2 — Sandbox Persistence + Graph Materializer

Register the Location Creation socket/adapter; materialize isolated normalized Location state with stable IDs, same-Sandbox parent validation, acyclicity, interface/local-ref resolution and one atomic graph apply. No canonical writes and no runtime activation.

### L11.3 — Manual Full-Schema Creation

Implement complete Creator-facing Manual authoring, write-free Preview, raw `.txt`, Cancel/no-write, explicit approval and actionable diagnostics using the exact same validator/materializer.

### L11.4 — AI Full-Schema Creation

Implement complete provider-facing structured fill, strong system-side Location authoring contract, natural Creator prompts, bounded repair, Telegram typing and the same Preview/export/Approve path as Manual. AI does not author grades or runtime state authority.

### L11.5 — Nested Composition + Embedded Items

Support child Location composition and exact Item-schema embedding with batch-local refs, structural/storage/placement distinctions, whole dependency validation and one atomic success/rollback boundary. No generic `contents` bag.

### L11.6 — Approved Detail/Browse + Edit Parity

Expose human-readable hierarchy/topology/facility/environment/economic data and derived Location GradeProfile. Implement Edit through the same exact schema/validator with stale guard, Preview/Apply/Done, audit and exact pause restoration where pausing is actually needed.

### L11.7 — Full Location Vertical Acceptance

Prove representative property/building and room/outdoor graphs, explicit interfaces, partial unknown geography, boundary semantics, facilities/resources, grading, nested Locations, embedded Items, Manual/AI parity, atomic approval, failure/no-write behavior, Edit parity, `canonical_state_fingerprint()` isolation and non-activation after creation.

---

# AFTER L11.7 — Genesis transition

Do not automatically continue ordinary feature expansion after Location acceptance.

Approved next architecture:

`docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`

Decision record:

`docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`

Sequence:

1. audit exact prototype Real World keep/wipe dependency set;
2. remove/disable/generalize legacy Darian/Thorne Estate/legacy Item reseeding authority;
3. perform controlled prototype-content reset while preserving reusable time/weather/economy/AI/runtime/schema foundations;
4. implement Transmigration foundation against the clean Real World;
5. Genesis transmigrate Locations/root topology first;
6. transmigrate Items/fixtures/containers and placement;
7. transmigrate Characters with valid starting Location bindings;
8. validate readiness/affordances;
9. explicitly activate runtime.

The destructive reset is not authorized before Location acceptance.

---

## Future Reincarnation / Renewal

Reincarnation is reserved for modern canonical content that already originates from the modern Creation/Transmigration contracts:

`canonical v1 -> Renew in Sandbox -> edit/regenerate/test -> compatibility + diff -> explicit Creator approval -> canonical v2`

Do not build a complex legacy-reincarnation bridge for the current prototype Darian/Estate/legacy Item content.

---

## Retained locks

- no automatic transmigration;
- target-universe compatibility before canonical promotion;
- `runtime_ready != running`;
- `canonical_state_fingerprint()` remains a core isolation proof;
- full autonomous Sandbox ticking remains separately unauthorized;
- grading describes explicit dimensions and never silently becomes access/requirements authority;
- missing grading evidence/reference means ungraded, not invented precision;
- fine-grained realism remains non-blocking by default unless a domain contract + Creator authorization says otherwise.

## Exact resume point

**Start with L11.0 Schema Refinement + Grading Contract from `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`. Refine the existing Location ontology rather than creating a competing one; make an explicit successor schema version if the exact payload breaks compatibility. Lock Geography, Boundary, interface kinds, registry-backed functional/facility/resource semantics, definition-vs-runtime ownership, minimal control/ownership and the Location GradeProfile/evidence matrix before any Location UI/AI/materialization work. Then proceed L11.1 through L11.7. Only after full Location acceptance begin the separately approved Real World prototype reset and Genesis transmigration transition.**
