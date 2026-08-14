# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-14

## Operating principles

- Python/SQLite runtime and live world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutation.
- Telegram is an observer/control adapter, never a simulation engine.
- Preserve the LEGO runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are first rich production exemplars, never reusable-engine identity.
- Reusable runtime/cognition/progression/query/control/inventory/nutrition logic is actor/entity/definition-id driven.
- Prefer minimum-runnable reversible slices.
- New invariant: one bounded exemplar; structurally equivalent follow-ons batch by pattern.
- Default flow: `branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Production-copy validation is required for concrete stateful/migration risk.
- Never accelerate/directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest deployment: **Deploy #181 `31817900997` SUCCESS**, PR #77 merge `e2c4275cedf1edcdcb36126e525371c86f5ef97c`.

Deploy readback verified:
- service active/healthy;
- schema v5;
- world `thorne-estate-v3.3-physical-attribute-training`;
- inventory seed + one-time wealthy reserve marker preserved;
- autonomy enabled/normal, paused false, retry null, speed 3.0x;
- sim `2025-05-05T07:00:00+00:00` at deploy readback;
- Darian naturally continued training in the Home Gym;
- cognition decision calls advanced naturally to 364;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram connected.

A historical provider 413 occurred on an 8,645-token cognition request. It is not the current retry state. Cognition enrichment therefore remains compact rather than copying raw histories.

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
- Training Method Semantics v1;
- Physical Attribute Progression Framework v1 for Strength, Stamina, Agility, Speed, Reflexes, Endurance, Flexibility.

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

## Body Composition Program — ACTIVE

Canonical:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/BODY_COMPOSITION_PROGRESSION_V1.md`

Research locks:
- no static universal `3500 kcal = 1 lb` rule;
- Weight/FM/FFM/BF% are coupled;
- sex may affect reference physiology but is not a crude hypertrophy multiplier;
- age is context, not a hard cliff;
- genetics are character-specific potential envelopes;
- hunger/energy scores are not kcal;
- protein/energy availability constrain lean adaptation;
- detailed fluid/glycogen/endocrine/micronutrient simulation remains deferred.

### BC-0 — Simulated Profile Re-seed Safety

**COMPLETE / DEPLOYED** via PR #69 / Deploy #175.
Ordinary re-init/deploy preserves engine-owned simulated profile state.

### BC-1 — Nutrition & Energy Evidence

**COMPLETE / DEPLOYED** via PR #70 / Deploy #176.
Provides actor-specific resting-energy reference, Compendium-informed action intensity, immutable intake/expenditure evidence and coverage-aware bounded aggregation. BC-1 itself never mutates Weight/BF.

### BC-2 — Body Composition Progression Exemplar — CURRENT PR #78

Canonical: `docs/BODY_COMPOSITION_PROGRESSION_V1.md`.

Candidate invariant:
`complete bounded BC-1 evidence + current FM/FFM + resistance-training evidence + recovery + genetic envelope -> deterministic 24h settlement -> atomic Weight/BF history + event`

Implemented candidate:
- first post-deploy completed-action boundary activates `body.weight_lb` and `body.body_fat_pct` as simulated `physiology_engine` fields while preserving 215 lb / 9% numerically;
- pre-activation history never creates retroactive gain/loss;
- 24 simulated-hour settlement windows;
- incomplete BC-1 windows produce an explicit no-mutation `deferred_incomplete_evidence` event and advance the cursor rather than inventing a deficit or permanently blocking future windows;
- passive energy partition uses Forbes small-change `dFFM/dBW = 10.4 / (10.4 + FM_kg)`;
- tissue-change energy densities use Hall 39.5 MJ/kg fat and 7.6 MJ/kg lean;
- passive tissue change is capped at 0.5 lb absolute body-weight change per 24h as a simulation plausibility guard;
- resistance-training recomposition is separate and only `training_method.workload_channels` containing `resistance` qualify; cardio/combat-only/tactical/mobility training cannot silently become hypertrophy stimulus;
- protein factor saturates at the 1.6 g/kg/day policy reference;
- lean adaptation fades to zero around a 500 kcal/day deficit, and is additionally constrained by recovery, resistance effective minutes, genetic FFM headroom and sustainable BF-floor headroom;
- genetic lean-condition weight range remains a character potential envelope, never an instantaneous snap target;
- only Weight/BF persist; FM/FFM/BMI remain derived views;
- coupled changed fields and profile histories commit atomically with a fully auditable settlement event;
- no schema change, extra LLM call, Darian-specific engine branch, BC-3 measurement mutation or fluid/endocrine/micronutrient model.

Validation already demonstrated during development:
- full CI green before final doc tail;
- inherited Strength/Stamina activation acceptances green;
- Body Composition Progression production-copy acceptance green;
- production-copy activation preserves starting numerical state and exercises a bounded 24h complete-evidence settlement without touching live production.

Final-head CI + BC-2 production-copy acceptance + inherited physical-progression gates must be green after canonical synchronization before merge/deploy.

### BC-3 — Body Measurement Progression Batch — NEXT

After BC-2 production activation/readback, unlock body circumference progression as one patterned batch rather than repetitive per-stat PRs.

BC-3 direction:
- neck, shoulders, chest, waist, hips, biceps relaxed/flexed, triceps, forearms, thighs and calves;
- combine live body composition with regional training stimulus/anatomy and character-specific structural/genetic envelopes;
- never derive every circumference from body weight alone;
- use exemplar-first only for a genuinely new measurement invariant, then batch structurally equivalent measurement fields in the same PR/deploy cycle.

## Later profile sequence

1. finish BC-2 PR #78 -> merge/deploy/readback;
2. BC-3 measurement progression batch;
3. skill progression family;
4. intellectual attributes;
5. mental/emotion dynamics;
6. later relationship/social/sexual physiology when prerequisites mature;
7. broad Mind/Behavior architecture only after enough real feature signals exist to justify it.

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

Finish **BC-2 PR #78**, rerun final-head gates, merge/deploy/read back the activation boundary, then proceed to the **BC-3 Body Measurement Progression Batch**.
