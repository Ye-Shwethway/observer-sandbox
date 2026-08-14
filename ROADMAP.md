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
- Reusable runtime/cognition/progression/query/control/inventory logic is entity-id driven.
- Universal definition and concrete instance are distinct; ownership, storage, carriage/equipped state and physical location remain separate.
- Prefer minimum-runnable reversible slices.
- New invariant: one bounded exemplar; structurally equivalent follow-ons batch by pattern.
- Default flow: `test -> focused tests + CI -> merge main -> deploy if runtime-affecting -> read-only production check -> sync test`.
- State-sensitive migrations use disposable production-copy validation.
- Never accelerate/directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest live runtime deployment before the current PR: **Deploy #177 `31791851792` SUCCESS**, PR #71 merge `73ec29e8d97a168fa81af85f8a223692f9adfbad`.

Verified:
- healthy/service active;
- schema v5;
- world `thorne-estate-v3.3-physical-attribute-training`;
- `inventory_seed_revision=thorne-estate-inventory-v1`;
- default actor `char_darian`;
- autonomy enabled/normal, paused false, retry null, speed 1.0;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram connected;
- decision calls 356;
- Darian sleeping in Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

Post-merge CI #624 succeeded. No forced action, production acceleration or model probe was used for Deploy #177 acceptance.

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

Foundation production-copy migration originally proved v4 -> v5 with sim/world/actor/profile preservation and stock no-refill semantics.

### Inventory Operations v1 — CURRENT CANDIDATE

PR #73 current implementation candidate before canonical-doc tail: `63dc759f1bfac3406135a051d1a4feb91eca98fe`.

Purpose: make inventory operational while keeping it universal.

Implemented:
- one-time wealthy-Estate food reserve migration while external economy/purchasing is absent;
- universal inventory query scopes for arbitrary **locations, characters, containers and all stocks**;
- Telegram Inventory is universe-wide, not Darian/Estate hardcoded;
- synthetic non-Estate market and non-Darian character + movable backpack regressions;
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

Candidate validation before docs synchronization:
- CI #629 SUCCESS — 230 tests passed; fresh schema-v5 init/status green;
- Inventory Foundation Acceptance #7 SUCCESS;
- Inventory Operations Acceptance #3 SUCCESS on disposable production copy.

Production-copy evidence:
- live source opened read-only/query-only and never mutated;
- schema 5 -> 5;
- sim time/world revision/actor runtime/body weight/BF preserved;
- reserve migration brought apples to 120 on the copy;
- test reduction 120 -> 113, then ordinary re-init remained 113;
- typed Creator replenish +24 -> 137;
- physical location resolved generically to Estate Kitchen;
- model calls 0; Telegram API calls 0.

## Eating Behavior v1 — NEXT AFTER INVENTORY OPERATIONS DEPLOYS

Do not implement a Darian-specific meal script.

Cognition receives deterministic food availability/portion context plus hunger/daypart, recent intake, energy/protein context, training/recovery, body-composition goal, preferences/diet constraints and convenience context. Character policy controls priorities; food semantics remain universal.

The model proposes structured food/portion intent. Deterministic inventory/nutrition code validates stock, decrements quantities, computes nutrients and persists evidence. The model never owns stock or macro arithmetic.

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

1. Inventory Operations v1 deploy/readback;
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

Finish PR #73 canonical-doc synchronization -> rerun final-head CI + both inventory acceptances -> merge -> deploy/readback -> sync `test` to `main`.

Then **Eating Behavior v1** is the next minimum-runnable slice. Do not activate BC-2 weight/BF mutation before natural definition-based intake/expenditure passes readiness.
