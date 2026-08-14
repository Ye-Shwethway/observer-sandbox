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

Latest runtime deployment: **Deploy #186 `31831203232` SUCCESS**, Regional Measurement Detraining v1 PR #88 merge `1ccfce79182942010bd3303fd7308891df9e1b77`.

Main CI #717 passed. Post-deploy read-only Runtime Read job `94867199936` verified:
- service active/healthy;
- schema v5;
- autonomy enabled/normal, paused false, retry null, speed 1.0x;
- sim `2025-05-05T12:40:00+00:00`;
- cognition decision calls 393;
- current/pending action `eat` in the Kitchen;
- Gemini `gemini-3.1-flash-lite` primary with tested Groq `qwen/qwen3.6-27b` fallback preserved;
- Weight 215.0 lb / BF 9.0% remain live `simulated` `physiology_engine` fields;
- BC-3 remains live-activated from `2025-05-05T11:47:00+00:00`; all eleven fields remain `simulated` under `body_progression_engine`, including hips 39.0.

Production was not accelerated to manufacture detraining or movement evidence.

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
- Training Anatomy / Movement Semantics v1;
- Regional Measurement Detraining v1.

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
- `docs/REGIONAL_MEASUREMENT_DETRAINING_V1.md`

Research locks:
- no static universal `3500 kcal = 1 lb` rule;
- Weight/FM/FFM/BF% are coupled;
- genetics are character-specific potential envelopes;
- protein/energy availability constrain lean adaptation;
- circumference progression combines body composition with regional resistance context;
- regional detraining may reverse post-activation training-acquired excess but never reinterpret authored activation anatomy as untrained;
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

**Weight progression/decline is therefore already owned by BC-2. Do not add a second Weight decay engine.** Later optional refinement may model short-term fluid/glycogen variation as a separate observed-state layer, not a competing structural-weight authority.

### BC-3 — Body Measurement Progression

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #82 / Deploy #183; natural activation at `2025-05-05T11:47:00+00:00`.

Invariant:
`BC-2 settlement + regional resistance evidence + authored anatomy/genetic envelope -> bounded regional measurement settlement -> atomic profile history + event`

Covers neck, shoulders, chest, waist, hips, biceps relaxed/flexed, triceps, forearms, thighs and calves. Darian's hips are 39.0 in; reusable schema includes `genetics.hips_max_in`, with Darian's authored envelope 41.0. All eleven values became engine-owned without numerical mutation at activation.

### Regional Measurement Detraining v1

**COMPLETE / DEPLOYED** via PR #88 / Deploy #186.

Canonical: `docs/REGIONAL_MEASUREMENT_DETRAINING_V1.md`.

Invariant:
`BC-3 activation baseline + immutable regional resistance history + bounded BC-2 settlement -> inactivity pressure -> reversible post-activation regional excess decay`

Behavior:
- 21-day grace before detraining pressure;
- pressure ramps over the next 63 simulated days;
- full-pressure decay is capped at 0.4% of remaining post-activation excess per normal 24h window before existing per-field clamps;
- recent qualifying training resets only materially loaded regions;
- Training Anatomy v1 regional load is preferred, with historical method-level fallback preserved;
- detraining-only loss cannot cross the authored BC-3 activation value;
- if BC-2 already reports negative partition FFM in a window, extra regional detraining is suppressed so the same tissue loss is not counted twice;
- no schema migration, new state table, extra model call or second body progression authority.

Validation:
- final PR head `d7389bb58c1b4761064fce049de6b1b4bcc58627`;
- CI #716 SUCCESS;
- Body Measurement Progression Acceptance #15 SUCCESS on a disposable production copy;
- main CI #717 SUCCESS;
- Deploy #186 SUCCESS;
- post-deploy read-only production check healthy with all existing body values preserved.

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

Initial reusable patterns: squat, hinge, horizontal press, vertical press, row, curl, extension, calf raise and Olympic pull.

BC-3 prefers movement-level regional load when present and keeps method-level weights as historical/no-selection fallback. BC-2 remains method/channel based and unchanged.

## Physical Profile Completion Gate — REQUIRED BEFORE SKILL PROGRESSION

Creator direction is to finish the physical/body profile family before crossing into skill, intellectual or mental progression because these domains obey materially different lifecycle rules.

Current physical-family authority map:
- Weight/BF/FM/FFM — BC-2, complete;
- ordinary circumferences — BC-3 + Training Anatomy + Regional Detraining, complete for current scope;
- Height — structural lifecycle still missing;
- sexual-anatomy measurements / sexual physiology — structural-vs-current-state lifecycle still missing;
- appearance/physiology-linked fields — require coverage audit to identify dynamic fields that are still static or text-only.

### Proposed Height Lifecycle v1

Target invariant:
`age/development stage + authored genetic height envelope + health/context -> bounded structural height lifecycle`

Requirements:
- childhood/adolescent growth when applicable;
- adult structural stability as the ordinary state;
- later-life gradual decline only when age/context warrants;
- temporary spinal compression/decompression, if later added, must be an observed/current-height layer rather than silently rewriting structural stature;
- injury/pathology changes remain exceptional and separately evidenced;
- Darian's adult height should not drift merely because the field becomes simulated.

### Proposed Sexual Anatomy & Physiology Lifecycle v1

Current schema already distinguishes intimate structural measurements (`sexual_anatomy.penis_length_in`, `sexual_anatomy.penis_girth_in`) from dynamic candidates such as erection firmness and genital sensitivity.

Target direction:
`developmental/genetic structural anatomy + current vascular/arousal/health state + age/pathology context -> structural baseline + temporary physiological presentation`

Requirements:
- adult structural dimensions are mostly stable rather than gym-style progression stats;
- puberty/development may change structural anatomy for younger characters;
- current physiological presentation may vary with arousal, firmness, vascular/health state and context;
- aging/pathology may cause gradual functional or structural decline when supported;
- intimate sensitivity/visibility rules remain authoritative;
- no claim that ordinary resistance training permanently enlarges sexual organs.

### Physical Profile Coverage Audit

After the two lifecycle slices above, audit physical/profile fields one-by-one and classify each as:
- canonical structural;
- derived;
- simulated dynamic;
- lifecycle-driven;
- intentionally static.

The audit must catch body-state-linked appearance fields that can otherwise become contradictory, such as abdominal definition or physiology-authority skin quality remaining stale after body composition/health changes.

Physical completion is the gate for proceeding to Skill Progression.

## Telegram Profile schema-driven UX — REQUIRED BEFORE BROAD PROFILE EXPANSION

Canonical debt: `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`.

Current good behavior: ordinary fields render by schema/domain data, so `body.hips_in` surfaced without Telegram-specific field code.

Remaining debt: `PROFILE_SECTIONS` in `profile_observer.py` is still fixed. Target direction:
`domain/collection -> section id + label + icon + order + visibility + renderer kind`

Sensitivity must remain authoritative; private/intimate fields never auto-surface merely because they exist.

## Public Repository Security — COMPLETE / PUBLIC

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md`, `SECURITY.md`.

Public hardening is complete. Manual UI verification remains where the GitHub App cannot fully read settings: outside-contributor workflow approval, Secret scanning/Push protection, and `main` branch/ruleset protection.

## Next development sequence

1. **Height Lifecycle v1**;
2. **Sexual Anatomy & Physiology Lifecycle v1**;
3. **Physical Profile Coverage Audit**;
4. **Telegram Profile schema-driven section UX**;
5. **Skill Progression Family**;
6. intellectual attributes;
7. mental/emotion dynamics;
8. later broader relationship/social systems;
9. broad Mind/Behavior architecture only after enough real feature signals justify it.

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

Re-read live production and current canonical repository first. Regional Measurement Detraining v1 is deployed and read back healthy.

The proposed next minimum-runnable runtime slice is **Height Lifecycle v1**. It should establish a reusable structural-height lifecycle with adult stability as a first-class outcome, use `genetics.height_max_in` as an authored envelope where appropriate, and avoid treating daily posture/compression noise as permanent height mutation.
