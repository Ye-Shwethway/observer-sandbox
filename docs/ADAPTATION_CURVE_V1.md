# Adaptation Curve v1 — Read-Only Strength Level Factor

Status: EXAMPLAR CANDIDATE / NO STAT MUTATION

## Purpose

Prove the first progression-math gate before any raw Strength mutation is permitted.

For current raw Strength `x`, natural ceiling `C`, ceiling multiplier `m`, and exponent `p`:

`effective_ceiling = C * m`

`remaining_fraction = clamp((effective_ceiling - x) / effective_ceiling, 0, 1)`

`level_factor = remaining_fraction ^ p`

v1 defaults:
- `C = 100`
- `m = 1.0`
- `p = 2.0`
- curve id `strength-level-curve-v1`

Reference points with default settings:
- Strength 20 -> 0.6400
- Strength 40 -> 0.3600
- Strength 60 -> 0.1600
- Strength 75 -> 0.0625
- Strength 90 -> 0.0100
- Strength 95 -> 0.0025
- Strength 99 -> 0.0001
- Strength 100+ -> 0 ordinary headroom

Interpretation: this is **not a gain amount**. It is one multiplicative difficulty factor that future adaptation preview will combine with eligible stimulus, stimulus saturation/diminishing returns, recovery realization and abstract special modifiers.

## Modifier boundary

A future special condition may modify effective ceiling separately from adaptation rate or recovery. v1 only proves the ceiling socket. It does not model real-world drug dosing or medical guidance.

## Mutation gate

This slice is read-only. It must not change `raps_pa.strength`, grade metadata, body measurements, skills, or schema version.

Raw stat mutation remains forbidden until the full gate sequence in `docs/TRAINING_PROGRESSION_GATES.md` is accepted, including detraining/prolonged-untrained decay.
