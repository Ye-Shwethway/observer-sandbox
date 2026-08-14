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

## Current production checkpoint

Latest runtime deployment before the inventory-v5 candidate: **Deploy #176 `31789221876` SUCCESS**, PR #70 merge `5d00003166ab5cf93a5bbc764cc6105219e9dce0`.

Last detailed readback established:
- service healthy;
- schema v4;
- world `thorne-estate-v3.3-physical-attribute-training`;
- default actor `char_darian`;
- autonomy enabled / normal, paused false, retry null;
- speed `1.0x`;
- primary Gemini `gemini-3.1-flash-lite`;
- fallback Groq `qwen/qwen3.6-27b`;
- Telegram connected;
- decision calls 356 at the readback boundary;
- Darian sleeping in Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

Creator observed the Telegram bot boot after Deploy #176. Re-read live production after PR #71 deploy; do not infer newer detailed physiology from the boot notification alone.

## Universal Character Engine

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.
Canonical contract: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

Darian is exemplar content, not reusable-engine identity. Reusable runtime/cognition/physiology/progression/query/control surfaces are actor/entity-id driven. Multi-character ambiguity fails closed. Another actor cannot silently inherit Darian policy. Missing actor location is invalid state. Synthetic non-Darian regression guards identity leakage.

## AI / Telegram state

P2.3 Telegram Creator AI Control v1, Runtime Cognition Fallback v1 and Telegram Home Lifecycle v1 are deployed.

Primary: Gemini `gemini-3.1-flash-lite`.
Configured fallback: Groq `qwen/qwen3.6-27b`.

CI/deploy does not perform model probes. One eligible provider-layer failure may use one configured fallback; deterministic validation failure never triggers fallback; fallback never rewrites primary.

## Training / physical progression state

Deployed:
- systemic fatigue/recovery;
- targeted training;
- readiness/effectiveness/effective load;
- minimum stimulus and load/recovery guard;
- causal living needs + circadian sleep pressure;
- Training Method Semantics v1;
- Dynamic Resource Awareness / Choice Breadth;
- Object Familiarity / Inspect Utility Guard.

Physical Attribute Progression Framework v1 is complete/deployed. All seven RAPS-PA attributes have active progression: Strength, Stamina, Agility, Speed, Reflexes, Endurance, Flexibility. Flexibility uses a real Mobility & Stretching Area / `mobility_stretching` evidence source.

## Body Composition Program — ACTIVE

Canonical contracts:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/INVENTORY_ITEM_ARCHITECTURE.md`

Evidence decisions:
- no universal `3500 kcal = 1 lb` rule;
- later body engine couples Weight/FM/FFM/BF% over bounded windows;
- sex is baseline/reference context, not a crude hypertrophy multiplier;
- age is context/modifier, not a hard cliff;
- genetics are character-specific potential envelopes;
- abstract hunger/energy scores are not kcal;
- protein/energy availability constrains later lean adaptation;
- expenditure is actor-scaled from resting physiology + authored intensity.

### BC-0 — Simulated Profile Re-seed Safety

**COMPLETE / DEPLOYED** via PR #69 / Deploy #175.
Ordinary re-init/deploy preserves `mode=simulated` profile values; non-simulated seed values remain intentionally updateable.

### BC-1 — Nutrition & Energy Balance Evidence

**COMPLETE / DEPLOYED** via PR #70 / Deploy #176.

BC-1 supplies Mifflin-St Jeor resting-energy reference, Compendium-informed activity intensity, immutable nutrition/expenditure event evidence and bounded coverage-aware aggregation. It does not mutate weight/BF. Production-copy validation showed ~2073 kcal/day REE for the current exemplar and preserved weight/BF with zero model/Telegram calls.

BC-1's direct Estate-object nutrition profiles are transitional compatibility data and should be retired as eating behavior moves onto universal item definitions/stacks.

## Universal Item & Inventory Architecture — CURRENT SLICE

Canonical contract: `docs/INVENTORY_ITEM_ARCHITECTURE.md`.

Core invariant:
`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

An apple is one universal definition everywhere. Estate/shop/backpack holdings are concrete stacks. A future Estate treadmill must be a concrete instance of a reusable equipment definition, not a `Darian's treadmill` definition.

Container semantics:
- fixed/immovable: estate/room storage, refrigerator, pantry, shelf, locker/rack;
- movable: backpack, bag, suitcase, crate, toolbox, medkit;
- moving a movable container logically moves its contents;
- inventory containment, ownership, carriage/equipped state and world location are distinct;
- existing structural `contains` remains world topology/fixture containment and is not mutable inventory state.

### Inventory Foundation v1 / PR #71

Status: **IMPLEMENTED / FINAL CI VERIFIED / PRODUCTION-COPY MIGRATION VERIFIED / MERGE-DEPLOY PENDING**.

The candidate introduces the first justified schema v5 invariant. Schema v4 already had `entity_definitions`, `entities.definition_id`, actions/events/relations, but lacked durable stack quantity/depletion. Schema v5 adds only normalized `inventory_stacks`; it does not create a parallel mini-runtime.

Candidate includes:
- universal food definitions in `config/items.v1.json`;
- concrete Estate stock stacks in `config/worlds/home.inventory.v1.json`;
- fixed container metadata;
- `stored_in` mutable inventory containment;
- `owned_by` ownership;
- deterministic quantity validation/decrement;
- definition-based quantity-scaled nutrition;
- first-seed-only stock quantities: normal initialize/deploy never refills consumed stock.

Initial definitions: apple, banana, cooked chicken breast, cooked white rice, eggs, oats, Greek yogurt, mixed vegetables, olive oil, whey protein powder.

Validation:
- initial CI #617: 220 pass / 1 stale schema-v4 expectation; new inventory tests passed;
- expectation corrected;
- final CI #620 SUCCESS;
- Inventory Foundation Acceptance #1 SUCCESS on disposable production copy;
- production copy migrated v4 -> v5 while preserving sim time, world revision, actor runtime, weight/BF;
- test apples 12 -> consume 2 -> 10 -> reinitialize -> still 10;
- model calls 0, Telegram calls 0, live DB unchanged.

## Next slice after PR #71 deploy — Eating Behavior v1

Do not implement a Darian-specific meal script.

Cognition should see deterministic available food/portion context plus recent intake, hunger/daypart, training/recovery, body-composition goal, preferences/diet constraints and convenience. Character policy controls priorities; universal food semantics stay universal.

The model proposes a structured food/portion intent. Deterministic inventory/nutrition code validates stock, decrements quantity, calculates nutrients and emits immutable evidence. The model never owns macro arithmetic or inventory mutation.

After Eating Behavior v1 deploy, observe natural intake/expenditure read-only. If meal cadence and evidence coverage are physiologically plausible, proceed to BC-2. If not, fix the smallest causal meal-behavior bridge; do not hide sparse eating by inflating one generic meal.

## Later body/object roadmap

After the natural evidence gate:
1. BC-2 coupled Weight/BF/FM/FFM progression exemplar;
2. BC-3 body measurement batch;
3. skill progression family;
4. intellectual/mental/emotion families as causal prerequisites mature.

Universal object migration proceeds by family, not as a side effect of the current body slice:
1. consumables (current exemplar);
2. movable containers / carried inventory;
3. fixed storage capacity semantics;
4. training equipment definitions + existing Estate instances;
5. tools/electronics/books/medical supplies;
6. clothing/equipment;
7. crafting/materials only when needed;
8. economy: vendors/prices/currencies/transactions/scarcity.

## Exact resume point

Finish **PR #71**: final docs head validation -> merge -> automatic Deploy/readback -> synchronize `test` to `main`.

Then implement **Eating Behavior v1**. Do not activate BC-2 weight/BF mutation until natural definition-based intake/expenditure evidence passes the readiness gate.

Do not add full Character Memory, multi-fallback/circuit-breaker systems, full RPG inventory UI/encumbrance, arbitrary container nesting, spoilage/deep recipes, all-object migration, currency/shops/economy, detailed endocrine/micronutrient simulation, or a second production character merely for testing as side effects.