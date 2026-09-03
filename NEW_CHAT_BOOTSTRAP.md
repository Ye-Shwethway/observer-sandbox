# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-09-03**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`
6. `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` for Creator Creation work
7. task-relevant canonical contracts/source
8. current branch/PR/CI/runtime evidence before completion/live claims.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.  
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.

Do not infer production deployment from merge alone.

---

# Current checkpoint

Immediate feature family: **modern Sandbox Location Creation**.

Verified progression:

- ✅ L11.0 — `location-v2` schema refinement + grading contract
- ✅ L11.1 — exact validator + registry/grading foundation
- ✅ L11.2 — isolated Sandbox persistence + graph materializer
- ✅ L11.3 — Manual full-schema creation
- ✅ L11.4 — AI full-schema creation
- ✅ L11.5 — Nested Composition + Embedded Items
- ▶ **L11.6 — Detail/Browse + Edit + Cleanup parity — IMPLEMENTED AND PRODUCTION DEPLOY GREEN; CREATOR TELEGRAM SMOKE REMAINS**
- L11.7 — Full Location vertical acceptance

Latest implementation chain:

- PR #397 — guarded Sandbox Location update service;
- PR #398 — Telegram Location Edit Preview/Apply/Done parity;
- PR #399 — complete human Location detail/readback;
- PR #400 — dependency-aware Sandbox Location cleanup.

PR #400 CI #1271 passed targeted regression plus CLI init/status smoke. Full-regression fallback was correctly skipped under path-aware CI selection.

Production deploy #385 for merge `8fa1655bd97421ea6b3e99f200ae316d2eb0ff4c` passed sync, install, cognition recovery, installed service entrypoint, runtime restart and runtime health. Failure diagnostics were not needed.

## L11.6 current truth

Approved Sandbox Location detail now exposes:

- readable identity, hierarchy/geography, physical quantities, boundary, access/control, environment, facilities/resources/capabilities, topology, economics and relationships;
- derived Location completeness GradeProfile presentation with no invented overall grade;
- `Edit Location` using exact `location-v2` source/validator;
- source-fingerprint stale protection;
- whole-payload preflight and same-Sandbox graph validation;
- Preview -> Apply -> Done;
- atomic projection rewrite and update audit evidence;
- no Sandbox time pause because approved Location runtime is not running yet;
- `Delete Location` with dependency-aware fail-closed review;
- active Character/Item relations, actor runtime placement and authoritative Location references block deletion;
- no cascading graph rewrite;
- safe delete requires a fresh source-fingerprint-bound review and explicit confirmation;
- blocked review arms no delete session; Cancel invalidates the armed session;
- deletion remains Sandbox-only and checks `canonical_state_fingerprint()` unchanged.

## Creator smoke before closing L11.6

On Telegram production:

1. `Sandbox World -> Locations -> <approved Location>`;
2. confirm readable detail and `✏️ Edit Location` + `🗑 Delete Location` actions;
3. edit a harmless field through Preview -> Apply -> Done and confirm detail readback;
4. open delete review on a Location with active dependencies and confirm deletion is blocked with readable reasons;
5. open delete review on an expendable unreferenced Location, Cancel once, reopen review, then explicitly confirm deletion;
6. confirm navigation remains healthy after delete.

Do not mark L11.6 fully closed until this Creator smoke passes.

---

# Current Location authority

- `docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`
- `docs/UNIVERSAL_LOCATION_SCHEMA_V2.md`
- `docs/LOCATION_GRADING_EVIDENCE_MATRIX_V1.md`
- `src/observer_sandbox/location_creation_schema_v2.py`
- `src/observer_sandbox/location_schema_registry_v2.py`
- `src/observer_sandbox/location_ai_contract.py`
- `src/observer_sandbox/sandbox_location_v2.py`
- `src/observer_sandbox/sandbox_location_composition.py`
- `src/observer_sandbox/sandbox_location_operations.py`
- `src/observer_sandbox/sandbox_location_cleanup.py`
- `src/observer_sandbox/telegram_sandbox_location_edit.py`
- `src/observer_sandbox/telegram_sandbox_location_cleanup.py`
- `docs/WORLD_LOCATION_NODE_MODEL.md`
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`

`location-v2` is the explicit successor to the retained v1 Location foundation, not a competing ontology.

---

# Next after L11.6 Creator smoke

Proceed to **L11.7 — Full Location Vertical Acceptance**.

Acceptance must cover at least:

- property/building and room/outdoor hierarchies;
- explicit topology/interfaces;
- access policy distinct from operating state;
- partial/unknown geography without fabrication;
- boundary semantics;
- facilities/resources/capabilities;
- derived grading where evidence exists;
- nested child Locations and embedded Items;
- Manual/AI parity;
- write-free Preview/export;
- atomic approval and rollback/no-write failures;
- Edit Preview/Apply/Done;
- dependency-safe cleanup;
- canonical Real World fingerprint stability;
- approved Locations remain not runtime-active.

Only after L11.7 closes does the approved Genesis transition begin.

---

# Approved later Genesis direction

Current Darian, Thorne Estate and legacy Item/fixture/inventory content are prototype-era exemplars, not preservation constraints.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

Destructive Real World reset remains unauthorized before L11.7.

Later sequence:

`prototype keep/wipe audit -> remove legacy reseeding -> controlled Real World content reset -> preserve reusable systems -> Transmigration foundation -> Genesis Locations -> Items/fixtures -> Characters -> readiness/affordances -> explicit activation`

A Character cannot be activated without a valid represented Location.

---

## Retained universal locks

- Create anywhere safely; canon nowhere automatically.
- No automatic transmigration.
- Schema-valid does not imply universe-compatible.
- Target-universe compatibility precedes canonical promotion.
- `runtime_ready != running`; Created is not alive.
- Full autonomous Sandbox ticking remains separately unauthorized.
- AI proposes facts; deterministic contracts validate/derive/mutate.
- Grades are derived; missing evidence/reference means ungraded, not invented precision.
- No automatic overall Location grade without explicit composite semantics.
- Current Real World prototype content still exists until reset is actually implemented and verified.
- Do not make deploy/live claims without current evidence.

## Exact resume sentence

**Production is green through PR #400 / deploy #385. Have the Creator smoke-test approved Location Detail -> Edit Preview/Apply/Done -> dependency-blocked Delete -> Cancel invalidation -> confirmed deletion of an expendable unreferenced Location. If that passes, mark L11.6 closed and begin L11.7 Full Location Vertical Acceptance.**
