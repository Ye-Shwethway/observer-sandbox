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
6. current branch/PR/CI/runtime evidence before making completion or live claims.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.

Workflow:
`test implementation -> focused verification -> PR/final CI -> merge main -> runtime deploy only when applicable -> verify evidence -> continuity sync -> main/test exact sync`.

Do not infer production deployment or Telegram live acceptance from merge alone.

---

## Repository checkpoint — IMPORTANT

### Latest merged `main`

`main` = `2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b`

This is PR **#347 — Align Sandbox Item details and future economic values**.

PR #347 closed the approved-Item presentation/economic gap exposed by live Item Batch testing:
- approved Sandbox Item detail now uses human-facing inventory-style presentation;
- human target names are preferred over raw relation IDs;
- quantity, container/owner, nutrition, physical facts, container capacity and training data are surfaced;
- existing approved economically-immaterial Items are displayed as value-not-assigned without silent mutation;
- new ordinary purchasable goods receive conservative economic proposals by default;
- unique durable goods normally use standalone-asset economics;
- stackable consumables normally use consumable-stock/derived-stock economics;
- containment does not imply included-in-parent valuation.

No existing approved Item is silently revalued.

### Current `test` — UNMERGED WIP

`test` = `6e93c66bf627d90622f4ec4a599d7cb2c3bba886`

`test` is **3 commits ahead of `main`, 0 behind**.

The only `main..test` file changes are:
- `src/observer_sandbox/telegram_sandbox_item_edit.py` — new WIP Item edit session/editor;
- `src/observer_sandbox/telegram_world_layers_item_edit_extension.py` — new Item-detail Edit entry;
- `src/observer_sandbox/telegram_world_layers.py` — installs that extension.

These changes were started immediately before this continuity sync.

**They have NOT yet been tested, reviewed through PR CI, merged, deployed, or live-accepted. Do not claim otherwise.**

The intended Item edit behavior is:
- enter from an approved active Sandbox Item detail card;
- pause Sandbox runtime only, preserving/restoring its previous pause state;
- Real World remains untouched;
- edit through the existing strict Item payload/update contract;
- `definition.key` and `instance.mode` remain immutable after creation;
- represented definition/instance/economic/module/requirement/relation fields are exposed;
- complex values use exact JSON;
- every edit is deterministic-contract validated before Preview;
- Apply rechecks a stale-preview guard and calls existing `update_sandbox_item()`;
- editor remains open/paused until explicit Done Editing.

Next chat must inspect these WIP files before changing them. They may require corrections before tests.

---

## Merged Telegram Item vertical through PR #347

The old continuity checkpoint at PR #332 is stale. The following Creator Item Telegram work is already merged on `main`:

- **#334** Single Item Creator Studio UX: AI + Exact JSON -> strict Item validation -> preview/reroll/approve -> existing I5.7 materialization.
- **#335** Item Batch UX: AI + Exact JSON -> whole-graph preview -> atomic I5.8 approval.
- **#336** batch retry-context, diagnostics path and typing/prompt-cleanup fixes.
- **#337** locked universal Creator AI full-schema-fill invariant.
- **#338** safe detailed Telegram AI/provider diagnostics.
- **#339** deterministic non-stackable `modules.stack` fill-slot normalization.
- **#340** exact bare batch-local `stored_in` ref -> explicit `$ref` normalization; no fuzzy guessing.
- **#341** exact empty valuation-method normalization for the legacy explicit economically-immaterial AI fill case.
- **#342** detailed Item batch review + `.txt` export.
- **#343** preserve enhanced review actions after detail -> back navigation.
- **#344** shared ordinary-realism/plausibility gate across Single/Batch Item creation.
- **#345** one bounded AI self-correction regeneration after deterministic rejection; no code-side semantic repair.
- **#346** human-facing draft review wording + better export filenames.
- **#347** approved Item detail/economic presentation parity and better future economic proposals.

### Universal Creator AI invariant

`Creator intent -> complete canonical type schema/form -> AI fills form -> narrow structural canonicalization only where explicitly allowed -> deterministic type/graph validation -> preview -> explicit approval -> Sandbox-only materialization`.

AI is a form-filler/proposal generator, not schema designer or mutation authority.

For full-form Creator AI contracts:
- stable schema shape is passed to structured generation;
- unused arrays use `[]`;
- nullable unknown/unused slots use `null`;
- narrow canonicalizers may strip only schema-defined unused placeholders or exact structural aliases already locked by contract;
- canonicalizers may not infer missing facts, fuzzy-match targets, relax deterministic validators or silently resolve contradictions.

### Item realism / self-correction lock

Default Creation Sandbox Item generation targets ordinary real-world physics unless a future target-universe contract explicitly overrides it.

- unknown nullable numeric facts should remain `null` rather than fabricated precision;
- deterministic plausibility checks can reject cross-field impossibility such as a container capacity exceeding known external bounding volume;
- after the first AI candidate is rejected, the same full-schema model may receive the safe deterministic reason and regenerate **once**;
- second failure is surfaced; retry is bounded and does not grant AI mutation authority.

---

## Backend foundation already complete

I5.2 through I5.10 remain complete:
- I5.2 creation reuse map;
- I5.3 universal quantity/measurement;
- I5.4 cross-domain grading;
- I5.5 universal requirements/access;
- I5.6 Universal Item Schema v1;
- I5.7 single Sandbox Item materialization;
- I5.8 atomic heterogeneous Item Batch;
- I5.9 Item/container operations;
- I5.10 Universal Location Schema v1.

Backend `update_sandbox_item()` already exists and is the authority the new Telegram Item editor must reuse rather than duplicating persistence semantics.

---

## Core semantic locks

### Item ontology

`Item Definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

### Relations

- `contains` = structural/static spatial containment;
- `located_at` = current dynamic physical presence;
- `stored_in` = inventory/container storage;
- `owned_by` = ownership;
- `carried_by` = carriage;
- `equipped_by` = equipped state.

Do not infer ownership from location/storage. Do not use `contains` for ordinary movable inventory.

### Creation / runtime

**Created is not alive.**  
`runtime_ready != running`.

### Isolation

Creation Sandbox mutable state must not mutate canonical Real World entity/item/inventory/economic/runtime state. Keep `canonical_state_fingerprint()` as a high-value acceptance invariant.

### Transmigration

Nothing transmigrates automatically.  
**Create anywhere safely; canon nowhere automatically.**  
**Schema-valid does not imply universe-compatible.**

I6 remains planning/validation only unless explicitly expanded. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed.

---

## Exact next work — finish current Item Edit WIP first

Do **not** jump to I5.11 while `main..test` contains the unverified Item editor unless the Creator explicitly changes direction.

Resume the current WIP:

1. Inspect `telegram_sandbox_item_edit.py` and its routing integration for correctness against existing Real World/Sandbox profile-edit patterns.
2. Ensure Telegram callback and free-text routing actually reach the Item editor. The three current commits only add the editor and Item-detail button/extension; routing completeness must be verified rather than assumed.
3. Verify strict payload reconstruction from `get_sandbox_item()` matches `validate_item_payload()` / `update_sandbox_item()` expectations.
4. Verify edit semantics for:
   - name/description/kind/mobility/capabilities/tags where contract permits;
   - stack quantity/unit for stack instances;
   - economic values/policy;
   - module objects/leaves;
   - requirements;
   - `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by`.
5. Preserve immutable `definition.key` and `instance.mode`.
6. Preserve shared-definition protection already enforced by backend.
7. Preserve relation validation, physical-mode exclusivity and container-cycle prevention already enforced by backend.
8. Preserve Sandbox-only pause/restore and zero canonical mutation.
9. Add focused tests for entry, text routing, validation rejection, preview, stale preview, apply, pause restoration, relation edits, economic edit and canonical fingerprint.
10. Run appropriate focused verification; then PR to `main`; merge only on green evidence; then sync `test` to final `main`.
11. Only after merge/live usability evidence should continuity mark Item Edit accepted.

No PR exists for this WIP at the time of this document update.

---

## After Item Edit acceptance

Return to the architecture chain:

### I5.11 — Sandbox Location Creation + Embedded Contents

Materialize strict I5.10 Locations in isolated Sandbox state, optionally with typed embedded Item contents.

Requirements remain:
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`, not `located_at`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 Item contracts;
- movable Items normally use `located_at`, unless exact content graph says `stored_in` a typed container;
- validate complete Location + contents graph before writes;
- one atomic apply/rollback;
- no automatic runtime readiness;
- no canonical writes.

Then I5.12 contents operations -> I5.13 Character/Location binding/readiness -> I5.14 runtime affordance bridge -> I5.15 vertical acceptance.

Full autonomous Sandbox ticking remains separately unauthorized.

---

## Exact resume sentence

**Repository truth at handoff: `main` is `2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b` (merged PR #347). `test` is `6e93c66bf627d90622f4ec4a599d7cb2c3bba886`, exactly 3 commits ahead and contains an untested/unmerged Sandbox Item Edit WIP in `telegram_sandbox_item_edit.py`, `telegram_world_layers_item_edit_extension.py`, and `telegram_world_layers.py`. Do not claim Item Edit completion. First verify routing/integration, add focused tests, correct any defects, run PR CI, merge to main only on green evidence, then exact-sync test. The merged Item Creator Studio vertical already includes PRs #334–#347, including full-schema AI fill, safe diagnostics, batch ref/stack/economic canonicalization, detailed review/export, ordinary-realism validation, one bounded self-correction retry, human review wording and improved approved Item economic/detail presentation. After Item Edit acceptance, resume I5.11 Location Creation + Embedded Contents.**
