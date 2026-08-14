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
- For physiology/body systems, reconcile human evidence before freezing formulas; simulation approximations must be documented as policy rather than biological law.
- For world objects, reusable definition and concrete universe instance are distinct identities. Ownership, physical containment and location are separate state.
- Default development: `test -> focused tests + CI -> merge main -> deploy if runtime-affecting -> read-only production check -> sync test`.
- Never accelerate or directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest runtime deployment: **Deploy #176 `31789221876` SUCCESS** from PR #70 merge `5d00003166ab5cf93a5bbc764cc6105219e9dce0`.

The last detailed readback before the inventory-v5 candidate established:
- service active / healthy;
- schema v4;
- world revision `thorne-estate-v3.3-physical-attribute-training`;
- default actor `char_darian`;
- autonomy enabled / normal, `paused=false`, `autonomy_retry=null`;
- speed `1.0x`;
- primary Gemini `gemini-3.1-flash-lite` preserved by ordinary bootstrap;
- fallback Groq `qwen/qwen3.6-27b` preserved;
- Telegram connected;
- `decision_calls=356` at readback;
- Darian sleeping in Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

Creator independently observed the Telegram bot boot after Deploy #176. Do not infer newer detailed live physiology from that notification alone; re-read production after the next runtime-affecting merge.

## Completed platform/runtime layers

- Foundation schema v4 — COMPLETE / production baseline through Deploy #176.
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

PR #68 final head `5ebe50d0752790c1abea7ee6d653be8ebd5a1c2e`; merge `3bceda924ed0fe18ce1d1360f6e0cc2c62c55f7e`; CI #608/post-merge #609 plus targeted acceptances green; Deploy #174 success.

All seven core RAPS-PA fields have live progression:
- Strength;
- Stamina;
- Agility;
- Speed;
- Reflexes;
- Endurance;
- Flexibility.

Speed/Reflexes/Endurance/Flexibility use the actor-generic policy-driven framework. Existing Strength/Stamina/Agility implementations remain stable. Flexibility has a real Mobility & Stretching Area and `mobility_stretching` evidence method. Activation never retroactively awards historical gain.

## Grading state

- Strength grading exemplar — COMPLETE / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / DEPLOYED for compatible 0..100 fields.
- IQ remains a separate scale.
- Skills grading/progression remains separate.
- Body composition/measurements are a distinct physiology family.

## Body Composition Progression Program — CURRENT ACTIVE PROGRAM

Canonical research contract: `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`.
Canonical BC-1 contract: `docs/NUTRITION_ENERGY_EVIDENCE.md`.
Canonical item/inventory contract: `docs/INVENTORY_ITEM_ARCHITECTURE.md`.

Creator requirement: realistic human body behavior must consider age, sex, individual genetic potential, nutrition/energy balance and plausible body proportions before formulas are frozen.

### Evidence-led decisions

Research reconciled from NIH/NIDDK Hall/Forbes dynamic body-weight work, resistance-training sex/age response evidence, genetic/inter-individual variability, protein/energy-deficit literature, body-composition references and the 2024 Compendium of Physical Activities.

Locked direction:
- no universal static `3500 kcal = 1 lb` law;
- model weight, FM, FFM and BF% as a coupled system over bounded settlement intervals;
- Hall/Forbes-style partitioning is a documented first-order approximation, not a full human metabolic model;
- sex affects baseline/reference physiology but is not a crude hypertrophy multiplier;
- age is context/modifier, not a hard response cliff;
- genetic potential is character-specific canonical/config data; population FFMI/FMI is plausibility context only;
- kcal/protein cannot be inferred from abstract hunger/energy scores;
- protein/energy availability constrains later lean adaptation;
- action expenditure is actor-scaled using a resting-energy reference plus authored Compendium-informed intensity anchors.

Current profile already declares `body.weight_lb`, `body.body_fat_pct`, derived `body.lean_mass_lb`, `body.fat_mass_lb`, `body.bmi`, canonical DOB/sex/height, and genetic lean-condition weight range/body-fat floor.

### BC-0 — Simulated Profile Re-seed Safety

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #69:
- tested head `2a23ff48207867a6684832b8fefdd260053eac78`;
- CI #610 SUCCESS;
- merge `e407533eff098f5803cc17469e8b9da8c24c21b8`;
- post-merge CI #611 SUCCESS;
- Deploy #175 SUCCESS.

Invariant: ordinary canonical seed import initializes inactive fields but preserves existing `mode=simulated` value/mode/authority/source. Non-simulated canonical/static fields remain intentionally seed-updatable.

### BC-1 — Minimum Nutrition & Energy Balance Evidence

Status: **COMPLETE / CI VERIFIED / PRODUCTION-COPY VALIDATED / DEPLOYED**.

PR #70:
- final head `bdc6e117074e961b7b21c01dc9d42181d11c6e89`;
- final CI #615 SUCCESS;
- final Nutrition & Energy Evidence Acceptance #3 SUCCESS;
- merge `5d00003166ab5cf93a5bbc764cc6105219e9dce0`;
- Deploy #176 SUCCESS.

Implementation:
- authored kcal/protein/carbohydrate/fat evidence;
- Mifflin-St Jeor actor-specific resting-energy reference;
- Compendium-informed action/training intensity anchors;
- immutable `nutrition_intake` and `energy_expenditure` event evidence;
- bounded `energy_balance_window()` with coverage/missing-evidence guard;
- historical pre-BC-1 actions are not silently recomputed;
- BC-1 never mutates weight or body fat.

Production-copy evidence on Darian-shaped live state showed about `2073.388 kcal/day` REE, an `800 kcal / 50 g protein` prepared meal, about `53.994 kcal` expenditure for the 25-minute eat action, unchanged weight/BF, zero model/Telegram calls and no live DB mutation.

BC-1 direct Estate-object nutrition profiles are now explicitly transitional. Definition-based item nutrition supersedes them as eating behavior migrates to inventory stacks.

## Universal Item & Inventory Program

Canonical contract: `docs/INVENTORY_ITEM_ARCHITECTURE.md`.

### Architecture invariant

`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

- An apple is one universal definition everywhere; Darian, a shop or a backpack may hold different concrete stacks of the same definition.
- A concrete treadmill at Thorne Estate eventually references a reusable treadmill/equipment definition; there is no `Darian's treadmill` definition.
- Structural world `contains` remains authored topology/containment and is not reused as mutable inventory state.
- Dynamic inventory containment, ownership, carriage and equipment state remain distinct semantics.

### Fixed and movable containers

Fixed/immovable container examples:
- estate/house/room storage space;
- refrigerator;
- pantry;
- supply shelf;
- locker / armory rack.

Movable container examples:
- backpack;
- bag;
- suitcase;
- crate;
- toolbox / medical kit.

A movable container carries its contained inventory with it logically. Container nesting must be bounded and cycle-free. Ownership does not imply physical possession, and carriage does not imply ownership.

### Inventory Foundation v1 — CURRENT SLICE

Status: **IMPLEMENTED ON PR #71 / CI VERIFIED / PRODUCTION-COPY MIGRATION VERIFIED / MERGE-DEPLOY PENDING**.

Schema v5 is now justified by a concrete missing persistence invariant: schema v4 had reusable `entity_definitions`, concrete `entities.definition_id`, generic relations/events/actions, but no durable quantity/depletion record for item stacks. The v5 candidate adds only normalized `inventory_stacks`; it does not create a parallel world model.

Candidate implementation:
- `config/items.v1.json`: universal food definitions with canonical unit/portion/nutrition semantics;
- `config/worlds/home.inventory.v1.json`: concrete Estate stock stacks and fixed storage containers;
- `inventory_stacks`: quantity + unit + seed metadata;
- stack entities reference reusable `entity_definitions`;
- mutable inventory containment uses `stored_in`;
- legal/economic ownership uses `owned_by`;
- deterministic quantity validation/decrement;
- definition-based nutrition scales by consumed quantity;
- depleted stacks remain identifiable at quantity zero;
- ordinary initialize/deploy does **not** replenish a live stack: seed quantity is first-install data only.

Initial universal food exemplar set includes apple, banana, cooked chicken breast, cooked white rice, eggs, oats, Greek yogurt, mixed vegetables, olive oil and whey protein powder. Estate stock is concrete inventory content; the definitions are not Estate-specific.

Validation on PR #71:
- initial CI #617 found only one stale `schema_version == 4` test expectation; all new inventory tests passed;
- stale expectation corrected to v5;
- final-head CI #620 SUCCESS;
- Inventory Foundation Acceptance #1 SUCCESS on a disposable live production copy;
- production copy migrated schema v4 -> v5 while preserving sim time, world revision, actor runtime, weight and BF;
- 12 seeded apples -> consume 2 -> 10, then reinitialize -> still 10 (no refill regression);
- model calls 0; Telegram calls 0; live production DB unchanged.

### Eating Behavior v1 — NEXT AFTER INVENTORY DEPLOY

Do not turn food choice into a hardcoded Darian meal script.

Cognition should receive deterministic food availability/portion context and may consider:
- hunger and time/daypart;
- recent intake and meal cadence;
- estimated energy/protein context;
- training/recovery state;
- body-composition goal;
- preferences/aversions/dietary constraints;
- cooking/convenience context;
- available stock;
- later budget/cost when economy exists.

Character policy controls priorities. Darian may naturally prioritize protein/recovery because he is fitness-oriented; chicken/apple/rice semantics remain universal definitions.

The model proposes a structured food/portion intent. Deterministic inventory/nutrition code validates quantity, decrements stock, calculates nutrient totals and records immutable evidence. The model never performs authoritative macro arithmetic or stock mutation.

### Natural intake readiness gate — REQUIRED BEFORE BC-2

After Inventory Foundation and Eating Behavior v1 deploy:
- observe ordinary production behavior read-only;
- verify meal cadence is plausible;
- verify daily intake/protein context is not an artifact of the old hunger loop;
- verify naturally selected foods have complete definition-based nutrition evidence;
- verify expenditure coverage/magnitudes remain plausible;
- do not hide sparse eating by inflating calories in one generic meal.

### BC-2 — Body Composition Progression Exemplar

Only after the readiness gate passes:
- activate coupled `body.weight_lb` + `body.body_fat_pct` through one actor-generic deterministic engine;
- derive FM/FFM/BMI consistently;
- aggregate causal definition-based nutrition, expenditure and training evidence over bounded windows;
- use bounded FM/FFM partitioning rather than one fixed tissue ratio;
- model resistance-training lean adaptation separately, constrained by training evidence, protein/energy availability, training state and personalized genetic headroom;
- no crude sex hypertrophy multiplier;
- age/sex enter only where evidence supports them;
- bootstrap at activation boundary without retroactive gain/loss;
- write coupled fields atomically with profile history/audit event;
- clamp/reject implausible single-window changes;
- no Darian-specific branch and no extra model calls.

### BC-3 — Body Measurement Progression Batch

Only after BC-2 is live/validated. Circumferences must combine composition, regional training/anatomy and character-specific structural/genetic envelopes; do not derive every circumference from body weight alone.

## Future universal object migration

Do not migrate every Estate object as a side effect of the body-composition prerequisite. Once the inventory/item invariant is deployed, follow exemplar-first then batch-by-pattern:

1. consumable food/drink definitions + stacks — current exemplar;
2. movable containers + carried inventory;
3. fixed storage fixtures/capacity semantics where needed;
4. training equipment definitions + existing Estate instances;
5. tools/electronics/books/medical supplies;
6. clothing/equipment/equipped-state surfaces;
7. material/crafting inputs only when a concrete gameplay need exists;
8. economy: ownership transfer, vendors, pricing, currencies, transactions, scarcity/replenishment.

Economic value is state/context, not item identity. The same universal apple may have different owners, locations, prices and availability over time.

## Planned profile/system unlock sequence

1. Inventory Foundation v1 merge/deploy/readback;
2. Eating Behavior v1;
3. natural intake/energy evidence readiness gate;
4. BC-2 body composition exemplar;
5. BC-3 body measurement batch;
6. skill progression exemplar;
7. compatible skill batch;
8. intellectual attribute exemplar/batch;
9. mental/emotion dynamics;
10. later social/relationship/sexual physiology families as causal prerequisites exist.

## Deferred boundaries

Do not add as side effects of the current minimum foundation:
- full Character Memory Engine;
- multi-fallback/circuit-breaker/provider-health systems;
- Telegram secret/model-parameter editing;
- second production character solely for testing;
- forced equipment rotation;
- full RPG inventory UI or encumbrance;
- spoilage/expiration and deep recipe/cooking graph;
- arbitrary deep nested containers;
- migration of every existing Estate object in the consumable exemplar;
- currency/shops/vendor/economy simulation;
- generalized crafting;
- detailed endocrine or menstrual-cycle/hormone engine;
- micronutrient or organ-by-organ metabolic simulation;
- exact fluid/glycogen fluctuation model;
- richer relationship engine;
- estate exterior/Tahoe traversal.

## Exact resume point

Finish **PR #71 Inventory Foundation v1**: canonical docs sync -> final-head CI + production-copy acceptance -> merge -> automatic Deploy/readback -> synchronize `test` to `main`.

Then implement **Eating Behavior v1** as the next minimum-runnable slice. Only after natural definition-based intake/expenditure evidence is plausible should BC-2 weight/BF mutation be activated.