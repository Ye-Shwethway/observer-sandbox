# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — SANDBOX CLEANUP / FRESH ITEM RETEST ACTIVE**  
Date: 2026-08-20

## Objective

Build Creator Creation through bounded reusable contracts that create realistic Sandbox content without mutating canonical Real World state.

Core rules:
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- AI fills structured canonical forms; deterministic services validate and mutate.
- Real World and Creation Sandbox mutable state remain isolated.

---

## Current repository boundary

### PR #350 — Item Edit live-entry hardening

Merged commit: `b0083c6155006ba7103878056bceecc95413e4a3`.
CI #1189 passed.

Item Edit preflights persisted Items before pause/session creation, restores pause/session state on entry-render failure, and surfaces bounded owner-facing error type/reason details.

Live evidence identified obsolete approved batch data at `modules.physical.mass.kind`.

Policy: do not weaken current `item-v1` validation to admit obsolete Sandbox test data. Clean old test objects and retest fresh current-schema creation first.

### PR #351 — Sandbox Character + Item Batch Delete

Merged commit: `f9131857fcc861a5dc3b747595fc22352cd737ff`.
CI #1190 passed.

Backend cleanup contract:
- Character + Item targets only;
- active/same-Sandbox/type validation before mutation;
- one atomic delete operation;
- FK-dependent Sandbox rows cascade;
- touched Item definitions removed only when no surviving instance references them;
- Sandbox delete audit events retained;
- canonical fingerprint checked before transaction release; mismatch rolls deletion back;
- Locations deliberately outside this cleanup slice.

### PR #353 / #354 — Telegram cleanup list wiring

PR #353 added scoped delete controls to Character/Item list surfaces, but live Telegram proved only Characters showed the control.

Root cause: the Item world-layer extension had captured a local Item-list closure in `sw:list:item`. A later wrapper around `base.sandbox_list_view` therefore could not decorate the live Item callback path.

PR **#354** fixes the composition boundary by decorating `sw:list:item` and `sw:list:character` callback results as well as direct list-view calls.

PR #354 merge commit: `0309ff4a0ba0ebeb814556acb58056e5b76fcf9f`.
CI **#1192** passed targeted regression + CLI smoke.

The regression test explicitly reproduces the captured Item callback bypass that caused the live screenshot mismatch.

Expected live navigation:
- `📦 Items -> 🗑 Select Items to Delete`;
- `👥 Characters -> 🗑 Select Characters to Delete`;
- Sandbox World root -> mixed `🗑 Batch Delete`;
- scoped Select All never crosses type boundaries;
- Cancel returns to the originating list with cleanup action still present.

---

## Completed Creator foundation — do not rebuild

- I0 Creator authority hardening;
- I1 universal creation proposal/socket core;
- I2 isolated Creation Sandbox persistence/lifecycle;
- I2.5 Sandbox clock/speed/pause/readiness/AI binding;
- I3 Character + Location representation proof;
- I4 Creator Studio proposal lifecycle;
- I4.1 Sandbox Character configuration UX;
- I5/I5.1 Sandbox Observer foundations;
- Character Manual/AI parity;
- Sandbox Character profile/edit/grade-target parity;
- explicit Real/Sandbox runtime controls;
- I5.2 reuse map;
- I5.3 universal quantity/measurement;
- I5.4 cross-domain grading;
- I5.5 requirements/access;
- I5.6 Universal Item Schema v1;
- I5.7 single Sandbox Item materialization;
- I5.8 atomic heterogeneous Item Batch;
- I5.9 Item/container operations and `update_sandbox_item()`;
- I5.10 Universal Location Schema v1;
- Item Creator Studio Single/Batch UX and current full-schema AI fill;
- Item review/export, realism validation, bounded self-correction;
- approved Item detail/economic presentation;
- Sandbox Item field edit/save parity;
- safe Item Edit entry diagnostics/rollback;
- atomic Character+Item Sandbox cleanup;
- scoped Telegram cleanup controls including the real Item callback-composition path.

---

## Universal Creator AI contract

`Creator intent -> complete canonical type schema/form -> AI fills form -> narrow explicitly-authorized canonicalization -> deterministic validation -> preview -> explicit approval -> Sandbox-only materialization`.

AI is not schema designer, validator bypass or direct mutation authority. Unknown nullable numeric facts remain null instead of fabricated precision.

---

## Locked Item ontology

`Item Definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations:
- `contains` = structural/static containment;
- `located_at` = dynamic physical presence;
- `stored_in` = storage/container;
- `owned_by` = ownership;
- `carried_by` = carriage;
- `equipped_by` = equipped state.

Ownership does not follow from physical presence/storage. Sandbox-only mutable state must not mutate Real World state.

---

# CURRENT ACCEPTANCE SLICE

## Legacy cleanup -> fresh current-schema Item -> live Edit/Save proof

Required live sequence:
1. Confirm production checkpoint includes PR #354 or later.
2. Open `📦 Items` and verify `🗑 Select Items to Delete` is present.
3. Select/delete obsolete legacy Items; clean test Character seeds as desired from Characters or mixed root cleanup.
4. Verify selected objects disappear and Locations remain untouched.
5. Create fresh current-schema Item(s) or Item Batch through Creator Studio.
6. Open a fresh approved Item -> `✏️ Edit Item`.
7. Exercise field input, Preview, Apply/Save, and Done Editing.
8. Verify Sandbox pre-edit pause state restores correctly.
9. Verify Real World/canonical state remains unchanged.

Failure policy:
- surface exact error/reason;
- repair concrete current-schema/runtime defects;
- do not add broad legacy canonicalization or validator relaxation incidentally.

A dedicated legacy migration path may be designed later only if preserving old Sandbox content becomes valuable. Current Creator direction is cleanup and fresh recreation.

---

# NEXT AFTER FRESH ITEM EDIT ACCEPTANCE

## I5.11 — Sandbox Location Creation + Embedded Contents

Objective: materialize strict I5.10 Locations in isolated Sandbox state, optionally with typed Item contents, while reusing Item contracts rather than inventing a Location-only contents model.

Required semantics:
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 contracts/services/storage;
- movable Items normally use `located_at`, unless exact graph establishes `stored_in` a typed container;
- validate complete Location + contents graph before writes;
- atomic whole-graph success or zero partial graph;
- no automatic runtime readiness;
- no autonomous ticking;
- no canonical writes.

Then I5.12 Location Contents Operations -> I5.13 Character ↔ Location Binding & Runtime Readiness -> I5.14 Item/Location Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

---

## I6 / Character locks

Transmigration remains inactive/planning-only. Nothing transmigrates automatically. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Existing Character parity contracts stay locked.

---

## Test / release policy

- smallest relevant tests while iterating;
- regression tests must cover actual extension/callback composition paths, not only direct wrappers;
- PR CI as repository acceptance gate;
- full fallback only for cross-cutting/unmapped risk;
- deploy/live behavior verified separately from merge;
- continuity docs updated after material work and persistent branches exact-synced after acceptance.

---

## Exact resume point

**PR #354 merged at `0309ff4a0ba0ebeb814556acb58056e5b76fcf9f` after CI #1192 passed. The live Item cleanup control was missing because `sw:list:item` used an earlier captured local Item-list closure and bypassed the later list wrapper. Callback-boundary decoration plus an exact regression now closes that path. Verify deployed `📦 Items -> 🗑 Select Items to Delete`, clean obsolete Sandbox Items/seeds, create fresh current-schema Items, and complete live Item Edit/Save acceptance. I5.11 follows only after that proof is green.**
