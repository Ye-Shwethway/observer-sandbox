# P3.5 — Minimum Effective Training Load

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED

## Purpose

Make the P3.4 `effectiveness` signal change immediate basic physiological training load without introducing long-term stimulus progression, attribute gain, body-measurement adaptation, grading, or tiers.

## Runtime rule

For `train` actions:

- passive time drift applies for the full planned duration;
- `effectiveness` scales training-specific immediate energy, hunger, thirst, and cleanliness effects;
- systemic fatigue remains separate and continues to use P3.3's `fatigue_cost_multiplier`, so poor readiness can produce less useful work while still causing disproportionately greater fatigue;
- sleepiness currently has no intrinsic train effect, so only passive drift changes it during training.

Semantic split:
- `readiness` = pre-action state summary;
- `effectiveness` = useful workload fraction;
- `fatigue_cost_multiplier` = physiological inefficiency cost;
- `effective_minutes` = planned session minutes × effectiveness.

`action_instances.outcome_json.training_load` and the matching `action_completed` event payload persist planned minutes, effectiveness, effective minutes, and source/version. No schema change was required.

## Verified reference behavior

Healthy reference (`energy 80 / thirst 15 / sleepiness 15 / fatigue 0`):
- effectiveness `1.000`;
- fatigue multiplier `1.000x`;
- 60 planned minutes -> `60.0` effective minutes;
- resulting energy `68.0`, hunger `26.5`, thirst `24.0`, sleepiness `18.0`, cleanliness `73.2`, fatigue `18.5`.

Degraded but legal reference (`energy 50 / thirst 45 / sleepiness 45 / fatigue 40`):
- effectiveness `0.595`;
- fatigue multiplier `1.202x`;
- 60 planned minutes -> `35.7` effective minutes;
- resulting energy `42.05`, hunger `24.88`, thirst `51.57`, sleepiness `48.0`, cleanliness `75.63`, fatigue `62.54`.

## Evidence

- PR #4 merged at `b6f29493a30a458133587463068df9814395eb75`;
- PR CI #324 / run `31674874707` SUCCESS;
- main CI #325 / run `31674911465` SUCCESS;
- P3 Effective Training Load Acceptance #1 / run `31674911581` SUCCESS on candidate source against a disposable production DB copy;
- acceptance used zero model calls, preserved action/outcome/event evidence, and proved skill score/tier/experience remained unchanged;
- release commit `22ff453715659d2c772ffcd19868716413a715a1`;
- Deploy Observer Sandbox #131 / run `31674963422` SUCCESS;
- production readback after deploy: service healthy, schema v4, autonomy enabled / normal / unpaused / `1.0x`, existing Gemini cognition binding preserved, Telegram API connected, owner/allowed-user configuration present.

The acceptance copy did not mutate production. The production readback snapshot immediately after deployment showed Darian in the Kitchen with a valid `eat` action; treat that as historical runtime evidence because autonomy continues afterward.

## Explicit non-goals / stop boundary

P3.5 does **not** implement or mutate:
- strength/endurance/agility or other attributes;
- skill score/tier/experience;
- muscle stimulus accumulation;
- hypertrophy/body measurements;
- soreness/injury;
- exercise taxonomy, reps, sets, or load programming;
- equipment/facility-quality modifiers;
- grading/tier progression;
- long-term adaptation/detraining;
- schema v5.

**STOP GATE:** after P3.5, do not start another development slice until the Creator discussion is complete and a new slice is explicitly authorized.
