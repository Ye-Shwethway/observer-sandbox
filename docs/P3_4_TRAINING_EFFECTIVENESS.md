# P3.4 — Minimum Training Effectiveness Outcome

Status: IMPLEMENTATION / ACCEPTANCE PENDING

## Purpose

Add the first positive training-outcome signal without introducing strength, skill, hypertrophy, grading, or a general training adaptation engine.

P3.3 established that existing authoritative live state can derive `training_readiness`, and that readiness can change training fatigue cost while the existing hard condition still controls legality. P3.4 reuses that same bounded readiness input to record a separate effectiveness outcome.

## Semantic split

- `readiness`: pre-action state summary derived from current energy, thirst, sleepiness, and systemic fatigue.
- `fatigue_cost_multiplier`: physiological cost applied to the training fatigue effect.
- `effectiveness`: useful training-stimulus fraction recorded with the action outcome.

For this first slice:

`effectiveness = readiness`

This deliberately creates a stable output socket before any progression domain consumes it.

Examples:
- readiness `1.0` -> effectiveness `1.0`, fatigue cost `1.0x`
- readiness `0.595` -> effectiveness `0.595`, fatigue cost `1.202x`

The two outputs have different meanings even though both currently derive from the same readiness value.

## Persistence

Effectiveness is carried inside the existing action-scoped `training_readiness` modifier snapshot and therefore persists through:

1. `action_instances.modifiers_json`;
2. completion `outcome_json.modifiers`;
3. `action_completed` event payload modifiers.

No new schema or canonical physiology field is introduced.

## Explicit non-goals

P3.4 must not mutate:
- skill score, tier, or experience;
- strength or other character attributes;
- muscle size/body measurements;
- grading/progression state;
- soreness/injury state;
- exercise programming, reps, sets, or load;
- equipment/facility quality;
- nutrition, stimulant, environment, or psychological modifiers.

Those remain future slices that may consume the effectiveness signal only when independently authorized.

## Acceptance

A disposable production-copy acceptance must prove:

1. healthy training records effectiveness `1.0` while preserving the existing `18.5` one-hour fatigue result;
2. the P3.3 degraded reference state records effectiveness `0.595`, fatigue multiplier `1.202`, and resulting fatigue `62.54`;
3. effectiveness persists in action-instance, completion-outcome, and event evidence;
4. production DB remains unchanged;
5. the acceptance path uses zero model calls.
