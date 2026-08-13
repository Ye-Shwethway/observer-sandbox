# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then task-relevant repo files. For roadmap work read `ROADMAP.md`; Telegram work read `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`; proactive notifications read `docs/TELEGRAM_NOTIFICATION_POLICY.md`; physiology/world-resource/item-effect work read `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

Authority order:
1. current Creator instruction;
2. canonical repository config/schema/architecture;
3. verified live VPS/runtime/DB evidence;
4. deployed repository/workflow evidence;
5. current CI/test evidence;
6. this bootstrap;
7. older chat/memory.

Never conflate committed, CI-validated, deployed, DB-applied, and live-behavior-verified states. Update this file after every material repo/runtime change.

## Production baseline

- Repo: `Ye-Shwethway/observer-sandbox` (private)
- VPS: `107.175.30.238`, Ubuntu 24.04
- App: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- systemd: `observer-sandbox`
- Schema: 3
- Continuous autonomy: enabled, normal mode, 1x, wake-on-demand cognition
- Current cognition provider: Gemini, dynamically resolved Flash-Lite binding for `character:char_darian / cognition`
- Telegram bot: live, Owner/Allowed split configured, per-user notifications persistent and default ON

Production continues autonomously. Re-read live state whenever exact current Darian state matters.

## Wake-on-demand cognition / cost policy

The service scheduler may tick every ~2 seconds, but the LLM is called only at a real decision boundary when autonomy is enabled, unpaused, not in retry/backoff, and no physical action is pending. Pending action time is deterministic and creates zero additional model calls. Preserve this policy; do not add periodic LLM heartbeats/background reflection without explicit Creator approval.

`cognition_wake_stats` persists cumulative decision calls and last wake metadata. Telegram `/status` shows Mind Calls.

## P1 physiology + item effects

Canonical files:
- `config/worlds/home.v1.json`
- `config/characters/darian.autonomy-policy.json`
- `src/observer_sandbox/simulation.py`
- `src/observer_sandbox/world.py`
- `src/observer_sandbox/model_decision.py`
- `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`

Current five basic physiological stats, clamped `0..100`:
- `needs.energy` — higher better
- `needs.hunger` — higher worse
- `needs.thirst` — higher worse
- `needs.sleepiness` — higher worse
- `physiology.cleanliness` — higher better

Current passive drift per simulated hour:
- energy `-2.0`
- hunger `+2.5`
- thirst `+3.0`
- sleepiness `+3.0`
- cleanliness `-0.8`

Recovery paths:
- energy -> rest/sleep; food may add secondary energy
- hunger -> authored food/eat resources
- thirst -> authored drink resources
- sleepiness -> sleep; rest gives mild relief
- cleanliness -> authored shower/wash resources

Targetless `rest` is legal everywhere. Object-backed rest remains legal. `idle` is light recovery and must not be net energy-negative. Recovery-labelled actions must improve their primary need after passive drift.

### Generic item-effect contract

Home world revision: `home-v1.1-effects`.

World objects may define action-specific `effects`. Seeding persists them as `game.effects`; `action_options()` exposes them to cognition; `apply_action()` applies them deterministically after passive/intrinsic action effects. The LLM never directly mutates needs.

Current authored recovery resources:
- Drinking Water / drink: thirst `-55`
- Sink / drink: thirst `-35`
- Meal Ingredients / eat: hunger `-50`, energy `+8`, thirst `+2`
- Pantry / eat: hunger `-40`, energy `+5`, thirst `+1`
- Shower / shower: cleanliness set `100`

Restorative target actions without matching authored effects are rejected. Future Energy Drink or similar items should use the same effect profile rather than hard-coded engine branches. Finite quantities, consumption, temporary modifiers, cooldown/tolerance, inventory depletion remain later work.

### Persistent-plan migration rule

Autonomy pending actions survive restarts. Capability/effect migrations must not invalidate a live pending action accidentally. During the first item-effect rollout, production already had `eat -> Pantry`; Pantry was preserved as a renewable ready-food abstraction with an authored eat effect so the persisted plan remained valid.

## Recovery-aware cognition policy v1.3

Policy revision: `darian-autonomy-p1-v1.3-recovery-aware`.

Critical thresholds remain:
- sleepiness >=80
- energy <=20
- thirst >=75
- hunger >=80

Strong recovery thresholds are now:
- sleepiness >=65
- energy <=40
- thirst >=50
- hunger >=55
- cleanliness <=50

Strong needs are recovery conditions, not merely warnings. Darian should not resume discretionary training/study/routine just because a depleted stat barely exits critical range. Recovery should continue until the active strong condition clears. Authored action-option effects are the factual basis for choosing food/drink/hygiene resources.

Deploy #87 / run `31661154628`: SUCCESS for the recovery-aware policy.

## Accelerated recovery acceptance lane

`.github/workflows/autonomy-acceptance.yml` is now a permanent bounded accelerated recovery tool.

It:
- copies the current production SQLite DB to a disposable `/tmp` DB;
- preserves character/world/needs/sim-time state;
- clears copied pending/lease/retry/current-action scheduler bookkeeping only;
- runs autonomy at `3600x` on the disposable DB;
- caps the run at six model decision boundaries;
- never mutates the production DB;
- prints the recovery trajectory plus an explicit production readback afterward.

This lane exists so development does not need to wait real hours for 1x recovery behavior.

### Acceptance #2 — exposed policy gap

Run `31661095165`: SUCCESS as a workflow, but `needs_acceptable=false` after six decisions.

From copied production state around:
- energy `23.832`
- hunger `63.665`
- thirst `28.335`
- sleepiness `34.835`
- cleanliness `43.2`

Trajectory included `rest -> eat -> move -> inspect -> read -> move gym`. Hunger recovered, but Energy around 32 and Cleanliness around 42 were no longer considered strong under v1.2, so cognition resumed discretionary routine too early. This identified a cognition threshold problem, not an item-effect math failure.

### Acceptance #3 — recovery-aware policy PASS

Run `31661169671`: SUCCESS.

Disposable trajectory:
1. eat -> Meal Ingredients, 20m
2. rest, 30m
3. rest, 30m
4. move -> Bathroom, 5m
5. shower, 15m
6. rest, 30m

Copied state before:
- energy `23.832`
- hunger `63.665`
- thirst `28.335`
- sleepiness `34.835`
- cleanliness `43.2`
- Kitchen, sim `2025-05-01T12:40:00+00:00`

Copied final state after 2h10 simulated time:
- energy `42.498`
- hunger `19.081`
- thirst `36.835`
- sleepiness `35.335`
- cleanliness `99.6`
- Bathroom, sim `2025-05-01T14:50:00+00:00`
- `needs_acceptable=true`

Acceptance band for this recovery test:
- energy >40
- hunger <55
- thirst <50
- sleepiness <65
- cleanliness >50

This is strong evidence that the current five-stat restoration + item-effect + recovery-aware cognition stack can exit the depleted state in a bounded accelerated production-copy run. It is not a claim that the production DB itself was advanced; production remained unchanged by the acceptance copy.

## Telegram Observer

P2.1 is LIVE. P2.2.1 Observer Home + inline navigation is implemented/deployed.

Current commands include `/start`, `/status`, `/watch`, `/history`, `/darian`, `/home`, `/pause`, `/resume`, `/speed`, `/whoami`, `/notify on|off` plus notification aliases including `/notion/on` and `/notion/off`.

Telegram presentation is a mandatory contract:
- visible sim time: `dd-mm-yyyy (Day) hh:mm AM/PM`
- friendly entity names, not internal IDs
- restrained emoji/dividers and clear whitespace
- ON/OFF, Yes/No rather than raw booleans
- default history hides engine/control bookkeeping
- large data should be sectioned/paginated
- Telegram stays a thin adapter; business logic remains in core query/control services

Notifications are per-user, persistent, default ON. `Universe is alive!` startup notification obeys the global notification preference.

## Roadmap / resume point

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED
- P0.5 Provider Layer: FOUNDATION COMPLETE
- P1 Living Darian: continuous autonomy LIVE; five-stat recovery + generic item effects + recovery-aware cognition accelerated acceptance PASS
- P2 Telegram Observer: ACTIVE; P2.1 live, P2.2.1 complete
- Next: **P2.2.2 Location hierarchy / room detail browsing**

P2.2.2 should expose Home/world -> rooms -> room detail including occupants, items/objects, exits/relations, current activity, with Back/Universe/Home navigation. Item detail should later expose authored capabilities/effects in human-friendly form.

Do not manually reset production needs just to make development easier. Use the accelerated disposable acceptance lane for fast simulation/testing, and only accelerate live production deliberately when a live proof is specifically needed.
