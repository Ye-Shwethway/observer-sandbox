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

## Current checkpoint

Recent live acceptance exposed and closed several Item-side issues:

1. Legacy approved Item batches can fail current Item Edit preflight because old persisted payloads contain fields no longer accepted by current `item-v1`, specifically observed: `modules.physical.mass.kind`.
2. Character+Item batch delete was added; the Item list initially missed its delete control because an earlier Item extension captured a local `sw:list:item` callback and bypassed a later list wrapper. PR #354 fixed the actual callback-composition path and CI #1192 passed.
3. Fresh current-schema Item generation then exposed a presentation-only economics issue: Telegram draft review rendered canonical minor-unit integers directly, e.g. `Market value (minor units): 3000`, even though USD 3000 minor units means `$30.00`. This was data-correct but user-hostile.

### PR #356 — human-friendly Item draft value presentation

Merged to `main` at `4e27e2045c6fee198e97d7c0b95c9eee18789a30`.
CI **#1193**: **success** (targeted tests + CLI smoke).

Accepted display contract:
- Telegram Item draft review uses the established `format_money_minor()` formatter;
- standalone values render as human currency, e.g. `Market value: $30.00`, `Replacement value: $35.00`;
- consumable unit values render with basis, e.g. `Unit value: $1.50 / bar`;
- raw `minor units` jargon and redundant `Currency: USD` are removed from the Creator-facing detail view;
- economic labels are simplified to `Value type` and `Net worth`;
- `.txt` draft export remains the raw technical/canonical payload with `market_value_minor`, `replacement_value_minor`, `unit_value_minor`, etc. unchanged.

This is presentation-only; Item schema/economic semantics and persisted values are unchanged.

---

## Cleanup / Item Edit safety retained

Sandbox batch delete:
- Characters and Items only; Locations excluded;
- complete target validation before mutation;
- atomic deletion;
- dependent Sandbox rows cleaned by FK behavior;
- shared Item definitions retained while surviving instances reference them and removed only when orphaned;
- Sandbox delete events retained;
- `canonical_state_fingerprint()` checked; mismatch rolls back;
- Real World/canonical state untouched.

Item Edit:
- preflights current persisted payload before pause/session creation;
- bounded owner-facing error type/reason;
- rollback/restore on failed entry;
- strict current `item-v1` remains authoritative;
- do not weaken the validator merely to admit obsolete Sandbox test data.

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

Core semantic locks remain:
- Sandbox-created content stays isolated from Real World;
- nothing transmigrates automatically;
- `runtime_ready != running`;
- Item ownership is orthogonal to location/storage;
- strict current schemas remain authoritative;
- full Sandbox autonomous ticking remains unauthorized.

---

## Immediate acceptance sequence

Before resuming I5.11:
1. verify deployed checkpoint includes PR #356 or later;
2. confirm Item draft review now shows formatted currency rather than raw minor-unit integers;
3. use the fresh current-schema Item/Batch already generated after legacy cleanup;
4. approve/open a fresh Item -> `✏️ Edit Item`;
5. exercise representative field change -> Preview -> Apply/Save -> Done Editing;
6. verify Sandbox pause restoration and canonical state isolation.

Only after this fresh current-schema Item Edit/Save gate passes should development resume **I5.11 — Sandbox Location Creation + Embedded Contents**.

Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Full autonomous Sandbox ticking remains separately unauthorized.

---

## Exact resume sentence

**PR #356 is merged at `4e27e2045c6fee198e97d7c0b95c9eee18789a30` after CI #1193 passed. Telegram Item draft economics now render human-facing currency via the shared formatter (`$30.00`, `$35.00`, `$1.50 / bar`) while the `.txt` export deliberately preserves raw canonical `*_minor` fields. This is presentation-only. Verify the deployed preview, then continue the fresh current-schema Item Edit/Preview/Apply/Done live acceptance. Resume I5.11 only after that gate passes.**
