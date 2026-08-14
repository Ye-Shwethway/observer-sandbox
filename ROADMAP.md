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
- Use one bounded exemplar for a genuinely new invariant, then batch structurally equivalent follow-ons.
- Default flow: `branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Use production-copy validation for concrete stateful/migration risk; never accelerate or directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest runtime deployment: **Deploy #185 `31829636147` SUCCESS**, Training Anatomy v1 PR #86 merge `e9f4920518c995765344052325c121e186f52489`.

Main CI #713 passed. Post-deploy read-only Runtime Read job `94862090792` verified:
- service active/healthy;
- schema v5;
- autonomy enabled/normal, paused false, retry null, speed 1.0x;
- sim `2025-05-05T12:20:00+00:00`;
- cognition decision calls 391;
- current/pending action `shower` in the Master Bathroom;
- Gemini `gemini-3.1-flash-lite` primary with tested Groq `qwen/qwen3.6-27b` fallback preserved;
- Weight 215.0 lb / BF 9.0% remain live `simulated` `physiology_engine` fields;
- BC-3 remains live-activated from `2025-05-05T11:47:00+00:00`; all eleven fields remain `simulated` under `body_progression_engine`, including hips 39.0.

No natural post-deploy resistance action had occurred at readback, so no live `movement_anatomy` event was yet expected. Production was not accelerated for evidence.

## Completed foundations

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
- Physical Attribute Progression Framework v1 for Strength, Stamina, Agility, Speed, Reflexes, Endurance and Flexibility;
- universal inventory/eating/nutrition slices through Meal Choice Intelligence;
- BC-2 Body Composition and BC-3 Body Measurement progression, both live-activated;
- Training Method Semantics v2;
- Training Anatomy / Movement Semantics v1.

## Universal Item / Eating Program

Invariant:
`Universal definition -> concrete stack -> reachable action context -> structured quantity -> deterministic validation -> state transition + immutable evidence`

- Inventory Foundation v1 — COMPLETE / DEPLOYED via PR #71 / Deploy #177.
- Inventory Operations v1 — COMPLETE / DEPLOYED via PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — COMPLETE / DEPLOYED via PR #74 / Deploy #179.
- Eating Behavior v1 — COMPLETE / DEPLOYED via PR #76 / Deploy #180.
- Meal Choice Intelligence v1 — COMPLETE / DEPLOYED via PR #77 / Deploy #181.

Canonical: `docs/EATING_BEHAVIOR_V1.md`, `docs/MEAL_CHOICE_INTELLIGENCE_V1.md`.

## Body Composition / Measurement Program

Canonical:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/BODY_COMPOSITION_PROGRESSION_V1.md`
- `docs/BODY_MEASUREMENT_PROGRESSION_V1.md`

Research locks:
- no static universal `3500 kcal = 1 lb` rule;
- Weight/FM/FFM/BF% are coupled;
- genetics are character-specific potential envelopes;
- protein/energy availability constrain lean adaptation;
- circumference progression combines body composition with regional resistance context;
- detailed fluid/glycogen/endocrine/micronutrient simulation remains deferred.

### BC-0 — Simulated Profile Re-seed Safety

COMPLETE / DEPLOYED via PR #69 / Deploy #175.

### BC-1 — Nutrition & Energy Evidence

COMPLETE / DEPLOYED via PR #70 / Deploy #176.

### BC-2 — Body Composition Progression

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #78 / Deploy #182.

Invariant:
`complete bounded BC-1 evidence + current FM/FFM + resistance evidence + recovery + genetic envelope -> deterministic 24h settlement -> atomic Weight/BF history + event`

Activation preserves numbers, windows are evidence-complete and bounded, incomplete evidence defers safely, resistance lean adaptation is constrained by nutrition/recovery/genetic headroom, and only Weight/BF persist while FM/FFM/BMI remain derived.

### BC-3 — Body Measurement Progression

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #82 / Deploy #183; natural activation at `2025-05-05T11:47:00+00:00`.

Invariant:
`BC-2 settlement + regional resistance evidence + authored anatomy/genetic envelope -> bounded regional measurement settlement -> atomic profile history + event`

Covers neck, shoulders, chest, waist, hips, biceps relaxed/flexed, triceps, forearms, thighs and calves. Darian's hips are 39.0 in; reusable schema includes `genetics.hips_max_in`, with Darian's authored envelope 41.0. All eleven values became engine-owned without numerical mutation at activation.

## Training Method Semantics v2

**COMPLETE / DEPLOYED** via PR #84 / Deploy #184.

Canonical: `docs/TRAINING_METHOD_SEMANTICS_V2.md`.

Invariant:
`concrete training target -> target binding -> reusable stable method definition -> effective-load evidence -> domain progression engines`

Reusable methods contain no character/concrete-object identity. Targets bind separately. Historical evidence compatibility is preserved with stable `method_id` and `source=training-method-semantics-v1`; catalog provenance is `training-method-semantics-v2`. Unknown targets fail closed.

## Training Anatomy / Movement Semantics v1

**COMPLETE / DEPLOYED** via PR #86 / Deploy #185.

Canonical: `docs/TRAINING_ANATOMY_V1.md`.

Invariant:
`train target -> reusable method -> selected reusable movement pattern(s) -> effective load -> deterministic movement anatomy -> BC-3 regional exposure`

Initial reusable patterns:
- squat;
- hinge;
- horizontal press;
- vertical press;
- row;
- curl;
- extension;
- calf raise;
- Olympic pull.

Behavior:
- movement definitions own normalized regional loading only, not progression formulas or actor state;
- resistance methods publish authored movement choices;
- cognition may select one to four exact movement ids from the chosen training option;
- invalid target/movement combinations fail server-side;
- selections persist in existing `action_instances.conditions_json`, requiring no migration;
- completed training events add `movement_anatomy` evidence when movements are explicit;
- BC-3 uses movement-level regional load when present and keeps existing method-level weights as historical/no-selection fallback;
- BC-2 remains method/channel based and unchanged;
- no additional model call.

Validation at final PR head `9234a948f91ec83ddc66fbd7430f038c9dcca741`:
- CI #712 SUCCESS;
- Body Measurement Progression Acceptance #14 SUCCESS;
- Minimum Training Stimulus Acceptance #17 SUCCESS;
- Eating Behavior Acceptance #17 SUCCESS;
- Nutrition & Energy Evidence Acceptance #15 SUCCESS;
- main CI #713 SUCCESS;
- Deploy #185 SUCCESS;
- post-deploy runtime readback healthy.

The acceptance cycle also made the BC-3 production-copy validator activation-state aware, because production has naturally passed the one-time bootstrap boundary.

## Telegram Profile schema-driven UX — REQUIRED FOLLOW-UP

Canonical debt: `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`.

Current good behavior: ordinary fields render by schema/domain data, so `body.hips_in` surfaced without Telegram-specific field code.

Remaining debt: `PROFILE_SECTIONS` in `profile_observer.py` is still fixed. Target direction:
`domain/collection -> section id + label + icon + order + visibility + renderer kind`

Sensitivity must remain authoritative; private/intimate fields never auto-surface merely because they exist. Complete this before broad Skill/Intellectual/Mental/Social profile expansion.

## Public Repository Security — COMPLETE / PUBLIC

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md`, `SECURITY.md`.

Public hardening is complete. Manual UI verification remains where the GitHub App cannot fully read settings: outside-contributor workflow approval, Secret scanning/Push protection, and `main` branch/ruleset protection.

## Next development sequence

1. **Regional Measurement Detraining** — region-specific training absence/disuse decay reconciled with systemic BC-2 FFM loss so the same tissue decline is not counted twice;
2. **Telegram Profile schema-driven section UX**;
3. skill progression family;
4. intellectual attributes;
5. mental/emotion dynamics;
6. later relationship/social/sexual physiology;
7. broad Mind/Behavior architecture only after enough real feature signals justify it.

Post-public GitHub settings verification remains opportunistic and non-blocking.

## Future universal object/inventory expansion

When justified: movable containers/carried inventory; fixed storage capacity; training equipment instances; tools/electronics/books/medical supplies; clothing/equipped state; materials/crafting; eventually economy/ownership/pricing/currency.

## Deferred boundaries

Do not add as side effects:
- broad Mind/Behavior Engine;
- Character Memory Engine;
- multi-fallback/circuit-breaker/provider-health expansion;
- Telegram secret/model-parameter editing;
- second production character solely for testing;
- automatic restocking, deep recipes, economy/currency, generalized crafting;
- detailed endocrine/micronutrient/organ simulation;
- estate exterior/Tahoe traversal.

## Exact resume point

Re-read live production and current canonical repository first. Training Anatomy v1 is deployed. If a natural post-deploy resistance session has happened, read its movement evidence without mutating production; otherwise do not force one.

The proposed next minimum-runnable slice is **Regional Measurement Detraining**: add regional disuse pressure to BC-3, with explicit accounting against BC-2 systemic lean-loss contribution to avoid double counting.
