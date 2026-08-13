# Observer Sandbox Architecture

## Foundation contract

Observer Sandbox is a small persistent universe built from composable primitives rather than character-specific scripts.

Canonical LEGO runtime expression:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

The LLM may propose a structured action but never receives arbitrary database-write authority. Deterministic runtime validation/application remains authoritative.

## Logical world model

Every meaningful thing is an entity node or reusable definition. Typed relations connect entities. The same model must scale from Darian inside one mansion to multiple characters, residences, regions, items and later environment modules.

Core distinctions:

1. **Definitions/Templates** — reusable semantics/defaults (`entity_definitions`, `action_definitions`).
2. **Instances** — concrete universe entities/actions (`entities`, `action_instances`).
3. **Runtime State** — mutable actor/global state (`actor_runtime`, fields, relations, `runtime_state`).
4. **Events** — append-oriented evidence of committed transitions.

## SQLite schema v4

Schema v4 keeps the original generic graph/profile/provider tables and adds the minimum composable-runtime layer.

### Universe-global state

`runtime_state` is for state shared by the universe, including:
- `sim_time`
- `speed`
- `paused`
- `world_id`
- global UI/notification/config state where appropriate.

Do not store character scheduler state as singleton global keys.

### Actor-scoped runtime

`actor_runtime` owns per-actor:
- autonomy enabled/mode
- pending action reference
- lease
- retry/backoff
- cognition wake reason/statistics.

Multiple actors may therefore hold independent pending actions against one global simulation clock.

### Action definitions and instances

`action_definitions` is the data-driven registry for core action metadata: duration bounds, target mode, required capability, co-location and extension metadata.

`action_instances` is the durable action envelope:
- action id/type
- actor
- place
- target
- participants/resources
- conditions/modifiers snapshot
- duration and planned wall/sim time
- status
- outcome/state-change data.

Specialized domain validators may still layer on top of generic action-definition metadata. Do not grow a single giant action switch statement.

### Time/concurrency rule

There is one universe simulation clock. An action instance owns its own interval from `planned_sim_time` to action end. Completing concurrent actions must not add their durations serially to the universe clock; the clock advances to the maximum committed action end reached so far.

### Conditions, effects and modifiers

Immediate effect specs support additive, multiplicative, set and clamp operations. `active_modifiers` provides the durable socket for sourced, time-bounded, conditional modifiers with stack policies.

The table/contract existing does not mean every future modifier engine is already implemented. New modules should consume this common contract rather than invent incompatible effect formats.

### Events and causality

`events` remains append-oriented and now has queryable linkage for:
- stable event UUID
- action id
- location id
- causal parent event id
- structured state changes.

`event_participants` normalizes multi-entity involvement. Domain-specific detail remains in payload JSON.

### Definition / instance

`entity_definitions` stores reusable semantics such as a future Energy Drink definition. Concrete universe instances reference a definition through `entities.definition_id`. Quantity/depletion/durability are intentionally deferred until inventory work.

## Spatial and possession semantics

`contains` means structural/static containment. `connected_to` means traversable topology.

For dynamic presence, `located_at` is the canonical generic relation. `src/observer_sandbox/location_runtime.py` exposes the generic resolver/setter; character `runtime.location` is retained as a mirrored compatibility/cache path during transition, and static fixtures may resolve their place through structural containment.

Future possession semantics must remain distinct:
- `located_at` — current physical presence
- `owned_by` — ownership
- `carried_by` — possession/carriage
- `equipped_by` — equipped state
- container/storage relations — physical containment inside movable containers.

Never overload ownership and physical location into one relation.

## Field modes and authority

Rich values may exist before their simulation module is active:
- `canonical`
- `static`
- `derived`
- `simulated`

Each field records an authority. Domain engines must not mutate fields they do not own.

## Canonical runtime pipeline

1. Observe actor/place/time/resources/conditions/recent events.
2. Resolve legal options from action definitions, capabilities, topology and state.
3. Propose one structured action.
4. Validate actor/target/place/time/resource/condition prerequisites.
5. Persist/schedule a first-class action instance and actor pending reference.
6. Complete or interrupt deterministically.
7. Commit authoritative state atomically.
8. Emit linked event/state-change evidence.
9. Notify/query downstream observer surfaces.
10. Wake only actors that reach a real decision boundary.

## Module boundary

Needs, sleep, physiology, training adaptation, emotion, relationships, memory, inventory and environment attach through explicit capabilities, actions, events, fields and modifiers. Do not give a module its own incompatible mini-runtime unless required by a proven domain constraint.

## AI provider layer

AI model IDs are never hard-coded into character or engine logic. Provider catalogs and bindings are resolved by scope/role. Built-in adapters include Gemini, NanoGPT, OpenAI and OpenRouter. Credentials are environment references, never plaintext database secrets.

Binding precedence remains task+role -> character+role -> engine+role -> character default -> global+role -> global default.

## Remote operation

GitHub is canonical for code/configuration. GitHub Actions deploys to the VPS and performs readback. The live SQLite database remains private on the VPS. Always distinguish committed, CI-validated, deployed, DB-applied and live-runtime-verified evidence.