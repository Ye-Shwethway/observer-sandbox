# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then task-relevant contracts.

Core/runtime/schema/action: `docs/ARCHITECTURE.md` + `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`.
Spatial: `docs/WORLD_LOCATION_NODE_MODEL.md`.
Character/profile: `docs/CHARACTER_PROFILE_SCHEMA.md`.
Telegram: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` + `docs/TELEGRAM_NOTIFICATION_POLICY.md`.
Needs/effects: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.
Future grading: `docs/FUTURE_GRADING_SYSTEM.md`.

Authority: current Creator instruction > canonical repo > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > old chat/memory. Never conflate committed, CI-validated, deployed, DB-applied and Creator-live-UX-verified states.

## Development policy — minimum runnable expansion

Schema v4 was the deliberate one-time broad foundation refinement. Normal development now follows:

`minimum required state -> minimum behavior/query -> minimum Creator-facing surface -> focused tests -> deploy/readback -> Creator acceptance -> next slice`.

Do not pre-build large inventory, grading, memory, relationship, environment, combat or regional systems merely because extension sockets exist. Avoid the Simiverse-style failure mode where extensive subsystem work accumulates before runnable checkpoints.

## Production baseline

- Repo: `Ye-Shwethway/observer-sandbox`
- VPS app: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- systemd: `observer-sandbox`
- SQLite schema: v4
- world root: `world_observer_universe`
- estate: `loc_thorne_estate`
- world identity revision: `thorne-estate-v3.0-scoped-ids`
- Darian autonomy: enabled / normal / 1x / wake-on-demand
- Telegram: live private Creator observer; notifications default ON per authorized user

## LEGO runtime foundation

Canonical expression:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

Schema v4 provides actor-scoped runtime, first-class action definitions/instances, concurrency-safe one-universe time, richer event linkage, definition->instance sockets, effects/modifier persistence sockets and generic `located_at` semantics.

Do not perform another broad foundation rewrite unless a concrete runnable feature proves a missing invariant.

## Future grading direction — RESERVED, NOT IMPLEMENTED

The Creator wants a future universal grading/progression language similar in spirit to the earlier Simiverse concept, useful across character attributes, skills, items, locations/facilities, quests/challenges and unlock conditions.

Current decision:
- no schema v5 now;
- schema v4 is sufficient for later additive grading;
- preserve authoritative raw values/state;
- grades normally derive from a named grading scheme rather than replacing raw values;
- grading must be cross-domain and presentation-independent;
- exact tiers/thresholds/caps/unlock rules are intentionally not frozen yet;
- first grading work must be one minimum-runnable domain slice, then expand only after acceptance.

P2.2.4 profile browsing intentionally shows raw authoritative profile values without grade badges.

Canonical note: `docs/FUTURE_GRADING_SYSTEM.md`.

## World/location state

Current hierarchy:
`world_observer_universe -> loc_thorne_estate -> floor/zone -> room -> object`.

IDs are globally scoped and path-independent. `contains` = structural hierarchy, `connected_to` = traversal, `located_at` = dynamic presence. Estate exterior remains locked/non-traversable. Later `loc_south_lake_tahoe` can be inserted above the estate without renaming existing nodes.

## P2 Telegram Observer

### P2.2.2B Estate Browser

Status: COMPLETE / LIVE UX VERIFIED.

Creator successfully navigated Universe -> Thorne Estate -> floor -> room and observed Darian in Kitchen.

### P2.2.3 Item/Object Browser

Status: COMPLETE / LIVE UX VERIFIED.

Implemented room object buttons, readable object detail, definition/instance awareness, capabilities, authored effects and Back-to-room navigation. Creator tested the deployed flow and confirmed it worked.

Evidence:
- query `715a575642012c7aaef92cc26d27e8d8ba69ce8a`
- Telegram `b26423aa1bc67ad239eb9059042e3efe5479d41c`
- tests `835f90a3bfbe13e165fa90187712ddc4da564dd7`
- CI #265 / run `31667412478` SUCCESS
- Deploy #116 / run `31667377479` SUCCESS

### P2.2.4 Character Profile Browser

Status: IMPLEMENTED / CI-VALIDATED / DEPLOYED — CREATOR UI ACCEPTANCE PENDING.

Current deployed flow:
`Characters -> Darian -> Profile -> section -> Back`.

Implemented sections:
- Identity
- Appearance
- Body
- Attributes
- Personality
- Skills
- Preferences & Habits
- Background

Data ownership:
- scalar profile values: `character_profile_values` + `profile_field_definitions`
- skills/preferences/hobbies/habits: normalized profile tables
- current runtime state remains separate from profile truth
- normal browser filters out `private` and `intimate` sensitivity fields at query time
- no grade badges yet
- no second-character Telegram session state yet

Implementation evidence:
- grading-direction doc `f3cf9438aa84b68bfca230ca0392b5dd4ff3604f`
- profile query `2d9c43ad5d66cae0d9ff0e6d4f6c474599afa012`
- profile presentation `db9f8702fc812a81f447f74d6e9e21d91b8419d5`
- Telegram integration `0fd68b22a7d5a8b7d360dc8a617124753b5b3847`
- focused tests `d926687d443bc6e5e841ef3c06d1a293d82ca71a`
- CI #272 / run `31668499392` SUCCESS
- Deploy #119 / run `31668483842` SUCCESS

Deploy #119 readback verified systemd active, Telegram API connected, schema v4 healthy, Darian autonomy enabled/normal/unpaused at 1x, cognition binding preserved and Darian still in Kitchen/rest at that readback.

Creator acceptance remaining: open Darian -> Profile, browse several sections, confirm readable values/layout/back navigation, and verify normal profile does not expose sensitive/private fields.

## Exact resume point

**Creator tests P2.2.4 Character Profile Browser in Telegram. If accepted, mark it LIVE UX VERIFIED and select the next independently runnable roadmap slice.**

Preserve 1x wake-on-demand production autonomy, scoped ids, locked unfinished boundaries, actor-scoped scheduler state, first-class actions/events, Telegram presentation rules, notification preferences, profile/runtime separation and the minimum-runnable expansion policy.
