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

Live evidence confirmed two separate issues around Sandbox Item cleanup/edit acceptance:

1. Legacy approved Item batches can fail current Item Edit preflight because old persisted payloads contain fields no longer accepted by current `item-v1`, specifically observed: `modules.physical.mass.kind`.
2. Initial Character+Item batch-delete UI wiring exposed Character cleanup correctly, but the Item extension captured its own local `sw:list:item` callback and bypassed the later `sandbox_list_view` wrapper. This made Item delete controls absent in live Telegram even though direct wrapper tests passed.

Repository fixes now accepted:
- PR **#350** — live Item Edit failure hardening and bounded diagnostics;
- PR **#351** — atomic Sandbox Character+Item batch delete;
- PR **#353** — list-scoped delete controls for Character/Item lists;
- PR **#354** — fix Item-list callback composition so the real `sw:list:item` path is decorated even when an earlier extension bypasses the base list wrapper.

PR #354 merge commit: `0309ff4a0ba0ebeb814556acb58056e5b76fcf9f`.
CI **#1192**: **success**. The regression suite now explicitly reproduces the earlier Item-extension callback-capture/bypass pattern.

Expected live Item UX after deploy:
`📦 SANDBOX ITEMS -> 🗑 Select Items to Delete -> item-only checkbox selection -> Select All/Clear -> Review -> final Delete confirmation`.

Character list keeps its character-only equivalent. Sandbox World root keeps mixed Character+Item cleanup. Locations remain intentionally excluded from this cleanup slice.

---

## Cleanup safety contract

Sandbox batch delete:
- validates the complete selected active object set before mutation;
- supports Characters and Items only in this slice;
- deletes selected objects atomically;
- relies on Sandbox FK cleanup for dependent rows;
- preserves shared Item definitions while surviving instances reference them;
- removes touched Item definitions only when orphaned;
- records Sandbox delete events;
- checks `canonical_state_fingerprint()` and rolls back if canonical state changes;
- never mutates Real World/canonical state.

Legacy Item schema incompatibility must **not** be solved by weakening the current validator. Preferred acceptance sequence is cleanup -> fresh current-schema creation -> live Edit/Save proof.

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
1. verify deployed checkpoint includes PR #354 or later;
2. open `📦 Items` and confirm `🗑 Select Items to Delete` is visible;
3. delete legacy Items and test Character seeds as desired;
4. create fresh current-schema Item(s)/Batch through Creator Studio;
5. open fresh Item -> `✏️ Edit Item`;
6. exercise field change -> Preview -> Apply/Save -> Done Editing;
7. verify Sandbox pause restoration and canonical state isolation.

Only after this live cleanup + fresh Item Edit/Save gate passes should development resume **I5.11 — Sandbox Location Creation + Embedded Contents**.

Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Full autonomous Sandbox ticking remains separately unauthorized.

---

## Exact resume sentence

**PR #354 is merged at `0309ff4a0ba0ebeb814556acb58056e5b76fcf9f` after CI #1192 passed. The live Item-list missing-delete-control bug was caused by the Item extension's captured `sw:list:item` callback bypassing the later list wrapper; regression coverage now reproduces and closes that composition path. Verify the deployed Item list shows `🗑 Select Items to Delete`, clean up legacy Items/seed Characters, then create a fresh current-schema Item and prove live Edit/Preview/Apply/Done. Resume I5.11 only after that gate passes.**
