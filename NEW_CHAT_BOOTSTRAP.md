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

Do not pre-build large future subsystems merely because schema v4 has sockets for them. Inventory, memory, relationships, environment, combat, modifiers and regional world expansion remain demand-driven. Avoid the Simiverse-style failure mode where extensive schema/docs/subsystems accumulate long before a usable runtime checkpoint exists.

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

Canonical expression:
`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.

Schema v4 provides actor-scoped scheduler state, first-class action definitions/instances, concurrency-safe single universe time, richer event linkage, definition->instance sockets, generic effect/modifier contracts and dynamic `located_at` semantics. Quasi remains test-only proof, not a production autonomous character.

## World / location architecture

Current hierarchy:
`world_observer_universe -> loc_thorne_estate -> floor/zone -> room -> object`.

Globally scoped/path-independent ids remain mandatory. `contains` is hierarchy, `connected_to` traversal, `located_at` dynamic presence. Estate exterior remains locked/non-traversable. Future regional insertion remains possible as `world_observer_universe -> loc_south_lake_tahoe -> loc_thorne_estate` without renaming existing nodes.

## Wake-on-demand / cost policy

Frequent scheduler ticks do not mean frequent LLM calls. Each active actor wakes a model only at a real decision boundary. Preserve this as characters scale; do not add periodic reflection/heartbeat loops without explicit Creator approval.

## Latest live liveness/readback evidence

Deploy #116 / run `31667377479` readback at 2026-08-13 04:33 UTC verified:
- systemd active;
- Telegram API connected;
- schema version 4 healthy;
- autonomy enabled / normal / paused false / speed 1.0;
- Darian at Kitchen with current action `rest`;
- valid actor-scoped pending action id;
- cognition binding preserved.

The earlier lack of a push notification was compatible with Darian still being inside a long pending rest action. Current scheduler advances committed sim time at action completion, so sim time can remain at action start while a long action is in progress.

## P2 Telegram Observer

P2.1 LIVE. P2.2.1 inline Observer Home COMPLETE. P2.2.2A scoped Thorne Estate foundation COMPLETE/LIVE VERIFIED.

### P2.2.2B Minimum Telegram Estate Browser

Status: **COMPLETE / LIVE UX VERIFIED**.

Implemented:
- Universe -> Thorne Estate -> floor/zone -> room through stable location callbacks;
- location/room detail renders child areas, occupants + current action, objects, exits and recent location activity when available;
- parent Back navigation derives from canonical `contains` relations;
- locked exterior displays as unavailable/view-only and remains non-traversable;
- occupant resolution uses generic dynamic-location contract;
- recent location activity queries schema-v4 event `location_id`.

Evidence:
- CI #260 / run `31666982672`: SUCCESS;
- Deploy #114 / run `31666950518`: SUCCESS;
- Creator exercised the deployed navigation and confirmed it worked, including observing Darian in the Kitchen.

### P2.2.3 Minimum Item/Object Browser

Status: **IMPLEMENTED / CI-VALIDATED / DEPLOYED — CREATOR UI ACCEPTANCE PENDING**.

Implemented:
- room object rows now open stable `obj:*` callbacks;
- object detail shows human-readable name, concrete-instance/definition status, current location, capabilities and authored effects;
- `entities.definition_id -> entity_definitions` is used when a definition exists; current instance-only fixtures remain valid;
- effective location resolves through generic dynamic/static location semantics;
- effect rendering handles current scalar deltas and schema-v4 add/multiply/set/clamp forms;
- Back returns to the actual room and Home remains available;
- no quantity/stacks/depletion/durability/inventory/ownership mutation was added.

Evidence:
- query contract commit `715a575642012c7aaef92cc26d27e8d8ba69ce8a`;
- Telegram browser commit `b26423aa1bc67ad239eb9059042e3efe5479d41c`;
- focused tests commit `835f90a3bfbe13e165fa90187712ddc4da564dd7`;
- CI #265 / run `31667412478`: SUCCESS;
- Deploy #116 / run `31667377479`: SUCCESS with runtime/service/Telegram readback green.

Creator acceptance remaining: open at least one room object in Telegram, confirm readable details/effects, and return to the room successfully.

## Exact next minimum runnable slice

After Creator item-browser acceptance, proceed to **P2.2.4 Character Profile Browser — single-character minimum**:
- Characters -> Darian -> profile section menu;
- read-only section browsing of existing canonical/profile data;
- paginate/section large data;
- keep current runtime state separate from canonical profile;
- do not add second-character session persistence yet.

P3 remains one richer simulation vertical slice, not a broad rich-state phase. Memory/relationships are demand-driven later. Quasi onboarding remains a later P5 character slice using schema v4 rather than another core rewrite.

Preserve actor-scoped runtime, first-class actions/events, scoped ids, one concurrency-safe universe clock, wake-on-demand cognition, locked unfinished boundaries, notification preferences, Telegram presentation rules and evidence-level distinctions.
