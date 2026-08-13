# Runtime Speed Control v1

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / CREATOR LIVE UX VERIFIED

## Purpose

Make universe speed usable during active development without cancelling or re-planning a running action.

## Contract

- Global speed remains bounded to `0 < speed <= 3600`.
- A speed change may occur while one or more actor actions are pending.
- Each pending action preserves identity, action type, target, planned simulated duration and simulated end time.
- Only the remaining wall-clock schedule is recalculated.
- Repeated speed changes preserve remaining simulated time rather than compounding error.
- Pause freezes pending-action wall countdown; resume shifts pending due times by actual paused wall duration.
- Speed may change while paused without consuming paused time.

No schema v5 is required. Existing `action_instances.due_wall_time` and `speed_at_plan` fields are sufficient.

## Creator surface

Telegram `/speed <value>` works during a running action.

Examples:
- `/speed 1` — normal real-time observation
- `/speed 10` — 60 simulated minutes take about 6 real minutes
- `/speed 30` — 60 simulated minutes take about 2 real minutes
- `/speed 60` — 60 simulated minutes take about 1 real minute

## Evidence

- PR #8 merge `1799dd7c7723866ec15dc29a05c682de8e1d5e4a`.
- Main CI #354 / run `31679969639` SUCCESS.
- Runtime Speed Control Acceptance #1 / run `31679969684` SUCCESS on candidate code + disposable production DB copy with zero model calls.
- Release commit `846fdeef1c35e88986e2dbb6909b4d10092f148a`.
- Deploy #134 / run `31680016710` SUCCESS.
- Creator live verification: a running 60-sim-minute Heavy Bag action was changed to `30x`; Telegram Runtime showed the same pending Train action, `60 sim min • ~2 min real @ 30x`, expected simulated completion unchanged, and roughly 1.3 real minutes remaining at observation time.

## Non-goals

This slice does not add automatic development-speed selection, per-character time scales, non-linear simulation time, or schema v5.
