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

Use production-copy validation for concrete stateful/migration risk. Never accelerate/mutate production merely to manufacture acceptance evidence.

Any new architecture/control/security invariant updates its canonical contract + ROADMAP + bootstrap in the same development cycle.

## Current verified production checkpoint

Latest runtime deployment: **Deploy #184 `31828453356` SUCCESS**, PR #84 merge `5c7d1524d7d4e66a9b4c92c8232a3a371113391d`.

Main CI #708 also passed after merge. A post-deploy read-only Runtime Read #12 rerun (`read-runtime` job `94858499326`) verified:
- service active/healthy;
- schema v5;
- autonomy enabled/normal, paused false, retry null, speed 1.0x;
- sim `2025-05-05T12:00:00+00:00`;
- decision calls 389;
- pending action `idle` in Darian's Master Suite;
- Gemini `gemini-3.1-flash-lite` primary and Groq `qwen/qwen3.6-27b` tested fallback preserved;
- Weight 215.0 lb and BF 9.0% remain live `simulated` `physiology_engine` fields;
- BC-2 activation boundary remains `2025-05-05T07:55:00+00:00`, numerical composition unchanged at activation;
- BC-3 naturally activated at `2025-05-05T11:47:00+00:00` with `status=bootstrapped`, `stat_mutated=false`, `deferred_fields=[]`;
- all eleven circumference fields are now live `simulated` `body_progression_engine` fields, including `body.hips_in=39.0`.

A historical provider 413 occurred on an 8,645-token cognition request. It is not current retry state; cognition enrichment stays compact.

## Universal invariants

Darian/Thorne Estate are production exemplars, never reusable-engine identity.

Inventory/eating:
`Universal food definition -> concrete stack -> reachable eating context -> structured quantity -> deterministic validation -> atomic stock transition + immutable evidence`

Cognition:
`deterministic state/context -> one model proposal -> authoritative validation -> deterministic mutation`

Body composition:
`complete bounded energy/nutrition evidence + current FM/FFM + resistance evidence + recovery + genetic envelope -> deterministic settlement -> coupled Weight/BF history + audit`

Body measurements:
`BC-2 body-composition settlement + regional resistance evidence + authored anatomy/genetic envelope -> bounded regional circumference settlement -> atomic profile history + event`

Training methods:
`concrete trainable target -> reusable target binding -> stable method definition -> effective-load evidence -> domain progression engines`

## Deployed food/nutrition checkpoint

- Inventory Foundation v1 — PR #71 / Deploy #177.
- Inventory Operations v1 — PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — PR #74 / Deploy #179.
- Eating Behavior v1 — PR #76 / Deploy #180.
- Meal Choice Intelligence v1 — PR #77 / Deploy #181.

Meal Choice Intelligence is a compact enrichment inside the existing single cognition call: same-day intake/macros/meal count, latest meal timing, recent training, recovery, REE reference and character nutrition policy. No broad Mind/Behavior Engine and no extra model call.

## BC-2 Body Composition Progression

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #78 / Deploy #182; preserved through Deploy #184.

Canonical:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/BODY_COMPOSITION_PROGRESSION_V1.md`

Live contract:
- activation preserves numerical Weight/BF exactly and establishes a non-retroactive settlement cursor;
- 24 simulated-hour evidence-complete windows;
- incomplete evidence creates an audited no-mutation deferred window;
- Forbes/Hall bounded partition, not fixed 3,500 kcal/lb;
- separate resistance-only lean adaptation constrained by protein, energy, recovery and genetic headroom;
- Weight/BF persist together; FM/FFM/BMI remain derived views;
- no schema migration or extra model call.

## BC-3 Body Measurement Progression Batch

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #82 / Deploy #183; natural activation verified after Deploy #184.

Canonical: `docs/BODY_MEASUREMENT_PROGRESSION_V1.md`.

BC-3 covers neck, shoulders, chest, waist, hips, biceps relaxed/flexed, triceps, forearms, thighs and calves.

Contract:
- consumes BC-2 bounded body-composition settlements rather than creating a second composition authority;
- combines whole-body FM/FFM signals with data-driven regional resistance exposure;
- uses character-specific structural/genetic envelopes rather than scaling every circumference from body weight;
- allows small systemic FFM effects in unexposed regions while regional resistance adds a stronger local increment;
- activation preserves authored circumference values numerically and establishes a non-retroactive cursor;
- all changed measurements persist atomically with history and one causal settlement event;
- no schema migration or extra model call.

Darian's canonical body profile includes `body.hips_in=39.0`; the reusable profile schema includes `genetics.hips_max_in`, with Darian's authored envelope 41.0. These are character-specific canon, not universal ratios.

Natural live activation occurred at `2025-05-05T11:47:00+00:00`: all eleven fields became `simulated` under `body_progression_engine`, numerical values were preserved, hips remained 39.0, and no fields were deferred.

## Training Method Semantics v2

**COMPLETE / DEPLOYED** via PR #84 / Deploy #184.

Canonical: `docs/TRAINING_METHOD_SEMANTICS_V2.md`.

Contract:
- reusable method definitions are keyed by stable `method_id` and contain no character or world-object identity;
- concrete world targets bind separately to reusable methods;
- different worlds/objects may reuse one method definition without duplicating semantic metadata;
- unknown/unbound targets fail closed;
- progression formulas remain owned by domain progression engines;
- historical event compatibility is preserved: persisted evidence retains `source=training-method-semantics-v1`, while new evidence adds `catalog_revision=training-method-semantics-v2`;
- no schema migration or extra model/Telegram call.

PR-head CI #707, Minimum Training Stimulus production-copy Acceptance #15 and Public Readiness Security Audit #22 passed. Main CI #708 and Deploy #184 passed. A synthetic non-Thorne target proved reuse of `barbell_strength_work` without a Darian/Thorne-specific engine branch.

The acceptance cycle also corrected stale validation setup: production-copy training validation now uses authoritative `located_at` via `set_dynamic_location(...)`, not only the legacy `runtime.location` cache.

## Telegram Profile schema-driven UX debt

Canonical debt record: `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`.

Current ordinary fields already render by represented schema/domain data, which is why `body.hips_in` appeared without a Telegram-specific patch. Preserve that pattern.

Remaining debt: the profile section registry itself is still a fixed `PROFILE_SECTIONS` tuple in `profile_observer.py`. Future ordinary sections should eventually be metadata/config-driven (`section id + label + icon + order + visibility + renderer kind`) so adding a new represented profile domain does not require Telegram adapter edits. Sensitivity remains authoritative and private/intimate fields must not auto-surface.

Complete this debt before broad profile/domain expansion makes the fixed registry expensive to unwind.

## Public repository security checkpoint

`Ye-Shwethway/observer-sandbox` is **PUBLIC**. Public Readiness Hardening v1/v1 fixup are complete, and Public Readiness Security Audit #22 passed on Training Method Semantics v2.

Canonical:
- `docs/PUBLIC_REPOSITORY_SECURITY.md`
- `SECURITY.md`

Manual UI verification remains for repository settings the GitHub App cannot fully read: outside-contributor fork workflow approval policy, Secret scanning / Push protection, and `main` branch/ruleset protection.

## Later sequence

1. Training Anatomy / Movement Semantics — reusable movement/exercise patterns with primary/secondary regional loading for more precise BC-3 signals;
2. Regional Measurement Detraining — region-specific disuse/decay reconciled with systemic BC-2 FFM loss to avoid double counting;
3. Telegram Profile schema-driven section UX before broad profile expansion;
4. skill progression family;
5. intellectual attributes;
6. mental/emotion dynamics;
7. later social/relationship/sexual physiology;
8. broad Mind/Behavior architecture only after enough feature families exist to justify it.

Post-public GitHub settings verification can be done opportunistically and does not block runtime development.

## Exact resume point

First re-read live production and current repository evidence. BC-3 is now naturally live-activated and Training Method Semantics v2 is deployed.

The proposed next minimum-runnable development slice is **Training Anatomy / Movement Semantics**: introduce reusable movement/exercise semantics beneath the now-universal method layer so squat/hinge/press/row/curl/extension/calf-style work can provide anatomically specific regional evidence without hard-coding Darian or a particular gym object.

Do not add economy/currency, automatic restocking, deep recipes/crafting, Character Memory, broad Mind/Behavior engines, or a second production character merely for testing as side effects.
