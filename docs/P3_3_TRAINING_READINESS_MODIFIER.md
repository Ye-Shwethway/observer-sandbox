# P3.3 — Minimum Training Readiness Modifier

Status: IMPLEMENTATION SLICE

## Purpose

Activate one concrete schema-v4 modifier path for training without building a universal modifier subsystem.

## Rule

Conditions continue to decide whether an action is legal. Modifiers change the magnitude/quality/cost/risk of an otherwise legal action.

For the first slice, training readiness is derived from existing authoritative live state only:

- energy
- thirst
- sleepiness
- systemic fatigue

No new canonical physiology fields are introduced.

## Readiness calculation

Each input contributes a normalized `0..1` readiness component. A comfortable baseline receives `1.0` for that component; deterioration toward the existing strong/critical or training-block thresholds reduces it toward `0.0`.

- energy: `75+ -> 1.0`, `20 or below -> 0.0`
- thirst: `25 or below -> 1.0`, `75+ -> 0.0`
- sleepiness: `25 or below -> 1.0`, `80+ -> 0.0`
- fatigue: `20 or below -> 1.0`, `70+ -> 0.0`

Overall readiness is the arithmetic mean of the four components, clamped to `0..1`.

## First real consequence

Training fatigue cost is multiplied by:

`1.0 + (1.0 - readiness) * 0.5`

Therefore:

- readiness `1.0` -> fatigue-cost multiplier `1.0x`
- readiness `0.5` -> `1.25x`
- readiness `0.0` -> `1.5x`

The existing hard training block at systemic fatigue `>=70` remains authoritative and unchanged.

The derived readiness and multiplier are persisted with action modifier/outcome evidence so observer surfaces and later slices can inspect what shaped the action without overwriting raw actor state.

## Explicit non-goals

- no universal cross-domain modifier resolver
- no injury/soreness model
- no stimulant/supplement model
- no nutrition adaptation engine
- no equipment/facility quality modifier
- no strength/skill progression
- no hypertrophy/body progression
- no grading/tier implementation
- no schema v5

## Acceptance

A bounded disposable production-copy acceptance must prove:

1. healthy baseline readiness preserves the existing one-hour training fatigue result;
2. degraded but still legal readiness produces a larger fatigue cost;
3. the modifier is persisted on the first-class action instance and completion outcome/event evidence;
4. the existing fatigue `>=70` training block still wins;
5. production DB is not mutated by the acceptance probe.
