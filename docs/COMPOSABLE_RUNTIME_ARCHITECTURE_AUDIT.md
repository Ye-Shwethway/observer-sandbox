# Composable Runtime Architecture Audit

Status: IMPLEMENTED FOUNDATION / PRE-EXPANSION GATE

## Goal

Canonical LEGO runtime rule:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> validated transition -> State Changes + Events`

The 2026-08-13 audit was performed before broader world and second-character expansion. Its structural findings have now been implemented as SQLite schema v4 foundation, while deliberately deferring full feature engines such as inventory, weather, memory and group synchronization.

## Implemented findings

### A1 — Actor-scoped runtime scheduling — IMPLEMENTED

`actor_runtime` now owns per-actor autonomy, pending action reference, lease, retry/backoff and cognition telemetry. Global `runtime_state` keeps universe-wide pause/speed/world/time. The long-running service enumerates active actor runtimes rather than assuming Darian is the only actor.

### A2 — First-class action instance — IMPLEMENTED

`action_instances` persists actor, action type, place, target, participants, resources, conditions, modifiers, timing, status and outcome. Actor runtime references the pending action by id rather than storing the entire plan as a singleton JSON blob.

### A3 — Data-driven action definitions — IMPLEMENTED FOUNDATION

`action_definitions` stores current action duration/target/capability/co-location metadata and is used by action-option resolution and validation. Specialized domain validators remain legal where generic metadata is insufficient; future verbs should extend the registry rather than grow character-specific switches.

### A4 — Conditions/modifiers/effect contract — IMPLEMENTED SOCKETS

Immediate effect specs support `add`, `multiply`, `set`, `clamp_min` and `clamp_max`. `active_modifiers` stores sourced/time-bounded modifiers with stack policy and conditions. A universal active-modifier resolver is intentionally not yet applied to every domain; feature modules will activate it incrementally.

### A5 — Event envelope / causality — IMPLEMENTED FOUNDATION

Events now support UUID, action id, location id, causal parent id and structured state-change data. `event_participants` supports multi-entity queries. Arbitrary domain detail remains payload JSON.

### A6 — Definition / instance separation — IMPLEMENTED FOUNDATION

`entity_definitions` stores reusable semantics; concrete `entities` may reference them with `definition_id`. This establishes the future Energy Drink/equipment/item definition-to-instance path without prematurely implementing quantities/durability.

### A7 — Ownership / containment / possession semantics — CONTRACT LOCKED

Semantic vocabulary is separated:
- `contains` structural/static containment
- `located_at` current dynamic presence
- `owned_by` ownership
- `carried_by` carriage/possession
- `equipped_by` equipped state
- container/storage relations for movable containment.

Full inventory mutation is deferred.

### A8 — Generic dynamic location — IMPLEMENTED FOUNDATION

`location_runtime.py` establishes `located_at` as the generic dynamic-location relation and exposes a generic resolver/setter. Character `runtime.location` remains a mirrored compatibility/cache representation for current code; static fixtures may resolve through structural `contains`. New movable entity systems should use the generic location contract.

## Multi-actor time invariant

One universe has one simulation clock. Each scheduled action has its own planned simulation interval. Concurrent actions do not serially double-count time: completion advances the universe clock to the maximum committed action end, not `current clock + every actor duration`.

Regression coverage includes two independent actors holding concurrent pending actions and completing same-start actions without doubling the global clock.

## Canonical runtime pipeline

1. Observe actor, place, global time, nearby resources, conditions/modifiers and recent events.
2. Resolve legal options from action definitions, capabilities, topology and state.
3. AI/deterministic policy proposes a structured action.
4. Runtime validates prerequisites.
5. Persist action instance and actor-scoped pending reference.
6. Complete/interrupt deterministically.
7. Commit authoritative state.
8. Emit linked event/state-change evidence.
9. Notify/query downstream observer surfaces.
10. Wake only actors at real decision boundaries.

## Intentionally deferred

The schema foundation does **not** mean these feature engines are implemented:
- inventory quantity/stack/depletion/durability
- rich relationship simulation
- memory selection/consolidation
- weather/environment simulation
- full temporary-modifier resolver across all domains
- complex multi-party reservation/synchronization/combat
- vehicles or broad regional traversal.

These should plug into the v4 contracts when their roadmap slice arrives.

## Acceptance boundary

The hardening gate is complete when all of the following are true:
- schema-v4/fresh DB tests pass;
- actor-scoped autonomy/wake tests pass;
- first-class action/event linkage tests pass;
- two-actor pending/concurrency clock tests pass;
- dynamic-location and definition/instance/modifier socket tests pass;
- accelerated disposable production-copy acceptance passes on v4;
- VPS readback verifies schema v4 and live actor runtime without breaking Telegram/autonomy.

Once those evidence conditions are satisfied, resume **P2.2.2B Telegram Estate Browser** before broader South Lake Tahoe expansion.