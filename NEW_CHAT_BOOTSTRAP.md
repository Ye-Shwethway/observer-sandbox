# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then task-relevant contracts. Core/runtime/schema/action work: `docs/ARCHITECTURE.md` + `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`. Spatial work: `docs/WORLD_LOCATION_NODE_MODEL.md`. Character/profile work: `docs/CHARACTER_PROFILE_SCHEMA.md`. Telegram: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` + `docs/TELEGRAM_NOTIFICATION_POLICY.md`. Needs/effects: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

Authority: current Creator instruction > canonical repo > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > old chat/memory. Never conflate committed, CI-validated, deployed, DB-applied and live-behavior-verified states.

## Development policy — minimum runnable expansion

The schema-v4 composable-runtime refinement was the deliberate one-time broad foundation pass. From now on, normal development proceeds through the smallest useful runnable vertical slice.

Default shape:
`minimum required state -> minimum deterministic/query behavior -> minimum Creator-facing observation/control -> focused tests/acceptance -> deploy/readback -> next slice`.

Do not pre-build large future subsystems merely because schema v4 has sockets for them. Inventory, memory, relationships, environment, combat, modifiers and regional world expansion remain demand-driven. A roadmap slice should become independently runnable/observable before moving to the next one.

Avoid the Simiverse-style failure mode where extensive schema/docs/subsystems accumulate long before a usable runtime checkpoint exists.

## Production baseline

- Repo: `Ye-Shwethway/observer-sandbox` private
- VPS app: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- systemd: `observer-sandbox`
- physical SQLite schema: version 4
- world root: `world_observer_universe`
- world identity revision: `thorne-estate-v3.0-scoped-ids`
- continuous Darian autonomy: enabled, normal, 1x
- cognition: configured Gemini character/cognition binding, wake-on-demand only
- Telegram: live, Owner/Allowed split; per-user notifications default ON

Production continues autonomously. Re-read live state whenever exact current Darian activity/stat values matter.

## Composable LEGO runtime — PRE-EXPANSION HARDENING COMPLETE

Canonical runtime expression:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

Schema-v4 foundation is implemented.

### State ownership

Universe-global `runtime_state` owns shared state such as `sim_time`, speed, pause, world id and global/UI settings where appropriate.

Per-actor `actor_runtime` owns autonomy enabled/mode, pending action id, lease, retry/backoff and cognition wake reason/stats. Retired Darian-only singleton scheduler JSON keys are no longer authoritative.

Character profile ontology remains separate from actor scheduler runtime: profile/domain fields describe character facts/state; `actor_runtime` describes scheduler/cognition operation; `action_instances` describe action instances/history.

### First-class actions / events / definitions

`action_definitions` contains data-driven core action metadata. `action_instances` persists action id/type, actor, place, target, participants/resources, condition/modifier snapshots, duration/planned timing, status and outcome/state-change data.

Events support queryable UUID, action id, location id, causal parent, structured state changes and normalized participants.

`entity_definitions` + `entities.definition_id` provide reusable definition -> concrete instance separation. Immediate effect operations support add/multiply/set/clamp; `active_modifiers` is a future persistence socket, not a mandate to build a universal modifier engine now.

### Multi-actor scheduling/time

The service enumerates active actor runtimes. One universe has one sim clock; each action has its own interval. Concurrent same-start actions do not serially double-count time.

Quasi remains test-only architecture proof, not a production autonomous character yet.

### Dynamic location / possession semantics

`contains` = structural hierarchy. `connected_to` = traversal. `located_at` = dynamic physical presence. Future `owned_by`, `carried_by`, `equipped_by` and container semantics remain distinct.

## Schema v4 evidence

CI #253 / run `31666099784`: SUCCESS on the complete schema-v4 code/test set before final documentation-only sync.

Deploy #112 / run `31665737560`: SUCCESS. Live readback verified systemd active, Telegram connected, schema 4, correct world id, autonomy enabled/normal, paused false, speed 1.0 and valid actor-scoped pending action.

Bounded Autonomy Acceptance #5 / run `31665851475`: SUCCESS on disposable production DB copy at 3600x with production read back unchanged; recovery trajectory ended with `needs_acceptable=true`.

Evidence level: schema-v4 hardening is implemented, CI-validated, deployed, DB-applied and live-runtime verified.

## World / location architecture

Current hierarchy:
`world_observer_universe -> loc_thorne_estate -> floor/zone -> room -> object`

Globally scoped/path-independent ids remain mandatory. Prototype spatial ids remain retired. Estate exterior is locked/non-traversable. Do not broaden outside yet.

Future regional insertion remains possible:
`world_observer_universe -> loc_south_lake_tahoe -> loc_thorne_estate`.

## Wake-on-demand / cost policy

Frequent scheduler ticks do not mean frequent LLM calls. Each active actor wakes a model only at a real decision boundary. Preserve this as characters scale; do not add periodic reflection/heartbeat loops without explicit Creator approval.

## Telegram / roadmap audit result

P2.1 LIVE. P2.2.1 inline Observer Home COMPLETE. P2.2.2A scoped Thorne Estate foundation COMPLETE/LIVE VERIFIED.

The 2026-08-13 roadmap audit found that schema v4 remains compatible with the intended future architecture; no additional foundation rewrite is required. The required correction was **development sequencing**, not ontology.

P2.2 is now a sequence of independent runnable checkpoints:

1. **P2.2.2B Minimum Telegram Estate Browser — NEXT**
   - Universe -> Thorne Estate -> floor/zone -> room
   - room detail: occupants, objects, exits, current/recent activity when available
   - graph-derived Back/Home navigation
   - no item mechanics/inventory/second-character work required for acceptance

2. **P2.2.3 Minimum Item/Object Browser**
   - open current room object -> detail -> back
   - show existing capabilities/effects/definition-instance data only
   - no quantity/durability/inventory engine yet

3. **P2.2.4 Character Profile Browser — single-character minimum**
   - Characters -> Darian -> profile sections
   - read-only/paginated canonical profile browsing
   - no selected-character session state required while only one production character exists

P2.3 remains later and must also be slice-by-slice, not a single large control project.

## Post-P2 sequencing

### P3 — First Richer Simulation Vertical Slice

Choose one concrete bounded simulation capability only when ready. Add only its required state/definitions, make deterministic behavior runnable, expose enough observer data, run bounded acceptance, deploy, then stop. No general-purpose rich-state framework first.

### P4 — Context / Memory / Relationship Slice When Required

Memory/relationship/context becomes demand-driven. Build the smallest mechanism only when a concrete autonomous behavior or observer use case needs it. No bulk memory ontology/background reflection mega-phase.

### P5 — Second Production Character

Quasi onboarding should use schema v4 rather than trigger another core rewrite. Minimum first slice: canonical profile/runtime seed, cognition binding/policy, valid location/state, independent wake-on-demand autonomy, Telegram character selection now that a second real character exists, and bounded two-actor acceptance. Rich relationships/group actions/shared memory remain separate later slices.

### Later South Lake Tahoe expansion

Regional expansion must also start with one runnable external destination/traversal path, not a large pre-authored region. Keep unimplemented Tahoe behind non-traversable boundaries and expand destination-by-destination.

## Exact resume point

**Resume P2.2.2B Minimum Telegram Estate Browser on schema v4.**

Do not perform another broad foundation refinement unless a concrete future slice proves a missing core invariant. Preserve actor-scoped runtime, first-class actions/events, scoped ids, one concurrency-safe universe clock, wake-on-demand cognition, locked unfinished boundaries, notification preferences, Telegram presentation rules and evidence-level distinctions.