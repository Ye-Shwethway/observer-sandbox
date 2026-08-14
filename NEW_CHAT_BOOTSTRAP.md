# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-14

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical contracts/source files
5. current live production evidence before implementation decisions

Current Creator instruction and newer repository/CI/deploy/live-runtime evidence override older chat memory.

## Development workflow

Default flow:
`test -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check -> sync test`

Keep only persistent `main` and reusable `test` branches unless an exceptional need is concrete. Production-copy validation is reserved for state-sensitive/migration work. Never accelerate or mutate live profile/world/progression merely to manufacture acceptance evidence.

Whenever a slice introduces a new architecture/control invariant, update its canonical contract plus `ROADMAP.md` and this bootstrap in the same cycle.

## Current verified production checkpoint

Latest deployment: **Deploy #177 `31791851792` SUCCESS**, PR #71 merge `73ec29e8d97a168fa81af85f8a223692f9adfbad`.

Deploy #177 readback:
- service active / healthy;
- **schema v5**;
- world `thorne-estate-v3.3-physical-attribute-training`;
- `inventory_seed_revision=thorne-estate-inventory-v1`;
- default actor `char_darian`;
- autonomy enabled / normal, paused false, retry null;
- speed `1.0x`;
- primary Gemini `gemini-3.1-flash-lite` preserved;
- fallback Groq `qwen/qwen3.6-27b` preserved;
- Telegram API connected; owner/allowed-user configuration present;
- decision calls 356 at readback;
- Darian remained sleeping in Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

Post-merge CI #624 SUCCESS. No production acceleration, forced action, model probe or direct live profile/body mutation was used.

## Universal Character Engine

Status: **COMPLETE / DEPLOYED**.
Canonical contract: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

Darian is exemplar content, not reusable-engine identity. Reusable runtime/cognition/physiology/progression/query/control surfaces are actor/entity-id driven. Multi-character ambiguity fails closed. Another actor cannot silently inherit Darian policy. Missing actor location is invalid state. Synthetic non-Darian regression guards identity leakage.

## AI / Telegram state

P2.3 Telegram Creator AI Control v1, Runtime Cognition Fallback v1 and Telegram Home Lifecycle v1 are deployed.

Primary: Gemini `gemini-3.1-flash-lite`.
Fallback: Groq `qwen/qwen3.6-27b`.

CI/deploy never deliberately consumes a model probe. One eligible provider-layer failure may use one configured fallback; deterministic action/runtime validation failure never triggers fallback; fallback never rewrites primary.

## Physical progression state

Deployed:
- systemic fatigue/recovery;
- targeted training;
- readiness/effectiveness/effective load;
- minimum stimulus and load/recovery guard;
- causal needs + circadian sleep pressure;
- Training Method Semantics v1;
- Dynamic Resource Awareness / Choice Breadth;
- Object Familiarity / Inspect Utility Guard.

Physical Attribute Progression Framework v1 is complete/deployed. All seven core RAPS-PA fields have active progression: Strength, Stamina, Agility, Speed, Reflexes, Endurance, Flexibility.

## Body Composition Program — ACTIVE

Canonical contracts:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/INVENTORY_ITEM_ARCHITECTURE.md`

Evidence direction:
- no universal `3500 kcal = 1 lb` law;
- later body engine couples Weight/FM/FFM/BF% over bounded windows;
- sex is baseline/reference context, not a crude hypertrophy multiplier;
- age is context/modifier, not a hard cliff;
- genetics are character-specific potential envelopes;
- hunger/energy scores are not kcal;
- protein/energy availability constrains later lean adaptation;
- expenditure is actor-scaled from resting physiology + authored intensity.

### BC-0 — Simulated Profile Re-seed Safety

**COMPLETE / DEPLOYED** via PR #69 / Deploy #175.
Ordinary re-init/deploy preserves engine-owned `mode=simulated` profile values.

### BC-1 — Nutrition & Energy Balance Evidence

**COMPLETE / DEPLOYED** via PR #70 / Deploy #176.

Provides actor-specific Mifflin-St Jeor resting energy, Compendium-informed action intensity, immutable nutrition/expenditure evidence and bounded coverage-aware aggregation. BC-1 does not mutate body weight/BF. Direct Estate-object nutrition profiles are transitional compatibility data now that universal definition-based food semantics exist.

## Universal Item & Inventory Architecture

Canonical contract: `docs/INVENTORY_ITEM_ARCHITECTURE.md`.

Core invariant:
`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

An apple is one universal definition everywhere. Estate/shop/backpack holdings are concrete stacks. Future training equipment follows the same rule: reusable equipment definition + concrete Estate instance, never a `Darian's treadmill` definition.

Container semantics:
- fixed/immovable: home/room storage, refrigerator, pantry, shelf, locker/rack;
- movable: backpack, bag, suitcase, crate, toolbox, medkit;
- moving a movable container logically moves its contents;
- structural `contains`, mutable inventory containment, ownership, carriage/equipped state and dynamic world location are distinct;
- nesting must remain bounded/cycle-free.

### Inventory Foundation v1

**COMPLETE / CI VERIFIED / PRODUCTION-COPY MIGRATION VERIFIED / DEPLOYED**.

PR #71:
- final head `7bd3849b0bf606c40901c83e2847d2bbf716f20f`;
- final CI #623 SUCCESS;
- Inventory Foundation Acceptance #4 SUCCESS;
- merge `73ec29e8d97a168fa81af85f8a223692f9adfbad`;
- post-merge CI #624 SUCCESS;
- Deploy #177 SUCCESS.

Schema v5 is the first justified schema extension beyond v4: reusable definitions/entities already existed, but durable stack quantity/depletion did not. v5 adds normalized `inventory_stacks` and reuses the existing graph/entity model.

Live v5 foundation includes:
- universal food definitions (`config/items.v1.json`);
- concrete Estate stock stacks (`config/worlds/home.inventory.v1.json`);
- fixed storage container metadata;
- `stored_in` mutable inventory containment;
- `owned_by` ownership;
- quantity/unit persistence and deterministic decrement;
- definition-based quantity-scaled nutrition;
- first-seed-only stock quantities: ordinary initialize/deploy never refills consumed stock.

Initial universal foods: apple, banana, cooked chicken breast, cooked white rice, eggs, oats, Greek yogurt, mixed vegetables, olive oil, whey protein powder.

Disposable production migration proved v4 -> v5 while preserving sim time, world revision, actor runtime, weight/BF. Test stock 12 apples -> consume 2 -> 10 -> reinitialize -> still 10. Zero model/Telegram calls; live source DB unchanged.

## Next minimum-runnable slice — Eating Behavior v1

Do not make a Darian-specific meal script.

Cognition should receive deterministic food availability/portion context plus hunger/daypart, recent intake/meal cadence, energy/protein context, training/recovery, body-composition goal, preferences/diet constraints and convenience. Character policy controls priorities; universal food semantics remain universal.

The model proposes a structured food/portion intent. Deterministic inventory/nutrition code validates availability, decrements quantity, calculates nutrients and emits immutable evidence. The model never owns macro arithmetic or stock mutation.

After Eating Behavior v1 deploy, observe natural production intake/expenditure read-only. If meal cadence and coverage are plausible, proceed to BC-2. If not, repair the smallest causal meal-behavior bridge rather than inflating a generic meal's calories.

## Later sequence

1. Eating Behavior v1;
2. natural intake/energy readiness gate;
3. BC-2 coupled Weight/BF/FM/FFM progression exemplar;
4. BC-3 body measurement batch;
5. skill progression family;
6. intellectual attributes;
7. mental/emotion dynamics;
8. later social/relationship/sexual physiology as prerequisites mature.

Universal object migration later proceeds by family:
1. consumables — exemplar complete;
2. movable containers / carried inventory;
3. fixed storage capacity semantics;
4. training equipment definitions + existing Estate instances;
5. tools/electronics/books/medical supplies;
6. clothing/equipped-state;
7. materials/crafting when justified;
8. economy: ownership transfer, vendors, pricing, currency, transactions, scarcity/replenishment.

## Exact resume point

Inventory Foundation v1 is live and repository branches are being returned to a clean synchronized checkpoint. **Next proposed implementation slice is Eating Behavior v1**. Do not activate BC-2 body-weight/BF mutation until natural definition-based intake/expenditure evidence passes the readiness gate.

Do not add full Character Memory, multi-fallback/circuit-breaker systems, full RPG inventory UI/encumbrance, arbitrary deep container nesting, spoilage/deep recipes, all-object migration, currency/shops/economy, detailed endocrine/micronutrient simulation or a second production character merely for testing as side effects.