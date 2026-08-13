# P3.5 — Minimum Effective Training Load

Status: IMPLEMENTATION / ACCEPTANCE PENDING

## Purpose

Make the P3.4 training-effectiveness signal change immediate basic physiological training load without introducing long-term stimulus progression, attribute gain, body-measurement adaptation, grading, or tiers.

## Rule

For `train` actions:

- passive time drift always applies for the full planned action duration;
- `effectiveness` scales the training-specific immediate energy, hunger, thirst, and cleanliness effects;
- systemic fatigue remains separate and continues to use P3.3's fatigue-cost multiplier so poor readiness can mean less productive work but disproportionately more fatigue;
- sleepiness currently has no intrinsic training-specific effect, so only passive drift changes it during training.

This preserves the semantic split:

- `readiness` = pre-action state summary;
- `effectiveness` = useful workload fraction;
- `fatigue_cost_multiplier` = physiological inefficiency cost;
- `effective_minutes` = planned session minutes multiplied by effectiveness.

## Reference behavior

Healthy reference:

- inputs: energy 80, thirst 15, sleepiness 15, fatigue 0;
- readiness/effectiveness 1.000;
- fatigue multiplier 1.000x;
- 60 planned minutes -> 60 effective minutes;
- resulting energy 68.0, hunger 26.5, thirst 24.0, sleepiness 18.0, cleanliness 73.2, fatigue 18.5.

Degraded but legal reference:

- inputs: energy 50, thirst 45, sleepiness 45, fatigue 40;
- readiness/effectiveness 0.595;
- fatigue multiplier 1.202x;
- 60 planned minutes -> 35.7 effective minutes;
- resulting energy 42.05, hunger 24.88, thirst 51.57, sleepiness 48.0, cleanliness 75.63, fatigue 62.54.

## Persistence

`action_instances.outcome_json.training_load` and the matching `action_completed` event payload record:

- planned minutes;
- effectiveness;
- effective minutes;
- source/version.

No new schema field is introduced.

## Explicit non-goals

P3.5 does not implement or mutate:

- strength, endurance, agility, or other attributes;
- skill score/tier/experience;
- muscle stimulus accumulation;
- hypertrophy/body measurements;
- soreness/injury;
- exercise taxonomy, reps, sets, or load programming;
- equipment/facility quality modifiers;
- grading/tier progression;
- long-term adaptation or detraining;
- schema v5.

## Acceptance

A bounded disposable production-copy acceptance must prove:

1. healthy effectiveness preserves full immediate training load and the existing fatigue result;
2. degraded effectiveness scales energy/hunger/thirst/cleanliness training effects while P3.3 fatigue inefficiency remains authoritative;
3. effective minutes persist in completion outcome and event evidence;
4. no long-term skill progression state changes;
5. production DB is not mutated;
6. zero model calls are required.
