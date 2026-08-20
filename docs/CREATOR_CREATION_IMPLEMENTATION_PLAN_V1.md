# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — FRESH ITEM EDIT ACCEPTANCE ACTIVE**  
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

Merged commit: `b0083c6155006ba7103878056bceecc95413e4a3`; CI #1189 passed.

Item Edit preflights persisted Items before pause/session creation, restores pause/session state on entry-render failure, and surfaces bounded owner-facing error type/reason details. Live evidence identified obsolete approved batch data at `modules.physical.mass.kind`.

Policy: do not weaken current `item-v1` validation to admit obsolete Sandbox test data.

### PR #351 / #353 / #354 — Sandbox cleanup

- PR #351: atomic Character+Item Sandbox batch delete; CI #1190 passed.
- PR #353: scoped Character/Item cleanup controls.
- PR #354: fixed the real `sw:list:item` callback-composition path after live Telegram proved the Item list bypassed the later wrapper; CI #1192 passed.

Cleanup remains Sandbox-only, atomic, canonical-fingerprint guarded, and excludes Locations in this slice.

### PR #356 — Item draft review economics presentation

Merged commit: `4e27e2045c6fee198e97d7c0b95c9eee18789a30`.
CI **#1193** passed targeted regression + CLI smoke.

Fresh current-schema generation showed the valuation data was reasonable but the Telegram review exposed raw implementation units. Example: `market_value_minor = 3000` is USD `$30.00`, but the old view rendered `Market value (minor units): 3000`, which was easy to misread as `$3,000`.

Accepted UI contract:
- reuse existing `format_money_minor()` rather than duplicate currency conversion;
- standalone review: `Market value: $30.00`, `Replacement value: $35.00`;
- consumable review: e.g. `Unit value: $1.50 / bar`;
- use human labels such as `Value type` and `Net worth`;
- hide raw `minor units` and redundant `Currency: USD` from the Creator-facing Telegram detail;
- keep `.txt` export as raw canonical/technical JSON, including `market_value_minor`, `replacement_value_minor`, `unit_value_minor`, etc.

PR #356 is presentation-only. It does not modify Item schema, economic values, validation, persistence, or approval behavior.

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
- Sandbox Item field edit/save parity and safe entry diagnostics;
- atomic Character+Item Sandbox cleanup with correct live Item callback composition;
- human-friendly Item draft value presentation with raw technical export preserved.

---

## Universal Creator AI contract

`Creator intent -> complete canonical type schema/form -> AI fills form -> narrow explicitly-authorized canonicalization -> deterministic validation -> preview -> explicit approval -> Sandbox-only materialization`.

AI is not schema designer, validator bypass or direct mutation authority. Unknown nullable numeric facts remain null instead of fabricated precision.

Presentation rule: Creator-facing review should translate canonical representation into human-readable labels/units without changing underlying canonical values. Technical exports may expose canonical/raw field names for audit/debugging.

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

## Fresh current-schema Item -> live Edit/Save proof

Legacy cleanup is operational and a fresh current-schema Item batch has been created. The remaining gate is current-data Item Edit acceptance.

Required live sequence:
1. Confirm production checkpoint includes PR #356 or later.
2. Verify Item draft review presents money as formatted currency rather than raw minor-unit integers.
3. Approve/use a fresh current-schema Item from the recreated batch.
4. Open the fresh approved Item -> `✏️ Edit Item`.
5. Exercise field input, Preview, Apply/Save, and Done Editing.
6. Verify Sandbox pre-edit pause state restores correctly.
7. Verify Real World/canonical state remains unchanged.

Failure policy:
- surface exact error/reason;
- repair concrete current-schema/runtime defects;
- do not add broad legacy canonicalization or validator relaxation incidentally.

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
- regression tests cover actual extension/callback composition paths, not only direct wrappers;
- Creator-facing UI should be human-readable while raw technical exports preserve canonical representation where useful;
- PR CI is repository acceptance gate;
- full fallback only for cross-cutting/unmapped risk;
- deploy/live behavior verified separately from merge;
- continuity docs updated after material work and persistent branches exact-synced after acceptance.

---

## Exact resume point

**PR #356 merged at `4e27e2045c6fee198e97d7c0b95c9eee18789a30` after CI #1193 passed. Telegram Item draft economics now use shared human-friendly currency formatting while `.txt` export deliberately preserves raw canonical `*_minor` fields. Verify the deployed review presentation, then complete fresh current-schema Item Edit/Preview/Apply/Done acceptance. I5.11 follows only after that proof is green.**
