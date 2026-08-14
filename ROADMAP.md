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
- Reusable runtime/cognition/progression/query/control/inventory/nutrition logic is entity/definition-id driven.
- Prefer minimum-runnable reversible slices.
- New invariant: one bounded exemplar; structurally equivalent follow-ons batch by pattern.
- Default flow: `branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Production-copy validation is used only for concrete stateful/migration risk.
- Never accelerate/directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest deployment: **Deploy #180 `31816335698` SUCCESS**, PR #76 merge `ed297348ea0ba77d8f02e9ebec41f19643e7f175`.

Fresh read-only Runtime Read attempt 6 completed successfully after deployment. Verified:
- service active/healthy;
- schema v5;
- world `thorne-estate-v3.3-physical-attribute-training`;
- `inventory_seed_revision=thorne-estate-inventory-v1`;
- wealthy food reserve migration remains applied once;
- autonomy enabled/normal, paused false, retry null;
- live speed 3.0x;
- sim time `2025-05-05T06:10:00+00:00` at that read;
- Darian in the Home Gym with a 50-minute structured `train` action pending;
- cognition decision calls 363;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram connected.

A historical cognition error showed a provider request/TPM 413 at 8,645 requested tokens. It was not the current retry state, but future cognition enrichment should remain compact rather than expanding raw histories.

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

## Body Composition Program — ACTIVE

Canonical:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/EATING_BEHAVIOR_V1.md`
- `docs/MEAL_CHOICE_INTELLIGENCE_V1.md`

Research direction remains:
- no static universal `3500 kcal = 1 lb` rule;
- body composition couples Weight/FM/FFM/BF% over bounded intervals;
- sex affects reference/baseline physiology but is not a crude hypertrophy multiplier;
- age is context, not a hard cliff;
- genetics are character-specific potential envelopes;
- hunger/energy scores are not kcal;
- protein/energy availability constrains lean adaptation;
- expenditure is actor-scaled from resting physiology + authored activity intensity.

### BC-0 — Simulated Profile Re-seed Safety

**COMPLETE / DEPLOYED** via PR #69 / Deploy #175.
Ordinary re-init/deploy preserves engine-owned simulated profile state.

### BC-1 — Nutrition & Energy Evidence

**COMPLETE / DEPLOYED** via PR #70 / Deploy #176.
Provides actor-specific resting-energy reference, Compendium-informed action intensity, immutable intake/expenditure evidence and coverage-aware bounded aggregation. BC-1 itself never mutates body weight/BF.

## Universal Item / Eating Program

Core invariant:
`Universal definition -> concrete stack -> reachable action context -> structured quantity -> deterministic validation -> state transition + immutable evidence`

### Inventory Foundation v1

**COMPLETE / DEPLOYED** via PR #71 / Deploy #177.
Schema v5 inventory stacks, universal food definitions, concrete Estate stocks and deterministic quantity-scaled nutrition are live. Ordinary init/deploy never refills changed stock.

### Inventory Operations v1

**COMPLETE / DEPLOYED** via PR #73 / Deploy #178.
Universe-wide inventory browsing, one-time wealthy Estate reserve and owner-only typed replenishment are live. Reserve migration is not recurring auto-restock.

### Food Nutrition Semantics & Visibility v1

**COMPLETE / DEPLOYED** via PR #74 / Deploy #179.
Definition-scoped default-portion nutrition facts and Telegram visibility are live. No duplicate nutrition database exists in Telegram.

### Eating Behavior v1

**COMPLETE / DEPLOYED** via PR #76 / Deploy #180.

Invariant:
`local eat capability + reachable inventory food stacks + structured quantities -> deterministic validation -> atomic stock decrement + immutable combined nutrition evidence`

Live code now supports:
- required structured cognition `resources`;
- one to six concrete meal stack IDs + quantities;
- deterministic 0.5x–2x default-portion guardrails, stock-capped, whole-piece validation;
- nearest enclosing inventory-scope access only from a local eat-capable context;
- persistence in existing `action_instances.resources_json` with no schema v6;
- completion-time revalidation and atomic multi-stack decrement;
- exact combined kcal/protein/carbs/fat snapshot into BC-1 `nutrition_intake`;
- rollback of the entire completion on any invalid/missing stock;
- legacy compatibility only for already-persisted pre-v1 empty-resource meals;
- Telegram completed-meal item quantities + combined macros.

## Meal Choice Intelligence v1 — CURRENT PR #77

Canonical: `docs/MEAL_CHOICE_INTELLIGENCE_V1.md`.

Purpose: improve food selection using the **existing single cognition call**, without creating a separate Mind Engine or Behavior Engine.

Candidate behavior:
- deterministic compact same-day intake/macros/meal-count summary;
- compact same-day expenditure + evidence coverage context;
- latest meal timing/kcal/protein;
- recent 12-hour training count/minutes + time since latest session;
- current hunger/energy/fatigue/sleepiness/thirst;
- actor-specific REE reference explicitly labeled as non-target;
- character-authored nutrition goal, energy intent, protein priority and dietary constraints;
- no raw-history expansion, no extra LLM call, no inventory/body mutation and no schema change.

Darian's authored policy is maintenance-oriented: preserve a lean muscular body composition while supporting training performance, recovery and ordinary health. Protein receives contextual priority after training/recovery demand rather than being maximized in every meal. No dietary constraint is currently authored.

Validation policy:
- focused read-only unit regressions;
- full CI;
- existing Eating Behavior acceptance remains green;
- no new production-copy gate because no stateful migration is introduced.

## BC-2 — Body Composition Progression Exemplar — NEXT AUTHORIZED SLICE

Proceed after Meal Choice Intelligence v1 merge/deploy/readback. Natural Eating Behavior should continue autonomously at the Creator-selected runtime speed; do not force or accelerate meals merely for acceptance.

BC-2 activation must be safe even before the next natural meal appears:
- establish an explicit activation boundary at deployment/activation sim time;
- never retroactively settle legacy/incomplete pre-activation history;
- settle only bounded windows with adequate persisted BC-1 evidence coverage;
- if evidence is incomplete, defer mutation rather than treating missing intake/expenditure as a deficit.

Minimum-runnable BC-2 target:
- actor-generic coupled mutation of `body.weight_lb` + `body.body_fat_pct`;
- derive FM/FFM/BMI consistently from those persisted values;
- bounded energy-partition approximation inspired by validated Hall/Forbes direction rather than a fixed 3,500-kcal rule;
- separate resistance-training lean adaptation constrained by protein, energy availability, recovery and character genetic headroom;
- age/sex effects only where evidence-supported;
- atomic profile value/history/audit mutation;
- implausible-window and physiological clamps;
- no Darian branch, no extra model call, no fluid/glycogen/endocrine/micronutrient simulation.

Natural meal observation remains useful evidence for later calibration, but current Creator instruction authorizes BC-2 implementation without waiting for a naturally timed meal. Runtime settlement guards, not forced production behavior, must provide safety.

### BC-3 — Body Measurement Progression Batch

After BC-2. Circumferences combine body composition, regional training/anatomy and character-specific structural/genetic envelopes rather than body weight alone.

## Future universal object/inventory expansion

Proceed by family:
1. consumable definitions/stacks — foundation complete;
2. movable containers + carried inventory;
3. fixed storage capacity semantics;
4. training equipment definitions + concrete instances;
5. tools/electronics/books/medical supplies;
6. clothing/equipped-state;
7. materials/crafting when justified;
8. economy: ownership transfer, vendors, pricing, currency/accounts, transactions, scarcity/replenishment.

## Later profile sequence

1. finish Meal Choice Intelligence v1 PR #77 -> merge/deploy/readback;
2. BC-2 body composition;
3. BC-3 measurements;
4. skill progression family;
5. intellectual attributes;
6. mental/emotion dynamics;
7. later relationship/social/sexual physiology when prerequisites mature;
8. broad Mind/Behavior architecture only after enough real feature signals exist to justify it.

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
- all-object migration at once;
- currency/shops/economy simulation;
- generalized crafting;
- detailed endocrine/micronutrient/organ metabolic simulation;
- estate exterior/Tahoe traversal.

## Exact resume point

Finish **Meal Choice Intelligence v1 PR #77**, merge/deploy/read back, then proceed directly to **BC-2 Body Composition Progression Exemplar** under activation-boundary and complete-evidence guards.
