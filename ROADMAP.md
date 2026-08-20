# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, live repo/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Real World and Creation Sandbox mutable state remain isolated.
- Reuse established semantics instead of cloning ontologies.
- `canonical_state_fingerprint()` remains a high-value zero-canonical-mutation invariant.

---

## Current repository checkpoint

Accepted recent Item-side fixes:
- **PR #350** — Item Edit preflight/rollback and bounded failure diagnostics;
- **PR #351** — atomic Sandbox Character+Item batch delete;
- **PR #353/#354** — scoped cleanup controls and real `sw:list:item` callback-composition fix;
- **PR #356** — human-friendly Item draft economic presentation.

PR #356 merge commit: `4e27e2045c6fee198e97d7c0b95c9eee18789a30`.
CI **#1193** ✅ targeted tests + CLI smoke.

### Item draft review presentation contract

Fresh current-schema batch data proved the economic values themselves were realistic; confusion came from exposing internal minor-unit integers directly in Telegram. For example, USD `market_value_minor = 3000` means `$30.00`, not `$3,000`.

Repository-accepted behavior now:
- reuse `telegram_economy.format_money_minor()` in Item draft detail;
- `Market value: $30.00` rather than `Market value (minor units): 3000`;
- `Replacement value: $35.00` rather than raw `3500`;
- consumables may show `Unit value: $1.50 / bar`;
- Creator-facing detail uses simpler `Value type` / `Net worth` labels and hides redundant USD/minor-unit implementation detail;
- technical `.txt` export remains raw canonical JSON with `*_minor` fields unchanged.

No Item schema, valuation data, economics semantics, persistence or validation was changed by PR #356.

---

## Completed Creator foundation

Retained complete:
- I5.2 Creation Contract Reuse Map;
- I5.3 Universal Quantity / Measurement;
- I5.4 Cross-Domain Grading;
- I5.5 Requirements / Access;
- I5.6 Universal Item Schema v1;
- I5.7 Single Sandbox Item materialization;
- I5.8 Atomic heterogeneous Item Batch;
- I5.9 Item / Container Operations;
- I5.10 Universal Location Schema v1.

Item Creator Studio/Telegram line includes current-schema Single/Batch creation, full-schema AI fill, validation diagnostics, human review + raw export, realism/self-correction policy, approved Item details/economics, Item Edit parity/diagnostics, and Sandbox Character/Item cleanup.

---

## Locked Item ontology

`Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations:
- `contains` structural/static containment;
- `located_at` dynamic physical presence;
- `stored_in` storage/container;
- `owned_by` ownership;
- `carried_by` carriage;
- `equipped_by` equipped state.

Ownership never follows automatically from location/storage.

---

## CURRENT ACCEPTANCE — fresh current-schema Item Edit

Legacy cleanup is now usable live and a fresh current-schema batch has been generated. Do **not** weaken current Item validation to accommodate obsolete test objects.

Required live sequence:
1. verify production checkpoint includes PR #356 or later;
2. verify Item draft value presentation uses formatted currency and no longer exposes raw minor-unit integers as user-facing prices;
3. approve/use a fresh current-schema Item from the recreated batch;
4. open it -> `✏️ Edit Item`;
5. edit representative fields -> Preview -> Apply -> Done Editing;
6. verify pre-edit Sandbox pause state restores;
7. verify Real World/canonical state unchanged.

If a fresh current-schema Item still fails, repair the concrete current-data/runtime issue and preserve strict current schemas.

---

## NEXT AFTER fresh Item Edit acceptance

### I5.11 — Sandbox Location Creation + Embedded Contents

Required semantics:
- strict I5.10 Location materialization;
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 contracts;
- ordinary movable Items use `located_at`, or exact `stored_in` typed containers;
- validate whole Location + contents graph before writes;
- one atomic apply/rollback;
- no automatic runtime readiness;
- no autonomous execution;
- no canonical writes.

Then I5.12 Location Contents Operations -> I5.13 Character/Location Binding & Runtime Readiness -> I5.14 Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

Full Sandbox autonomous ticking remains separately unauthorized.

---

## Transmigration / Character locks

Nothing transmigrates automatically. I6 stays planning/validation only unless Creator expands scope. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Existing Character Manual/AI parity and Sandbox profile/edit/grade-target behavior stay locked.

---

## Test / release policy

- smallest relevant tests while iterating;
- regression tests cover actual extension/callback composition paths where layering matters;
- Creator-facing previews should use human-readable presentation while technical exports may preserve canonical/raw representation;
- PR CI is the repository acceptance gate;
- deploy/live behavior is verified separately from merge;
- continuity docs are updated after material work and persistent branches exact-synced after acceptance.

---

## Exact resume point

**PR #356 is merged at `4e27e2045c6fee198e97d7c0b95c9eee18789a30`; CI #1193 is green. Item draft review now formats canonical minor-unit values as human currency using the shared formatter while raw `.txt` export remains canonical. Verify this presentation live, then complete fresh Item Edit/Preview/Apply/Done acceptance. I5.11 begins only after that gate closes.**
