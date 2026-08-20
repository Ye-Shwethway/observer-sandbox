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

PR **#348 — Add Sandbox Item edit Telegram routing parity** is merged.

Merge commit: `cee6337e9dc479988f2d3a4c78e52b70ef1b7b84`.

Final acceptance head: `b980c52447d84bb072764e5f29cf99d8abd933d9`.

Acceptance evidence:
- CI #1188 (`32369393983`) ✅;
- 68 selected affected test files ✅;
- CLI init/status smoke ✅;
- Public Readiness Security Audit #197 (`32369394081`) ✅.

The accepted slice includes:
- strict `telegram_sandbox_item_edit.py` editor/session with Preview/Apply, stale guard, immutable `definition.key` / `instance.mode`, Sandbox pause/restore and `update_sandbox_item()` reuse;
- `telegram_world_layers_item_edit_extension.py` wrapping the actual `sandbox_object_view`, adding `✏️ Edit Item`, and routing canonical `sw:iedit:enter:<object_id>` / `sw:iedit:*` callbacks;
- `telegram_sandbox_item_edit_adapter.py` routing pending Item-field free text through the legacy polling contract while preserving slash commands and the returned editor keyboard;
- focused routing regression coverage.

Repository acceptance is complete. Deployment/live Telegram acceptance remains evidence-gated until the merge-triggered deploy/runtime result is verified.

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

## COMPLETED — Sandbox Item Edit Telegram parity

Repository acceptance: ✅ PR #348.

Behavior:
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

Deployment boundary:
- `.github/workflows/deploy.yml` applies to `main` `src/**` pushes when `VPS_DEPLOY_ENABLED == 'true'`;
- merge-triggered deployment/runtime evidence is not yet verified at this roadmap checkpoint;
- do not claim live Telegram acceptance until verified.

---

## NEXT — I5.11 Sandbox Location Creation + Embedded Contents

Start only after closing the deploy/runtime evidence check for PR #348.

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

**PR #348 is merged at `cee6337e9dc479988f2d3a4c78e52b70ef1b7b84`; CI #1188 and Security Audit #197 are green. Item Edit callback/free-text parity is repository-accepted. Verify the applicable merge-triggered deployment/runtime result next, then finish continuity/main-test exact sync. After that, begin I5.11 Location Creation + Embedded Contents.**
