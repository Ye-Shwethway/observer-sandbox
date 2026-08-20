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
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.
Do not infer production deployment or Telegram live acceptance from merge alone.

---

## Current checkpoint

Recent Item acceptance produced two useful live corrections.

### PR #356 — human-friendly draft value presentation

Merged at `4e27e2045c6fee198e97d7c0b95c9eee18789a30`; CI **#1193** passed.

Telegram Item draft detail now renders canonical money as human currency (`$30.00`, `$35.00`, `$1.50 / bar`) through the shared economy formatter. Raw `.txt` export intentionally keeps canonical `*_minor` fields for audit/debugging.

### PR #358 — fresh Item Edit quantity-normalization fix

Merged at `9c93739655fc6981a8c5bfd31a7c83a4cce16f62`; CI **#1194** passed targeted tests + CLI smoke.

Live evidence from a newly-created, newly-approved current-schema batch disproved the earlier assumption that `modules.physical.mass.kind` was merely obsolete legacy data.

Exact root cause:
- Item authoring input uses physical quantities shaped as `{value, unit}`;
- `validate_item_payload()` normalizes them through `PhysicalQuantity.as_dict()` into `{kind, value, unit}`;
- that normalized payload is persisted by current Item materialization;
- Item Edit reconstructs the persisted Item and re-runs `validate_item_payload()`;
- the validator previously accepted only `{value, unit}`, so it rejected its own normalized output with `unknown field(s): ['kind']`.

PR #358 makes this boundary idempotent in a bounded way:
- raw authoring `{value, unit}` remains valid;
- normalized `{kind, value, unit}` is also valid only when `kind` exactly matches the expected physical dimension;
- arbitrary extra quantity fields remain rejected;
- mismatched kinds remain rejected;
- regression explicitly covers `validate -> persisted normalized Item -> enter Item Edit`.

This is not broad legacy-schema relaxation. It is acceptance of the validator's own exact normalized representation.

---

## Retained safety / ontology locks

- Sandbox-created content stays isolated from Real World.
- Nothing transmigrates automatically.
- `runtime_ready != running`.
- Strict Item semantics remain authoritative.
- Ownership is orthogonal to location/storage.
- Item relations remain: `contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by` with their existing meanings.
- Item Edit preflights before pausing, restores previous pause state, previews before Apply, uses deterministic `update_sandbox_item()`, and must not mutate canonical Real World state.
- Sandbox Character+Item cleanup remains atomic/canonical-fingerprint guarded; Locations are still excluded from that cleanup slice.
- Full Sandbox autonomous ticking remains unauthorized.

I5.2 through I5.10 remain complete; do not rebuild them.

---

## Immediate live acceptance

Before I5.11:
1. verify deployed runtime includes PR #358 or later;
2. reopen one of the freshly-approved Items from the current batch;
3. enter `✏️ Edit Item` — the prior `modules.physical.mass.kind` failure should no longer occur;
4. edit a representative field -> Preview -> Apply -> Done Editing;
5. verify pre-edit Sandbox pause state is restored;
6. verify Real World/canonical state remains unchanged.

The current approved batch does **not** need to be deleted/recreated merely because it contains normalized `kind`; PR #358 is specifically designed to accept that exact persisted current representation.

After live Edit/Save passes, resume **I5.11 — Sandbox Location Creation + Embedded Contents**.

Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Full autonomous Sandbox ticking remains separately unauthorized.

---

## Exact resume sentence

**PR #358 merged at `9c93739655fc6981a8c5bfd31a7c83a4cce16f62` after CI #1194 passed. Fresh current-schema Item Edit failed because the Item validator persisted its own normalized physical quantity shape `{kind,value,unit}` but previously re-accepted only authoring shape `{value,unit}`. PR #358 makes that normalization boundary idempotent while still rejecting mismatched kinds and arbitrary extras. Verify deployment, reopen the already-approved fresh batch, complete Edit/Preview/Apply/Done, then begin I5.11.**
