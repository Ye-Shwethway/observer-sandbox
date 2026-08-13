# Physiology and Item Effects

Status: ACTIVE LIVING ENGINE CONTRACT
Scope: basic living needs, recovery actions, target/item effects, P3 systemic fatigue/readiness/effectiveness/effective-load behavior, and schema-v4 modifier sockets.

## Purpose

The living runtime must remain recoverable. LLM cognition chooses structured actions; deterministic runtime owns validation and state changes.

## Basic physiological state

Values clamp to `0..100`:
- `needs.energy`: higher is better
- `needs.hunger`: higher is worse
- `needs.thirst`: higher is worse
- `needs.sleepiness`: higher is worse
- `physiology.cleanliness`: higher is better
- `physiology.fatigue`: higher is worse

Live physiology remains generic simulated field state rather than canonical profile truth.

## Recovery invariant

Reachable restoration paths must exist for energy, hunger, thirst, sleepiness, cleanliness, and systemic fatigue. A recovery-labelled action must improve its intended need after passive drift; cognition must not be offered fake recovery whose deterministic result contradicts its purpose.

## Passive drift and intrinsic effects

Passive per simulated hour:
- energy `-2.0`
- hunger `+2.5`
- thirst `+3.0`
- sleepiness `+3.0`
- cleanliness `-0.8`
- systemic fatigue `-1.5`

Base intrinsic per-hour action effects:
- sleep: energy `+11`, sleepiness `-15`, hunger `+0.5`, thirst `+0.75`, fatigue `-10`
- rest: energy `+10`, sleepiness `-4`, fatigue `-7`
- idle: energy `+3`, fatigue `-2`
- train: energy `-10`, hunger `+4`, thirst `+6`, cleanliness `-6`, fatigue `+20`
- read: energy `-0.5`, fatigue `-1`

These are simulation tuning values, not medical claims.

## Training condition / modifier / workload contract

Training now has deliberately separated semantics:

1. **Condition:** systemic fatigue `>=70` blocks training in both action option generation and direct validation. Baseline living policy avoids normal morning training at fatigue `>=55`.
2. **Readiness:** P3.3 derives pre-action readiness from energy, thirst, sleepiness, and systemic fatigue.
3. **Physiological inefficiency:** P3.3 derives `fatigue_cost_multiplier`; training fatigue uses this multiplier.
4. **Effectiveness:** P3.4 records a useful-work fraction. In the current v1 formula `effectiveness = readiness`.
5. **Effective workload:** P3.5 records `effective_minutes = planned_minutes × effectiveness` and scales the intrinsic training-specific energy/hunger/thirst/cleanliness effects by effectiveness.

Passive drift always applies across the full planned duration. Sleepiness has no current intrinsic train-specific effect, so training changes it only through passive drift. Systemic fatigue deliberately does **not** scale down with effectiveness; it uses the separate fatigue-cost multiplier so poor readiness can mean less useful work but disproportionately higher fatigue.

Healthy one-hour reference at effectiveness `1.0` retains the old full training load and net fatigue `+18.5`.

Degraded reference (`energy 50`, `thirst 45`, `sleepiness 45`, `fatigue 40`) yields readiness/effectiveness `0.595`, fatigue multiplier `1.202x`, `35.7` effective minutes from a 60-minute session, and resulting state energy `42.05`, hunger `24.88`, thirst `51.57`, sleepiness `48.0`, cleanliness `75.63`, fatigue `62.54`.

The effective-load evidence is persisted in the first-class action outcome and completion event. It is not a new physiology field.

## Current non-progression boundary

Training currently does **not** mutate:
- strength or other attributes;
- skill score/tier/experience;
- muscle/body measurements;
- accumulated adaptation stimulus;
- soreness/injury;
- grading/tier progression.

Do not infer long-term progression merely from the existence of `effectiveness` or `effective_minutes`.

## Observer surface

Telegram Profile -> Recovery exposes live systemic fatigue and derived training readiness. P3.4/P3.5 add action/outcome evidence but no new standalone Telegram field.

## Shared effect operation contract

Schema v4 immediate effect specs support `add`, `multiply`, `set`, `clamp_min`, and `clamp_max`; legacy flat numerics remain additive. Authored resource effects remain deterministic and must match exposed recovery capabilities.

## Temporary/sourced modifiers

`active_modifiers` is the durable socket for future sourced/time-bounded effects. Its existence is not permission to pre-build a universal modifier evaluator. New modifier sources must arrive only through concrete runnable needs.

## Migration / testing safety

First-class pending actions must be preserved, revalidated, cancelled, or explicitly migrated when world/effect semantics change.

Regression coverage must prove recovery direction, authored effects, action legality, systemic-fatigue behavior, readiness/effectiveness persistence, P3.5 immediate-load scaling, effective-minute evidence, and the absence of unintended long-term progression mutations.

**Post-P3.5 stop gate:** no further training/progression/grading slice is authorized until Creator discussion explicitly selects it.
