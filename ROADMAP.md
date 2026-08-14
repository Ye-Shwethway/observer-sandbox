# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-14

## Operating principles

- Python/SQLite runtime and world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutation.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Preserve the composable runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian is the first richly specified exemplar, never reusable-engine identity.
- Character-specific facts/policy/world content are data; reusable simulation/cognition/progression/query/control logic is actor/entity-id driven.
- Prefer minimum-runnable reversible slices.
- Use exemplar-first for genuinely new invariants, then batch structurally equivalent follow-ons.
- For physiology/body systems, reconcile human evidence before freezing formulas; simulation approximations are documented policy, not biological law.
- For world objects, reusable definition and concrete universe instance are distinct identities. Ownership, physical containment and location are separate state.
- Default development: `test -> focused tests + CI -> merge main -> deploy if runtime-affecting -> read-only production check -> sync test`.
- Never accelerate or directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest runtime deployment: **Deploy #177 `31791851792` SUCCESS** from PR #71 merge `73ec29e8d97a168fa81af85f8a223692f9adfbad`.

Deploy #177 readback verified:
- service active / healthy;
- **schema v5**;
- world revision `thorne-estate-v3.3-physical-attribute-training`;
- default actor `char_darian`;
- `inventory_seed_revision=thorne-estate-inventory-v1`;
- autonomy enabled / normal, `paused=false`, `autonomy_retry=null`;
- speed `1.0x`;
- primary Gemini `gemini-3.1-flash-lite` preserved;
- fallback Groq `qwen/qwen3.6-27b` preserved;
- Telegram connected with owner/allowed-user config present;
- cognition `decision_calls=356` at readback;
- Darian remained sleeping in Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

Post-merge CI #624 SUCCESS. No model probe, forced action, production acceleration or direct live-state mutation was used for the inventory deployment.

## Completed platform/runtime layers

- Foundation schema v4 runtime model — COMPLETE; superseded operationally by schema v5 inventory extension.
- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 dynamic AI provider/runtime layer — COMPLETE.
- P1 continuous autonomy — LIVE.
- P2 Telegram Observer/Profile/Control — COMPLETE / LIVE VERIFIED.
- P2.3 Telegram Creator AI Control v1 — COMPLETE / DEPLOYED / CREATOR-EXERCISED.
- Runtime Cognition Fallback v1 — COMPLETE / DEPLOYED / CREATOR-CONFIGURED.
- Telegram Home lifecycle — COMPLETE / DEPLOYED.
- Universal Character Engine Contract — COMPLETE / CI VERIFIED / DEPLOYED.
- Dynamic Resource Awareness / Choice Breadth — DEPLOYED.
- Object Familiarity / Inspect Utility Guard — DEPLOYED.
- P3.1 systemic fatigue/recovery — COMPLETE / LIVE VERIFIED.
- P3.2 targeted training — COMPLETE.
- P3.3 readiness — COMPLETE / DEPLOYED.
- P3.4 effectiveness — COMPLETE / DEPLOYED.
- P3.5 effective training load — COMPLETE / DEPLOYED.
- Minimum Training Stimulus v1 — COMPLETE / DEPLOYED.
- Training Session Load & Recovery Guard v1 — COMPLETE / DEPLOYED.
- Causal living needs + sleep pressure/circadian behavior — DEPLOYED.
- Training Method Semantics v1 — COMPLETE / DEPLOYED.

## Universal Character Engine

Canonical contract: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

Invariant:
- explicit actor -> configured valid default actor -> sole actor resolution;
- ambiguous multi-character implicit selection fails closed;
- another actor cannot inherit Darian cognition policy silently;
- missing location is invalid state, not implicit Master Suite;
- global resume wakes every eligible actor;
- Darian/Thorne named data remains exemplar content only;
- synthetic non-Darian regression guards identity leakage.

## Physical Attribute Progression Framework v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.
Canonical contract: `docs/PHYSICAL_ATTRIBUTE_PROGRESSION_FRAMEWORK.md`.

All seven core RAPS-PA fields have active progression: Strength, Stamina, Agility, Speed, Reflexes, Endurance, Flexibility. Speed/Reflexes/Endurance/Flexibility use the actor-generic policy-driven framework. Flexibility has real `mobility_stretching` evidence. Existing Strength/Stamina/Agility implementations remain stable.

## Body Composition Progression Program — CURRENT ACTIVE PROGRAM

Canonical contracts:
- `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`
- `docs/NUTRITION_ENERGY_EVIDENCE.md`
- `docs/INVENTORY_ITEM_ARCHITECTURE.md`

Creator requirement: realistic human body behavior must consider age, sex, individual genetic potential, nutrition/energy balance and plausible body proportions before formulas are frozen.

Locked research direction:
- no universal static `3500 kcal = 1 lb` law;
- model weight, FM, FFM and BF% as a coupled system over bounded settlement intervals;
- Hall/Forbes-style partitioning is a documented first-order approximation, not a full metabolic model;
- sex affects baseline/reference physiology but is not a crude hypertrophy multiplier;
- age is context/modifier, not a hard response cliff;
- genetic potential is character-specific config/canonical data; population FFMI/FMI is plausibility context only;
- kcal/protein cannot be inferred from abstract hunger/energy scores;
- protein/energy availability constrains later lean adaptation;
- expenditure is actor-scaled from resting physiology + authored Compendium-informed intensity.

### BC-0 — Simulated Profile Re-seed Safety

Status: **COMPLETE / DEPLOYED** via PR #69 / Deploy #175.

Ordinary seed import initializes inactive/non-simulated fields but preserves existing `mode=simulated` values and their authority/source across ordinary re-init/deploy.

### BC-1 — Minimum Nutrition & Energy Balance Evidence

Status: **COMPLETE / DEPLOYED** via PR #70 / Deploy #176.

BC-1 provides:
- Mifflin-St Jeor actor-specific resting-energy reference;
- Compendium-informed action/training intensity anchors;
- immutable nutrition/expenditure event evidence;
- bounded coverage-aware `energy_balance_window()`;
- no retroactive reinterpretation of pre-BC-1 history;
- no body-weight/BF mutation.

Disposable-production validation showed approximately `2073.388 kcal/day` REE for the current exemplar, an `800 kcal / 50 g protein` prepared-meal evidence event and unchanged weight/BF. BC-1 direct Estate-object nutrition profiles are transitional compatibility data and are superseded by definition-based nutrition as Eating Behavior v1 activates.

## Universal Item & Inventory Program

Canonical contract: `docs/INVENTORY_ITEM_ARCHITECTURE.md`.

Core invariant:
`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

- An apple is one universal definition everywhere; a home, shop, character or backpack may hold concrete stacks of that definition.
- A Thorne Estate treadmill eventually becomes a concrete instance of a reusable equipment definition; there is no `Darian's treadmill` definition.
- Structural world `contains` remains authored topology/fixture containment and is not reused as mutable inventory state.
- Inventory containment, ownership, carriage/equipped state and world location remain separate semantics.

### Fixed and movable containers

Fixed/immovable examples:
- estate/room storage;
- refrigerator;
- pantry;
- shelf;
- locker / armory rack.

Movable examples:
- backpack;
- bag / suitcase;
- crate;
- toolbox / medical kit.

Moving a movable container logically moves its contents. Container nesting must remain bounded and cycle-free. Ownership never implies physical possession.

### Inventory Foundation v1

Status: **COMPLETE / CI VERIFIED / PRODUCTION-COPY MIGRATION VERIFIED / DEPLOYED**.

Delivery:
- PR #71 final head `7bd3849b0bf606c40901c83e2847d2bbf716f20f`;
- final CI #623 SUCCESS;
- Inventory Foundation Acceptance #4 SUCCESS on disposable production copy;
- merge `73ec29e8d97a168fa81af85f8a223692f9adfbad`;
- post-merge CI #624 SUCCESS;
- Deploy #177 SUCCESS with live schema v5 readback.

Schema v5 is justified by one concrete missing invariant: schema v4 already had reusable `entity_definitions`, concrete `entities.definition_id`, generic relations/actions/events, but no durable stack quantity/depletion record. v5 adds only normalized `inventory_stacks`; it does not create a parallel world model.

Implemented:
- universal food definitions in `config/items.v1.json`;
- concrete Estate stock in `config/worlds/home.inventory.v1.json`;
- fixed container metadata;
- `stored_in` mutable inventory containment;
- `owned_by` ownership;
- quantity/unit persistence;
- deterministic availability validation and decrement;
- definition-based quantity-scaled nutrition;
- first-seed-only stock: ordinary initialize/deploy does not replenish consumed quantity.

Initial universal food definitions: apple, banana, cooked chicken breast, cooked white rice, eggs, oats, Greek yogurt, mixed vegetables, olive oil and whey protein powder.

Production-copy migration evidence:
- schema v4 -> v5;
- sim time, world revision, actor runtime, weight and BF preserved;
- seeded apples 12 -> consume 2 -> 10 -> reinitialize -> still 10;
- model calls 0; Telegram calls 0; live source DB untouched.

Deploy #177 confirms the production database is now schema v5 with inventory seed revision active while cognition/autonomy/Telegram and current Darian state remain preserved.

## Eating Behavior v1 — NEXT MINIMUM-RUNNABLE SLICE

Do not implement a Darian-specific meal script.

Cognition should receive deterministic food availability/portion context and may consider:
- hunger/daypart;
- recent intake and meal cadence;
- energy/protein context;
- training/recovery state;
- body-composition goal;
- preferences/aversions/dietary constraints;
- cooking/convenience context;
- available stock;
- future budget/cost context when economy exists.

Character policy controls priorities. Darian may naturally prioritize protein/recovery because he is fitness-oriented; chicken/apple/rice semantics remain universal.

The model proposes structured food/portion intent. Deterministic inventory/nutrition code validates quantity, decrements stock, calculates nutrient totals and records immutable evidence. The model never owns macro arithmetic or stock mutation.

### Natural intake readiness gate — REQUIRED BEFORE BC-2

After Eating Behavior v1 deploy:
- observe ordinary production behavior read-only;
- verify meal cadence and total intake are physiologically plausible;
- verify naturally selected foods have complete definition-based nutrition evidence;
- verify expenditure coverage/magnitudes remain plausible;
- do not hide sparse eating by inflating calories in one generic meal.

### BC-2 — Body Composition Progression Exemplar

Only after the readiness gate passes:
- activate coupled `body.weight_lb` + `body.body_fat_pct` through one actor-generic deterministic engine;
- derive FM/FFM/BMI consistently;
- aggregate definition-based nutrition, expenditure and training evidence over bounded windows;
- use bounded FM/FFM partitioning rather than one fixed tissue ratio;
- model resistance-training lean adaptation separately, constrained by training evidence, protein/energy availability, training state and personalized genetic headroom;
- no crude sex hypertrophy multiplier;
- age/sex enter only where supported by evidence;
- bootstrap at activation boundary without retroactive gain/loss;
- write coupled fields atomically with profile history/audit event;
- clamp/reject implausible single-window changes;
- no Darian-specific branch and no extra model calls.

### BC-3 — Body Measurement Progression Batch

Only after BC-2 is live/validated. Circumferences must combine composition, regional training/anatomy and character-specific structural/genetic envelopes; never derive every circumference from body weight alone.

## Future universal object migration

Proceed by family, not one-off rewrites:
1. consumable food/drink definitions + stacks — exemplar complete;
2. movable containers + carried inventory;
3. fixed storage capacity semantics where needed;
4. training equipment definitions + existing Estate instances;
5. tools/electronics/books/medical supplies;
6. clothing/equipment/equipped-state;
7. materials/crafting only when required;
8. economy: ownership transfer, vendors, prices/listings, currencies/accounts, transactions, scarcity/replenishment.

Economic value is context/state, not item identity. The same apple definition may have different owners, locations, prices and availability over time.

## Planned sequence

1. Eating Behavior v1;
2. natural intake/energy readiness gate;
3. BC-2 body composition exemplar;
4. BC-3 body measurement batch;
5. skill progression exemplar + compatible batch;
6. intellectual attribute family;
7. mental/emotion dynamics;
8. later social/relationship/sexual physiology as causal prerequisites mature.

## Deferred boundaries

Do not add as side effects of the current body program:
- full Character Memory Engine;
- multi-fallback/circuit-breaker/provider-health systems;
- Telegram secret/model-parameter editing;
- second production character solely for testing;
- forced equipment rotation;
- full RPG inventory UI/encumbrance;
- spoilage/expiration or deep recipe graph;
- arbitrary deep container nesting;
- all-object migration at once;
- currency/shops/economy simulation;
- generalized crafting;
- detailed endocrine/micronutrient/organ-by-organ metabolic simulation;
- exact fluid/glycogen model;
- richer relationship engine;
- estate exterior/Tahoe traversal.

## Exact resume point

Repository/runtime checkpoint is clean after Inventory Foundation v1. **Next authorized proposal is Eating Behavior v1** under the universal item/inventory contract. After it is deployed, observe natural definition-based intake/expenditure before activating BC-2 weight/BF mutation.