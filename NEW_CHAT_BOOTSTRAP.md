# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then task-relevant repo files. Read `ROADMAP.md` for roadmap work, `docs/ARCHITECTURE.md` for core runtime work, `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md` for the current pre-expansion architecture audit, `docs/WORLD_LOCATION_NODE_MODEL.md` for spatial/world topology, `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` for Telegram work, `docs/TELEGRAM_NOTIFICATION_POLICY.md` for proactive notifications, and `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md` for needs/world-resource/item-effect work.

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

## Core composable-universe target

The Creator's intended LEGO-like runtime expression is:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> validated transition -> State Changes + Events`

`docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md` is the current one-time pre-expansion audit. It is **PROPOSED architecture**, not yet implementation authorization.

Audit conclusion: the entity/relation graph, field-authority model, deterministic validation/application boundary, global sim clock and scoped world identities are good foundations, but several Darian-only prototype seams should be removed before broad South Lake Tahoe expansion or a second autonomous character.

Recommended hardening gate:
1. actor-scoped runtime/autonomy state instead of singleton pending/lease/retry/cognition keys;
2. first-class action-instance envelope with action id, actor/participants, target/resources, place, planned start/end time, conditions/modifiers and status;
3. data-driven action-definition registry before the verb vocabulary grows;
4. generic conditions/modifiers/effects contract including future temporary/source/stack semantics;
5. queryable event envelope with location, participants, action/causal references and state-change summary;
6. definition/template vs concrete instance vs runtime-state distinction;
7. explicit ownership/possession/dynamic-location semantics before inventory/movable objects grow;
8. fresh-DB + legacy-development migration + accelerated acceptance after the cutover.

Deferred until their slices: full inventory quantities/stacks/durability, rich relationship simulation, memory engine, environment/weather, complex synchronized group actions.

## Wake-on-demand / cost policy

The scheduler may tick about every 2 seconds, but the LLM wakes only at a real decision boundary. In-progress action time is deterministic and creates zero additional model calls. Preserve this policy; do not add periodic LLM heartbeats/background reflection without explicit Creator approval.

## World / location node architecture — scoped identity reset COMPLETE

Canonical contract: `docs/WORLD_LOCATION_NODE_MODEL.md`.

Identity rules:
- world ids: `world_*`
- location ids: `loc_*`
- object/resource ids: `obj_*`
- character ids such as `char_darian` remain globally person-specific
- repeated display names are allowed; technical ids must remain globally unique
- ids are place-scoped but path-independent; mutable floor/parent topology belongs in relations

Current hierarchy:
`world_observer_universe -> loc_thorne_estate -> floor/zone -> room -> object`

Examples: `loc_thorne_estate_kitchen`, `loc_thorne_estate_master_suite`, `loc_thorne_estate_home_gym`, `obj_thorne_estate_kitchen_refrigerator`. Future examples: `loc_south_lake_tahoe`, `loc_quasi_home`, `loc_quasi_home_kitchen`.

Prototype ids `observer_universe`, `home`, `zone_*`, `room_*`, and generic estate `obj_*` ids are retired.

World seed revision: `thorne-estate-v3.0-scoped-ids`. The estate exterior boundary is locked/non-traversable. Do not expand outside yet.

The legacy spatial reset migration preserves character/profile data, physiology values, AI bindings, Telegram preferences and historical events; maps Darian to the corresponding scoped location; clears stale pending/lease/retry state; pauses transactionally during cutover; then restores prior pause state after new service initialization.

Physical SQLite schema remains v3 because the existing graph tables support the scoped identities. Deterministic baseline routing now derives shortest paths from `connected_to`; production cognition receives only legal adjacent actions.

Evidence: CI #221 / run `31664180403` SUCCESS. Deploy #101 / run `31663995353` SUCCESS and live migration verified with `world_id=world_observer_universe`, `world_identity_revision=thorne-estate-v3.0-scoped-ids`, Darian at `loc_thorne_estate_kitchen`, autonomy enabled normal/unpaused at 1x, systemd active and Telegram API connected.

## P1 physiology + item effects

Five basic stats clamp `0..100`: energy high-good; hunger/thirst/sleepiness high-bad; cleanliness high-good.

Passive hourly drift: energy `-2.0`, hunger `+2.5`, thirst `+3.0`, sleepiness `+3.0`, cleanliness `-0.8`.

Recovery paths: energy -> rest/sleep; hunger -> authored food; thirst -> authored drink; sleepiness -> sleep/rest; cleanliness -> shower/wash. Generic `game.effects` remain authoritative for item/resource physiological effects.

Policy revision: `darian-autonomy-p1-v1.3-recovery-aware`. `.github/workflows/autonomy-acceptance.yml` provides bounded 3600x disposable-copy recovery acceptance instead of waiting real hours.

## Telegram Observer

P2.1 LIVE. P2.2.1 Observer Home + inline navigation implemented/deployed. P2.2.2A scoped Thorne Estate world foundation COMPLETE / LIVE VERIFIED.

P2.2.2B Telegram Estate Browser is technically ready, but roadmap now records a **Creator decision point**: approve the bounded composable-runtime hardening gate before P2.2.2B, or explicitly defer it and continue the Estate Browser first.

Presentation contract remains: friendly names, `dd-mm-yyyy (Day) hh:mm AM/PM`, restrained mobile UI, no raw ids/log dumps, section/paginate large data, Telegram remains a thin adapter.

## Proactive notification contract

Per-user persistent notifications default ON. `/notify off` suppresses proactive pushes but not interactive replies. Current proactive pushes are startup and successful action-completion summaries. Action pushes happen downstream of deterministic commit and deduplicate by action id.

## Roadmap / resume

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED
- P0.5 Provider Layer: FOUNDATION COMPLETE
- P1 Living Darian: continuous autonomy LIVE; recovery/item-effect hardening accepted
- P2 Telegram Observer: ACTIVE
  - P2.1 LIVE
  - P2.2.1 COMPLETE
  - P2.2.2A Thorne Estate interior + scoped identity reset COMPLETE / LIVE VERIFIED
  - P2.2.2B Estate Browser READY AFTER ARCHITECTURE-GATE DECISION
- pre-expansion composable runtime audit: COMPLETE / PROPOSED, not yet implemented

Do not broaden into South Lake Tahoe or add a second autonomous character while singleton runtime assumptions remain unless the Creator explicitly chooses to defer the hardening gate. Preserve wake-on-demand cognition, globally scoped/path-independent ids, locked unfinished boundaries, notification preferences, Telegram presentation rules, and evidence-level distinctions.
