# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-13

## Product principles

- Python/SQLite runtime/world state is authoritative.
- AI proposes structured cognition; it never directly mutates arbitrary world state.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Cognition remains wake-on-demand; no periodic LLM heartbeat by default.
- Canonical runtime composition:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Schema v4 is the current composable foundation. Do not introduce schema v5 without a concrete missing invariant.
- Development proceeds by minimum runnable vertical slices, not subsystem-first expansion.

## Development policy — minimum runnable expansion

Each feature should normally contain only:
1. minimum new canonical/runtime state required;
2. minimum deterministic/query behavior;
3. minimum Creator-facing observation/control surface if needed;
4. focused tests;
5. disposable production-copy acceptance when runtime behavior matters;
6. deploy/readback;
7. Creator UX acceptance when a Creator-facing surface changes.

Prefer:
`one small feature -> run -> observe -> validate -> keep -> next feature`

over broad speculative subsystem construction.

## Foundation — COMPLETE

Schema v4 provides universe-global state separate from actor runtime, data-driven actions, first-class action instances/events, place/target/participants/resources/conditions/modifiers/outcomes, concurrency-safe simulation time, generic effects/modifier sockets, and globally scoped spatial/resource identities. No broad foundation rewrite is currently required.

## P0 / P0.5 / P1

- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 AI Provider Layer — FOUNDATION COMPLETE; Darian preserves the configured Gemini cognition binding.
- P1 Living Darian Minimum — CONTINUOUS AUTONOMY LIVE / ENGINE HARDENING PASSED.

## P2 — Telegram Observer

- P2.1 Mobile Observer MVP — LIVE.
- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.

Creator controls remain typed and audited; do not expand them into arbitrary editing/admin-console behavior.

## P3 — Richer Simulation Vertical Slices

### P3.1 — Minimum Systemic Training Fatigue / Recovery
Status: COMPLETE / LIVE UX VERIFIED.

Live systemic fatigue, recovery paths, hard training block at fatigue `>=70`, baseline training avoidance at `>=55`, and Telegram Recovery observation are proven.

### P3.2 — Minimum Targeted Training Session
Status: COMPLETE / ACCEPTANCE VERIFIED.

Heavy Bag and Free Weights are real capability/co-location-valid training targets; selected target persists through action/event evidence and observer presentation.

### P3.3 — Minimum Training Readiness Modifier
Status: COMPLETE / DEPLOYED / LIVE UX VERIFIED.

Readiness derives from energy, thirst, sleepiness, and systemic fatigue. It changes fatigue cost without replacing hard conditions.

Degraded reference: readiness `0.595`, fatigue multiplier `1.202x`, one-hour resulting fatigue `62.54`.

Evidence: P3 Training Readiness Acceptance #5 / run `31673341881` SUCCESS; Deploy #129 / run `31673382889` SUCCESS; Creator verified Telegram Recovery readiness.

### P3.4 — Minimum Training Effectiveness Outcome
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Effectiveness is a positive useful-work fraction recorded in action/outcome evidence; v1 uses `effectiveness = readiness`. It does not mutate progression.

Evidence:
- merge `ea69d5c0f81bf5500fca9b4d6ea62a251fbdcd9f`;
- main CI #318 / run `31673822574` SUCCESS;
- P3 Training Effectiveness Acceptance #1 / run `31673822547` SUCCESS;
- Deploy #130 / run `31673858850` SUCCESS.

### P3.5 — Minimum Effective Training Load
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Canonical detail: `docs/P3_5_EFFECTIVE_TRAINING_LOAD.md` and `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

P3.5 completes the current short-term training loop:

`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology`

Rules:
- passive drift applies for full planned duration;
- effectiveness scales training-specific energy/hunger/thirst/cleanliness effects;
- fatigue remains on the separate P3.3 fatigue-cost multiplier;
- `effective_minutes = planned_minutes × effectiveness` persists in outcome/event evidence;
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
- P3 Effective Training Load Acceptance #1 / run `31674911581` SUCCESS, zero model calls, disposable production copy, progression unchanged;
- release commit `22ff453715659d2c772ffcd19868716413a715a1`;
- Deploy #131 / run `31674963422` SUCCESS;
- production readback healthy with schema v4, autonomy enabled/normal/unpaused/`1x`, preserved Gemini cognition binding, and Telegram API connected.

## Explicitly deferred after P3.5

No current implementation exists for:
- accumulated stimulus/adaptation;
- strength/endurance/other attribute progression;
- skill XP/tier progression;
- hypertrophy/body measurements;
- soreness/injury;
- exercise taxonomy/programming/reps/sets/load;
- equipment/facility quality effects on progression;
- universal grading/tier evaluation;
- schema v5.

The existence of effectiveness/effective minutes is an extension socket, not authorization to implement these systems.

## P4 / P5 / regional expansion

P4 context/memory/relationships remains demand-driven and later. P5 second production character remains later. South Lake Tahoe expansion remains later and must proceed destination-by-destination when authorized.

## Current resume point — DISCUSSION STOP GATE

P3.5 is complete, acceptance verified, and deployed. **No next slice is currently selected or authorized.** The Creator explicitly requested discussion after P3.5 and instructed development not to continue beyond it.

Do not design or implement P3.6, grading, stimulus/adaptation, body progression, or another unrelated slice until the Creator discussion concludes with explicit direction.

Preserve schema v4, 1x wake-on-demand autonomy, globally scoped ids, actor-scoped scheduler state, first-class actions/events, Telegram presentation rules, profile/runtime separation, typed/audited Creator control, and incremental expansion only through explicitly authorized minimum-runnable needs.
