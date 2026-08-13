# Runtime Speed Control v1

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / CREATOR LIVE UX VERIFICATION PENDING

## Purpose

Make universe speed usable during active development without cancelling or re-planning a running action.

## Contract

- Global speed remains bounded to `0 < speed <= 3600`.
- A speed change may occur while one or more actor actions are pending.
- Each pending action preserves its identity, action type, target, planned simulated duration and simulated end time.
- Only the remaining wall-clock schedule is recalculated.
- Remaining simulated minutes are derived from the current pending due time and its current scheduling speed, then converted to a new wall due time at the requested speed.
- Repeated speed changes preserve remaining simulated time rather than compounding error from the original plan.
- Pause freezes pending-action wall countdown. Resume shifts pending due times by the actual paused wall duration.
- Speed may change while paused; the calculation is anchored to the pause start so paused wall time is not consumed.

No schema v5 is required. The existing `action_instances.due_wall_time` and `speed_at_plan` scheduling fields are sufficient for the minimum runnable contract.

## Creator surface

Telegram already exposes:

`/speed <value>`

Examples:
- `/speed 1` — normal real-time observation
- `/speed 10` — 60 simulated minutes take about 6 real minutes
- `/speed 30` — 60 simulated minutes take about 2 real minutes
- `/speed 60` — 60 simulated minutes take about 1 real minute

The command now works even when an action is already running.

## Evidence

- PR #8 merged at `1799dd7c7723866ec15dc29a05c682de8e1d5e4a`.
- PR CI #353 passed after the legacy pending-speed guard test was updated to the new contract.
- Main CI #354 / run `31679969639` SUCCESS.
- Runtime Speed Control Acceptance #1 / run `31679969684` SUCCESS on candidate code + disposable production DB copy with zero model calls.
- Acceptance proved a 60-sim-minute pending action scheduled at 1x could be changed to 60x after 10 simulated minutes had elapsed, preserving the same action id and rescheduling the remaining 50 simulated minutes to 50 real seconds.
- Acceptance also proved a 100-second pause shifts the pending due time by 100 seconds rather than consuming action countdown.
- Release commit `846fdeef1c35e88986e2dbb6909b4d10092f148a`.
- Deploy #134 / run `31680016710` SUCCESS.
- Deploy readback: service healthy, schema v4, autonomy enabled/normal/unpaused, speed still 1x until Creator changes it, existing pending action preserved, Gemini binding preserved, Telegram API connected.

## Non-goals

This slice does not add:
- automatic development-speed selection;
- Telegram speed preset buttons;
- per-character time scales;
- non-linear simulation time;
- action-duration planning profiles;
- schema v5.

## Next checkpoint

Creator should test a live speed change through Telegram while an action is pending, preferably `/speed 60`, then inspect `/status` or the character card to confirm the same pending action remains with a much shorter real-time remainder.
