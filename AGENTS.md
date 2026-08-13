# Observer Sandbox Repository Instructions

## Startup

Before making material changes, read `NEW_CHAT_BOOTSTRAP.md` and treat newer repository/runtime evidence as authoritative over remembered chat context.

Also read directly relevant contracts. For core/runtime/schema/action work read `docs/ARCHITECTURE.md` and `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`; for world/location/topology work read `docs/WORLD_LOCATION_NODE_MODEL.md`; for Telegram work read `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`; for living-needs/recovery/item effects read `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`; for character-profile work inspect `docs/CHARACTER_PROFILE_SCHEMA.md` plus `config/characters/`; for deployment/runtime work inspect `.github/workflows/` and `deploy/`.

## Continuity rule

`NEW_CHAT_BOOTSTRAP.md` is the durable cross-chat handoff. After every material repository or verified runtime change, update it in the same work session. Never conflate authored/committed, CI-validated, deployed, DB-applied and live-runtime-verified evidence.

## Authority order

1. Explicit current Creator instruction.
2. Current canonical repository config/schema/contracts.
3. Verified live VPS/runtime/database evidence.
4. Deployed workflow evidence.
5. Current CI/test evidence.
6. `NEW_CHAT_BOOTSTRAP.md`.
7. Older chat/model memory.

## Composable runtime contract

All new simulation/runtime work must preserve the LEGO rule:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

- LLMs propose structured actions; they never mutate arbitrary DB/world state directly.
- Universe-global state (`sim_time`, speed, pause, world identity) stays separate from actor-scoped scheduler/cognition state.
- Actor autonomy, pending action, lease, retry and wake telemetry belong to `actor_runtime`; do not reintroduce singleton Darian scheduler keys.
- Actions are first-class `action_instances` referencing data-driven `action_definitions`.
- New action types should extend definition metadata and reusable validation primitives rather than grow character-specific switch logic.
- One shared universe clock must not double-count concurrent actor durations; action intervals are independently recorded.
- Events must retain action/location/state-change linkage and participants where relevant.
- Definitions/Templates, Instances and Runtime State are distinct concepts.
- Conditions/modifiers should use the shared effect/modifier contract; do not invent incompatible per-feature effect formats.
- Full feature engines may remain deferred, but their implementations must attach through these generic contracts.

## World / location node contract

All spatial/world changes must preserve `docs/WORLD_LOCATION_NODE_MODEL.md`.

- Locations are recursively nestable graph nodes, not hard-coded screen labels.
- Entity ids are technical identities, never display names.
- Spatial/resource ids are globally unique, type-prefixed and place-scoped where names repeat: `world_*`, `loc_*`, `obj_*`.
- Keep ids path-independent; mutable parent/floor topology belongs in relations.
- Canonical current root is `world_observer_universe`; Thorne Estate is `loc_thorne_estate`.
- Prototype ids `home`, `observer_universe`, `zone_*`, `room_*` and generic estate `obj_*` are obsolete.
- `contains` means structural/static containment; `connected_to` means traversable topology; `located_at` is generic dynamic presence.
- Ownership/possession (`owned_by`, `carried_by`, `equipped_by`) must not be conflated with current physical location.
- Locked/unimplemented boundaries must have no traversable edge.
- Canon facts and provisional layout must remain distinguishable.
- Deterministic routing derives from graph relations, not hard-coded room-pair tables.
- Telegram/UI consumes generic query contracts rather than mansion-specific topology.

## Living physiology and item-effect contract

All needs/recovery changes must preserve `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

- Recovery-labelled actions must improve the intended need after passive drift.
- Every current basic physiological stat retains a reachable restoration path.
- Food/drink/shower effects are authored deterministic effects, not prompt prose.
- `action_options()` exposes useful effect information to cognition while the deterministic engine remains authoritative.
- Shared effect operations include add/multiply/set/clamp; temporary/sourced modifiers use the composable modifier contract.
- Do not add restorative capabilities without deterministic effects and regression coverage.
- Persistent first-class pending actions must be considered during world/effect migrations.

## Telegram presentation contract

Every Creator-facing Telegram message follows `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.

- visible sim time: `dd-mm-yyyy (Day) hh:mm AM/PM`;
- canonical ISO time remains internal;
- friendly entity names in normal views;
- concise sections, whitespace and restrained icons;
- ON/OFF and Yes/No instead of raw booleans;
- default history suppresses engine/control bookkeeping;
- paginate/section large datasets;
- presentation stays downstream of generic query/control services;
- proactive character-action notifications must resolve the actual actor name, not assume Darian forever.

## Scope discipline

Observer Sandbox is intentionally small and modular. Do not recreate EIDOLON/Simiverse-scale subsystem sprawl. Build bounded, tested vertical slices on the generic contracts above.