# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, live repo contracts/config/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate, derive and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Real World and Creation Sandbox mutable state remain isolated.
- Reuse established semantics through adapters instead of cloning ontologies.
- Grades are derived interpretation, not persisted competing truth.

---

## Current repository checkpoint

### Merged `main`

`main` = `2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b` — PR **#347, Align Sandbox Item details and future economic values**.

Merged Item Telegram/economic refinement line:
`#334 Single Item UX -> #335 Batch UX -> #336 retry/typing -> #337 full-schema AI fill -> #338 diagnostics -> #339 stack normalization -> #340 exact local stored_in ref -> #341 immaterial valuation placeholder -> #342 review/export -> #343 review-back -> #344 ordinary-realism gate -> #345 one bounded self-correction -> #346 human review/export naming -> #347 approved Item detail/economic parity`.

### Current `test` / PR #348

Sandbox Item Edit parity is now an **active PR**, not merely an unwired WIP.

Current implementation line includes:
- `telegram_sandbox_item_edit.py` — strict Item edit session, Preview/Apply, stale-preview guard, immutable `definition.key` / `instance.mode`, Sandbox pause/restore, existing `update_sandbox_item()` reuse;
- `telegram_world_layers_item_edit_extension.py` — `✏️ Edit Item` launcher **and `sw:iedit:*` callback routing**;
- `telegram_sandbox_item_edit_adapter.py` — active field free-text routing through the legacy polling contract while preserving slash commands;
- `telegram_creator_studio.py` — installs the free-text compatibility adapter before Creator bot hook capture;
- `tests/test_telegram_sandbox_item_edit_routing.py` — focused callback/text/keyboard/delegation regression coverage.

PR **#348 — Add Sandbox Item edit Telegram routing parity** is open from `test` to `main`.

At this synchronization point, repository mutation and PR creation are confirmed. **CI/merge/deploy/live acceptance are still pending evidence and must not be claimed yet.**

---

## Backend Creator Creation foundation

Completed and retained:
- **I5.2** Creation Contract Reuse Map.
- **I5.3** Universal Quantity / Measurement.
- **I5.4** Cross-Domain Grading.
- **I5.5** Requirements / Access.
- **I5.6** Universal Item Schema v1.
- **I5.7** Single Sandbox Item materialization.
- **I5.8** Atomic heterogeneous Item Batch.
- **I5.9** Item / Container Operations, including validated `update_sandbox_item()`.
- **I5.10** Universal Location Schema v1.

---

## Creator AI architecture lock

`Creator intent -> full canonical type form/schema -> structured AI fill -> narrow explicitly-defined canonicalization -> deterministic validation -> preview -> explicit approval -> Sandbox-only materialization`.

AI does not design schemas, repair arbitrary contradictions, weaken validators or directly mutate state.

Default Item generation remains ordinary real-world physics unless a future target-universe contract explicitly overrides it. Unknown nullable numeric facts remain null instead of false precision. One bounded AI regeneration is allowed after a deterministic rejection; a second failure is surfaced.

---

## Locked Item ontology

`Definition -> unique instance OR stack -> physical placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations:
- `contains` — structural/static containment;
- `located_at` — dynamic physical presence;
- `stored_in` — inventory/container storage;
- `owned_by` — ownership;
- `carried_by` — carriage;
- `equipped_by` — equipped state.

Ownership never follows automatically from location/storage. Ordinary movable inventory does not use structural `contains` merely because it is inside a place.

Sandbox isolation remains mandatory; keep `canonical_state_fingerprint()` as a high-value zero-canonical-mutation acceptance invariant.

---

## CURRENT — Sandbox Item Edit Telegram parity

PR: **#348**.

Target behavior now implemented repo-side:
- approved active Sandbox Item detail exposes `✏️ Edit Item`;
- `sw:iedit:*` callbacks enter/navigate the editor using the configured Creator owner identity;
- selected field value is consumed as the next free-text Telegram message;
- slash commands remain on the normal command path;
- Sandbox runtime alone auto-pauses and restores its previous pause state on exit;
- Real World stays untouched;
- current Item payload is reconstructed through the existing Item contract;
- `definition.key` and `instance.mode` remain immutable;
- definition, instance, economic policy, modules, requirements and relationships are editable where contract permits;
- complex values use exact JSON;
- candidate changes pass `validate_item_payload()` before Preview;
- Apply rejects stale previews and reuses `update_sandbox_item()`;
- backend shared-definition, relation, cycle and physical-placement safeguards remain authoritative.

Verification still required before merge:
- PR #348 Actions/CI green;
- focused routing tests pass in CI;
- wider affected Telegram/Item regression suite remains green;
- mergeability confirmed;
- after merge, exact-sync `test` to final `main`;
- deploy/live Telegram evidence only if the workflow actually deploys this slice.

Do not mark Item Edit accepted/live until those evidence gates close.

---

## NEXT AFTER Item Edit acceptance

### I5.11 — Sandbox Location Creation + Embedded Contents

Objective: materialize strict I5.10 Locations in isolated Sandbox state, optionally with typed Item contents, without creating a parallel Item model.

Required semantics:
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`, not `located_at`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 contracts/services/storage;
- movable Items normally use `located_at`, unless exact graph says `stored_in` a typed container;
- validate the complete Location + contents graph before writes;
- one atomic apply/rollback;
- no automatic runtime readiness;
- no autonomous execution;
- no canonical writes.

Then:
- **I5.12** Location Contents Operations;
- **I5.13** Character ↔ Location Binding & Runtime Readiness;
- **I5.14** Item / Location Runtime Affordance Bridge;
- **I5.15** Sandbox Vertical Acceptance.

Full Sandbox autonomous ticking remains separately unauthorized.

---

## Transmigration / Character locks

Nothing transmigrates automatically. I6 remains planning/validation only unless Creator expands scope.

Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Existing Character Manual/AI parity and Sandbox profile/edit/grade-target behavior must not be weakened by Item/Location work.

---

## Runtime / deploy evidence boundary

Repository mutation proves only repository mutation. PR/CI proves repository acceptance only. Merge does not itself prove deployment or live Telegram acceptance.

---

## Exact resume point

**`main` remains `2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b` (PR #347). `test` now contains the routed Sandbox Item Edit implementation and focused routing tests, with PR #348 open to `main`. Callback and free-text gaps have been repo-side wired. Next: inspect PR #348 Actions, fix only concrete failures, merge only on green evidence, then exact-sync `test` and update continuity with the final merge/deploy truth. After Item Edit acceptance, resume I5.11 Location Creation + Embedded Contents.**
