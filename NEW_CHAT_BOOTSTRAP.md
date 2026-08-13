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

## Latest live liveness check — 2026-08-13 04:25 UTC

Deploy #114 readback verified:
- systemd active;
- Telegram API connected;
- schema version 4 healthy;
- autonomy enabled / normal / paused false / speed 1.0;
- Darian at Kitchen with current action `rest`;
- valid actor-scoped pending action id `f8041eed-aeed-4f0f-a303-92eed9ca72fd`;
- decision calls remained 19, last decision wall time `2026-08-13 03:54:55 UTC`.

At that readback only about 30.5 wall minutes had elapsed since the decision, so a 60-minute rest action could legitimately still be pending. The current scheduler advances committed simulation time at action completion, so sim time may remain at the action start while a long action is in progress. Lack of a new notification during that window is not evidence that the service/universe stopped.

## P2 Telegram Observer

P2.1 LIVE. P2.2.1 inline Observer Home COMPLETE. P2.2.2A scoped Thorne Estate foundation COMPLETE/LIVE VERIFIED.

### P2.2.2B Minimum Telegram Estate Browser

Status: **IMPLEMENTED / CI-VALIDATED / DEPLOYED — CREATOR UI ACCEPTANCE PENDING**.

Implemented:
- Universe -> Thorne Estate -> floor/zone -> room through stable location callbacks;
- location/room detail renders child areas, occupants + current action, objects, exits and recent location activity when available;
- parent Back navigation derives from canonical `contains` relations;
- locked exterior displays as unavailable/view-only and remains non-traversable;
- occupant resolution uses generic dynamic-location contract;
- recent location activity queries schema-v4 event `location_id`;
- no item-detail/inventory behavior was added prematurely.

Evidence:
- query contract commit `46b3e44bdd089b37a0eae6d9257c401ad904820f`;
- Telegram browser commit `6ca1be4a886756a280e8aeec35feb4f0c27765d4`;
- recursive navigation tests commit `6ec152df67116ceea75c4c77046c3ec54264f6a1`;
- CI #260 / run `31666982672`: SUCCESS;
- Deploy #114 / run `31666950518`: SUCCESS with live runtime/service/Telegram readback green.

Do not call the browser live-UX-verified until the Creator personally exercises the deployed callbacks in Telegram.

## Next minimum runnable slice

After Creator estate-browser UI acceptance, resume **P2.2.3 Minimum Item/Object Browser**:
- open an existing room object -> detail -> back;
- show name, type/definition, capabilities, current location and authored effects where present;
- use definition/instance-aware presentation;
- do not add quantity/stacks/depletion/durability/inventory mutation yet.

P2.2.4 after that is a single-character Darian Profile Browser. P3 becomes one richer simulation vertical slice, not a broad rich-state phase. Memory/relationships are demand-driven later. Quasi onboarding is a later P5 character slice using existing schema v4 rather than another core rewrite.

Preserve actor-scoped runtime, first-class actions/events, scoped ids, one concurrency-safe universe clock, wake-on-demand cognition, locked unfinished boundaries, notification preferences, Telegram presentation rules and evidence-level distinctions.