# Recovery Realization v1

Status: READ-ONLY PROOF

Scope: Free Weights + Strength progression family only. This gate does not mutate raw Strength, consume stimulus, create adaptation state, or change schema version.

## Purpose

Convert elapsed simulated recovery time plus current recovery quality into a bounded `recovery_factor` for later adaptation preview composition.

## v1 semantics

- Curve id: `strength-recovery-realization-v1`.
- Source stimulus: latest positive Strength training-stimulus completion event by **simulated time**, not event insertion id.
- Time gate:
  - `<= 6h` after latest Strength stimulus -> `time_factor = 0`;
  - `6h .. 48h` -> linear ramp from 0 to 1;
  - `>= 48h` -> `time_factor = 1`.
- State quality is the mean of three bounded components:
  - energy: 20 bad -> 75 good;
  - alertness from sleepiness: 80 bad -> 25 good;
  - systemic fatigue recovery: 70 bad -> 20 good.
- `fatigue >= 70` hard-blocks realization to zero.
- Abstract `recovery_multiplier` is a simulation socket distinct from level/ceiling and adaptation-rate modifiers.
- Final factor: `clamp(time_factor * state_quality * recovery_multiplier, 0, 1)`, unless hard-blocked.

No hydration/nutrition submodel is introduced in v1. Those require concrete progression evidence before expansion.

## Mutation gate

Recovery Realization v1 remains evidence-only. Required next gates before any raw Strength mutation:

1. Detraining / Prolonged-Untrained Decay v1.
2. Adaptation Preview v1 composing level, saturation, recovery and detraining evidence.
3. Stat Mutation Gate v1 only after all prior gates are accepted.
