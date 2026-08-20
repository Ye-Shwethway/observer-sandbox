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
`test implementation -> focused verification -> PR/final CI -> merge main -> runtime deploy only when applicable -> verify evidence -> continuity sync -> main/test exact sync`.

Do not infer production deployment or Telegram live acceptance from merge alone.

---

## Repository checkpoint

### Latest merged `main`

`main` = `2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b`

This is PR **#347 — Align Sandbox Item details and future economic values**.

Merged Item Telegram refinement line is #334–#347, including Single/Batch Item Creator Studio UX, full-schema AI fill, diagnostics, strict narrow canonicalization, detailed review/export, ordinary-realism validation, one bounded self-correction retry and approved Item economic/detail presentation.

### Current `test` / active PR

Sandbox Item Edit parity is now repo-mutated and under PR review.

Confirmed commits in the routing completion line include:
- `bee72400503e6021ccea3d24e1c4fb4776858e65` — free-text compatibility adapter added;
- `8689b8e0c1f394b5c050f01ac7ceceaa0b38f9eb` — adapter installed before Creator bot hook capture;
- `cfcda161f15737ca0db5528ee65b7e28a881db94` — `sw:iedit:*` callback routing installed;
- `3cb186c19b240ba87eba7b2a8cbaf1c8e9845418` — focused routing tests added;
- later continuity commits update current repo truth.

PR **#348 — Add Sandbox Item edit Telegram routing parity** is open from `test` to `main`.

Current implementation now has:
- Item detail `✏️ Edit Item` launcher;
- deterministic `sw:iedit:*` callback routing;
- active Item field free-text routing through the existing polling loop;
- slash commands preserved during field edit;
- field-by-field Preview/Apply;
- strict `item-v1` validation;
- stale-preview protection;
- `definition.key` and `instance.mode` immutable;
- existing `update_sandbox_item()` persistence authority reused;
- Sandbox-only runtime pause/restore semantics;
- focused callback/text/keyboard/delegation regression tests.

**Current evidence boundary:** repository mutation + PR creation are confirmed. CI, merge, deployment and live Telegram acceptance are not yet confirmed at this checkpoint. Do not claim them until current GitHub/runtime evidence says so.

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

### Creator AI

`Creator intent -> complete canonical type schema/form -> AI fills form -> narrow explicitly-approved structural canonicalization -> deterministic validation -> preview -> explicit approval -> Sandbox-only materialization`.

AI is proposal/form-fill, not schema designer, validator bypass or mutation authority.

### Item ontology

`Item Definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations:
- `contains` = structural/static containment;
- `located_at` = dynamic physical presence;
- `stored_in` = inventory/container storage;
- `owned_by` = ownership;
- `carried_by` = carriage;
- `equipped_by` = equipped state.

Do not infer ownership from location/storage. Do not use `contains` for ordinary movable inventory merely because it is inside a place.

### Creation / runtime

**Created is not alive.** `runtime_ready != running`.

### Isolation

Creation Sandbox mutable state must not mutate canonical Real World entity/item/inventory/economic/runtime state. Keep `canonical_state_fingerprint()` as a high-value acceptance invariant.

### Transmigration

Nothing transmigrates automatically. **Create anywhere safely; canon nowhere automatically.** **Schema-valid does not imply universe-compatible.**

I6 remains planning/validation only unless explicitly expanded. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed.

---

## Exact current work — finish PR #348

Do not jump to I5.11 until Item Edit acceptance closes unless the Creator explicitly redirects.

Next actions:
1. Inspect PR #348 Actions/CI for the current head.
2. Fix only concrete failures; do not redesign already-working Item contracts.
3. Ensure focused routing tests and affected Telegram/Item regression suites are green.
4. Preserve Item editor invariants: strict validation, stale-preview guard, backend shared-definition/relation/cycle/physical-mode safeguards, Sandbox pause restoration and zero canonical mutation.
5. Merge PR #348 only on green evidence.
6. If deploy workflow applies, verify deploy/runtime separately; do not infer live Telegram acceptance from merge.
7. Update `NEW_CHAT_BOOTSTRAP.md`, `ROADMAP.md`, and `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md` with final merge/deploy evidence.
8. Exact-sync `test` to final `main`.

---

## After Item Edit acceptance

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

**Repository truth at handoff: `main` remains `2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b` (PR #347). `test` contains the routed Sandbox Item Edit implementation and focused routing regression tests; PR #348 is open to `main`. The earlier missing `sw:iedit:*` callback wire and active field free-text wire have now been implemented repo-side. CI/merge/deploy/live acceptance remain evidence-gated. First inspect PR #348 Actions, repair only concrete failures, merge on green, verify deployment separately if applicable, update all continuity docs with final evidence, then exact-sync `test`. After acceptance, resume I5.11 Location Creation + Embedded Contents.**
