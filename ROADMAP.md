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
- Universal definition and concrete instance are distinct; ownership, storage, carriage/equipped state and physical location remain separate.
- Prefer minimum-runnable reversible slices.
- New invariant: one bounded exemplar; structurally equivalent follow-ons batch by pattern.
- Default flow: `test -> focused tests + CI -> merge main -> deploy if runtime-affecting -> read-only production check -> sync test`.
- State-sensitive migrations use disposable production-copy validation.
- Never accelerate/directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest deployed production before current PR #76: **Deploy #179 `31812160413` SUCCESS**, PR #74 merge `edd345c317a52b702c00dd7889ad1eefffa51927`.

A fresh read-only runtime read before Eating Behavior implementation showed production had advanced naturally to sim time `2025-05-05T05:37:00+00:00`, with Darian in the Kitchen and a legacy in-flight `eat` action whose persisted resources were empty. That observation established the transition rule: an already-persisted pre-v1 empty-resource meal may finish under legacy BC-1 semantics, while newly planned meals must use structured inventory resources.

Verified deployed baseline remains:
- healthy/service active;
- schema v5;
- world `thorne-estate-v3.3-physical-attribute-training`;
- `inventory_seed_revision=thorne-estate-inventory-v1`;
- wealthy food reserve migration applied exactly once;
- autonomy enabled/normal, paused false, speed 1.0;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram connected.

## Completed runtime/profile foundations

- schema v4 composable runtime foundation — complete; operationally extended by schema v5 inventory stack persistence;
- P0/P0.5 foundation + dynamic provider layer — complete;
- P1 continuous autonomy — live;
- P2 Telegram Observer/Profile/Control — deployed;
- P2.3 Creator AI Control v1 — deployed/Creator-exercised;
- Runtime Cognition Fallback v1 — deployed/Creator-configured;
- Telegram Home lifecycle — deployed;
- Universal Character Engine — deployed;
- Dynamic Resource Awareness / Choice Breadth — deployed;
- Object Familiarity / Inspect Utility Guard — deployed;
- fatigue/recovery, targeted training, readiness/effectiveness/effective load — deployed;
- Minimum Training Stimulus + Session Load/Recovery Guard — deployed;
- causal needs + sleep/circadian behavior — deployed;
- Training Method Semantics v1 — deployed;
- Physical Attribute Progression Framework v1 — deployed for Strength, Stamina, Agility, Speed, Reflexes, Endurance, Flexibility.

## Body Composition Program — ACTIVE

Canonical:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/INVENTORY_ITEM_ARCHITECTURE.md`
- `docs/INVENTORY_OPERATIONS_V1.md`
- `docs/EATING_BEHAVIOR_V1.md`

Research direction remains:
- no static universal `3500 kcal = 1 lb` law;
- later engine couples Weight/FM/FFM/BF% over bounded intervals;
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

## Universal Item & Inventory Program

Core invariant:
`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

### Inventory Foundation v1

**COMPLETE / DEPLOYED** via PR #71 / Deploy #177.

- schema v5 normalized `inventory_stacks`;
- universal food definitions;
- concrete Estate stacks;
- fixed container metadata;
- `stored_in` and `owned_by` separation;
- deterministic decrement + quantity-scaled nutrition;
- ordinary init/deploy never refills changed stock.

### Inventory Operations v1

**COMPLETE / DEPLOYED** via PR #73 / Deploy #178.

- one-time wealthy-Estate food reserve while external economy/purchasing is absent;
- universal inventory query scopes for arbitrary locations, characters, containers and all stocks;
- Telegram Inventory is universe-wide, not Darian/Estate hardcoded;
- authorized users browse read-only;
- only Telegram Owner/Creator may replenish;
- typed existing-stack positive replenishment with confirmation + audit;
- no simulation-time advance, ownership/container rewrite, arbitrary SQL or LLM call.

This is one explicit baseline migration, **not recurring auto-restock**. After marker application, ordinary re-init/deploy preserves depletion.

### Food Nutrition Semantics & Visibility v1

**COMPLETE / DEPLOYED** via PR #74 / Deploy #179.

Invariant:
`universal food definition + requested/default portion -> deterministic nutrient facts`

Deployed:
- reusable definition-scoped nutrition projection;
- deterministic kcal/protein/carbohydrate/fat scaling;
- Telegram stack detail displays Nutrient Facts for the authored default portion;
- no schema change, inventory mutation, new nutrition values or LLM call.

Regression examples:
- cooked chicken breast 200 g -> 330 kcal / 62 g protein / 0 g carbs / 7.2 g fat;
- apple 1 piece -> 95 kcal / 0.5 g protein / 25 g carbs / 0.3 g fat.

## Eating Behavior v1 — CURRENT CANDIDATE PR #76

Canonical: `docs/EATING_BEHAVIOR_V1.md`.

Invariant:
`local eat capability + reachable inventory food stacks + structured quantities -> deterministic validation -> atomic stock decrement + immutable combined nutrition evidence`

Implemented candidate:
- live cognition schema now carries a required `resources` array;
- `eat` chooses one to six exact inventory stack IDs plus bounded quantities; non-eat actions require `resources=[]`;
- cognition receives deterministic stock/default-portion/min/max/macronutrient context but never owns macro arithmetic;
- v1 portion guardrail is 0.5x–2x authored default, stock-capped, with whole-number piece quantities;
- direct local inventory wins; an eat-capable room with no direct stack may use the nearest enclosing structural inventory scope, preserving site provisioning without global remote consumption;
- structured resources persist in existing `action_instances.resources_json`; no schema v6;
- completion revalidates and atomically decrements all selected stacks in the same SQLite completion transaction;
- combined definition-based kcal/protein/carbs/fat snapshots into the existing BC-1 `nutrition_intake` event field;
- any failed resource/stock validation rolls back the whole action completion rather than partially consuming food;
- already-persisted pre-v1 empty-resource eat actions may finish via legacy target-based BC-1 evidence without inventory decrement; newly planned eats fail closed without resources;
- Telegram `CHARACTER UPDATE` for a structured meal shows consumed food quantities and combined kcal/P/C/F;
- synthetic non-Estate inventory regression proves the meal-resource engine is not Darian/Estate-specific.

Candidate evidence before canonical-doc tail:
- CI #652 SUCCESS;
- Eating Behavior v1 Acceptance #3 SUCCESS on disposable production copy;
- Nutrition & Energy Evidence v1 Acceptance #6 SUCCESS;
- acceptance uses no model/Telegram calls and never mutates production;
- production-copy structured settlement is verified rollback-safe.

After docs synchronization, rerun final-head gates before merge/deploy.

### Natural intake readiness gate — NEXT AFTER EATING BEHAVIOR DEPLOYS

Do **not** jump straight to BC-2.

Observe natural production read-only and verify:
- model-selected meals are actually using structured resources;
- meal cadence and portions are plausible;
- daily kcal/protein/macros are plausible for the actor/context;
- inventory decreases match completed structured meal evidence;
- BC-1 expenditure coverage remains adequate;
- no repeated decision/schema/backoff failure emerges from the larger meal-resource cognition context.

Never force a production meal merely to manufacture acceptance evidence. If natural cadence is wrong, fix the smallest behavior/needs bridge rather than hiding it with implausible meal sizes.

### BC-2 — Body Composition Progression Exemplar

Only after readiness passes:
- coupled `body.weight_lb` + `body.body_fat_pct` actor-generic mutation;
- consistent FM/FFM/BMI derivation;
- bounded energy partition + separate RT lean adaptation;
- protein/energy/training/genetic headroom constraints;
- evidence-supported age/sex effects only;
- no retroactive activation gains/losses;
- atomic profile history/audit;
- implausible-window guards;
- no Darian branch or extra model calls.

### BC-3 — Body Measurement Progression Batch

After BC-2. Circumferences combine composition, regional training/anatomy and character-specific structural/genetic envelopes rather than body weight alone.

## Future universal object/inventory expansion

Proceed by family:
1. consumable definitions/stacks — foundation complete;
2. movable containers + carried inventory;
3. fixed storage capacity semantics;
4. training equipment definitions + concrete Estate instances;
5. tools/electronics/books/medical supplies;
6. clothing/equipped-state;
7. materials/crafting when justified;
8. economy: ownership transfer, vendors, pricing, currency/accounts, transactions, scarcity/replenishment.

The inventory explorer/control backend remains shared for all future entities. A future shop, character, warehouse or backpack must not require a new named inventory subsystem.

## Later profile sequence

1. finish Eating Behavior v1 PR #76 -> merge/deploy/readback;
2. natural intake/energy readiness gate;
3. BC-2 body composition;
4. BC-3 measurements;
5. skill progression family;
6. intellectual attributes;
7. mental/emotion dynamics;
8. later relationship/social/sexual physiology as prerequisites mature.

## Deferred boundaries

Do not add as side effects:
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

Finish PR #76 canonical synchronization -> rerun final-head CI + Eating Behavior v1 Acceptance + Nutrition & Energy Evidence v1 Acceptance -> merge -> deploy/readback -> sync `test`.

Then perform the **natural intake readiness gate** read-only. Do not activate BC-2 weight/BF mutation until natural structured intake/expenditure passes readiness.
