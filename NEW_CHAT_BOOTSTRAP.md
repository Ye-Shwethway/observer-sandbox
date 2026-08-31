# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-31**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`
6. task-relevant canonical contracts/source
7. current branch/PR/CI/runtime evidence before completion/live claims.

For Creator Creation work, `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` is mandatory.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.  
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.

Do not infer production deployment from merge alone.

---

# Current checkpoint

Immediate authorized feature family: **modern Sandbox Location Creation**.

Verified progression:

- ✅ L11.0 — `location-v2` schema refinement + grading contract
- ✅ L11.1 — exact validator + registry/grading foundation
- ✅ L11.2 — isolated Sandbox persistence + graph materializer
- ✅ L11.3 — Manual full-schema creation: Guided Build + Exact JSON + Preview/export/approval
- ✅ L11.4 — AI full-schema creation
- ▶ **L11.5 — Nested Composition + Embedded Items — CURRENT NEXT SLICE**
- L11.6 — Detail/Browse + Edit parity
- L11.7 — Full Location vertical acceptance

Recent verified checkpoints:

- PR #379 / CI #1223 — approved Sandbox Character Full Profile `.txt` export
- PR #380 / CI #1225 — Guided Manual Location Builder
- PR #382 / CI #1226 — complete Location AI full-schema creation
- PR #382 merge checkpoint: `7c9d6febb3668cfb32040b92788085eb73e28c30` before continuity-only follow-up

No deploy/live claim is implied by these merges.

---

# Current Location contracts

- `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`
- `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/UNIVERSAL_LOCATION_SCHEMA_V2.md`
- `docs/LOCATION_GRADING_EVIDENCE_MATRIX_V1.md`
- `src/observer_sandbox/location_creation_schema_v2.py`
- `src/observer_sandbox/location_schema_registry_v2.py`
- `src/observer_sandbox/location_ai_contract.py`
- `src/observer_sandbox/sandbox_location_v2.py`
- `docs/WORLD_LOCATION_NODE_MODEL.md`
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`

`location-v2` is an explicit successor to the retained v1 Location foundation, not a competing ontology.

---

# Closed Location foundation

## L11.0 — Schema / grading

`location-v2` includes:
- Geography;
- Boundary;
- typed interfaces;
- registry-backed functional/facility/resource/capability semantics;
- definition/configuration vs initial/live runtime-state separation;
- minimal control/ownership;
- Location grading evidence/profile contract.

Grades are derived. Creator/AI does not author final grade letters, thresholds, evaluator IDs or reference profiles.

## L11.1 — Exact validator

Exact v2 validation/canonicalization is executable. Unknown precision remains unknown. Completeness remains derived, not authored.

## L11.2 — Sandbox persistence/materializer

Validated Locations materialize only into Creation Sandbox state with stable IDs, same-Sandbox graph checks, acyclic hierarchy, explicit topology projection and atomic apply. Approval does not activate runtime and does not mutate canonical Real World state.

## L11.3 — Manual full-schema creation

Manual supports:
- Guided Build from sparse valid `location-v2`;
- 13 sections: Identity, Structure, Geography, Spatial, Boundary, Access, Operations, Topology, Facilities, Environment, Control, Economics, Provenance;
- one-section replacement + whole-payload revalidation + revision increments;
- advanced Exact JSON;
- write-free Preview + `.txt`;
- Cancel/no-write;
- revision-bound explicit approval via the same L11.2 materializer.

## L11.4 — AI full-schema creation

Closed through PR #382 / CI #1226.

AI Location now uses:
- short natural-language Creator intent;
- complete strict provider-facing `location-v2` structured schema rather than loose `{type: object}`;
- authoritative registry-backed nested shapes/enums;
- final deterministic `validate_location_payload_v2()` authority;
- at most one deterministic representation-only repair pass;
- repair may remove grade/derived metadata or normalize safe representation details, but may not invent missing facts, coordinates, topology, economic values or refs;
- semantic-invalid/missing required content => no draft/no materialization;
- reroll through the same schema/validator/revision model;
- best-effort Telegram `typing` feedback for generation/reroll; transport failure is non-authoritative;
- same Preview/export/approval/materializer as Manual;
- no runtime activation and zero canonical Real World mutation.

---

# Immediate resume — L11.5 Nested Composition + Embedded Items

Do not invent a generic `contents` bag or weaker embedded schemas.

First audit and reuse:

1. current Item Batch local-ref and atomic creation/materialization patterns;
2. current `sandbox_location_v2` parent/interface graph validation/materialization;
3. current Creation draft/Preview/export/revision-bound approval infrastructure.

Then define the **smallest explicit composition envelope** necessary to represent a useful Location graph.

Required semantics:

- child Locations use exact current `location-v2` member payloads;
- embedded Items use exact current Item payload / Batch semantics;
- local references are deterministic and resolve before writes;
- structural child relation = `contains`;
- movable Item placement normally = `located_at`;
- Item in a typed container = `stored_in`;
- ownership remains independent of placement/storage;
- topology destination may reference active same-Sandbox Locations or same-composition local Location refs;
- graph must reject structural cycles;
- cross-Sandbox refs fail closed;
- any invalid member/ref/dependency => **zero materialized writes**;
- whole composition gets one write-free Preview/export before approval;
- one explicit revision-bound approval applies the entire graph atomically;
- materialized members remain not runtime-active;
- `canonical_state_fingerprint()` remains unchanged.

Recommended first proof composition:

`Property/Building -> child Room -> one embedded movable Item`

Then add:

- sibling/child interface local-ref resolution;
- one Item stored in a valid typed container if the current Item contract cleanly supports it;
- failure/rollback proofs.

Do not expand into arbitrary world-generation breadth during this slice.

---

# Location grading lock

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived Location GradeProfile`

- completeness — mandatory;
- spatial scale — evidence/reference gated;
- infrastructure capability — evidence/reference gated;
- connectivity — graph-context gated;
- asset value — economy/reference gated;
- security — deferred;
- no automatic overall grade without explicit composite semantics;
- grades never become access authorization automatically.

---

# Recent Character export parity

Approved active Sandbox Characters expose **📄 Export Full Profile (.txt)** from Character detail and Profile menu.

Export reads current approved Sandbox profile persistence, including Creator-edited values, Skills, Preferences, Hobbies and Habits. Live runtime-owned changing state is intentionally excluded. Export is read-only and reuses shared Telegram text-document delivery.

---

# Approved Real World Genesis direction — later

Current Darian, Thorne Estate and legacy Item/fixture/inventory content are prototype-era exemplars, not preservation constraints.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

Destructive reset is **not authorized before L11.7**.

After Location acceptance:

`prototype keep/wipe audit -> remove legacy reseeding -> controlled Real World content reset -> preserve reusable systems -> Transmigration foundation -> Genesis Locations -> Items/fixtures -> Characters -> readiness/affordances -> explicit activation`

A Character cannot be activated without a valid represented Location.

---

# Future Reincarnation

`modern canonical v1 -> Renew in Sandbox -> edit/regenerate/test -> compatibility + diff -> explicit Creator approval -> canonical v2`

Do not build a complex legacy preservation bridge.

---

## Retained universal locks

- Create anywhere safely; canon nowhere automatically.
- No automatic transmigration.
- Target-universe compatibility precedes canonical promotion.
- `runtime_ready != running`; Created is not alive.
- Full autonomous Sandbox ticking remains separately unauthorized.
- Fine realism remains non-blocking unless explicitly authorized.
- Current Real World prototype content still exists until reset is actually implemented and verified.
- Do not make deploy/live claims without current evidence.

## Exact resume sentence

**Begin L11.5 by reading the current Item Batch local-ref/atomic creation implementation and `sandbox_location_v2` graph materializer. Build the smallest explicit composition envelope that contains exact `location-v2` child members and exact current Item members, resolves local parent/topology/placement/storage refs before writes, validates the complete dependency graph, previews/exports it write-free, and applies it in one revision-bound Sandbox-only transaction with zero writes on any failure. Do not introduce a generic contents bag, weaker duplicate schemas, runtime activation or canonical writes.**
