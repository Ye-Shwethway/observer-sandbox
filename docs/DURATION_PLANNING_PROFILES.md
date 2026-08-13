# Deterministic Action Duration Planning Profiles

Status: IMPLEMENTED CANDIDATE / NOT YET DEPLOYED

## Purpose

Separate broad action legality from ordinary planning realism.

Existing `action_definitions` min/max duration values remain compatibility and validation bounds. They are intentionally broad enough to preserve already-running persisted actions across deployments.

For newly model-planned actions, a narrower deterministic preferred range may be attached by action type and, where useful, by target. The model sees both ranges. If it proposes a duration outside the preferred planning range, the cognition adapter clamps the requested duration to the nearest preferred bound before the action is handed to runtime validation/scheduling.

This does not modify existing pending actions, action targets, reasons, simulation time, or schema.

## v1 generic planning profiles

- move: 2–8 min
- eat: 10–30 min
- drink: 2–5 min
- shower: 8–20 min
- rest: 10–60 min
- inspect: 2–6 min
- use: 2–10 min
- train: 30–90 min
- read: 20–60 min
- idle: 5–20 min

Sleep is intentionally not clamped in v1 because nap and overnight sleep semantics are not yet separated. Existing need/routine duration guidance remains authoritative there.

## v1 target overrides

- Refrigerator inspect: 2–5 min
- Pantry inspect: 2–5 min
- Stove use: 10–30 min
- Research Desk read: 20–90 min
- Heavy Bag train: 20–45 min
- Free Weights train: 45–90 min
- Combat Mat train: 20–60 min
- Practice Dummy train: 20–60 min

## Architecture boundary

This is a cognition/planning constraint, not a new action-legality system. `validate_action()` and persisted `action_definitions` retain their existing broad duration bounds. Fixed deterministic providers and old pending actions are not rewritten by these profiles.

Later activity-semantic slices may replace generic `use` with richer verbs. Duration profiles should then follow those concrete semantics rather than growing a giant target-specific exception map.
