# Stimulus Saturation / Diminishing Returns v1 — Read-Only

Status: EXAMPLAR CANDIDATE / NO STAT MUTATION

Purpose: reduce the marginal adaptation value of repeated recent same-domain Strength stimulus without introducing a mutable progression counter.

v1 derives recent Strength stimulus from existing `action_completed` event payload evidence over a 72 simulated-hour rolling window.

Formula:
`factor = 1 / (1 + alpha * recent_strength_stimulus_units)`

Defaults:
- curve id `strength-stimulus-saturation-v1`
- window `72 sim hours`
- `alpha = 0.3`

Reference factors:
- recent 0.0 units -> 1.0000
- recent 1.0 -> 0.7692
- recent 2.0 -> 0.6250
- recent 4.0 -> 0.4545

This is one future multiplicative adaptation factor only. It is not a gain, does not consume stimulus, and does not mutate Strength or event history.

Only `training_stimulus.domain == strength` counts. Other domains are ignored. Evidence outside the rolling window is ignored.

Raw stat mutation remains forbidden by `docs/TRAINING_PROGRESSION_GATES.md`. Recovery Realization, Detraining/Prolonged-Untrained Decay, and composed Adaptation Preview remain mandatory later gates.
