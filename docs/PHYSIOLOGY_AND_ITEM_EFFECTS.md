# Physiology and Item Effects

Status: ACTIVE P1 ENGINE CONTRACT
Scope: Basic living needs, recovery actions, and target/item-driven stat effects.

## Purpose

The living runtime must remain recoverable. A character may become tired, hungry, thirsty, dirty, or low on energy, but the authored world must provide legitimate actions/resources that can move every basic physiological stat back toward a healthy range.

The LLM chooses a structured action. The deterministic engine owns all resulting stat changes.

## Basic physiological state

All current values are clamped to `0..100`.

- `needs.energy`: higher is better.
- `needs.hunger`: higher is worse.
- `needs.thirst`: higher is worse.
- `needs.sleepiness`: higher is worse.
- `physiology.cleanliness`: higher is better.

## Recovery invariant

For every basic stat there must be at least one reachable recovery path in the authored world:

- energy -> rest and sleep; food may provide a smaller boost.
- hunger -> authored food/eat targets.
- thirst -> authored drink targets.
- sleepiness -> sleep; rest provides mild relief.
- cleanliness -> authored shower/wash targets.

A recovery-labelled action must still improve its primary need after passive time drift is included. The cognition layer must not be offered a fake recovery action whose deterministic result contradicts its reason.

## Baseline time drift

Per simulated hour before action-specific effects:

- energy: `-2.0`
- hunger: `+2.5`
- thirst: `+3.0`
- sleepiness: `+3.0`
- cleanliness: `-0.8`

These are gameplay/simulation baseline values, not medical claims. They should be tuned through bounded simulation tests rather than changed ad hoc in prompts.

## Intrinsic action effects

Intrinsic effects belong to the action itself rather than a particular object.

Per simulated hour:

- sleep: energy `+11`, sleepiness `-15`, hunger `+0.5`, thirst `+0.75`, in addition to baseline drift.
- rest: energy `+10`, sleepiness `-4`, in addition to baseline drift.
- idle: energy `+3`, in addition to baseline drift; this is only light recovery.
- train: energy `-10`, hunger `+4`, thirst `+6`, cleanliness `-6`, in addition to baseline drift.
- read: energy `-0.5`, in addition to baseline drift.

Therefore one hour of targetless rest is currently net about `+8 energy` and `-1 sleepiness`, while one hour of idle is net about `+1 energy`.

## Target / item effect profiles

World objects may define action-specific effects in `config/worlds/home.v1.json` using an `effects` object.

Example shape:

```json
{
  "id": "obj_example_drink",
  "name": "Example Drink",
  "capabilities": ["drink"],
  "effects": {
    "drink": {
      "needs.energy": 10.0,
      "needs.thirst": -12.0,
      "needs.sleepiness": -8.0
    }
  }
}
```

Numeric values are flat deltas applied after passive and intrinsic action effects. A field may also use a set operation:

```json
{"physiology.cleanliness": {"set": 100.0}}
```

Current Home v1 authored recovery resources:

- Drinking Water / drink: thirst `-55`.
- Sink / drink: thirst `-35`.
- Meal Ingredients / eat: hunger `-50`, energy `+8`, thirst `+2`.
- Shower / shower: cleanliness set to `100`.

Food/drink/shower capabilities must have an authored matching physiological effect. Objects such as Refrigerator, Pantry and Dining Table are containers/facilities and must not pretend to be food merely because they are near food.

## Cognition visibility

`action_options()` exposes the authored target effect profile with each legal action option. This allows the model mind to compare legal recovery resources while the runtime validator and state-transition engine remain authoritative.

Do not rely on prompt prose alone to teach the model that an item restores a need. The effect must exist in the world definition and be surfaced through the legal action option.

## Future consumables

Future items such as an energy drink, medication, supplement, or finite food item should use the same effect contract, but quantity/consumption, temporary modifiers, cooldowns, tolerance, and inventory depletion belong to later richer item/physiology work.

Do not model a finite consumable as infinitely reusable merely because it has an effect profile. Until inventory quantities exist, Home v1 recovery resources should be treated as renewable household resource abstractions.

## Testing contract

Regression tests must prove:

- rest and sleep increase energy from depleted states;
- rest/sleep reduce sleep pressure in the intended direction;
- authored water reduces thirst;
- authored food reduces hunger and can provide its authored secondary effects;
- shower restores cleanliness;
- effect metadata appears in legal action options;
- restorative item actions without authored effects are rejected;
- a bounded simulated day stays within `0..100` and does not enter an unrecoverable needs loop.
