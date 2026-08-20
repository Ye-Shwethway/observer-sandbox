# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-20**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. task-relevant canonical contracts/source
6. current branch/PR/CI/runtime evidence before completion or live claims.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.

Workflow:
`test implementation -> focused verification -> PR/final CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> main/test exact sync`.

Do not infer production deployment or Telegram live acceptance from merge alone.

---

## Repository checkpoint

### Latest accepted repository slice

PR **#348 — Add Sandbox Item edit Telegram routing parity** merged to `main`.

Merge commit: `cee6337e9dc479988f2d3a4c78e52b70ef1b7b84`.

Final PR head before merge: `b980c52447d84bb072764e5f29cf99d8abd933d9`.

Acceptance evidence:
- CI **#1188** / run `32369393983`: **success**;
- selected affected scope: **68 test files**;
- targeted PR tests: **success**;
- CLI smoke init/status: **success**;
- Public Readiness Security Audit **#197** / run `32369394081`: **success**;
- PR mergeability confirmed before merge.

The concrete integration defects found during CI were fixed before acceptance:
1. world-layer installer API compatibility;
2. Item edit launcher aligned to actual `sandbox_object_view`;
3. launcher aligned to canonical `sw:iedit:enter:<object_id>` callback contract.

### Item Edit behavior now repository-accepted

- approved active Sandbox Item detail exposes `✏️ Edit Item`;
- `sw:iedit:*` callbacks route into the existing Item editor with configured Creator owner identity;
- pending field input consumes the next free-text Telegram message;
- slash commands remain on the normal command path;
- returned Item-editor keyboard survives the legacy polling text/keyboard split;
- field-by-field Preview/Apply;
- strict `item-v1` validation;
- stale-preview protection;
- immutable `definition.key` and `instance.mode`;
- existing `update_sandbox_item()` remains persistence authority;
- shared-definition / relation / cycle / physical-mode safeguards remain backend-authoritative;
- Sandbox-only pause/restore semantics; Real World remains untouched.

### Deployment boundary

`.github/workflows/deploy.yml` is configured to trigger on `main` pushes touching `src/**`, including PR #348's merge, when `VPS_DEPLOY_ENABLED == 'true'`.

At this synchronization point, **the merge-triggered deployment/runtime result has not yet been verified**. Repository acceptance is green; production/live Telegram acceptance remains a separate evidence claim until deploy/runtime evidence is checked.

---

## Backend foundation retained

I5.2 through I5.10 remain complete:
- I5.2 creation reuse map;
- I5.3 universal quantity/measurement;
- I5.4 cross-domain grading;
- I5.5 universal requirements/access;
- I5.6 Universal Item Schema v1;
- I5.7 single Sandbox Item materialization;
- I5.8 atomic heterogeneous Item Batch;
- I5.9 Item/container operations, including `update_sandbox_item()`;
- I5.10 Universal Location Schema v1.

---

## Core semantic locks

Creator AI:
`Creator intent -> complete canonical type schema/form -> AI fills form -> narrow explicitly-approved structural canonicalization -> deterministic validation -> preview -> explicit approval -> Sandbox-only materialization`.

Item ontology:
`Item Definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations:
- `contains` = structural/static containment;
- `located_at` = dynamic physical presence;
- `stored_in` = inventory/container storage;
- `owned_by` = ownership;
- `carried_by` = carriage;
- `equipped_by` = equipped state.

Do not infer ownership from location/storage. Do not use `contains` for ordinary movable inventory merely because it is inside a place.

**Created is not alive.** `runtime_ready != running`.

Creation Sandbox mutable state must not mutate canonical Real World entity/item/inventory/economic/runtime state. Keep `canonical_state_fingerprint()` as a high-value acceptance invariant.

Nothing transmigrates automatically. **Create anywhere safely; canon nowhere automatically.** **Schema-valid does not imply universe-compatible.**

I6 remains planning/validation only unless explicitly expanded. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed.

---

## Next implementation slice after deployment verification

Resume **I5.11 — Sandbox Location Creation + Embedded Contents**:
- strict I5.10 Location materialization;
- optional typed embedded Item contents via existing I5.6/I5.8 contracts;
- same-Sandbox active parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface destinations validate active same-Sandbox Locations;
- movable Items normally use `located_at`, or exact `stored_in` typed containers;
- whole graph validate-before-write;
- one atomic apply/rollback;
- no automatic runtime readiness, autonomous execution or canonical writes.

Then I5.12 contents operations -> I5.13 Character/Location binding/readiness -> I5.14 runtime affordance bridge -> I5.15 vertical acceptance.

Full autonomous Sandbox ticking remains separately unauthorized.

---

## Exact resume sentence

**PR #348 is merged at `cee6337e9dc479988f2d3a4c78e52b70ef1b7b84` after CI #1188 and Security Audit #197 passed. Sandbox Item Edit Telegram routing parity is repository-accepted. The deploy workflow is applicable to this `src/**` merge, but deployment/live Telegram evidence has not yet been verified at this checkpoint. First verify the merge-triggered deploy/runtime result, then finalize continuity and exact-sync `test` with `main`. Once that boundary is green, resume I5.11 Location Creation + Embedded Contents.**
