# Observer Sandbox Architecture

## Foundation contract

Observer Sandbox is a small persistent universe built from composable primitives rather than character-specific scripts.

Canonical LEGO runtime expression:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

The LLM may propose a structured action but never receives arbitrary database-write authority. Deterministic runtime validation/application remains authoritative.

## Universal character-engine invariant

Darian Thorne is the first richly specified production exemplar, not the identity embedded in universe rules. Reusable runtime, cognition, physiology, progression, query and control engines operate on actor/entity ids plus domain state and policy. Character-specific facts, preferences, routines and authored cognition policy remain data/configuration.

Canonical detail: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

Implicit actor selection may use a configured valid `default_actor_id`, or the sole existing character while the universe contains exactly one character. If multiple characters exist without a valid default, reusable engine APIs must require an explicit actor id rather than guessing Darian or the first database row.

Named convenience content such as Darian's canonical JSON, Thorne Estate seed data and `/darian` UI aliases may remain character-specific. Those are exemplar/content surfaces, not reusable engine identity.

## Logical world model

Every meaningful thing is an entity node or reusable definition. Typed relations connect entities. The same model must scale from Darian inside one mansion to multiple characters, residences, regions, items and later environment/economic modules.

Core distinctions:

1. **Definitions/Templates** — reusable semantics/defaults (`entity_definitions`, `action_definitions`).
2. **Instances** — concrete universe entities/actions (`entities`, `action_instances`).
3. **Runtime State** — mutable actor/global/item state (`actor_runtime`, fields, relations, `inventory_stacks`, `runtime_state`).
4. **Events** — append-oriented evidence of committed transitions.

A universal definition never includes a character/household identity merely because one current instance belongs there. `item.food.apple` remains the same definition in a home, shop or backpack. A Thorne Estate treadmill eventually becomes a concrete instance of a reusable equipment definition rather than a definition named for Darian or the Estate.

## SQLite schema evolution

### Schema v4 foundation

Schema v4 established the generic graph/profile/provider layer plus:
- `entity_definitions` and `entities.definition_id`;
- action definitions/instances;
- actor-scoped autonomy runtime;
- active modifiers;
- event causality/participants;
- dynamic-location support.

### Schema v5 inventory invariant

Inventory Foundation v1 provides the first concrete reason to advance the schema beyond v4. Reusable definitions and concrete entities already existed, but durable stack quantity/depletion did not.

Schema v5 adds only normalized `inventory_stacks` persistence:
- `entity_id` — concrete stack entity;
- `quantity` — non-negative current amount;
- `unit` — canonical quantity unit for that stack/definition;
- seed/metadata/audit timestamps.

Container and ownership semantics continue to use the generic entity/field/relation architecture; schema v5 does not create a parallel item/world runtime.

A seed quantity is installation/bootstrap data only. Once an inventory stack exists, ordinary initialize/deploy must not reset or replenish its live quantity.

## Universe-global state

`runtime_state` is for state shared by the universe, including:
- `sim_time`;
- `speed`;
- `paused`;
- `world_id`;
- `default_actor_id` as a convenience selector, not actor-owned scheduler state;
- global UI/notification/config state where appropriate;
- inventory seed revision metadata where useful for operational readback.

Do not store character scheduler state as singleton global keys.

## Actor-scoped runtime

`actor_runtime` owns per-actor:
- autonomy enabled/mode;
- pending action reference;
- lease;
- retry/backoff;
- cognition wake reason/statistics.

Multiple actors may therefore hold independent pending actions against one global simulation clock.

## Action definitions and instances

`action_definitions` is the data-driven registry for core action metadata: duration bounds, target mode, required capability, co-location and extension metadata.

`action_instances` is the durable action envelope:
- action id/type;
- actor;
- place;
- target;
- participants/resources;
- conditions/modifiers snapshot;
- duration and planned wall/sim time;
- status;
- outcome/state-change data.

Specialized domain validators may layer on top of generic action-definition metadata. Do not grow a single giant action switch statement.

## Time/concurrency rule

There is one universe simulation clock. An action instance owns its own interval from `planned_sim_time` to action end. Completing concurrent actions must not add their durations serially to the universe clock; the clock advances to the maximum committed action end reached so far.

## Conditions, effects and modifiers

Immediate effect specs support additive, multiplicative, set and clamp operations. `active_modifiers` provides the durable socket for sourced, time-bounded, conditional modifiers with stack policies.

The table/contract existing does not mean every future modifier engine is already implemented. New modules should consume this common contract rather than invent incompatible effect formats.

## Events and causality

`events` is append-oriented and has queryable linkage for:
- stable event UUID;
- action id;
- location id;
- causal parent event id;
- structured state changes.

`event_participants` normalizes multi-entity involvement. Domain-specific detail remains in payload JSON. Nutrition/energy evidence and future inventory consumption evidence should snapshot the concrete definition/stack/quantity used rather than require later reinterpretation of mutable state.

## Universal item / inventory semantics

Canonical detail: `docs/INVENTORY_ITEM_ARCHITECTURE.md`.

Core invariant:

`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

### Definitions

`entity_definitions` stores reusable semantic identity. Food definitions may carry canonical unit, default portion and nutrient basis. Future equipment definitions may carry training/tool semantics. Economic price/ownership/location never belongs to universal semantic identity.

### Concrete instances and stacks

Concrete stack entities reference `entities.definition_id` and their mutable amount resides in `inventory_stacks`.

Stackable examples:
- apples by piece;
- rice/chicken/oats by mass;
- future liquids/materials by canonical volume/mass/count.

Unique/non-stackable examples use a concrete instance with quantity 1 and may later gain instance-specific condition/durability:
- treadmill;
- backpack;
- laptop;
- tool/weapon;
- unique document/artifact.

### Fixed versus movable containers

A container is an entity capable of physically holding movable inventory.

Fixed/immovable examples:
- house/room storage space;
- refrigerator;
- pantry;
- shelf;
- locker/rack.

Movable examples:
- backpack;
- bag/suitcase;
- crate;
- toolbox/medkit.

Container mobility is metadata/state on the container entity. Moving a movable container logically moves the contained items with it; the engine should not require rewriting every contained stack's world location. Container nesting must remain bounded and cycle-free.

### Spatial, inventory-containment and possession semantics

Do not overload relations:
- structural `contains` — authored world/layout containment (world -> floor -> room -> fixture/object);
- `connected_to` — traversable topology;
- `located_at` — current dynamic physical presence;
- `stored_in` — mutable inventory containment for item/stack -> container;
- `owned_by` — legal/economic ownership;
- `carried_by` — direct carriage when later activated;
- `equipped_by` — equipped state when later activated.

Ownership is not physical location. A character may carry something they do not own; an owned item may remain at home.

## Field modes and authority

Rich values may exist before their simulation module is active:
- `canonical`;
- `static`;
- `derived`;
- `simulated`.

Each field records an authority. Domain engines must not mutate fields they do not own. Ordinary seed import must preserve active simulated profile state; ordinary inventory seed import must likewise preserve existing live stack quantity.

## Canonical runtime pipeline

1. Observe actor/place/time/resources/conditions/recent events.
2. Resolve legal options from action definitions, capabilities, topology, inventory availability and state.
3. Propose one structured action/intent.
4. Deterministically validate actor/target/place/time/resource/quantity/condition prerequisites.
5. Persist/schedule a first-class action instance and actor pending reference.
6. Complete or interrupt deterministically.
7. Commit authoritative state atomically, including inventory quantity where applicable.
8. Emit linked event/state-change/evidence snapshots.
9. Notify/query downstream observer surfaces.
10. Wake only actors that reach a real decision boundary.

For eating, cognition may choose food/portion intent based on character policy and deterministic availability context, but inventory/nutrition code owns quantity validation, decrement and nutrient arithmetic.

## Module boundary

Needs, sleep, physiology, training adaptation, emotion, relationships, memory, inventory, economy and environment attach through explicit definitions, capabilities, actions, events, fields, relations and modifiers. Do not give a module its own incompatible mini-runtime unless required by a proven domain constraint.

Progression modules must be actor-generic. Darian's values/history are exemplar inputs; a compatible future actor uses the same engine through its own field values, evidence, recovery state and domain policy.

Inventory is equally universal: Darian/Thorne Estate may supply the first concrete stock fixtures, but reusable food/equipment semantics cannot depend on Darian's identity.

## Future object/economy direction

Migrate existing world objects by structural family after the consumable exemplar is proven:
1. food/drink definitions + stacks;
2. movable containers/carried inventory;
3. fixed storage capacity semantics where needed;
4. training equipment definitions + existing Estate instances;
5. tools/electronics/books/medical supplies;
6. clothing/equipped-state;
7. materials/crafting only when required;
8. economy: ownership transfer, vendors, listings/prices, currency/accounts, transactions, scarcity/replenishment.

Do not bundle all of these into the body-composition prerequisite. Inventory Foundation v1 only proves the reusable definition/instance/container/quantity invariant.

## AI provider layer

AI model IDs are never hard-coded into character or engine logic. Provider catalogs and bindings are resolved by scope/role. Built-in providers include Gemini, Groq, NanoGPT, OpenAI and OpenRouter, with generic OpenAI-compatible runtime support where applicable. Credentials are environment references, never plaintext database secrets.

Binding precedence remains task+role -> character+role -> engine+role -> character default -> global+role -> global default.

Character cognition policy is configuration-driven: each registered character resolves its own authored policy. A future actor must not silently inherit Darian's policy merely because Darian is the current production exemplar.

Runtime Cognition Fallback v1 allows one tested fallback provider/model after an eligible provider-layer failure. Fallback never rewrites primary binding and never triggers on deterministic action/target/duration/runtime validation failures. See `docs/AI_RUNTIME_FALLBACK.md`.

## Remote operation

GitHub is canonical for code/configuration. GitHub Actions deploys to the VPS and performs readback. The live SQLite database remains private on the VPS. Always distinguish committed, CI-validated, production-copy-validated, deployed, DB-applied and live-runtime-verified evidence.