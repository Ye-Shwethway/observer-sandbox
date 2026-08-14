# Regional Measurement Detraining v1

Status: implementation contract

## Purpose

Regional Measurement Detraining extends BC-3 so training-acquired regional circumference does not persist forever after the corresponding resistance stimulus disappears.

Invariant:

`BC-3 activation baseline + immutable regional resistance history + bounded BC-2 settlement window -> regional inactivity pressure -> reversible post-activation excess decay`

This remains part of the existing `body_progression_engine`. It is not a second body-composition or anatomy authority.

## Baseline protection

Detraining never erodes authored BC-3 activation anatomy by itself.

The activation measurement is the local floor for detraining-only loss. A region may fall below that number only through other authoritative BC-3 signals such as systemic BC-2 lean-mass loss or adiposity change.

This matters because the engine does not pretend that absence of post-activation training history proves the character was historically untrained.

## Regional inactivity evidence

The engine derives inactivity from immutable completed resistance-training events after BC-3 activation.

For each BC-3 region it records the most recent qualifying resistance exposure. Training Anatomy v1 `movement_anatomy.regional_load` is preferred; historical/no-selection events retain Training Method Semantics method-level fallback.

A regional load below the authored minimum exposure threshold does not reset that region's detraining clock.

No new state table or schema migration is required. The clock is reconstructed deterministically from event evidence.

## Conservative time course

The v1 policy intentionally avoids immediate shrinkage:

- 21 simulated days of grace after the last qualifying regional stimulus;
- pressure then ramps over 63 simulated days;
- at full pressure, a normal 24-hour BC-2 window may remove at most 0.4% of the region's remaining post-activation excess;
- existing BC-3 per-field absolute window clamps still apply.

These are conservative simulation parameters rather than claims of an exact universal biological curve. Human detraining evidence is heterogeneous, especially over short cessation periods; longer cessation more consistently shows loss of muscle size.

## Double-count protection

BC-2 already supplies systemic FFM loss to BC-3 through `partition_delta_ffm_lb`.

When that signal is negative, regional detraining adds no extra circumference loss in the same settlement window. The ordinary BC-3 `lean_loss_delta_in` remains authoritative for that systemic tissue decline.

This prevents one biological loss from being charged twice as both whole-body lean loss and regional disuse loss.

## Training protection

Recent qualifying regional resistance work resets only the regions it materially loads.

A chest/press session can therefore protect chest, shoulders and triceps while calves or thighs continue accumulating inactivity pressure. This is downstream of universal movement/method evidence and contains no Darian or Thorne Estate branch.

## Persistence and audit

Every ordinary BC-3 settlement now includes:

- `regional_detraining.source`;
- whether extra detraining was suppressed by systemic FFM loss;
- per-region last qualifying exposure time;
- per-region inactive days and current pressure;
- per-field `regional_detraining_delta_in` in projection detail.

The same atomic profile-history + settlement-event transaction remains authoritative.

## Validation

Focused regressions prove:

- no detraining pressure during the grace period;
- pressure ramps after the grace period;
- recent training resets only qualifying regions;
- detraining erodes only post-activation excess and cannot cross the authored activation baseline by itself;
- negative BC-2 partition FFM suppresses extra regional detraining, preventing double counting.

The existing BC-3 disposable-production-copy acceptance also verifies the new audit metadata against current production-shaped state without mutating production.

## Deferred

This slice does not add:

- age-related sarcopenia;
- illness or immobilization-specific atrophy multipliers;
- injury-specific local atrophy;
- bone remodeling;
- fluid/glycogen circumference noise;
- height lifecycle;
- sexual-anatomy lifecycle;
- an extra LLM call.
