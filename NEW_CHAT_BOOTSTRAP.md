# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-09-04**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` for Creator Creation work
6. task-relevant canonical plans/contracts/source
7. current branch/PR/CI/runtime evidence before completion/live claims.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.  
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.

Do not infer production deployment from merge alone.

---

# Current checkpoint

## ✅ Modern Sandbox Location Creation — FULL VERTICAL ACCEPTED

All Location slices are closed:

- ✅ L11.0 — `location-v2` schema refinement + grading contract
- ✅ L11.1 — exact validator + registry/grading foundation
- ✅ L11.2 — isolated Sandbox persistence + graph materializer
- ✅ L11.3 — Manual full-schema creation
- ✅ L11.4 — AI full-schema creation
- ✅ L11.5 — Nested Composition + Embedded Items
- ✅ L11.6 — Detail/Browse + Edit + Cleanup parity
- ✅ L11.7 — Full Location Vertical Acceptance

Final Location acceptance:
- `docs/LOCATION_VERTICAL_ACCEPTANCE_V1.md`
- PR #407
- CI #1282 final acceptance + CLI init/status smoke green
- merge `c3e8cbb556d0037c8310261398c19a0939bec09a`

Accepted Location boundaries remain:
- exact `location-v2` authority;
- nested Location + heterogeneous Item composition;
- Manual/AI parity;
- write-free Preview/export;
- revision-bound explicit approval;
- Creator-friendly field Edit;
- dependency-safe cleanup;
- canonical Real World isolation;
- approved Locations remain not runtime-active;
- no automatic transmigration.

---

# Genesis transition

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

Current Real World Darian/Thorne Estate/legacy Item content still exists. G1 did not delete it.

Canonical Genesis plan: `docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`  
G1 authority: `docs/GENESIS_G1_PROTOTYPE_CONTENT_RESET_AUDIT_V1.md`

## ✅ G1 — Prototype Content Reset Audit & Contract — CLOSED

G1 closure evidence:
- PR #409 — G1 reset audit contract + roadmap authority
- Public Readiness Security Audit #236 — green
- merge `0dab6ca980510a8ef1553dd7d34fa86c5a0bc047`
- docs/audit only; no canonical DB mutation and no runtime/seed code change

G1 locked explicit:
- **KEEP**
- **WIPE**
- **RESEED-AUTHORITY REMOVE / GENERALIZE**
- **DEPENDENCY / ORDER**
- **NO-TOUCH**
- **BACKUP / ROLLBACK**
- **POST-RESET verification**

Critical G1 findings:

- `runtime.status()` currently calls `_initialize_conn()`, so health/status can invoke prototype seeders;
- `seed_home_and_darian()` can recreate Darian + Thorne Estate after DB-only deletion;
- Estate campus/inventory, Darian economy, Estate media and several represented simulator seeders are prototype-bound startup surfaces;
- generic reusable Item/action/economy/media infrastructure must survive while exemplar materialization is removed/generalized;
- production Character seed files currently seed Darian only; Quasi/Elias must not be assumed to exist without live DB evidence;
- `world_observer_universe` remains the default KEEP root unless a separate explicit universe-identity migration is approved;
- exact G3 deletion rows require live production DB preflight;
- post-reset may legitimately contain zero canonical Characters;
- current `resolve_actor_id()` makes that state unhealthy for `status()`;
- therefore healthy zero-Character canonical runtime is a hard G2/G3 prerequisite.

G1 closure **does not authorize destructive reset**.

## ▶ NEXT — G2 Remove Legacy Reseeding Authority + Healthy Empty Canonical World

G2 is implementation work but must leave the existing canonical prototype rows intact.

Required work:

1. remove/generalize `seed_home_and_darian()` from ordinary initialization/status;
2. remove/generalize Estate campus bootstrap;
3. split generic Item-definition registration from Estate inventory materialization;
4. remove Darian-specific economy seed from ordinary bootstrap while preserving generic economy engine;
5. generalize/remove hard-coded Estate media bootstrap;
6. separate reusable technology/tactical/represented-skill contracts from Thorne Estate simulator fixture materialization;
7. retain generic seeders that create only reusable action vocabulary and no live exemplar fixture;
8. audit remaining content-bound memory/familiarity/value/bootstrap surfaces;
9. support healthy init/status with zero canonical Characters and no synthetic actor;
10. skip actor-specific recovery/progression/migration when no valid actor exists;
11. prove ordinary init/status/restart cannot recreate prototype content once it is absent in a controlled test fixture;
12. preserve Creation Sandbox and generic universe infrastructure.

G2 verification must include focused/path-aware tests, PR/CI, merge, deploy/runtime health and post-deploy verification.

Do **not** execute G3 destructive reset during G2.

## Later Genesis sequence

1. ✅ G1 — Prototype Content Reset Audit & Contract
2. ▶ G2 — Remove/generalize legacy reseeding + healthy empty canonical world
3. G3 — Controlled Real World content reset — explicit Creator authorization required
4. G4 — Transmigration Foundation
5. G5 — Genesis Transmigration: Locations -> Items/fixtures/containers -> Characters -> readiness/affordances -> explicit activation

A Character cannot be activated without a valid represented Location.

---

# Retained universal locks

- Create anywhere safely; canon nowhere automatically.
- No automatic transmigration.
- Schema-valid does not imply universe-compatible.
- Target-universe compatibility precedes canonical promotion.
- `runtime_ready != running`; Created is not alive.
- Full autonomous Sandbox ticking remains separately unauthorized.
- AI proposes facts; deterministic contracts validate/derive/mutate.
- Grades are derived; missing evidence/reference means ungraded.
- No automatic overall Location grade without explicit composite semantics.
- Creation Sandbox is NO-TOUCH for Genesis reset work.
- Current Real World prototype content remains until G3 is separately authorized and verified.
- G2 must remove resurrection/bootstrap authority without deleting current prototype content.
- Do not make deploy/live claims without current evidence.

## Exact resume sentence

**G1 is closed through PR #409 / Public Readiness Security Audit #236 / merge `0dab6ca980510a8ef1553dd7d34fa86c5a0bc047`. Begin G2 by removing/generalizing prototype reseed authority and supporting healthy zero-canonical-Character init/status, while leaving current Darian/Thorne Estate canonical prototype rows untouched until explicitly authorized G3.**
