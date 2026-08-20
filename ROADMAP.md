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

Live acceptance work exposed two independent Item-side issues:

1. Older approved Item batches can fail current Item Edit because persisted legacy payloads contain obsolete fields such as `modules.physical.mass.kind`.
2. Initial batch-delete list wiring worked for Characters but not Items because the Item world-layer extension captured its own `sw:list:item` callback and therefore bypassed a later `base.sandbox_list_view` wrapper.

Accepted repository fixes:
- **PR #350** — Item Edit preflight/rollback and bounded failure diagnostics;
- **PR #351** — atomic Sandbox Character+Item batch delete;
- **PR #353** — scoped Character/Item list delete controls;
- **PR #354** — callback-boundary composition fix for the real `sw:list:item` path.

PR #354 merge commit: `0309ff4a0ba0ebeb814556acb58056e5b76fcf9f`.
CI **#1192** ✅ targeted tests + CLI smoke.

The #354 regression explicitly reproduces the extension-capture pattern where `sw:list:item` returns an earlier local Item-list closure without invoking the later base list wrapper. The batch-delete extension now decorates both list-view and callback boundaries.

Expected deployed UX:
- `📦 SANDBOX ITEMS -> 🗑 Select Items to Delete`;
- `👥 SANDBOX CHARACTERS -> 🗑 Select Characters to Delete`;
- Sandbox World root retains mixed Character+Item batch cleanup;
- Locations remain excluded from this cleanup slice.

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

Item Creator Studio/Telegram line includes current-schema Single/Batch creation, full-schema AI fill, validation diagnostics, review/export, realism/self-correction policy, approved Item details/economics, Item Edit parity, live Item Edit diagnostics, and Sandbox Character/Item cleanup.

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

## CURRENT ACCEPTANCE — cleanup legacy data and retest fresh Item Edit

Do **not** weaken current Item validation to accommodate obsolete test objects.

Required live sequence:
1. verify production checkpoint includes PR #354 or later;
2. open `📦 Items` and verify `🗑 Select Items to Delete` appears;
3. remove obsolete Sandbox Items and test Character seeds as desired;
4. create fresh current-schema Item(s)/Batch through Creator Studio;
5. open a fresh approved Item -> `✏️ Edit Item`;
6. edit representative fields -> Preview -> Apply -> Done Editing;
7. verify pre-edit Sandbox pause state restores;
8. verify Real World/canonical state unchanged.

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

## Exact resume point

**PR #354 is merged at `0309ff4a0ba0ebeb814556acb58056e5b76fcf9f` after CI #1192 passed. The missing Item delete control was a callback-composition bug: the Item extension's captured `sw:list:item` path bypassed the later list wrapper. The real callback path is now regression-covered and decorated. Verify live `📦 Items -> 🗑 Select Items to Delete`, clean legacy Sandbox test data, then create fresh current-schema Items and complete live Item Edit/Save acceptance. I5.11 begins only after that gate closes.**
