# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Core/runtime/schema/action: `docs/ARCHITECTURE.md` + `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`.
Spatial: `docs/WORLD_LOCATION_NODE_MODEL.md`.
Character/profile: `docs/CHARACTER_PROFILE_SCHEMA.md`.
Telegram: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` + `docs/TELEGRAM_NOTIFICATION_POLICY.md`.
Creator controls: `docs/CREATOR_CONTROL_POLICY.md`.
Needs/effects/training: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`, `docs/P3_3_TRAINING_READINESS_MODIFIER.md`, `docs/P3_4_TRAINING_EFFECTIVENESS.md`, `docs/P3_5_EFFECTIVE_TRAINING_LOAD.md`.
Future grading: `docs/FUTURE_GRADING_SYSTEM.md`.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory. Never conflate authored, CI-validated, acceptance-verified, deployed, DB-applied, and Creator-live-UX-verified states.

## Development policy — minimum runnable expansion

Schema v4 is the broad composable foundation. Normal development follows:

`minimum required state -> minimum deterministic behavior/evidence -> minimum Creator-facing surface if needed -> focused tests -> disposable acceptance -> deploy/readback -> Creator acceptance -> next slice`.

Do not pre-build large inventory, grading, memory, relationship, environment, combat, training, or regional subsystems merely because extension sockets exist.

## Production baseline

- Repo: `Ye-Shwethway/observer-sandbox`
- VPS app: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- systemd: `observer-sandbox`
- SQLite schema: v4
- world root: `world_observer_universe`
- estate: `loc_thorne_estate`
- world identity revision: `thorne-estate-v3.0-scoped-ids`
- Darian autonomy: enabled / normal / unpaused / `1x` / wake-on-demand
- cognition: existing Gemini character binding preserved
- Telegram: connected private Creator observer; owner/allowed-user configuration present

Production continues autonomously. Re-read live state whenever exact current Darian action/stats matter.

## Canonical runtime rule

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

LLMs propose structured actions only. Deterministic runtime owns legality and mutation. First-class action instances/events preserve target, modifiers, outcome, state changes, location, and participant evidence.

## Proven Creator-facing state

- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.
- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.

P3.3 reference degraded state: energy `50`, thirst `45`, sleepiness `45`, fatigue `40` -> readiness `0.595`, fatigue multiplier `1.202x`, resulting one-hour fatigue `62.54`. Fatigue `>=70` remains a hard training condition.

## P3.4 — Minimum Training Effectiveness Outcome

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Canonical doc: `docs/P3_4_TRAINING_EFFECTIVENESS.md`.

P3.4 separated:
- readiness = pre-action state summary;
- fatigue-cost multiplier = physiological cost;
- effectiveness = useful training-work fraction recorded in action/outcome evidence.

For v1, `effectiveness = readiness`. It does not mutate skill/attribute/body progression.

Evidence:
- merge `ea69d5c0f81bf5500fca9b4d6ea62a251fbdcd9f`;
- main CI #318 / run `31673822574` SUCCESS;
- P3 Training Effectiveness Acceptance #1 / run `31673822547` SUCCESS;
- Deploy #130 / run `31673858850` SUCCESS.

## P3.5 — Minimum Effective Training Load

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Canonical docs: `docs/P3_5_EFFECTIVE_TRAINING_LOAD.md` + `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

P3.5 makes effectiveness change immediate session-level physiology only:
- passive drift remains full-duration;
- intrinsic training energy/hunger/thirst/cleanliness effects scale by effectiveness;
- systemic fatigue remains on P3.3's separate fatigue-cost multiplier;
- `effective_minutes = planned_minutes × effectiveness` is persisted in action outcome and completion-event evidence;
- no long-term skill/attribute/body/grading progression is mutated.

Verified degraded reference:
- effectiveness `0.595`;
- 60 planned minutes -> `35.7` effective minutes;
- fatigue multiplier `1.202x`;
- resulting energy `42.05`, hunger `24.88`, thirst `51.57`, sleepiness `48.0`, cleanliness `75.63`, fatigue `62.54`.

Evidence:
- PR #4 merge `b6f29493a30a458133587463068df9814395eb75`;
- PR CI #324 / run `31674874707` SUCCESS;
- main CI #325 / run `31674911465` SUCCESS;
- P3 Effective Training Load Acceptance #1 / run `31674911581` SUCCESS on candidate code against a disposable production DB copy, zero model calls, no skill score/tier/experience mutation;
- release commit `22ff453715659d2c772ffcd19868716413a715a1`;
- Deploy #131 / run `31674963422` SUCCESS;
- post-deploy readback: service healthy, schema v4, autonomy enabled/normal/unpaused/`1x`, Gemini cognition binding preserved, Telegram API connected.

## Deferred boundaries

Still not implemented:
- accumulated training stimulus/adaptation;
- attribute gain;
- skill XP/progression;
- hypertrophy/body-measurement progression;
- soreness/injury;
- exercise taxonomy/programming/reps/sets/load;
- equipment/facility-quality modifier expansion;
- grading/tier progression;
- schema v5.

## Exact resume point — STOP / DISCUSSION REQUIRED

P3.5 is complete, acceptance-verified, and deployed. **Do not select, design, or implement a P3.6 or any other new development slice yet.** The Creator explicitly requested a discussion after P3.5 before development continues.

A fresh chat must reconcile canonical state first, then remain at this discussion gate until the Creator explicitly authorizes the next direction.

Preserve schema v4, 1x wake-on-demand autonomy, globally scoped ids, actor-scoped runtime, first-class actions/events, Telegram presentation rules, profile/runtime separation, typed/audited Creator control, and incremental expansion only through explicitly chosen minimum-runnable needs.
