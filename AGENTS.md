# Observer Sandbox Repository Instructions

## Startup

Before making material changes, read `NEW_CHAT_BOOTSTRAP.md` and treat newer repository/runtime evidence as authoritative over remembered chat context.

Also read directly relevant contracts. For core/runtime/schema/action work read `docs/ARCHITECTURE.md` and `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`; for world/location/topology work read `docs/WORLD_LOCATION_NODE_MODEL.md`; for Telegram work read `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`; for privileged runtime/world mutation read `docs/CREATOR_CONTROL_POLICY.md`; for living-needs/recovery/item effects read `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`; for character-profile work inspect `docs/CHARACTER_PROFILE_SCHEMA.md` plus `config/characters/`; for validation/release/deployment work read `docs/PRODUCTION_VALIDATION_AND_RELEASE_PROTOCOL.md`, then inspect `.github/workflows/` and `deploy/` only as needed.

## Continuity rule

`NEW_CHAT_BOOTSTRAP.md` is the durable cross-chat handoff. After every material repository or verified runtime change, update it in the same work session. Never conflate authored/committed, CI-validated, deployed, DB-applied and live-runtime-verified evidence.

## Production validation and release contract

All production-copy acceptance and production release work must follow `docs/PRODUCTION_VALIDATION_AND_RELEASE_PROTOCOL.md`.

- Do not invent a new SSH/SQLite-copy/deploy workflow for each feature.
- Production-state acceptance must reuse `.github/workflows/reusable-production-copy-validation.yml` unless a concrete missing invariant makes the shared path insufficient.
- Feature-specific acceptance logic belongs in a focused validator under `scripts/validation/`; it receives only the disposable DB through `OBSERVER_SANDBOX_DB`.
- The shared SQLite copy primitive is `scripts/validation/create_disposable_db_copy.py`; do not replace it with ad-hoc `cp`/heredoc copy logic.
- Validation may accelerate or mutate only the disposable copy. Never accelerate or directly edit production for testing.
- Feature validators must not call models, Telegram or other external side effects and must not operate systemd/service controls.
- If the shared protocol itself is insufficient, update the protocol document + shared helper/workflow + focused self-test first; then reuse the updated mechanism. Do not carry feature-local infrastructure forks forward.
- Runtime-affecting accepted changes deploy only through the canonical `.github/workflows/deploy.yml` path. Docs/test/validation-tooling-only changes do not need ceremonial production deploys.
- Post-deploy production checks are read-only unless the Creator separately authorizes a control mutation.

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

## Creator control contract

All privileged direct world/runtime mutations must follow `docs/CREATOR_CONTROL_POLICY.md`.

- Creator controls are typed administrative interventions, not character actions and not LLM/cognition proposals.
- Creator authorization permits a bounded mutation; it does not silently transfer domain field ownership away from the normal engine.
- Telegram owner-only controls must re-check authority server-side; hiding a button is not authorization.
- A potentially destructive/mutating inline control should use an explicit confirmation step.
- If a control makes an outstanding action semantically stale, cancel/invalidate that action and clear relevant lease/retry state before cognition resumes.
- Every successful privileged mutation must write a queryable audit event containing actor/target context, request source, before/after evidence and state changes.
- Reuse the same backend control service from Telegram, CLI and Actions; do not duplicate SQLite mutation logic in UI/workflow adapters.
- LLMs never receive Creator-control authority.
- Do not build arbitrary-field editors, SQL consoles or generic unrestricted admin mutation surfaces; add one narrow control only when a concrete operational use case exists.

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

## Expansion execution policy

Use **exemplar-first, then batch-by-pattern** for repeated world/action/content expansion.

- The first item in a new structural pattern is a small standalone exemplar used to prove schema shape, validation, persistence, observability and acceptance behavior.
- Once that pattern is green and deployed, structurally equivalent follow-on items should normally be implemented as one bounded batch rather than one PR/deploy per item.
- A batch should use one branch/PR, one focused regression suite, one disposable production-copy dry-run covering every item, iterative fixes on that copy as needed, then merge only when the entire batch is green, followed by one production deploy/readback.
- Batch only items that reuse the same proven invariant and validation path. If an item requires a new state model, new authority rule, new mutation invariant or materially different runtime semantics, remove it from the batch and treat it as a new exemplar.
- Do not batch merely to maximize item count. Keep batches reviewable and rollback-friendly.

## Scope discipline

Observer Sandbox is intentionally small and modular. Do not recreate EIDOLON/Simiverse-scale subsystem sprawl. Build bounded, tested vertical slices on the generic contracts above.
