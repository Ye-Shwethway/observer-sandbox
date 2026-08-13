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

## Development policy

Each feature should normally contain only minimum required state/behavior, minimum Creator-facing surface, focused tests, disposable production-copy acceptance when runtime behavior matters, deploy/readback, and Creator live acceptance where appropriate.

Prefer:
`one small feature -> run -> observe -> validate -> keep -> next feature`.

## Foundation / P0 / P1

- Foundation schema v4 — COMPLETE.
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

### P3.2 — Minimum Targeted Training Session
Status: COMPLETE / ACCEPTANCE VERIFIED.

### P3.3 — Minimum Training Readiness Modifier
Status: COMPLETE / DEPLOYED / LIVE UX VERIFIED.

Readiness derives from energy, thirst, sleepiness, and systemic fatigue; it changes fatigue cost without replacing hard conditions.

### P3.4 — Minimum Training Effectiveness Outcome
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Effectiveness is a positive useful-work fraction recorded in action/outcome evidence; v1 uses `effectiveness = readiness`. It does not mutate progression.

### P3.5 — Minimum Effective Training Load
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Canonical detail: `docs/P3_5_EFFECTIVE_TRAINING_LOAD.md` and `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

P3.5 completes the current short-term loop:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology`.

No accumulated stimulus, strength/skill progression, hypertrophy/body measurements, grading, or tiers are implemented.

## Post-P3.5 Stabilization — Autonomy Breadth + Time Observability v1

Status: DEPLOYED / ACCEPTANCE VERIFIED / CREATOR LIVE BEHAVIOR VERIFICATION PENDING.

Canonical detail: `docs/AUTONOMY_BREADTH_TIME_OBSERVABILITY.md`.

This bounded release responds to Creator-observed Kitchen/Pantry/Refrigerator/Stove repetition and opaque action timing.

Delivered:
- world object breadth expanded from 15 to 27 instances using existing estate topology and generic action vocabulary;
- meaningful fixtures added across the wider estate, with seven previously sparse non-kitchen purposeful rooms acceptance-proven to expose legal action targets;
- Darian autonomy policy v1.4 discourages serial same-room generic inspect/use loops and default kitchen appliance inspection when needs are comfortable;
- normal model guidance prefers simple inspection around 2–6 simulated minutes and simple use around 2–10, while persisted compatibility bounds remain broad enough to preserve already-running actions;
- Telegram completion notification now exposes completed duration and may include the newly planned next action, its duration, and expected simulated completion timestamp;
- one committed action still produces at most one proactive notification per recipient;
- time semantics remain linear: at 1x, N simulated minutes normally imply approximately N real minutes of scheduled wall wait.

Evidence:
- PR #5 merge `ac19e132bc5fa10688bb54e69fe885b1ae196510`, CI #332 SUCCESS;
- safety correction PR #6 merge `29be3e8d70d99b23f17380a7bfd4d5adf8a07101`, CI #334 SUCCESS;
- main CI #336 / run `31676984174` SUCCESS;
- Autonomy Breadth and Time Acceptance #2 / run `31676984134` SUCCESS on candidate code + disposable production DB copy, zero model calls;
- release commit `7163284d19df19cda252437563d13c83d939b197`;
- Deploy #132 / run `31677053654` SUCCESS with healthy schema-v4 service, normal/unpaused/1x autonomy, preserved pending action and Gemini binding, and connected Telegram API.

Behavioral diversity itself is not deterministic CI evidence. Creator live notification observation is the acceptance surface for deciding whether v1.4 breadth guidance is sufficient.

## Deferred after current release

Not implemented:
- deterministic per-action/per-target duration profiles;
- accumulated training stimulus/adaptation;
- strength/endurance/other attribute progression;
- skill XP/tier progression;
- hypertrophy/body measurements;
- soreness/injury;
- exercise programming/reps/sets/load;
- inventory/resource depletion;
- universal grading/tier evaluation;
- exterior/Tahoe traversal;
- schema v5.

## P4 / P5 / regional expansion

P4 context/memory/relationships remains demand-driven and later. P5 second production character remains later. South Lake Tahoe expansion remains later and must proceed destination-by-destination when authorized.

## Current resume point — LIVE OBSERVATION

The autonomy breadth/time stabilization release is deployed. Next action is **observation rather than immediate new development**:

- confirm Telegram messages show duration plus useful next-action ETA;
- observe whether Darian begins choosing a broader mix of meaningful estate rooms/objects;
- note any still-implausible durations.

If duration choice remains weak, discuss one bounded deterministic per-action/per-target duration-profile slice. Do not use a blanket persisted-bound reduction that can invalidate pending actions.

Do not automatically return to training progression/grading work until the Creator selects that direction after live observation.

Preserve schema v4, 1x wake-on-demand autonomy, globally scoped ids, actor-scoped scheduler state, first-class actions/events, Telegram presentation rules, profile/runtime separation, typed/audited Creator control, and incremental expansion only through explicitly authorized minimum-runnable needs.