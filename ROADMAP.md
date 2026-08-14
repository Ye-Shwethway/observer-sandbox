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

Latest live runtime deployment: **Deploy #178 `31801236464` SUCCESS**, PR #73 merge `9d1e3f77f62d5e9a044788dee089e6bcbba6bf77`.

Verified:
- healthy/service active;
- schema v5;
- world `thorne-estate-v3.3-physical-attribute-training`;
- `inventory_seed_revision=thorne-estate-inventory-v1`;
- wealthy food reserve migration applied exactly once;
- default actor `char_darian`;
- autonomy enabled/normal, paused false, retry null, speed 1.0;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram connected;
- decision calls 356;
- Darian sleeping in Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

Post-merge CI #642 succeeded. No forced action, production acceleration or model probe was used for Deploy #178 acceptance. `main` and reusable `test` were synchronized at the merge checkpoint.

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

Wealthy Estate reserve minimums:
- apples 120 pieces;
- bananas 90 pieces;
- cooked chicken 30 kg;
- cooked rice 36 kg;
- eggs 240;
- oats 15 kg;
- Greek yogurt 16 kg;
- mixed vegetables 30 kg;
- olive oil 8 kg;
- whey protein 10 kg.

This is one explicit baseline migration, **not recurring auto-restock**. After marker application, ordinary re-init/deploy preserves depletion.

Verified final evidence:
- PR final CI #641 SUCCESS;
- Inventory Foundation Acceptance #19 SUCCESS;
- Inventory Operations Acceptance #15 SUCCESS;
- merge `9d1e3f77f62d5e9a044788dee089e6bcbba6bf77`;
- post-merge CI #642 SUCCESS;
- Deploy #178 SUCCESS with live reserve marker, preserved sim/runtime/body/cognition state and Telegram API connectivity.

## Food Nutrition Semantics & Visibility v1 — CURRENT PR #74

Purpose: expose already-authored universal food nutrition semantics before building natural eating decisions.

Invariant:
`universal food definition + requested/default portion -> deterministic nutrient facts`

Current candidate:
- reusable definition-scoped nutrition projection in `nutrition_facts.py`;
- no stock/location/character identity in nutrition arithmetic;
- default portion falls back to the authored nutrition basis when needed;
- canonical unit and nutrition unit must agree;
- deterministic kcal/protein/carbohydrate/fat scaling;
- Telegram stack detail displays **Nutrient Facts · Default Portion** with serving, energy, protein, carbs, fat and authored basis;
- facts remain viewable independently of current stock quantity;
- no schema change, inventory mutation, new nutrition values or LLM call.

Examples under regression:
- cooked chicken breast default 200 g -> 330 kcal / 62 g protein / 0 g carbs / 7.2 g fat from the universal 100 g basis;
- apple default 1 piece -> 95 kcal / 0.5 g protein / 25 g carbs / 0.3 g fat.

Candidate validation before canonical-doc tail:
- CI #643 SUCCESS;
- Inventory Operations Acceptance #16 SUCCESS.

This slice does **not** yet add meal selection, multi-item meal plans, portion bounds, satiety calibration or stock consumption behavior. Those belong to Eating Behavior v1.

## Eating Behavior v1 — NEXT AFTER PR #74 DEPLOYS

Do not implement a Darian-specific meal script.

Cognition receives deterministic food availability/portion context plus hunger/daypart, recent intake, energy/protein context, training/recovery, body-composition goal, preferences/diet constraints and convenience context. Character policy controls priorities; food semantics remain universal.

The model proposes structured food/portion intent. Deterministic inventory/nutrition code validates stock, decrements quantities, computes nutrients and persists evidence. The model never owns stock or macro arithmetic.

Minimum-runnable direction should support a **multi-food meal resource list** using structured resources/quantities, atomically validated/consumed by the engine. Portion constraints must be deterministic and definition/policy based rather than generated free-form by the model.

### Natural intake readiness gate — before BC-2

After Eating Behavior v1 deployment, observe natural production evidence read-only. Verify plausible meal cadence/intake, complete definition-based nutrition evidence and plausible expenditure coverage. Fix the minimum behavior bridge if needed; never hide a cadence defect by inflating one generic meal.

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

1. Food Nutrition Semantics & Visibility v1 deploy/readback;
2. Eating Behavior v1;
3. natural intake/energy readiness gate;
4. BC-2 body composition;
5. BC-3 measurements;
6. skill progression family;
7. intellectual attributes;
8. mental/emotion dynamics;
9. later relationship/social/sexual physiology as prerequisites mature.

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

Finish PR #74 canonical-doc synchronization -> rerun final-head CI + Inventory Operations Acceptance -> merge -> deploy/readback -> sync `test` to `main`.

Then **Eating Behavior v1** is the next minimum-runnable slice. Do not activate BC-2 weight/BF mutation before natural definition-based intake/expenditure passes readiness.
