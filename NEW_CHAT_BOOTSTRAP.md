# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then task-relevant repo files. Read `ROADMAP.md` for roadmap work, `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` for Telegram work, `docs/TELEGRAM_NOTIFICATION_POLICY.md` for proactive notifications, and `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md` for needs/world-resource/item-effect work.

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
- cognition mode: wake-on-demand only; scheduler ticks do not imply LLM calls
- Telegram: live, Owner/Allowed split configured
- notifications: persistent per user, default ON

Production continues autonomously. Re-read live state whenever exact current Darian state matters.

## Wake-on-demand / cost policy

The scheduler may tick about every 2 seconds, but the LLM wakes only at a real decision boundary: autonomy enabled, unpaused, not in retry/backoff, and no physical action pending. In-progress action time is deterministic and creates zero additional model calls. Preserve this policy; do not add periodic LLM heartbeats/background reflection without explicit Creator approval.

## P1 physiology + item effects

Five basic stats clamp `0..100`:
- energy: high good
- hunger: high bad
- thirst: high bad
- sleepiness: high bad
- cleanliness: high good

Passive hourly drift: energy `-2.0`, hunger `+2.5`, thirst `+3.0`, sleepiness `+3.0`, cleanliness `-0.8`.

Recovery paths:
- energy -> rest/sleep; food may add secondary energy
- hunger -> authored food/eat resources
- thirst -> authored drink resources
- sleepiness -> sleep; rest gives mild relief
- cleanliness -> shower/wash resources

Targetless `rest` is legal everywhere. Recovery-labelled actions must improve their primary need after passive drift.

World revision `home-v1.1-effects` supports generic action-specific `effects`. Seeding persists them as `game.effects`; `action_options()` exposes effects to cognition; `apply_action()` applies them deterministically. The LLM never directly mutates needs.

Current recovery resources:
- Drinking Water: thirst `-55`
- Sink drink: thirst `-35`
- Meal Ingredients: hunger `-50`, energy `+8`, thirst `+2`
- Pantry ready-food abstraction: hunger `-40`, energy `+5`, thirst `+1`
- Shower: cleanliness set `100`

Future Energy Drink or similar consumables must use the generic effect contract. Finite quantity, depletion, temporary modifiers, cooldown/tolerance remain later work.

## Recovery-aware cognition policy

Revision: `darian-autonomy-p1-v1.3-recovery-aware`.

Critical: sleepiness >=80, energy <=20, thirst >=75, hunger >=80.
Strong recovery conditions: sleepiness >=65, energy <=40, thirst >=50, hunger >=55, cleanliness <=50.

Strong needs outrank discretionary routine until they clear. Deploy #87 / run `31661154628`: SUCCESS.

## Accelerated recovery acceptance

`.github/workflows/autonomy-acceptance.yml` copies the live production SQLite DB to a disposable `/tmp` DB, clears copied scheduler bookkeeping, runs at `3600x`, caps model decisions, prints the trajectory, and never mutates production. Use this instead of waiting real hours during development.

Acceptance #3 run `31661169671`: SUCCESS. From copied depleted state (energy 23.832, hunger 63.665, thirst 28.335, sleepiness 34.835, cleanliness 43.2), six actions `eat -> rest -> rest -> move Bathroom -> shower -> rest` reached energy 42.498, hunger 19.081, thirst 36.835, sleepiness 35.335, cleanliness 99.6 with `needs_acceptable=true`.

## Telegram Observer

P2.1 LIVE. P2.2.1 Observer Home + inline navigation implemented/deployed. Next main product slice after current notification checkpoint: **P2.2.2 Location hierarchy / room detail browsing**.

Presentation contract:
- visible sim time `dd-mm-yyyy (Day) hh:mm AM/PM`
- friendly entity names, never internal IDs when a display name exists
- restrained emoji/dividers and clear whitespace
- ON/OFF and Yes/No rather than raw booleans
- default history suppresses engine/control bookkeeping
- section/paginate large data
- Telegram remains a thin adapter; simulation/query/control truth remains in core services

Commands include `/start`, `/status`, `/watch`, `/history`, `/darian`, `/home`, `/pause`, `/resume`, `/speed`, `/whoami`, `/notify on|off`, plus aliases including `/notion/on` and `/notion/off`.

## Proactive notification contract

Global notification preference is per-user, persistent, and **default ON**. `/notify off` suppresses proactive pushes but never interactive command/callback replies.

Current proactive notifications:
1. startup `Universe is alive!`;
2. **character action completion summaries**.

After a successful autonomous action has committed its deterministic state changes, each authorized user with notifications ON should receive one mobile-friendly summary containing:
- character name;
- completed action + human-readable target;
- formatted simulated timestamp;
- cognition reason;
- location/transition;
- changed basic physiological stats as before -> after with deltas.

Do not notify on planning, `in_progress` ticks, bookkeeping events, or recovered duplicate completion records. Telegram delivery is downstream/best-effort and must never roll back a committed universe action. Successful deliveries persist `telegram_last_action_notification:<user_id>` so the same action id is not pushed twice.

Implementation:
- `src/observer_sandbox/telegram_notifications.py`
- completion hook in `src/observer_sandbox/service.py`
- policy: `docs/TELEGRAM_NOTIFICATION_POLICY.md`

Evidence:
- notifier/service commits culminated in `f17e93400c479571f1c664f90096713fc98266e2` for human-readable targets;
- Deploy #90 / run `31661514961`: SUCCESS; service active, Telegram API connected, autonomy still live;
- CI #194 / run `31661582673`: SUCCESS after fixing a stale v1.2 policy assertion; notification tests cover UI formatting, default-ON delivery, OFF suppression, and action-id dedupe.

Evidence level: action-completion push is **implemented, CI-validated, and deployed**. Do not call live Telegram delivery verified until an actual post-deploy completed production action notification is observed by the Creator.

Latest deploy readback around 2026-08-13T02:40Z showed Darian in Kitchen at sim `2025-05-01T13:00:00+00:00`, energy 28.165, hunger 24.498, thirst 30.335, sleepiness 35.835, cleanliness 42.933, with a pending targetless `rest` for 30 simulated minutes and autonomy enabled at 1x. Treat this as historical snapshot, not permanently current state.

## Roadmap / resume

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED
- P0.5 Provider Layer: FOUNDATION COMPLETE
- P1 Living Darian: continuous autonomy LIVE; five-stat recovery + generic item effects + recovery-aware cognition accelerated acceptance PASS
- P2 Telegram Observer: ACTIVE; P2.1 live, P2.2.1 complete
- immediate checkpoint: observe first post-deploy action-completion push and mark live delivery verified
- next implementation slice: **P2.2.2 Location hierarchy / room detail browsing**

Do not reset production needs just for development. Use accelerated disposable acceptance for fast engine tests. Preserve wake-on-demand cognition, notification preferences, Telegram presentation rules, and evidence-level distinctions.
