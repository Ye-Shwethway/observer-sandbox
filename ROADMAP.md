# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Python/SQLite runtime and live world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutation.
- Telegram is an observer/control adapter, never a simulation engine.
- Preserve the LEGO runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are first rich production exemplars, never reusable-engine identity.
- Reusable runtime/cognition/progression/query/control/inventory/nutrition/training logic is actor/entity/definition-id driven.
- Prefer minimum-runnable reversible slices.
- One bounded exemplar for a genuinely new invariant; structurally equivalent follow-ons batch by pattern.
- Default flow: `branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Production-copy validation is required for concrete stateful/migration risk.
- Never accelerate/directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest runtime deployment: **Deploy #184 `31828453356` SUCCESS**, Training Method Semantics v2 PR #84 merge `5c7d1524d7d4e66a9b4c92c8232a3a371113391d`.

Main CI #708 passed. A post-deploy read-only Runtime Read #12 rerun (`read-runtime` job `94858499326`) verified:
- service active/healthy;
- schema v5;
- autonomy enabled/normal, paused false, retry null, speed 1.0x;
- sim `2025-05-05T12:00:00+00:00`;
- cognition decision calls 389;
- pending action `idle` in Darian's Master Suite;
- Gemini `gemini-3.1-flash-lite` primary with tested Groq `qwen/qwen3.6-27b` fallback preserved;
- `body.weight_lb=215.0` and `body.body_fat_pct=9.0` remain live `simulated` `physiology_engine` fields;
- BC-2 activation boundary remains `2025-05-05T07:55:00+00:00`, numerical body composition unchanged at activation;
- BC-3 naturally activated at `2025-05-05T11:47:00+00:00`, `status=bootstrapped`, `stat_mutated=false`, `deferred_fields=[]`;
- all eleven BC-3 measurements are live `simulated` `body_progression_engine` fields, with `body.hips_in=39.0` preserved.

A historical provider 413 occurred on an 8,645-token cognition request. It is not current retry state. Cognition enrichment remains compact rather than copying raw histories.

## Completed runtime/profile foundations

- schema v4 composable runtime foundation, operationally extended by schema v5 inventory stacks;
- P0/P0.5 foundation + dynamic provider layer;
- P1 continuous autonomy;
- P2 Telegram Observer/Profile/Control;
- P2.3 Creator AI Control v1;
- Runtime Cognition Fallback v1;
- Telegram Home lifecycle;
- Universal Character Engine;
- Dynamic Resource Awareness / Choice Breadth;
- Object Familiarity / Inspect Utility Guard;
- fatigue/recovery, targeted training, readiness/effectiveness/effective load;
- Minimum Training Stimulus + Session Load/Recovery Guard;
- causal needs + sleep/circadian behavior;
- Training Method Semantics v2 — reusable method definitions separated from world-target bindings;
- Physical Attribute Progression Framework v1 for Strength, Stamina, Agility, Speed, Reflexes, Endurance, Flexibility;
- BC-2 Body Composition and BC-3 Body Measurement progression, both live-activated.

## Universal Item / Eating Program

Core invariant:
`Universal definition -> concrete stack -> reachable action context -> structured quantity -> deterministic validation -> state transition + immutable evidence`

- Inventory Foundation v1 — **COMPLETE / DEPLOYED** via PR #71 / Deploy #177.
- Inventory Operations v1 — **COMPLETE / DEPLOYED** via PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — **COMPLETE / DEPLOYED** via PR #74 / Deploy #179.
- Eating Behavior v1 — **COMPLETE / DEPLOYED** via PR #76 / Deploy #180.
- Meal Choice Intelligence v1 — **COMPLETE / DEPLOYED** via PR #77 / Deploy #181.

Meal Choice Intelligence uses the existing single cognition call and adds compact same-day intake/macros/meal-count, latest meal timing, recent training, recovery, actor REE reference and character nutrition policy. It is not a broad Mind/Behavior Engine and introduces no extra model call.

Canonical:
- `docs/EATING_BEHAVIOR_V1.md`
- `docs/MEAL_CHOICE_INTELLIGENCE_V1.md`

## Body Composition / Measurement Program

Canonical:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/BODY_COMPOSITION_PROGRESSION_V1.md`
- `docs/BODY_MEASUREMENT_PROGRESSION_V1.md`

Research locks:
- no static universal `3500 kcal = 1 lb` rule;
- Weight/FM/FFM/BF% are coupled;
- sex may affect reference physiology but is not a crude hypertrophy multiplier;
- age is context, not a hard cliff;
- genetics are character-specific potential envelopes;
- hunger/energy scores are not kcal;
- protein/energy availability constrain lean adaptation;
- circumference progression combines body composition and regional training context rather than scaling every field from body weight;
- detailed fluid/glycogen/endocrine/micronutrient simulation remains deferred.

### BC-0 — Simulated Profile Re-seed Safety

**COMPLETE / DEPLOYED** via PR #69 / Deploy #175. Ordinary re-init/deploy preserves engine-owned simulated profile state.

### BC-1 — Nutrition & Energy Evidence

**COMPLETE / DEPLOYED** via PR #70 / Deploy #176. Provides actor-specific resting-energy reference, Compendium-informed action intensity, immutable intake/expenditure evidence and coverage-aware bounded aggregation. BC-1 itself never mutates Weight/BF.

### BC-2 — Body Composition Progression Exemplar

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #78 / Deploy #182 and preserved through Deploy #184.

Invariant:
`complete bounded BC-1 evidence + current FM/FFM + resistance-training evidence + recovery + genetic envelope -> deterministic 24h settlement -> atomic Weight/BF history + event`

Live behavior:
- activation preserves Weight/BF numerically and prevents retroactive gain/loss;
- 24 simulated-hour settlement windows;
- incomplete evidence creates an audited no-mutation deferred window rather than an artificial deficit;
- passive partition uses Forbes small-change FFM share and Hall tissue-change energy densities rather than a fixed 3,500-kcal rule;
- resistance-only lean adaptation is constrained by protein, energy availability, recovery, effective minutes, genetic FFM headroom and BF-floor headroom;
- only Weight/BF persist; FM/FFM/BMI remain derived views;
- no extra LLM call, Darian-specific engine branch or schema migration.

### BC-3 — Body Measurement Progression Batch

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #82 / Deploy #183; natural activation verified after Deploy #184.

Invariant:
`BC-2 bounded body-composition settlement + regional resistance evidence + authored anatomy/genetic envelope -> bounded regional measurement settlement -> atomic profile history + event`

BC-3 behavior:
- covers neck, shoulders, chest, waist, hips, biceps relaxed/flexed, triceps, forearms, thighs and calves in one batched implementation;
- consumes BC-2 settlement events as its body-composition cadence and does not introduce a second nutrition/composition authority;
- combines general FM/FFM changes with data-driven regional resistance exposure;
- small whole-body FFM effects may affect an unexposed region, while regional resistance creates an additional stronger local increment;
- uses character-specific circumference maxima/targets and activation-relative safety guards;
- preserves authored circumference values numerically at activation and prevents retroactive progression;
- changed fields, profile history and causal settlement event are atomic;
- no schema migration and no extra model call.

Darian's complete authored measurement family includes `body.hips_in=39.0`; reusable schema includes `genetics.hips_max_in`, with Darian's authored hip envelope 41.0. These are character-specific canon, not universal ratios.

Live activation at `2025-05-05T11:47:00+00:00` changed all eleven measurement fields to `simulated` under `body_progression_engine` without numerical mutation. Hips remained 39.0 and `deferred_fields=[]`.

## Training Method Semantics v2

**COMPLETE / DEPLOYED** via PR #84 / Deploy #184.

Canonical: `docs/TRAINING_METHOD_SEMANTICS_V2.md`.

Invariant:
`concrete training target -> target binding -> reusable stable method definition -> effective-load evidence -> domain progression engines`

Behavior:
- reusable `methods` are keyed by stable `method_id` and contain no character identity or concrete world-object id;
- separate `bindings` map current trainable objects to reusable methods;
- a synthetic non-Thorne target proved that another world object can reuse `barbell_strength_work` without copied method metadata or an engine branch;
- unknown/unbound targets fail closed rather than guessing from object names;
- downstream Strength/Stamina/BC-2/BC-3 semantics continue to consume stable method ids/workload channels;
- persisted event evidence retains `source=training-method-semantics-v1` because the evidence contract did not change, while new events add `catalog_revision=training-method-semantics-v2` for provenance;
- historical v1 events therefore remain valid with no migration;
- no schema migration or extra model/Telegram call.

Validation:
- PR-head CI #707 SUCCESS;
- Minimum Training Stimulus production-copy Acceptance #15 SUCCESS;
- Public Readiness Security Audit #22 SUCCESS;
- main CI #708 SUCCESS;
- Deploy #184 SUCCESS;
- post-deploy runtime healthy.

Acceptance also fixed stale validation setup: current authoritative dynamic location is `located_at`; the production-copy training validator now uses `set_dynamic_location(...)` rather than only writing the legacy `runtime.location` cache.

## Telegram Profile schema-driven UX — REQUIRED FOLLOW-UP

Canonical debt record: `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`.

Current good behavior:
- ordinary represented fields are queried/rendered by schema domain, not hard-coded field rows;
- therefore new normal-sensitivity fields such as `body.hips_in` auto-appear in the existing Body section without a Telegram-specific patch.

Remaining debt:
- `PROFILE_SECTIONS` in `profile_observer.py` is still a fixed registry;
- a wholly new ordinary profile domain/section may still require code-level registration.

Target direction:
`domain/collection -> section id + label + icon + order + visibility + renderer kind`

Ordinary future sections should become metadata/config-driven; special renderers remain only for genuinely different data shapes. Sensitivity must remain authoritative so private/intimate fields never auto-surface merely because they exist in schema.

Complete this debt before broad Skill/Intellectual/Mental/Social profile expansion makes the fixed registry expensive to unwind.

## Public Repository Security — COMPLETE / PUBLIC

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md` and `SECURITY.md`.

`Ye-Shwethway/observer-sandbox` is public. Public Readiness Hardening v1/v1 fixup are complete; Public Readiness Security Audit #22 also passed on PR #84.

Security locks remain unchanged. Manual UI verification is still needed where the GitHub App cannot fully read account-level repository settings: outside-contributor workflow approval, Secret scanning/Push protection, and `main` branch/ruleset protection.

## Next development sequence

1. **Training Anatomy / Movement Semantics** — reusable movement/exercise patterns beneath universal method definitions, with primary/secondary regional loading for anatomically specific BC-3 evidence;
2. **Regional Measurement Detraining** — region-specific training absence/disuse decay reconciled with systemic BC-2 FFM loss so decline is realistic without double counting;
3. **Telegram Profile schema-driven section UX** before broad profile expansion;
4. skill progression family;
5. intellectual attributes;
6. mental/emotion dynamics;
7. later relationship/social/sexual physiology when prerequisites mature;
8. broad Mind/Behavior architecture only after enough real feature signals exist to justify it.

Post-public GitHub settings verification can proceed opportunistically and does not block runtime development.

## Future universal object/inventory expansion

Proceed by family when needed:
1. movable containers + carried inventory;
2. fixed storage capacity semantics;
3. training equipment definitions + concrete instances;
4. tools/electronics/books/medical supplies;
5. clothing/equipped-state;
6. materials/crafting when justified;
7. economy: ownership transfer, vendors, pricing, currency/accounts, transactions, scarcity/replenishment.

## Deferred boundaries

Do not add as side effects:
- broad Mind Engine / Behavior Engine now;
- Character Memory Engine;
- multi-fallback/circuit-breaker/provider-health expansion;
- Telegram secret/model-parameter editing;
- second production character solely for testing;
- automatic economy restocking;
- full RPG encumbrance/capacity UI;
- arbitrary-depth nested containers;
- spoilage/deep recipe graph;
- currency/shops/economy simulation;
- generalized crafting;
- detailed endocrine/micronutrient/organ metabolic simulation;
- estate exterior/Tahoe traversal.

## Exact resume point

Re-read live production and current canonical repository first. BC-3 is naturally live-activated and Training Method Semantics v2 is deployed.

The proposed next minimum-runnable slice is **Training Anatomy / Movement Semantics**. It should add reusable movement/exercise semantics such as squat, hinge, horizontal/vertical press, row, curl, extension and calf patterns, then emit anatomically specific regional evidence while keeping actor identity, concrete gym objects and BC-3 formulas outside the movement-definition layer.
