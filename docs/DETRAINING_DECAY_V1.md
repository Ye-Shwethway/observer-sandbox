# Detraining / Prolonged-Untrained Decay v1

Status: READ-ONLY PROOF

Scope: Strength progression family only. This gate derives bounded decay pressure; it does not mutate raw Strength, create negative adaptation state, or change schema version.

## v1 semantics

- Curve id: `strength-detraining-decay-v1`.
- Latest positive Strength training-stimulus event establishes the most recent trained boundary.
- If no Strength-training history exists, v1 does **not** invent a decay start point.
- Grace period: first 14 simulated days untrained produce zero decay pressure.
- After grace, slow time exposure is:
  `time_factor = 1 - exp(-overdue_days / 60)`.
- Higher current levels are more exposed:
  `level_exposure = clamp(current_strength / effective_ceiling, 0, 1)^2`.
- Final read-only pressure:
  `decay_pressure = clamp(time_factor * level_exposure * detraining_multiplier, 0, 1)`.
- `detraining_multiplier` is an abstract simulation modifier socket only.

This is not a medical or real-world detraining model. It is deterministic simulation tuning designed to create a slow, auditable regression pressure after prolonged inactivity.

## Mutation gate

No raw stat loss occurs in this slice. Required next step is Adaptation Preview v1, which must compose positive adaptation evidence and negative detraining evidence without mutation. Only after preview acceptance may Stat Mutation Gate v1 be considered.
