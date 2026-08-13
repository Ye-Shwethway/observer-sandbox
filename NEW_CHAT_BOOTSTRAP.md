# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then task-relevant contracts. Core/runtime/schema/action work: `docs/ARCHITECTURE.md` + `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`. Spatial work: `docs/WORLD_LOCATION_NODE_MODEL.md`. Character/profile work: `docs/CHARACTER_PROFILE_SCHEMA.md`. Telegram: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` + `docs/TELEGRAM_NOTIFICATION_POLICY.md`. Needs/effects: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

Authority: current Creator instruction > canonical repo > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > old chat/memory. Never conflate committed, CI-validated, deployed, DB-applied and live-behavior-verified states.

## Production baseline

- Repo: `Ye-Shwethway/observer-sandbox` private
- VPS app: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- systemd: `observer-sandbox`
- **physical SQLite schema: version 4**
- world root: `world_observer_universe`
- world identity revision: `thorne-estate-v3.0-scoped-ids`
- continuous Darian autonomy: enabled, normal, 1x
- cognition: configured Gemini character/cognition binding, wake-on-demand only
- Telegram: live, Owner/Allowed split; per-user notifications default ON

Production continues autonomously. Re-read live state whenever exact current Darian activity/stat values matter.

## Composable LEGO runtime — PRE-EXPANSION HARDENING COMPLETE

Canonical runtime expression:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

The prior audit is no longer merely proposed. Schema-v4 foundation is implemented.

### State ownership

Universe-global `runtime_state` owns shared state such as `sim_time`, speed, pause, world id and global/UI settings where appropriate.

Per-actor `actor_runtime` owns autonomy enabled/mode, pending action id, lease, retry/backoff and cognition wake reason/stats. Retired Darian-only singleton scheduler JSON keys are migrated into `actor_runtime` and are no longer authoritative.

Character profile ontology remains separate from actor scheduler runtime: profile/domain fields describe character facts/state; `actor_runtime` describes scheduler/cognition operation; `action_instances` describe current/history action instances.

### First-class actions

`action_definitions` contains data-driven core action metadata. Current verbs include move/sleep/eat/drink/shower/rest/inspect/use/train/read/idle.

`action_instances` persists action id/type, actor, place, target, participants/resources, condition/modifier snapshots, duration/planned timing, status and outcome/state-change data. Actor runtime references a pending action by id. Domain-specific validation may layer on top of generic action-definition metadata.

### Multi-actor scheduling/time

The service enumerates all active actor runtimes; it no longer structurally assumes only Darian can be scheduled.

One universe has one sim clock, while each action has its own interval. Same-start concurrent actor actions do **not** serially double-count duration; the universe clock advances to the maximum committed action end. Tests include Darian + a Quasi stub with independent pending actions and concurrent completion.

Quasi is **not yet a production autonomous character**; the stub is test-only proof of architecture.

### Events

Events now support queryable event UUID, action id, location id, caused-by event id, structured state changes and normalized `event_participants`. Action-completion events link back to the action instance.

### Definitions / instances / modifiers

`entity_definitions` + `entities.definition_id` provide reusable-definition -> concrete-instance separation for future items/equipment.

Immediate effect operations support add/multiply/set/clamp. `active_modifiers` provides the persistence socket for sourced/time-bounded/conditional modifiers and stack policy. Full modifier evaluation across every future domain remains deferred.

### Dynamic location / possession semantics

`contains` = structural/static hierarchy. `connected_to` = traversable topology. `located_at` = dynamic physical presence. Future ownership/possession remains distinct: `owned_by`, `carried_by`, `equipped_by`, container/storage semantics.

`src/observer_sandbox/location_runtime.py` exposes the generic dynamic-location boundary. Character `runtime.location` remains a mirrored compatibility/cache path during transition; static fixtures may resolve through structural containment.

## Schema v4 migration/evidence

Key implementation commits:
- composition schema `c617ffe13c2cc081d3ef34d9f7357a808fe5c285`
- DB schema v4 `9f3accd77e1f0cff399a136981c2e887b9362f1a`
- actor runtime `88998c35ab1ef7507cbbfffe2cf8c9e086cb85ae`
- runtime migration `3916e4a124c5d0667ac82cecb5b0b8aec7e58e33`
- event linkage `e8c1da4745799089c697dedfe65ea36749e0b9a8`
- actor-scoped scheduler `00cfa11fe60d3ab4708b7dbb09fe98610da2acd7`
- concurrency-safe action time `f2b372c577514e97b23c4b330bfc37dbfa9c1fa6`
- multi-actor service loop `9b210e3c9b332659a3303c4cd1a74c59c02de1cc`
- generic dynamic location `57c62df9f542e36c29007a4fae8bf6defb5bcc4f`
- actor-generic Telegram action notification `dffd5869ff7431ce2a21f05d3b92b9f8086d33a8`

CI #253 / run `31666099784`: SUCCESS on the complete schema-v4 code/test set before final documentation-only sync. It includes fresh schema boot, actor-scoped autonomy/wake behavior, first-class action/event linkage, independent multi-actor pending actions, concurrency-clock invariant, definition-instance/modifier sockets and dynamic-location contract.

Deploy #112 / run `31665737560`: SUCCESS. Live readback verified systemd active, Telegram API connected, **schema_version=4**, `world_id=world_observer_universe`, autonomy enabled/normal, paused false, speed 1.0 and a valid actor-scoped pending action id. Cognition telemetry survived migration; old legacy pending was cleared at migration boundary rather than invented as a partial v4 action.

Bounded Autonomy Acceptance #5 / run `31665851475`: SUCCESS on a disposable production DB copy at 3600x. Production was read back unchanged afterward. Starting copied state included Energy 32.165 / Cleanliness 42.533. Trajectory: rest 60m -> move to Master Bathroom 5m -> rest 30m -> shower 15m. Final copied state: Energy 43.498, Hunger 30.331, Thirst 37.335, Sleepiness 34.835, Cleanliness 100.0, `needs_acceptable=true`.

Evidence level: **schema-v4 composable runtime hardening is implemented, CI-validated, deployed, DB-applied and live-runtime verified; bounded disposable behavior acceptance also passes.**

## World / location architecture

Globally scoped/path-independent ids remain mandatory. Current hierarchy:
`world_observer_universe -> loc_thorne_estate -> floor/zone -> room -> object`

Prototype `home`/`room_*`/generic estate object ids remain retired. Estate exterior is locked/non-traversable. Do not broaden outside yet. Future insertion remains:
`world_observer_universe -> loc_south_lake_tahoe -> loc_thorne_estate`, with later sibling locations such as `loc_quasi_home`.

## Physiology / effects

Five current stats retain recovery paths. Passive drift remains energy -2/h, hunger +2.5/h, thirst +3/h, sleepiness +3/h, cleanliness -0.8/h. Recovery-aware Darian policy remains v1.3. Generic `game.effects` are authoritative for current resources, and schema-v4 effect/modifier operations are the future common contract.

## Wake-on-demand / cost policy

Frequent scheduler ticks do not mean frequent LLM calls. Each active actor wakes a model only at a real decision boundary: autonomy enabled, unpaused, no pending action, no retry block. Preserve this as characters scale.

## Telegram

P2.1 LIVE; P2.2.1 inline Observer Home COMPLETE; P2.2.2A scoped Thorne Estate foundation COMPLETE/LIVE VERIFIED.

Action-completion notifications are downstream of deterministic commit, per-user gated/deduplicated and now resolve the actual actor name rather than hard-coding Darian. Telegram presentation rules remain mandatory.

## Roadmap / exact resume point

- P0 Foundation/Remote Control: COMPLETE
- P0.5 Provider Layer: FOUNDATION COMPLETE
- P1 Living Darian: LIVE; engine/recovery/composition hardening PASSED
- P2 Telegram Observer: ACTIVE
  - P2.1 LIVE
  - P2.2.1 COMPLETE
  - P2.2.2A Thorne Estate interior/scoped IDs COMPLETE
  - pre-expansion schema-v4 composable runtime gate COMPLETE
  - **P2.2.2B Telegram Estate Browser NEXT**
  - P2.2.3 Item Browser after Estate Browser
  - generic character selection/profile browsing after that
- P3+ later

Do not expand South Lake Tahoe yet. Resume the recursive Telegram Estate Browser on schema v4. Preserve actor-scoped runtime, first-class actions/events, scoped ids, one concurrency-safe universe clock, wake-on-demand cognition, locked unfinished boundaries, notification preferences and evidence-level distinctions.