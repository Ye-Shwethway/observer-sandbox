# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then task-relevant repo files. Read `ROADMAP.md` for roadmap work, `docs/WORLD_LOCATION_NODE_MODEL.md` for spatial/world topology, `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` for Telegram work, `docs/TELEGRAM_NOTIFICATION_POLICY.md` for proactive notifications, and `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md` for needs/world-resource/item-effect work.

Authority: current Creator instruction > canonical repo > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > old chat/memory. Never conflate committed, CI-validated, deployed, DB-applied, and live-behavior-verified states. Update this file after material changes.

## Production baseline

- Repo: `Ye-Shwethway/observer-sandbox` private
- VPS: `107.175.30.238`, Ubuntu 24.04
- App: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- systemd: `observer-sandbox`
- physical SQLite schema: version 3
- continuous autonomy: enabled, normal, 1x
- cognition: Gemini dynamically resolved Flash-Lite binding for `character:char_darian / cognition`
- cognition mode: wake-on-demand only
- Telegram: live, Owner/Allowed split configured
- notifications: persistent per user, default ON

Production continues autonomously. Re-read live state whenever exact current Darian state matters.

## Wake-on-demand / cost policy

The scheduler may tick about every 2 seconds, but the LLM wakes only at a real decision boundary: autonomy enabled, unpaused, not in retry/backoff, and no physical action pending. In-progress action time is deterministic and creates zero additional model calls. Preserve this policy; do not add periodic LLM heartbeats/background reflection without explicit Creator approval.

## World / location node architecture — scoped identity reset COMPLETE

Canonical contract: `docs/WORLD_LOCATION_NODE_MODEL.md`.

The Creator explicitly chose clean early-development architecture over preserving prototype spatial ids. Spatial/resource identity is now globally scoped.

### Identity rules

- world ids: `world_*`
- location ids: `loc_*`
- object/resource ids: `obj_*`
- character ids such as `char_darian` remain globally person-specific
- ids are technical identities, not display labels
- repeated display names are allowed; ids must remain globally unique
- ids should be place-scoped but path-independent; mutable floor/parent topology belongs in `contains` relations rather than the full id path

Examples:
- `world_observer_universe`
- `loc_thorne_estate`
- `loc_thorne_estate_kitchen`
- `loc_thorne_estate_master_suite`
- `loc_thorne_estate_home_gym`
- `obj_thorne_estate_kitchen_refrigerator`
- `obj_thorne_estate_gym_heavy_bag`
- future `loc_south_lake_tahoe`
- future `loc_quasi_home` and `loc_quasi_home_kitchen`

Prototype ids `observer_universe`, `home`, `zone_*`, `room_*`, and generic estate `obj_*` ids are retired and must not be reintroduced.

### Current hierarchy

World seed revision: `thorne-estate-v3.0-scoped-ids`.

`world_observer_universe -> loc_thorne_estate -> floor/zone -> room -> object`

Current estate child zones:
- `loc_thorne_estate_ground_floor`
- `loc_thorne_estate_second_floor`
- `loc_thorne_estate_third_floor`
- `loc_thorne_estate_underground`
- `loc_thorne_estate_exterior_boundary` (locked/non-traversable)

Current room set includes Grand Foyer, Living Room, Kitchen, Dining Area, Library & Study, Garage & Workshop, Darian's Master Suite, Master Bathroom, Quasi's Room, Guest Rooms, Surveillance & Intelligence Hub, Secure Communications Room, Training Hall, Top-Class Home Gym, Medical Bay, Armory & Storage, Food Supply Storage, and Underground Bunker.

Canonical mansion source establishes the South Lake Tahoe estate, modern fortress/security character, three stories plus reinforced underground level and the major mansion areas. The source does not place every area on an exact floor; non-source placements remain `provisional_layout` rather than silently becoming canon.

### Future regional expansion

Do not expand outside yet. When ready, insert the regional node without renaming estate identities:

`world_observer_universe -> loc_south_lake_tahoe -> loc_thorne_estate`

Other residences/locations then become siblings, e.g. `loc_quasi_home`. Their own Kitchen/Bedroom/etc. may share display names safely because their ids are place-scoped.

### Exterior lock

`loc_thorne_estate_exterior_boundary` has access `locked`, `traversable=false`, and no `connected_to` edge. Darian cannot leave the mansion until outer-environment nodes are explicitly authored and traversal is unlocked by graph migration.

### Clean migration behavior

`src/observer_sandbox/world.py` has an explicit legacy-id reset migration.

On detecting old spatial ids it:
1. remembers previous pause state;
2. transactionally pauses runtime;
3. clears pending/lease/retry scheduler records that may contain obsolete ids;
4. maps Darian's current old location to the equivalent scoped node;
5. sets current action idle;
6. commits the pause before deleting old spatial entities so the old running service cannot race a stale action;
7. deletes legacy spatial/object entities;
8. seeds the new scoped graph and records `world_identity_revision`;
9. after the new service initializes, restores the previous pause state.

Character/profile data, physiology values, AI bindings, Telegram preferences and historical events are preserved. Historical event payloads may still contain old development-era ids; new runtime/world state does not.

The physical SQLite schema remains v3 because the existing entity/relation/field tables already support globally scoped ids and recursive containment. This was a world identity/data migration, not a table-shape migration.

### Routing

The old hard-coded five-room `NEXT_HOP` routing table is removed. Deterministic baseline/dry-run routing now computes shortest paths over authored `connected_to` relations. Production LLM cognition still sees only legal adjacent actions from `action_options()`.

### Query layer

`src/observer_sandbox/observer_query.py` exposes generic location details: parent, child locations, objects/effects, occupants/residents, physical exits, kind/access/canon/metadata. Telegram must consume this contract rather than hard-code mansion topology.

### Evidence

Core scoped-id commits include:
- config revision: `e9c2dd09cbd38f5bf1e366df0f24f324309e3aeb`
- migration: `e8b201af6442a37df52d446b7f0d4b6f4037fadd`
- runtime root: `800c6fadd13729348ae77d764941fe80e1afc11e`
- graph-derived routing: `d69002157bd156c1b09258a485f555801b8f459d`
- query default: `8cb948277d665d268ca093acc8295aee5b0e2d37`
- Telegram estate id: `827862604aea88a3f93c834047b41d564e682595`

CI #221 / run `31664180403`: SUCCESS. Full suite passed after all old fixture ids were retired; fresh initialization, autonomy/wake behavior, Telegram contracts, 24h living behavior and scoped-id paths are covered. A dedicated legacy reset regression simulates old runtime/pending ids and verifies remap/pending-clear/pause handoff.

Deploy #101 / run `31663995353`: SUCCESS and live migration verified. Readback after service restart showed:
- `world_id = world_observer_universe`
- `world_identity_revision = thorne-estate-v3.0-scoped-ids`
- `paused = false`, speed `1.0`, autonomy enabled normal
- Darian location `loc_thorne_estate_kitchen` / display `Kitchen`
- old pending state had been cleared during migration and a new scoped-era decision was planned afterward (`rest`, targetless)
- cognition last wake reason included `world_identity_migrated`
- systemd active and Telegram API connected

Evidence level: **clean scoped world identity reset is implemented, CI-validated, deployed, DB-applied and live-runtime verified.**

## P1 physiology + item effects

Five basic stats clamp `0..100`: energy high-good; hunger/thirst/sleepiness high-bad; cleanliness high-good.

Passive hourly drift: energy `-2.0`, hunger `+2.5`, thirst `+3.0`, sleepiness `+3.0`, cleanliness `-0.8`.

Recovery paths:
- energy -> rest/sleep; food may add secondary energy
- hunger -> authored food/eat resources
- thirst -> authored drink resources
- sleepiness -> sleep; rest mild relief
- cleanliness -> shower/wash resources

Targetless `rest` is legal everywhere. Recovery-labelled actions must improve their primary need after passive drift.

Generic `game.effects` remain authoritative for item/resource physiological effects. Current scoped recovery resources include estate drinking water, master-bathroom sink/shower, kitchen meal ingredients/pantry, and master bed/rest.

Future Energy Drink or similar consumables must use the generic effect contract. Finite quantity, depletion, temporary modifiers, cooldown/tolerance remain later work.

## Recovery-aware cognition / accelerated acceptance

Policy revision: `darian-autonomy-p1-v1.3-recovery-aware`.

Critical: sleepiness >=80, energy <=20, thirst >=75, hunger >=80.
Strong recovery: sleepiness >=65, energy <=40, thirst >=50, hunger >=55, cleanliness <=50.

`.github/workflows/autonomy-acceptance.yml` runs bounded accelerated recovery against a disposable copy of production DB at 3600x and never mutates production. Use this lane instead of waiting real hours during development.

## Telegram Observer

P2.1 LIVE. P2.2.1 Observer Home + inline navigation implemented/deployed. **P2.2.2A scoped Thorne Estate world foundation is COMPLETE / LIVE VERIFIED. Next: P2.2.2B Telegram Estate Browser.**

Presentation contract:
- visible sim time `dd-mm-yyyy (Day) hh:mm AM/PM`
- friendly names instead of internal ids
- restrained emoji/dividers and whitespace
- ON/OFF and Yes/No rather than raw booleans
- default history suppresses engine/control bookkeeping
- section/paginate large data
- Telegram stays a thin adapter over generic query/control services

P2.2.2B target flow:
`Universe -> Thorne Estate -> Floor/Zone -> Room`

Room views should show occupants, contained objects, physical exits and current activity. Back navigation should follow actual parent-node data. Locked exterior may be visible as unavailable but must never become a legal movement affordance.

## Proactive notification contract

Global notification preference is per-user, persistent, default ON. `/notify off` suppresses proactive pushes but never interactive command/callback replies.

Current proactive notifications:
1. startup `Universe is alive!`;
2. successful character action-completion summaries.

Action-completion push is downstream/best-effort after deterministic state commit, includes human-readable action/target/time/reason/location and changed physiological stats, and deduplicates by action id per user.

Production runtime has contained `telegram_last_action_notification:<user>` written only after Telegram `_send` succeeds, so Telegram API acceptance of at least one production action push is live-verified. Creator-visible receipt remains a separate UX observation until the Creator explicitly confirms it.

## Roadmap / resume

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED
- P0.5 Provider Layer: FOUNDATION COMPLETE
- P1 Living Darian: continuous autonomy LIVE; recovery/item-effect hardening accepted
- P2 Telegram Observer: ACTIVE
  - P2.1 LIVE
  - P2.2.1 COMPLETE
  - P2.2.2A Thorne Estate interior + clean spatial identity reset COMPLETE / LIVE VERIFIED
  - **P2.2.2B Telegram Estate Browser NEXT**
- P2.2.3 Item browsing after estate browser
- P3+ later

Do not broaden into South Lake Tahoe yet. First prove recursive Estate browsing on the scoped node graph. Preserve wake-on-demand cognition, globally scoped/path-independent ids, locked unfinished boundaries, notification preferences, Telegram presentation rules, and evidence-level distinctions.
