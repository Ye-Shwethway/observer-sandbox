# Strength Adaptation Preview v1

Status: READ-ONLY COMPOSITION PROOF

This gate composes the already-proven Strength progression signals into projected positive and negative deltas. It does **not** mutate raw Strength, consume stimulus, write settlement cursors, or change schema version.

## Positive preview

`positive_delta = base_positive_scale * recent_strength_stimulus * level_factor * saturation_factor * recovery_factor * adaptation_rate_multiplier`

Proof tuning:
- `base_positive_scale = 0.25` raw Strength points per fully-realized low-level stimulus unit before difficulty/saturation/recovery;
- natural level/ceiling difficulty remains the quadratic `strength-level-curve-v1`;
- recent-stimulus saturation remains the 72-sim-hour `strength-stimulus-saturation-v1`;
- recovery remains `strength-recovery-realization-v1`.

At Strength 90, one recent fully recovered Strength stimulus unit with no special modifiers projects only about `+0.001923` raw Strength before mutation is allowed.

## Negative preview

`negative_delta = base_detraining_points_per_day * decay_pressure * preview_days * decay_rate_multiplier`

Proof tuning:
- `base_detraining_points_per_day = 0.02` at maximum decay pressure;
- default preview horizon = 1 simulated day;
- decay pressure comes from `strength-detraining-decay-v1`.

This is a projected daily regression magnitude, not a mutation instruction. A future settlement mechanism must track elapsed settled time so the same negative interval cannot be applied repeatedly.

## Modifier separation

- ceiling multiplier changes effective adaptation headroom;
- adaptation-rate multiplier changes positive realized rate;
- recovery multiplier changes recovery realization;
- detraining multiplier changes decay pressure;
- decay-rate multiplier changes negative realized rate.

Do not collapse these into one generic gain multiplier.

## Stat Mutation Gate requirement

After this preview passes, raw-stat mutation may be designed, but it must include an idempotent settlement cursor/evidence boundary so positive stimulus and negative elapsed time are never double-applied. Tiny decimal raw Strength updates and audit evidence remain mandatory.
