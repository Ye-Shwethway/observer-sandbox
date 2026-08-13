# Physiology and Item Effects

Status: ACTIVE LIVING ENGINE CONTRACT
Scope: Basic living needs, recovery actions, target/item effects, first P3 systemic-fatigue behavior, and schema-v4 modifier sockets.

## Purpose

The living runtime must remain recoverable. A character may become tired, hungry, thirsty, dirty, low on energy or temporarily fatigued, but authored actions/resources must provide legitimate paths back toward a healthy operating range. The LLM chooses a structured action; deterministic runtime owns state changes.

## Basic physiological state

Values clamp to `0..100`:
- `needs.energy`: higher is better
- `needs.hunger`: higher is worse
- `needs.thirst`: higher is worse
- `needs.sleepiness`: higher is worse
- `physiology.cleanliness`: higher is better
- `physiology.fatigue`: higher is worse; current first richer-simulation metric for accumulated systemic training/recovery load.

`physiology.fatigue` was already reserved by the character profile ontology. P3 activates it as live simulated state in the generic `fields` store rather than creating another schema revision or copying scheduler state into the canonical profile tables.

## Recovery invariant

Reachable recovery paths must exist:
- energy -> rest/sleep; food may add a secondary boost
- hunger -> authored food/eat targets
- thirst -> authored drink targets
- sleepiness -> sleep; rest mild relief
- cleanliness -> authored shower/wash targets
- systemic fatigue -> rest/sleep and ordinary low-load time.

A recovery-labelled action must improve its primary need after passive drift. Cognition must never be offered a fake recovery whose deterministic result contradicts its reason.

## Baseline drift and intrinsic effects

Passive per simulated hour:
- energy `-2.0`
- hunger `+2.5`
- thirst `+3.0`
- sleepiness `+3.0`
- cleanliness `-0.8`
- systemic fatigue `-1.5`

Intrinsic per-hour action effects are currently:
- sleep: energy `+11`, sleepiness `-15`, hunger `+0.5`, thirst `+0.75`, fatigue `-10`
- rest: energy `+10`, sleepiness `-4`, fatigue `-7`
- idle: energy `+3`, fatigue `-2`
- train: energy `-10`, hunger `+4`, thirst `+6`, cleanliness `-6`, fatigue `+20`
- read: energy `-0.5`, fatigue `-1`

Passive drift and intrinsic action effects combine. For example, one simulated hour of training currently produces a net systemic-fatigue increase of `+18.5`, while one hour of rest produces a net decrease of `-8.5`.

These are simulation tuning values, not medical claims.

## Minimum training/recovery guard

P3's first richer vertical slice intentionally adds only one deterministic behavioral consequence:
- `train` options are withheld when systemic fatigue is `>= 70`;
- direct validation also rejects a `train` action at that threshold, so a model cannot bypass the guard;
- the baseline deterministic living policy stops electing a normal morning training block at fatigue `>= 55` and prioritizes recovery once fatigue is high.

This is deliberately not a full training-adaptation engine. No strength gain, hypertrophy, muscle-group soreness model, workout programming, exercise taxonomy, injury probability or grading progression is implemented by this slice.

## Observer surface

The ordinary Telegram character Profile now gains a read-only `Recovery` section once live fatigue exists. It reads `physiology.fatigue` from generic simulated fields and resolves its human label through the profile field definition.

This keeps the architecture separation intact:
- canonical/static profile truth remains in character profile storage;
- live physiology remains simulated state owned by its engine;
- actor scheduler state remains in `actor_runtime`;
- action history remains in first-class actions/events.

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

`active_modifiers` is the persistence contract for future temporary effects such as stimulant, injury, illness, environmental exposure or more detailed training fatigue. It records:
- subject
- source entity/action
- field
- operation/value
- start/end sim time
- stack key/policy
- conditions/metadata.

The current systemic-fatigue value does not require a temporary modifier row: it is a directly simulated accumulated state. The existence of `active_modifiers` remains a schema socket, not a claim that all modifiers are currently evaluated by every engine.

## Migration safety

Pending actions are first-class `action_instances` referenced by actor-scoped runtime. World/effect migrations must preserve, revalidate, cancel or explicitly migrate outstanding action instances; never silently invalidate them.

## Future consumables

Finite consumables should not be modeled as infinitely reusable. Energy drinks, medication, finite food, supplements and similar resources require inventory quantity/depletion before becoming finite production items. Temporary effects should use `active_modifiers`, not ad-hoc prompt memory.

## Testing contract

Regression tests must prove recovery direction, authored effects, option visibility, invalid restorative targets, bounded living behavior and safe pending-action migration.

For the P3 systemic-fatigue slice, focused tests additionally prove:
- training raises fatigue deterministically;
- recovery lowers it;
- high fatigue blocks further training in both option generation and validation;
- fatigue is captured in action/event state changes;
- the Telegram profile observer can read the live Recovery value without copying it into canonical profile values.
