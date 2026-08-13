# Strength Progression Settlement v1

Status: CORE MUTATION GATE — NOT AUTOMATICALLY WIRED

This is the first raw-stat mutation mechanism in Observer Sandbox. Scope remains **Free Weights + Strength only**.

## Safety model

1. **Bootstrap is non-mutating.** The first settlement records a progression cursor and marks all pre-feature Strength stimulus events consumed. Deployment cannot retroactively change Strength from old history.
2. **Stimulus is consumed once.** Settlement events record consumed source event ids. Previously consumed stimulus cannot be credited again.
3. **Recovery eligibility is conservative.** Positive Strength stimulus is only consumed after at least 48 simulated hours and while systemic fatigue is below the existing 70 hard block. Zero-recovery evidence remains pending rather than being discarded.
4. **Detraining is interval-integrated.** Negative progression integrates the existing slow detraining curve across the exact unsettled simulated-time interval, with Strength training events resetting the untrained clock.
5. **Every cursor advance is audited.** A `strength_progression_settled` event records the settled interval even when the raw stat does not change.
6. **Every mutation is historized.** `character_profile_history` records old/new Strength, simulated mode, progression authority, reason, and simulated time.
7. **Same-boundary replay is a no-op.** Re-running settlement at the same simulated timestamp cannot reapply positive or negative progression.

## v1 positive settlement

For each newly eligible unconsumed Strength stimulus event:

`delta = 0.25 * stimulus_units * level_factor * historical_saturation_factor * recovery_factor * adaptation_rate_multiplier`

The current raw Strength is re-evaluated after each consumed stimulus event, preserving diminishing headroom.

## v1 negative settlement

Detraining uses the analytic integral of:

`time_factor = 1 - exp(-overdue_days / 60)`

after the 14-day grace period. Training events inside the settlement interval reset the untrained clock.

`negative_delta = 0.02 * integrated_time_factor_days * level_exposure * detraining_multiplier * decay_rate_multiplier`

## Raw value authority

When a non-zero net delta is applied:
- `character_profile_values.raps_pa.strength` becomes `mode='simulated'`;
- authority/source become `strength-progression-settlement-v1`;
- raw value is rounded to six decimal places and clamped to the v1 0..100 Strength scale;
- derived grading continues to read the raw value and remains a presentation/query layer.

## Activation boundary

This core function is deliberately **not yet called automatically by the service loop**. Production activation is a separate final slice after disposable production-copy acceptance proves bootstrap safety, positive settlement, negative settlement, history/audit evidence, and replay idempotency.
