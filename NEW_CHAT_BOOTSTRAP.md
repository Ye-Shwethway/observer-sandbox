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
- schema: 3
- continuous autonomy: enabled, normal, 1x
- cognition: Gemini dynamically resolved Flash-Lite binding for `character:char_darian / cognition`
- cognition mode: wake-on-demand only
- Telegram: live, Owner/Allowed split configured
- notifications: persistent per user, default ON

Production continues autonomously. Re-read live state whenever exact current Darian state matters.

## Wake-on-demand / cost policy

The scheduler may tick about every 2 seconds, but the LLM wakes only at a real decision boundary: autonomy enabled, unpaused, not in retry/backoff, and no physical action pending. In-progress action time is deterministic and creates zero additional model calls. Preserve this policy; do not add periodic LLM heartbeats/background reflection without explicit Creator approval.

## World / location node architecture

Canonical contract: `docs/WORLD_LOCATION_NODE_MODEL.md`.

Locations are recursive graph nodes rather than hard-coded screen concepts. Current hierarchy:

`observer_universe -> home (Thorne Estate) -> floor/zone -> room -> object`

Important identity rules:
- `observer_universe` is the generic world root;
- stable id `home` is now the **Thorne Estate location node**, not the world root;
- a future South Lake Tahoe regional node may be inserted above `home` without changing the estate id;
- future locations such as Quasi's home can become sibling nodes under the regional node;
- containment (`contains`) and traversal (`connected_to`) are separate.

### Thorne Estate interior foundation

World seed revision: `thorne-estate-v2.0-interior-nodes`.

Canonical mansion source establishes South Lake Tahoe location, modern fortress/high-tech security, three stories plus reinforced underground level, living quarters, training hall, top-class gym, surveillance/intelligence hub, armory/storage, garage/workshop, library/study, medical room, food-supply storage, underground bunker and security/escape infrastructure.

Current node foundation:
- Thorne Estate (`home`)
  - Ground Floor (`zone_ground`)
  - Second Floor (`zone_second`)
  - Third Floor (`zone_third`)
  - Underground Level (`zone_underground`)
  - Estate Exterior (`boundary_exterior`, locked/non-traversable)

Current room nodes include Grand Foyer, Living Room, Kitchen, Dining Area, Library & Study, Garage & Workshop, Darian's Master Suite, Master Bathroom, Quasi's Room, Guest Rooms, Surveillance & Intelligence Hub, Secure Communications Room, Training Hall, Top-Class Home Gym, Medical Bay, Armory & Storage, Food Supply Storage, Underground Bunker.

The source does not assign every area to an exact floor. Non-source placements are explicitly marked `provisional_layout`; do not promote them to canon silently.

Stable P1 ids retained:
- `room_bedroom` -> Darian's Master Suite
- `room_bathroom` -> Master Bathroom
- `room_living` -> Living Room
- `room_kitchen` -> Kitchen
- `room_gym` -> Top-Class Home Gym

This preserves runtime locations, pending actions, history, notifications and existing observer links.

The exterior boundary has access `locked`, `traversable=false`, and no `connected_to` edge. The character cannot leave the mansion until outer environment nodes are explicitly implemented/unlocked.

### Node seeding / query behavior

`src/observer_sandbox/world.py` supports recursive `locations + parent` seeds while retaining backward compatibility with the original flat `rooms` form. Seed-owned containment and adjacency are rebuilt safely without resetting character state/entity ids.

`src/observer_sandbox/observer_query.py` now exposes generic location details:
- parent node;
- child location nodes;
- contained objects/effects;
- occupants/residents;
- physical exits;
- kind/access/canon/metadata.

Telegram must use this generic contract rather than hard-code mansion topology.

Evidence:
- world graph seed commit `e4290bfe1b2f0932ef9d9ef303e5d69d1ae6686a`, compatibility topology commit `7e5b90b4a09b257c7153966ff15a51b1b36bc50d`;
- recursive seeder commit `b599131d67b88acdf2d9b738b2a19d701eb993da`;
- runtime world-root migration commit `66b1107a84db8da53ce66c4305cda2ff0245391f`;
- generic recursive query commit `374d94b69335798fdbfec70fca4ec3514058d796`;
- CI #207 / run `31663313620`: SUCCESS on latest documented foundation;
- Deploy #95 / run `31663114003`: SUCCESS, systemd active and Telegram API connected;
- Deploy #95 live readback showed `world_id=observer_universe`, proving runtime migration applied while Darian's persistent state/pending autonomy remained intact.

Evidence level: **P2.2.2A Thorne Estate interior node foundation is implemented, CI-validated, deployed, and runtime world-root migration is live-verified.** Telegram deep estate navigation is not yet implemented; that is P2.2.2B.

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

Generic `game.effects` remain authoritative for item/resource physiological effects. Current recovery resources include Drinking Water, Sink water, Meal Ingredients, Pantry ready-food abstraction, Shower and Bed/Rest.

Future Energy Drink or similar consumables must use the generic effect contract. Finite quantity, depletion, temporary modifiers, cooldown/tolerance remain later work.

## Recovery-aware cognition / accelerated acceptance

Policy revision: `darian-autonomy-p1-v1.3-recovery-aware`.

Critical: sleepiness >=80, energy <=20, thirst >=75, hunger >=80.
Strong recovery: sleepiness >=65, energy <=40, thirst >=50, hunger >=55, cleanliness <=50.

`.github/workflows/autonomy-acceptance.yml` runs bounded accelerated recovery against a disposable copy of production DB at 3600x and never mutates production.

Acceptance run `31661169671` reached the acceptable recovery band in six decisions from the depleted production snapshot. Use this lane instead of waiting real hours during development.

## Telegram Observer

P2.1 LIVE. P2.2.1 Observer Home + inline navigation implemented/deployed. P2.2.2A world/backend location foundation is now complete. **Next: P2.2.2B Telegram Estate Browser.**

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

Evidence:
- Deploy #90 / run `31661514961`: SUCCESS;
- CI #194 / run `31661582673`: SUCCESS;
- later Deploy #95 live runtime contained `telegram_last_action_notification:<user>` with a completed production action id. The dispatcher writes this marker only after Telegram `_send` succeeds, so Telegram API acceptance of at least one production action push is live-verified. Creator-visible receipt confirmation remains a separate UX observation.

## Roadmap / resume

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED
- P0.5 Provider Layer: FOUNDATION COMPLETE
- P1 Living Darian: continuous autonomy LIVE; recovery/item-effect hardening accepted
- P2 Telegram Observer: ACTIVE
  - P2.1 LIVE
  - P2.2.1 COMPLETE
  - P2.2.2A Thorne Estate interior node foundation COMPLETE / LIVE MIGRATION VERIFIED
  - **P2.2.2B Telegram Estate Browser NEXT**
- P2.2.3 Item browsing after estate browser
- P3+ later

Do not reset production state casually. Preserve wake-on-demand cognition, stable location ids, locked unfinished boundaries, notification preferences, Telegram presentation rules, and evidence-level distinctions.
