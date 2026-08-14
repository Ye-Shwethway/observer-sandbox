# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-15

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical contracts/source files
5. current live production evidence before implementation decisions.

Current Creator instruction and newer repository/CI/deploy/live evidence override older chat memory.

## Development workflow

Default:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use production-copy validation for concrete stateful/migration risk. Never accelerate/mutate production merely to manufacture acceptance evidence. New architecture/control/security invariants update their canonical contract + ROADMAP + bootstrap in the same cycle.

## Current verified production checkpoint

Latest runtime deployment: **Deploy #185 `31829636147` SUCCESS**, Training Anatomy v1 PR #86 merge `e9f4920518c995765344052325c121e186f52489`.

Main CI #713 passed. Post-deploy read-only Runtime Read job `94862090792` verified:
- service active/healthy;
- schema v5;
- autonomy enabled/normal, paused false, retry null, speed 1.0x;
- sim `2025-05-05T12:20:00+00:00`;
- decision calls 391;
- current/pending action `shower` in the Master Bathroom;
- Gemini `gemini-3.1-flash-lite` primary and tested Groq `qwen/qwen3.6-27b` fallback preserved;
- Weight 215.0 lb and BF 9.0% remain live `simulated` `physiology_engine` fields;
- BC-3 remains live-activated from `2025-05-05T11:47:00+00:00`, all eleven measurements remain `simulated` under `body_progression_engine`, hips remains 39.0, and no fields are deferred.

No natural post-deploy resistance action had occurred by this readback, so live production had not yet emitted a Training Anatomy `movement_anatomy` event. Do not accelerate production merely to manufacture one; the feature is already covered by deterministic and disposable-production-copy acceptance.

A historical provider 413 on an 8,645-token request remains old evidence only; current retry is null.

## Universal invariants

Darian/Thorne Estate are production exemplars, never reusable-engine identity.

Inventory/eating:
`Universal definition -> concrete stack -> reachable action context -> structured quantity -> deterministic validation -> state transition + immutable evidence`

Cognition:
`deterministic state/context -> one model proposal -> authoritative validation -> deterministic mutation`

Body composition:
`complete bounded energy/nutrition evidence + current FM/FFM + resistance evidence + recovery + genetic envelope -> deterministic settlement -> coupled Weight/BF history + audit`

Body measurements:
`BC-2 settlement + regional resistance evidence + authored anatomy/genetic envelope -> bounded regional circumference settlement -> atomic profile history + event`

Training:
`concrete target -> reusable method -> optional selected reusable movement patterns -> effective load -> deterministic method/anatomy evidence -> domain progression engines`

## Deployed nutrition/body checkpoint

- Inventory Foundation v1 — PR #71 / Deploy #177.
- Inventory Operations v1 — PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — PR #74 / Deploy #179.
- Eating Behavior v1 — PR #76 / Deploy #180.
- Meal Choice Intelligence v1 — PR #77 / Deploy #181.
- BC-2 Body Composition — **COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #78 / Deploy #182.
- BC-3 Body Measurement — **COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #82 / Deploy #183; natural activation verified at `2025-05-05T11:47:00+00:00`.

Canonical body docs:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/BODY_COMPOSITION_PROGRESSION_V1.md`
- `docs/BODY_MEASUREMENT_PROGRESSION_V1.md`

Darian's complete measurement family includes `body.hips_in=39.0`; reusable schema includes `genetics.hips_max_in`, with Darian's authored envelope 41.0. These are character-specific canon, not universal ratios.

## Training Method Semantics v2

**COMPLETE / DEPLOYED** via PR #84 / Deploy #184.

Canonical: `docs/TRAINING_METHOD_SEMANTICS_V2.md`.

Contract:
- reusable method definitions are keyed by stable `method_id` and contain no actor/world-object identity;
- concrete targets bind separately to reusable methods;
- unknown/unbound targets fail closed;
- progression formulas remain domain-owned;
- persisted historical-compatible method evidence retains `source=training-method-semantics-v1`; new evidence adds `catalog_revision=training-method-semantics-v2`;
- no schema migration or extra model/Telegram call.

## Training Anatomy / Movement Semantics v1

**COMPLETE / DEPLOYED** via PR #86 / Deploy #185.

Canonical: `docs/TRAINING_ANATOMY_V1.md`.

Initial reusable movement catalog:
- squat;
- hinge;
- horizontal press;
- vertical press;
- row;
- curl;
- extension;
- calf raise;
- Olympic pull.

Contract:
- movement definitions own normalized regional loading only; no actor identity, concrete object identity, genetics, recovery, hypertrophy formulas or circumference mutation;
- resistance method definitions list the movement ids they support;
- cognition returns bounded `training_movements` only from the selected option's authored movement choices;
- server-side validation rejects invalid target/movement combinations;
- selected movement ids persist in existing `action_instances.conditions_json`, so no schema migration is required;
- completed training events add deterministic `movement_anatomy={movement_ids,regional_load,source}` when explicit movements exist;
- BC-3 prefers movement-level regional load for new events and falls back to proven method-level `method_region_weights` for historical/no-selection events;
- BC-2 remains method/channel based and unchanged;
- no extra model call.

Validation at final PR head `9234a948f91ec83ddc66fbd7430f038c9dcca741`:
- CI #712 SUCCESS;
- Body Measurement Progression Acceptance #14 SUCCESS;
- Minimum Training Stimulus Acceptance #17 SUCCESS;
- Eating Behavior Acceptance #17 SUCCESS;
- Nutrition & Energy Evidence Acceptance #15 SUCCESS.

The acceptance cycle also fixed stale BC-3 validation: disposable production copies may now begin either pre-activation or already live-activated. The validator checks both states without touching live production.

## Telegram Profile schema-driven UX debt

Canonical debt record: `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`.

Ordinary represented fields already render by schema/domain data, which is why `body.hips_in` surfaced without a Telegram-specific patch. Remaining debt is the fixed `PROFILE_SECTIONS` registry in `profile_observer.py`.

Target direction:
`domain/collection -> section id + label + icon + order + visibility + renderer kind`

Sensitivity remains authoritative; private/intimate fields must never auto-surface merely because they exist in schema. Complete this before broad Skill/Intellectual/Mental/Social profile expansion makes the fixed registry expensive to unwind.

## Public repository security checkpoint

`Ye-Shwethway/observer-sandbox` is PUBLIC. Public hardening is complete; manual UI verification remains for outside-contributor workflow approval, Secret scanning/Push protection, and `main` branch/ruleset protection where the GitHub App cannot fully read account-level settings.

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md`, `SECURITY.md`.

## Later sequence

1. **Regional Measurement Detraining** — region-specific disuse/decay reconciled with systemic BC-2 FFM loss to avoid double counting;
2. **Telegram Profile schema-driven section UX** before broad profile expansion;
3. skill progression family;
4. intellectual attributes;
5. mental/emotion dynamics;
6. later social/relationship/sexual physiology;
7. broad Mind/Behavior architecture only after enough real feature families justify it.

Post-public GitHub settings verification is opportunistic and does not block runtime development.

## Exact resume point

First re-read live production and current canonical repository. Training Anatomy v1 is deployed; a natural movement-aware production training event may or may not have occurred since the last readback.

The proposed next minimum-runnable runtime slice is **Regional Measurement Detraining**. It should add region-specific absence/disuse pressure to BC-3 while explicitly reconciling it with systemic BC-2 lean-mass loss so the same tissue loss is not counted twice.

Telegram schema-driven section UX remains required immediately after that slice unless the Creator gives a newer instruction.

Do not add economy/currency, automatic restocking, deep recipes/crafting, Character Memory, broad Mind/Behavior engines, or a second production character merely for testing as side effects.
