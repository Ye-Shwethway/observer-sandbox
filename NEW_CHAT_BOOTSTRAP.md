# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-21**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md` for current Location work
6. task-relevant canonical contracts/source
7. current branch/PR/CI/runtime evidence before completion/live claims.

For any Creator Creation work, `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` is mandatory before material planning/coding/review/debugging.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.
Do not infer production deployment from merge alone.

---

# Current checkpoint

The representative post-rollback Item acceptance gate is explicitly approved and closed.

The immediate authorized work is **modern Sandbox Location Creation**, because Characters and Items cannot form a runnable rebuilt world without represented spatial structure, topology and placement.

Canonical current docs:

- `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/LOCATION_CREATION_KICKOFF_V1.md`
- `docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`
- `docs/WORLD_LOCATION_NODE_MODEL.md`
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`
- `docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`
- `docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`

---

# Immediate resume — L11.0 Schema Refinement + Grading Contract

Do **not** start Location UI/AI/materialization yet.

The existing `location-v1` schema/validator are the authoritative foundation, but Creator approved one refinement pass before implementation.

Do not create a competing second Location ontology. If the refined exact payload remains compatible, retain the existing version. If required/top-level/nested structure changes incompatibly, create an explicit successor such as `location-v2` rather than silently changing `location-v1` semantics.

Approved refinement scope:

1. optional Geography module;
2. explicit Boundary semantics;
3. richer registry-backed interface kinds;
4. registry-backed functional classes/facility/resource/capability vocabulary;
5. stable definition/configuration vs initial/live runtime-state separation;
6. minimal control/ownership semantics;
7. Location-specific universal grading evidence/profile.

L11.0 must lock the final exact schema, registry vocabulary, ownership/state map and grading evidence matrix before L11.1 begins.

---

# Location grading lock

Reuse:

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived Location GradeProfile`

Current `location-completeness-v1` remains the mandatory representation-completeness dimension.

Planned/evidence-gated dimensions:

- completeness — mandatory;
- spatial scale — magnitude only, kind/reference aware;
- infrastructure/facility capability — registry evidence based;
- connectivity/mobility — graph evidence based and separate from access;
- asset value — economy/reference gated;
- security/protection — deferred until authoritative raw security evidence exists.

Rules:

- AI/Creator does not author final grade letters/thresholds/evaluator ids/reference profiles;
- missing evidence/reference => ungraded dimension;
- no automatic overall Location grade without explicit composite semantics;
- Location grades never automatically grant access or satisfy Character requirements.

---

# Location slice sequence

- **L11.0** Schema Refinement + Grading Contract
- **L11.1** Exact Validator + Registry/Grading Foundation
- **L11.2** Sandbox Persistence + Graph Materializer
- **L11.3** Manual Full-Schema Creation
- **L11.4** AI Full-Schema Creation
- **L11.5** Nested Composition + Embedded Items
- **L11.6** Approved Detail/Browse + Edit Parity
- **L11.7** Full Location Vertical Acceptance

All later Location work follows the shared Creation pipeline:

`versioned schema -> registered socket -> Manual/AI same exact payload -> canonicalize -> strict validate -> graph/dependency validate -> write-free preview/export -> explicit Sandbox approval -> atomic materialization -> detail/browse -> Edit Preview/Apply/Done -> cleanup`

No automatic runtime activation or Real World mutation.

---

# Structural Location locks

- stable technical identity independent of display path/name;
- `contains` = structural hierarchy;
- `connected_to` / interfaces = traversable topology;
- `located_at` = dynamic physical presence;
- access authorization != topology != current operating state;
- one canonical structural parent in first implementation;
- structural hierarchy must be acyclic;
- parent/interface refs resolve only within valid same-Sandbox/dependency scope;
- unknown geometry/geography remains unknown;
- no arbitrary generic `contents` bag;
- nested child Locations reuse exact Location schema;
- embedded Items reuse exact Item member schema/Batch semantics;
- whole composition validates before one atomic apply;
- movable Items normally use `located_at`, or `stored_in` when a valid typed container exists;
- ownership remains independent.

---

# Approved Real World Genesis direction — later

Current Darian, Thorne Estate and legacy Item/fixture/inventory world are prototype-era exemplars, not preservation constraints.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

The destructive reset is **not authorized before L11.7 Location acceptance**.

After Location acceptance:

`prototype keep/wipe audit -> remove/disable legacy reseeding -> controlled Real World content reset -> preserve time/weather/economy/AI/runtime/schema foundations -> Transmigration foundation -> Genesis Locations -> Items/fixtures -> Characters -> readiness/affordances -> explicit activation`

A Character cannot be activated without a valid represented Location.

---

# Reincarnation / Renewal — future

Reincarnation is reserved for modern canonical content originally created through the modern Creation/Transmigration contracts:

`modern canonical v1 -> Renew in Sandbox -> edit/regenerate/test -> compatibility + diff -> explicit Creator approval -> canonical v2`

Do not build a complex legacy-upgrade bridge for current prototype content.

---

## Retained universal locks

- Create anywhere safely; canon nowhere automatically.
- Sandbox-created content never transmigrates automatically.
- Target-universe compatibility precedes transmigration.
- `runtime_ready != running`; Created is not alive.
- `canonical_state_fingerprint()` remains a core isolation proof.
- Full autonomous Sandbox ticking remains separately unauthorized.
- Fine-grained realism remains non-blocking by default unless an explicit domain contract + Creator authorization changes that.
- Until reset is actually implemented/verified, current Real World prototype content still exists; do not claim otherwise.
- Do not make deploy/live claims without current evidence.

## Exact resume sentence

**Begin L11.0 from `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`. Refine the existing Location schema foundation before UI/AI/materialization: lock optional Geography, Boundary, registry-backed interface/functional/facility/resource semantics, definition-vs-initial/live runtime ownership, minimal control/ownership and the Location GradeProfile/evidence matrix. Use an explicit successor schema version if exact payload compatibility breaks. Then proceed L11.1 through L11.7. Only after full Location acceptance begin the approved prototype Real World reset and Genesis transmigration transition.**
