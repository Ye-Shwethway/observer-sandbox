# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-14

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
`test -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check -> sync test`

Keep persistent `main` + reusable `test`. Use disposable production-copy validation for state-sensitive migrations. Never accelerate/mutate production merely to manufacture acceptance evidence.

Any new architecture/control invariant updates its canonical contract + ROADMAP + bootstrap in the same development cycle.

## Current verified production checkpoint

Latest live runtime deployment: **Deploy #178 `31801236464` SUCCESS**, PR #73 merge `9d1e3f77f62d5e9a044788dee089e6bcbba6bf77`.

Readback:
- healthy/service active;
- schema v5;
- world `thorne-estate-v3.3-physical-attribute-training`;
- `inventory_seed_revision=thorne-estate-inventory-v1`;
- wealthy reserve migration marker applied once;
- default actor `char_darian`;
- autonomy enabled/normal, paused false, retry null, speed 1.0;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram connected;
- decision calls 356;
- Darian sleeping in Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

Post-merge CI #642 succeeded. No production acceleration, forced action or model probe was used for Deploy #178 acceptance. `main` and reusable `test` were synchronized at this checkpoint.

## Universal character invariant

Darian is exemplar content, never reusable-engine identity. Runtime/cognition/physiology/progression/query/control/inventory/nutrition surfaces are actor/entity/definition-id driven. Multi-character ambiguity fails closed; another actor cannot silently inherit Darian policy. Synthetic non-Darian regressions guard identity leakage.

## Current AI / Telegram

Creator AI Control v1, one-fallback Runtime Cognition, Telegram Home lifecycle and generic observer surfaces are deployed.

Telegram is an adapter, not a simulation engine. It must not own SQLite/world/inventory mutations. Owner and Allowed-user roles remain separate; every mutation rechecks authorization server-side.

## Physical/body progression

Deployed:
- fatigue/recovery;
- targeted training/readiness/effectiveness/effective load;
- Minimum Training Stimulus + Session Load/Recovery Guard;
- causal needs + circadian sleep pressure;
- Training Method Semantics;
- all seven RAPS-PA progression fields: Strength, Stamina, Agility, Speed, Reflexes, Endurance, Flexibility.

BC-0 simulated profile reseed safety is deployed via PR #69 / Deploy #175.
BC-1 Nutrition & Energy Evidence is deployed via PR #70 / Deploy #176. BC-1 does not mutate weight/BF.

## Universal Item & Inventory Architecture

Canonical:
- `docs/INVENTORY_ITEM_ARCHITECTURE.md`
- `docs/INVENTORY_OPERATIONS_V1.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`

Invariant:
`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

- apple/chicken/rice/etc. semantics are universal definitions;
- home/shop/backpack holdings are concrete stacks/instances;
- future training equipment follows reusable definition + concrete instance;
- `contains`, `stored_in`, `owned_by`, `carried_by`, `equipped_by`, `located_at` are distinct semantics;
- fixed containers and movable containers share the same inventory model;
- moving a movable container logically moves contents;
- ordinary initialize/deploy never refills changed stock.

### Inventory Foundation v1

**COMPLETE / DEPLOYED** via PR #71 / Deploy #177.

Schema v5 adds normalized `inventory_stacks` to the existing generic graph/entity model. Universal food definitions, Estate stacks, fixed-container metadata, deterministic decrement and quantity-scaled nutrition are live.

### Inventory Operations v1

**COMPLETE / DEPLOYED** via PR #73 / Deploy #178.

Critical Creator invariant: Telegram Inventory is **not** a Darian's-Estate inventory page. Creator/authorized observers browse inventory related to any location, any character, any fixed/movable container and all stocks in the universe.

Canonical hierarchy:
`Inventory -> Locations | Characters | Containers | All Stocks -> Scope -> Stack`

Darian's Estate is first production exemplar only. Query/control backend takes stable entity/stack ids.

Deployed:
- one-time Creator-approved wealthy-Estate food reserve while economy/purchasing is absent;
- generic universe-wide inventory scopes;
- Telegram `/start -> Inventory` and `/inventory`;
- authorized users browse read-only;
- Owner-only stack replenishment with confirmation;
- typed `/replenish <stack_id> <positive_quantity>`;
- `creator_inventory_replenished` audit event;
- no direct Telegram SQL, no LLM mutation, no simulation-time advance;
- no schema v6.

Wealthy reserve minimums:
- apples 120 pieces; bananas 90;
- cooked chicken 30 kg; cooked rice 36 kg;
- eggs 240; oats 15 kg;
- Greek yogurt 16 kg; mixed vegetables 30 kg;
- olive oil 8 kg; whey protein 10 kg.

This is a **one-time migration**, not recurring restock. Durable marker prevents reapplication; later depletion stays depleted unless an explicit Creator/economy operation changes it.

Final evidence:
- PR CI #641 SUCCESS;
- Inventory Foundation Acceptance #19 SUCCESS;
- Inventory Operations Acceptance #15 SUCCESS;
- merge `9d1e3f77f62d5e9a044788dee089e6bcbba6bf77`;
- post-merge CI #642 SUCCESS;
- Deploy #178 SUCCESS.

## Food Nutrition Semantics & Visibility v1 — CURRENT PR #74

Purpose: expose universal food nutrient facts before natural eating behavior is allowed to depend on them.

Invariant:
`universal food definition + requested/default portion -> deterministic nutrient facts`

Candidate behavior:
- reusable definition-scoped nutrition projection;
- no character/location/stock identity in nutrient arithmetic;
- default serving comes from `default_portion_quantity`, falling back to the authored nutrition basis;
- unit mismatch fails explicitly;
- deterministic energy/protein/carbohydrate/fat scaling;
- Telegram item detail shows `NUTRIENT FACTS · DEFAULT PORTION` with serving, kcal, protein, carbs, fat and basis;
- facts are definition facts and remain viewable regardless of current stack quantity;
- no schema change, new nutrition values, stock mutation, body mutation or LLM call.

Regression examples:
- cooked chicken breast default 200 g -> 330 kcal / 62 g protein / 0 g carbs / 7.2 g fat;
- apple default 1 piece -> 95 kcal / 0.5 g protein / 25 g carbs / 0.3 g fat.

Candidate evidence before docs tail:
- CI #643 SUCCESS;
- Inventory Operations Acceptance #16 SUCCESS.

## Next slice after PR #74 deployment — Eating Behavior v1

Do not make a Darian-specific meal script.

Cognition receives deterministic food/portion availability plus hunger/daypart, recent intake, protein/energy context, training/recovery, body-composition goal, preferences/diet constraints and convenience. Character policy controls priorities; universal food definitions remain universal.

Model proposes structured food/portion intent. Deterministic inventory/nutrition validates stock, decrements quantities, computes nutrients and records evidence. Model never owns stock or macro arithmetic.

Minimum-runnable direction: structured **multi-food meal resources + quantities**, deterministic portion bounds/validation, atomic stock consumption, combined nutrient evidence, and bounded needs/satiety effects. Do not introduce recipes/cooking/economy as side effects.

After deployment, observe natural production intake/expenditure read-only before BC-2. If cadence is implausible, fix the smallest behavior bridge rather than inflate calories artificially.

## Later sequence

1. finish PR #74 -> merge/deploy/readback/sync;
2. Eating Behavior v1;
3. natural intake readiness gate;
4. BC-2 coupled Weight/BF/FM/FFM progression;
5. BC-3 measurements;
6. skills;
7. intellectual attributes;
8. mental/emotion dynamics;
9. later social/relationship/sexual physiology when causal prerequisites exist.

Universal object migration later proceeds by family: movable containers/carried inventory -> storage capacity -> training equipment definitions/instances -> tools/electronics/books/medical -> clothing/equipped state -> materials/crafting -> economy (ownership transfer, vendors, pricing, currency/accounts, transactions, supply).

## Exact resume point

PR #74 implementation and initial checks are green. Finish canonical-doc synchronization, rerun **final-head CI + Inventory Operations Acceptance**, then merge PR #74, deploy/readback, verify live Telegram nutrient facts and preserved autonomy/cognition/inventory/body state, then sync `test` to `main`.

Do not activate BC-2 before natural Eating Behavior evidence passes readiness. Do not add economy/currency, automatic restocking, full RPG encumbrance, arbitrary deep container nesting, all-object migration, Character Memory or a second production character merely for testing as side effects.
