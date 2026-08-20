# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-20**

## Startup / authority

Read in order: `AGENTS.md` -> this file -> `ROADMAP.md` -> `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md` -> task-relevant source/contracts -> current branch/PR/CI/runtime evidence.

Authority: `current Creator instruction > live repo contracts/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only. Normal flow: `test -> focused verification -> PR/CI -> main -> deploy/runtime verification when applicable -> continuity sync -> main/test exact sync`.

Do not infer live Telegram acceptance from repository merge alone.

---

## Current repository checkpoint

### PR #350 — live Item Edit entry hardening

Merged commit: `b0083c6155006ba7103878056bceecc95413e4a3`.

CI **#1189** passed targeted tests + CLI smoke.

Live Creator evidence exposed a real legacy-data incompatibility:
`modules.physical.mass has unknown field(s): ['kind']`.

This came from an older approved Item batch whose persisted payload predates the current strict `item-v1` shape. Item Edit now:
- preflights the current payload before pausing Sandbox runtime;
- rolls back session/runtime state if editor entry fails;
- surfaces bounded `Error` + `Reason` diagnostics instead of only `Observer action failed safely`;
- preserves zero Item mutation / zero canonical mutation on failure.

### PR #351 — Sandbox Character + Item Batch Delete

Merged commit: `f9131857fcc861a5dc3b747595fc22352cd737ff`.

CI **#1190** passed targeted regression + CLI smoke.

Repository-accepted behavior:
- Sandbox World exposes `🗑 Batch Delete` when active Characters or Items exist;
- mixed Character + Item selection in one cleanup session;
- per-object toggles plus `Select All` / `Clear`;
- explicit review + final confirmation before mutation;
- Locations intentionally excluded from this cleanup slice;
- all selected targets revalidated as active, same-Sandbox Character/Item objects;
- one atomic delete transaction;
- dependent Sandbox rows cascade through existing FKs;
- touched Item definitions are deleted only if no surviving Item instance still references them;
- canonical state fingerprint is checked inside the transaction and any mismatch rolls the operation back;
- delete audit events remain in Sandbox history;
- Real World/canonical state remains untouched.

Current `main` after PR #351: `f9131857fcc861a5dc3b747595fc22352cd737ff`.

---

## Core semantic locks

- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Sandbox mutable state never mutates canonical Real World state.
- AI fills canonical structured forms; deterministic contracts validate and mutate.
- Item ontology: `Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.
- Relations: `contains` structural; `located_at` physical presence; `stored_in` storage; `owned_by` ownership; `carried_by` carriage; `equipped_by` equipped state.
- Ownership is never inferred from location/storage.
- Existing Character Manual/AI parity and Sandbox Profile/Edit/grade-target behavior must not be weakened.
- Nothing transmigrates automatically; I6 remains planning/validation only.
- Adrian Vale remains Sandbox-only; second Real World Character gate remains closed.

Backend foundation I5.2–I5.10 remains complete, including Universal Item Schema v1, Item Batch, Item operations, and Universal Location Schema v1.

---

## Exact next acceptance sequence

Do **not** jump directly to I5.11 yet.

1. Verify PR #351 deployment/runtime reaches Telegram.
2. In Sandbox World, use `🗑 Batch Delete` to remove the old Character seeds and legacy pre-current-schema Items selected by Creator.
3. Create a **fresh Item / Item Batch** through the current Creator Studio schema.
4. Open an approved fresh Item and re-run `✏️ Edit Item` end-to-end: entry -> field edit -> preview -> apply/save -> done/restore runtime state.
5. Confirm canonical fingerprint/Real World remains unchanged.
6. If fresh current-schema Item Edit passes live, close Item cleanup/edit acceptance.
7. Then resume **I5.11 — Sandbox Location Creation + Embedded Contents**.

Full autonomous Sandbox ticking remains separately unauthorized.

---

## Exact resume sentence

**Repository truth: PR #350 merged at `b0083c6155006ba7103878056bceecc95413e4a3` and made Item Edit entry diagnostics/rollback safe. Live evidence then proved the failing Item was legacy-schema data (`modules.physical.mass.kind`). PR #351 merged at `f9131857fcc861a5dc3b747595fc22352cd737ff` after CI #1190 passed, adding atomic mixed Character+Item Sandbox batch delete with explicit confirmation and canonical fingerprint protection. Next: verify deployment, delete the selected legacy Sandbox seeds/items, create fresh current-schema Items, and re-run live Item Edit acceptance. Only after that passes should I5.11 Location Creation + Embedded Contents resume.**
