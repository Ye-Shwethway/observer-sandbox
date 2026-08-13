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
Needs/effects/training: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`, `docs/P3_3_TRAINING_READINESS_MODIFIER.md`, `docs/P3_4_TRAINING_EFFECTIVENESS.md`.
Future grading: `docs/FUTURE_GRADING_SYSTEM.md`.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory. Never conflate authored, CI-validated, acceptance-verified, deployed, DB-applied, and Creator-live-UX-verified states.

## Development policy — minimum runnable expansion

Schema v4 is the broad composable foundation. Normal development now follows:

`minimum required state -> minimum deterministic behavior/evidence -> minimum Creator-facing surface if needed -> focused tests -> disposable acceptance -> deploy/readback -> Creator acceptance -> next slice`.

Do not pre-build large inventory, grading, memory, relationship, environment, combat, training, or regional subsystems merely because schema sockets exist. Prefer one independently runnable feature at a time.

## Production baseline

- Repo: `Ye-Shwethway/observer-sandbox`
- VPS app: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- systemd: `observer-sandbox`
- SQLite schema: v4
- world root: `world_observer_universe`
- estate: `loc_thorne_estate`
- world identity revision: `thorne-estate-v3.0-scoped-ids`
- Darian autonomy: enabled / normal / unpaused / 1x / wake-on-demand
- cognition: existing Gemini character binding preserved through recent deploys
- Telegram: connected private Creator observer; owner/allowed-user configuration present

Production continues autonomously. Re-read live state whenever exact current Darian action/stats matter.

## Canonical runtime rule

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

LLMs propose structured actions only. Deterministic runtime owns legality and mutation. Universe-global clock/pause/speed stay separate from actor-scoped scheduler/cognition state. First-class `action_instances` and linked events retain target, modifiers, outcome, state-change, location, and participant evidence.

## Proven Creator-facing surfaces

### P2.2 Browse the Sandbox
Status: COMPLETE / LIVE UX VERIFIED.

Proven live flows include Estate/location browsing, object detail browsing, and Character Profile sections. Static/canonical profile truth remains separate from live runtime/domain state.

### P2.3.1 Restore Basic Stats
Status: COMPLETE / LIVE UX VERIFIED.

Typed/audited Creator control restores basic living stats, cancels stale pending work, clears lease/retry state, preserves autonomy mode/time/location/profile canon, writes an audit event, and is exposed through CLI, owner-only Telegram confirmation flow, and guarded GitHub Actions backend reuse. Do not broaden this into arbitrary field editing.

## P3 richer simulation vertical slices

### P3.1 — Minimum Systemic Training Fatigue / Recovery
Status: COMPLETE / LIVE UX VERIFIED.

`physiology.fatigue` is simulated `0..100` state. Training adds intrinsic fatigue while ordinary time/rest/sleep recover it. Training is unavailable at fatigue `>=70`; baseline policy avoids ordinary morning training at fatigue `>=55`. Telegram Profile -> Recovery exposes live systemic fatigue. Disposable acceptance and Creator live UX were successful.

### P3.2 — Minimum Targeted Training Session
Status: COMPLETE / ACCEPTANCE VERIFIED.

Home Gym `Heavy Bag` and `Free Weights` are legal `train` targets only when co-located and capability-valid. Target selection persists through action instance and completion event evidence, and Telegram/history presentation resolves friendly names. No exercise taxonomy, sets/reps/load, progression, hypertrophy, injury, or grading was added.

### P3.3 — Minimum Training Readiness Modifier
Status: COMPLETE / DEPLOYED / LIVE UX VERIFIED.

Canonical doc: `docs/P3_3_TRAINING_READINESS_MODIFIER.md`.

Readiness derives from existing authoritative energy, thirst, sleepiness, and systemic fatigue. It remains derived state rather than a new canonical physiology field.

Reference behavior:
- healthy inputs `80/15/15/0` -> readiness `1.000`, fatigue-cost multiplier `1.000x`, one-hour resulting fatigue `18.5`;
- degraded legal inputs `50/45/45/40` -> readiness `0.595`, Telegram Recovery `59.5%`, fatigue-cost multiplier `1.202x`, resulting fatigue `62.54`;
- fatigue `>=70` hard condition still blocks training.

Evidence:
- P3 Training Readiness Acceptance #5 / run `31673341881` SUCCESS with zero model calls on a disposable production copy;
- release commit `9b8b59b86696515829508b532558ffce1134c507`;
- Deploy #129 / run `31673382889` SUCCESS;
- Creator tested Telegram Profile -> Recovery and confirmed the deployed readiness presentation works.

### P3.4 — Minimum Training Effectiveness Outcome
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Canonical doc: `docs/P3_4_TRAINING_EFFECTIVENESS.md`.

Purpose: create the first positive training-outcome signal without mutating progression state.

Semantic split:
- `readiness` = pre-action state summary;
- `fatigue_cost_multiplier` = physiological cost;
- `effectiveness` = useful training-stimulus fraction recorded as first-class outcome evidence.

For v1, `effectiveness = readiness`. This is intentionally a stable output socket, not yet a strength/skill/hypertrophy engine.

Persistence is through existing schema-v4 paths:
- `action_instances.modifiers_json`;
- completion `outcome_json.modifiers`;
- `action_completed` event payload modifiers.

Reference behavior:
- healthy -> effectiveness `1.0`, fatigue-cost multiplier `1.0x`, resulting fatigue `18.5`;
- degraded reference -> effectiveness `0.595`, fatigue-cost multiplier `1.202x`, resulting fatigue `62.54`.

Regression coverage explicitly proves P3.4 does not change skill score/tier/experience.

Evidence:
- PR #3, merged commit `ea69d5c0f81bf5500fca9b4d6ea62a251fbdcd9f`;
- PR CI #317 SUCCESS;
- main CI #318 / run `31673822574` SUCCESS;
- P3 Training Effectiveness Acceptance #1 / run `31673822547` SUCCESS with zero model calls and unchanged production DB;
- release commit `818752a5976d988fcd3445ed3f0cc984f637d1cb`;
- Deploy #130 / run `31673858850` SUCCESS.

P3.4 intentionally adds no new standalone Telegram row: effectiveness exists as action/outcome evidence for a future bounded consumer.

## Explicitly deferred boundaries

Still not implemented merely because P3.4 provides an effectiveness socket:
- skill/strength/experience gain;
- hypertrophy/body progression;
- exercise taxonomy/programming, reps/sets/load;
- muscle soreness/injury;
- equipment/facility-quality modifiers;
- nutrition/stimulant/environment/psychological modifier expansion;
- universal grading/progression engine;
- schema v5.

## Exact resume point

P2.2, P2.3.1, P3.1, and P3.3 are LIVE UX VERIFIED. P3.2 is acceptance verified. P3.4 is merged, main-CI verified, disposable-acceptance verified, and deployed successfully in production.

The next feature must be selected as another minimum runnable slice. Do not automatically turn the new `effectiveness` field into broad progression. A sensible next direction is one narrow consumer of effectiveness—such as a minimal session-history/observer readout or a single bounded progression proof—but choose and document the slice before implementing it.

Preserve 1x wake-on-demand autonomy, schema v4, scoped ids, locked unfinished world boundaries, actor-scoped runtime, first-class actions/events, Telegram presentation rules, profile/runtime separation, typed Creator authority, and incremental modifier expansion.
