# Physiology and Item Effects

Status: ACTIVE P1 ENGINE CONTRACT
Scope: Basic living needs, recovery actions, target/item effects, and schema-v4 modifier sockets.

## Purpose

The living runtime must remain recoverable. A character may become tired, hungry, thirsty, dirty or low on energy, but the authored world must provide legitimate actions/resources that move every basic physiological stat toward a healthy range. The LLM chooses a structured action; deterministic runtime owns stat changes.

## Basic physiological state

Values clamp to `0..100`:
- `needs.energy`: higher is better
- `needs.hunger`: higher is worse
- `needs.thirst`: higher is worse
- `needs.sleepiness`: higher is worse
- `physiology.cleanliness`: higher is better

## Recovery invariant

Reachable recovery paths must exist:
- energy -> rest/sleep; food may add a secondary boost
- hunger -> authored food/eat targets
- thirst -> authored drink targets
- sleepiness -> sleep; rest mild relief
- cleanliness -> authored shower/wash targets

A recovery-labelled action must improve its primary need after passive drift. Cognition must never be offered a fake recovery whose deterministic result contradicts its reason.

## Baseline drift and intrinsic effects

Passive per simulated hour:
- energy `-2.0`
- hunger `+2.5`
- thirst `+3.0`
- sleepiness `+3.0`
- cleanliness `-0.8`

Intrinsic per-hour action effects are currently:
- sleep: energy `+11`, sleepiness `-15`, hunger `+0.5`, thirst `+0.75`
- rest: energy `+10`, sleepiness `-4`
- idle: energy `+3`
- train: energy `-10`, hunger `+4`, thirst `+6`, cleanliness `-6`
- read: energy `-0.5`

These are simulation tuning values, not medical claims.

## Shared effect operation contract

Schema v4 generalizes effect specs so future systems do not invent incompatible formats. A physiological field may use:

```json
{"needs.energy": {"add": 10}}
```

Supported immediate operations:
- `add`
- `multiply`
- `set`
- `clamp_min`
- `clamp_max`

Legacy flat numeric values remain additive for current authored resources.

Example:

```json
{
  "drink": {
    "needs.energy": {"add": 10},
    "needs.thirst": {"add": -12},
    "needs.sleepiness": {"add": -8}
  }
}
```

## Target/resource effects

Current Thorne Estate recovery abstractions include drinking water, sink water, meal ingredients, pantry ready food, shower and bed/rest resources. Food/drink/shower capabilities must have matching deterministic effects. Facilities must not expose fake recovery capabilities merely because they are near a resource.

`action_options()` exposes relevant authored effects to cognition; validation/application remain deterministic.

## Definitions versus instances

Schema v4 establishes `entity_definitions` plus `entities.definition_id`.

A future Energy Drink should therefore be modeled conceptually as:
- reusable definition: name, capabilities, base effects, metadata
- concrete instance/stack: identity, current location/container, quantity/state when inventory exists.

Do not duplicate immutable product semantics into every physical instance. Quantity, stack depletion and durability remain deferred inventory features.

## Temporary/sourced modifiers

`active_modifiers` is the persistence contract for future temporary effects such as stimulant, injury, illness, environmental exposure or training fatigue. It records:
- subject
- source entity/action
- field
- operation/value
- start/end sim time
- stack key/policy
- conditions/metadata.

The existence of this table is a schema socket, not a claim that all active modifiers are currently evaluated by every engine. Feature modules should progressively attach through this common contract.

## Migration safety

Pending actions are now first-class `action_instances` referenced by actor-scoped runtime. World/effect migrations must still preserve, revalidate, cancel or explicitly migrate outstanding action instances; never silently invalidate them.

## Future consumables

Finite consumables should not be modeled as infinitely reusable. Energy drinks, medication, finite food, supplements and similar resources require inventory quantity/depletion before becoming finite production items. Temporary effects should use `active_modifiers`, not ad-hoc prompt memory.

## Testing contract

Regression tests must prove recovery direction, authored effects, option visibility, invalid restorative targets, bounded living behavior and safe pending-action migration. Schema-v4 tests additionally prove definition/instance and active-modifier sockets without pretending the later inventory/modifier engines are complete.