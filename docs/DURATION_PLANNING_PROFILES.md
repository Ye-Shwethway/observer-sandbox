# Deterministic Action Duration Planning Profiles

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED

## Purpose

Separate broad action legality from ordinary planning realism.

Existing `action_definitions` min/max duration values remain compatibility and validation bounds. They stay broad enough to preserve already-running persisted actions across deployments.

For newly model-planned actions, a narrower deterministic preferred range is attached by action type and, where useful, by target. The model sees both ranges. If it proposes a duration outside the preferred planning range, the cognition adapter clamps the requested duration to the nearest preferred bound before runtime validation/scheduling.

This does not modify existing pending actions, action targets, reasons, simulation time, or schema.

## Current generic planning profiles

- move: 2–8 min
- eat: 10–30 min
- drink: 2–5 min
- shower: 8–20 min
- rest: 10–60 min
- inspect: 2–6 min
- use: 2–10 min
- train: 30–90 min
- read: 20–60 min
- research: 20–90 min
- idle: 5–20 min

Sleep is intentionally not clamped because nap and overnight sleep semantics are not yet separated. Existing need/routine duration guidance remains authoritative there.

## Current target overrides

- Refrigerator inspect: 2–5 min
- Pantry inspect: 2–5 min
- Stove use: 10–30 min
- Research Desk read: 20–90 min
- Research Desk research: 30–90 min
- Heavy Bag train: 20–45 min
- Free Weights train: 45–90 min
- Combat Mat train: 20–60 min
- Practice Dummy train: 20–60 min

## Architecture boundary

This is a cognition/planning constraint, not a new action-legality system. `validate_action()` and persisted `action_definitions` retain their broad duration bounds. Fixed deterministic providers and old pending actions are not rewritten by these profiles.

Activity-semantic slices should add concrete duration semantics only for concrete verbs/targets rather than growing a giant generic exception map.

## Evidence

Initial duration-profile slice:
- PR #9 merge `4d7d949002a4444f6ae6424e502fa872f6d90a33`.
- PR CI #357 / run `31680626619` SUCCESS.
- Main CI #358 / run `31680683357` SUCCESS.
- Duration Planning Profiles Acceptance #1 / run `31680683416` SUCCESS.
- Release commit `1130b2ec09c456293cdb7e6a5451cef15deffa56`.
- Deploy #135 / run `31680728818` SUCCESS.

Research extension:
- PR #10 merge `c50f4cf9a87b15589be3b3ea4878990da7e69d02`.
- Research Action Semantics Acceptance #1 / run `31681716339` SUCCESS.
- Deploy #136 / run `31681760620` SUCCESS.
