# P3.4 — Minimum Training Effectiveness Outcome

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED

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

P3.4 does not mutate:
- skill score, tier, or experience;
- strength or other character attributes;
- muscle size/body measurements;
- grading/progression state;
- soreness/injury state;
- exercise programming, reps, sets, or load;
- equipment/facility quality;
- nutrition, stimulant, environment, or psychological modifiers.

Those remain future slices that may consume the effectiveness signal only when independently authorized.

## Acceptance evidence

PR #3 merged at `ea69d5c0f81bf5500fca9b4d6ea62a251fbdcd9f` after PR CI #317 succeeded.

Main CI #318 / run `31673822574` succeeded.

P3 Training Effectiveness Acceptance #1 / run `31673822547` succeeded on merged candidate source against a disposable production DB copy with zero model calls.

Verified values:
- healthy reference: effectiveness `1.0`, fatigue-cost multiplier `1.0x`, one-hour resulting fatigue `18.5`;
- degraded reference: effectiveness `0.595`, fatigue-cost multiplier `1.202x`, one-hour resulting fatigue `62.54`;
- effectiveness persisted through action instance, completion outcome, and `action_completed` event evidence;
- production readback remained healthy and unchanged by the disposable probe.

## Deployment evidence

`deploy/RELEASE` was advanced by commit `818752a5976d988fcd3445ed3f0cc984f637d1cb` to `P3.4-minimum-training-effectiveness-outcome`.

Deploy Observer Sandbox #130 / run `31673858850` succeeded. The deploy completed application sync, dependency/install step, cognition configuration, service restart, and runtime verification successfully.

P3.4 is therefore deployed in production. It has no new standalone Telegram field in this slice; effectiveness is first-class action/outcome evidence intended for a later consumer such as progression, history detail, or another bounded observer surface.
