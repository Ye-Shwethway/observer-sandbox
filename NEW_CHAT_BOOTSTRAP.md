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
Needs/training: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`, `docs/P3_3_TRAINING_READINESS_MODIFIER.md`, `docs/P3_4_TRAINING_EFFECTIVENESS.md`, `docs/P3_5_EFFECTIVE_TRAINING_LOAD.md`.
Current autonomy breadth/time release: `docs/AUTONOMY_BREADTH_TIME_OBSERVABILITY.md`.
Future grading: `docs/FUTURE_GRADING_SYSTEM.md`.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory. Never conflate committed, CI-validated, acceptance-verified, deployed, DB-applied, and Creator-live-verified states.

## Development policy

Use minimum runnable expansion:

`minimum required state -> minimum behavior/evidence -> minimum Creator-facing surface -> focused tests -> disposable acceptance -> deploy/readback -> Creator acceptance -> next slice`.

Do not pre-build large inventory, grading, memory, relationship, environment, combat, training, or regional systems merely because extension sockets exist.

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
- Telegram: connected private Creator observer

Production continues autonomously. Re-read live state whenever exact current Darian action/stats matter.

## Canonical runtime rule

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

LLMs propose structured actions only. Deterministic runtime owns legality and mutation. First-class actions/events preserve target, modifiers, outcome, state changes, location, and participant evidence.

## Proven feature state

- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.
- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.
- P3.4 Training Effectiveness Outcome — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

P3.5 completes the current short-term training loop:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology`.
It does not implement accumulated stimulus, attribute/skill gain, body-measurement progression, grading, or tiers.

## Autonomy Breadth + Time Observability v1

Status: DEPLOYED / ACCEPTANCE VERIFIED / CREATOR LIVE BEHAVIOR VERIFICATION PENDING.

Canonical detail: `docs/AUTONOMY_BREADTH_TIME_OBSERVABILITY.md`.

Motivation was Creator-observed production repetition around Kitchen/Pantry/Refrigerator/Stove and opaque action timing.

Delivered:
- estate object seed expanded from 15 to 27 objects without new topology/exterior traversal;
- purposeful actionable fixtures added across Master Suite, Living Room, Library, Garage, Intelligence Hub, Comms, Training Hall, Medical Bay, Armory, Food Storage, and Bunker;
- seven previously sparse non-kitchen purposeful rooms are acceptance-proven to expose legal targets;
- Darian policy revision `darian-autonomy-p1-v1.4-breadth-duration-aware` discourages serial same-room generic inspect/use loops and default kitchen appliance inspection;
- normal guidance prefers quick inspection `2–6` simulated minutes and simple use `2–10` when the purpose is not sustained;
- persisted compatibility bounds remain `inspect 1–60` and `use 1–120` so a deploy cannot invalidate an already-running action;
- Telegram completion push now shows completed duration and may show the immediately planned next action, next duration, and expected simulated completion timestamp;
- proactive notification contract remains at most one push per committed action.

Time semantics are unchanged and linear: action interval advances by `duration_minutes`; scheduler wall wait is approximately `duration_minutes × 60 / speed`. At production `1x`, one sim minute is about one real minute between normal action boundaries.

Evidence:
- PR #5 merge `ac19e132bc5fa10688bb54e69fe885b1ae196510`; PR CI #332 / `31676550067` SUCCESS;
- pending-action safety PR #6 merge `29be3e8d70d99b23f17380a7bfd4d5adf8a07101`; PR CI #334 / `31676811535` SUCCESS;
- accepted main `802b17fce70f9d3b28d29fd2dc56267b17f3fb9f`;
- main CI #336 / `31676984174` SUCCESS;
- Autonomy Breadth and Time Acceptance #2 / `31676984134` SUCCESS: 27 objects, seven non-kitchen target rooms, quick-duration guidance, pending-compatible bounds, timing UI visible, zero model calls, production DB unchanged;
- release commit `7163284d19df19cda252437563d13c83d939b197`;
- Deploy #132 / `31677053654` SUCCESS;
- deploy readback: service healthy, schema v4, autonomy enabled/normal/unpaused/1x, existing pending action preserved, Gemini binding preserved, Telegram API connected.

The first acceptance attempt failed only from acceptance-harness SSH/SQL quoting; no failed candidate was deployed.

## Deferred boundaries

Still not implemented:
- deterministic per-action/per-target duration profiles;
- accumulated training stimulus/adaptation;
- attribute or skill progression;
- hypertrophy/body-measurement progression;
- soreness/injury;
- exercise programming/reps/sets/load;
- inventory/depletion;
- grading/tier progression;
- exterior/Tahoe traversal;
- schema v5.

## Exact resume point

The autonomy breadth/time stabilization release is deployed. **Do not claim behavioral diversity is live-verified yet.** The Creator should observe normal Telegram production messages and verify two things:

1. notifications now expose useful duration/next-action ETA information;
2. Darian actually begins using a broader mix of estate rooms/objects rather than falling back into repeated kitchen appliance loops.

If duration guidance still produces implausible choices, the next relevant discussion is a bounded deterministic per-action/per-target duration-profile design, not another blanket narrowing of persisted action bounds.

Do not automatically resume long-term training progression/grading work from P3.5. Choose the next development direction only after the Creator reviews this live behavior.

Preserve schema v4, 1x wake-on-demand autonomy, globally scoped ids, actor-scoped runtime, first-class actions/events, Telegram presentation rules, profile/runtime separation, typed/audited Creator control, and incremental expansion.