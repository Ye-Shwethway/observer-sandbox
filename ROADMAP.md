# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-14

## Operating principles

- Python/SQLite runtime and world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutations.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Preserve the composable runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Schema v4 remains the current foundation; do not introduce schema v5 without a concrete missing invariant.
- Prefer minimum runnable slices and reversible changes.
- Use exemplar-first only for genuinely new invariants; batch structurally equivalent follow-ons.
- Default development flow:
  `test -> focused tests + CI -> merge to main -> automatic deploy when runtime-affecting -> read-only production check`.
- Keep only persistent `main` and reusable `test` branches unless a concrete exceptional need requires otherwise.
- Production-copy validation is optional and reserved for genuinely state-sensitive or migration-heavy changes that local tests/CI cannot cover well enough.

## Current production baseline

- Repository: `Ye-Shwethway/observer-sandbox`
- VPS application: `/opt/observer-sandbox`
- Production DB: `/var/lib/observer-sandbox/observer.sqlite3`
- Service: `observer-sandbox`
- Schema: v4
- World revision: `thorne-estate-v3.2-training-environment`
- Autonomy: enabled / normal
- Cognition: Gemini `gemini-3.5-flash-lite`
- Telegram: connected
- Latest verified speed: `1.0x` at Deploy #164 readback; speed is Creator-controlled and must be re-read whenever exact cadence matters.
- Latest deployment: Deploy #164 `31739837957` SUCCESS from PR #53 merge `701599074e9e9824384e624f11c288feb07d0924`.

## Completed foundation and observer layers

- Foundation schema v4 — COMPLETE.
- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 AI Provider Layer foundation — COMPLETE; configured Gemini cognition preserved.
- P1 Living Darian Minimum — CONTINUOUS AUTONOMY LIVE.
- P2 Telegram Observer MVP / browse / profile-control surfaces — COMPLETE / LIVE VERIFIED.
- Runtime speed control, action ETA, autonomy timing/observability, research/monitor semantics — DEPLOYED.

## Training and physiology

- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE VERIFIED.
- P3.2 Targeted Training Session — COMPLETE.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED.
- P3.4 Training Effectiveness Outcome — COMPLETE / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / DEPLOYED.
- Minimum Training Stimulus v1 — COMPLETE / DEPLOYED.
- Training Session Load & Recovery Guard v1 — COMPLETE / CI VERIFIED / DEPLOYED.
- Causal hunger, thirst, energy, sleepiness, cleanliness and fatigue resolution — DEPLOYED.

### Training Session Load & Recovery Guard v1

PR #53 tested head `4c8d8f3caa3814f2def3c168e76b9d426bf37416`; CI #570 / run `31739634403` succeeded; merged as `701599074e9e9824384e624f11c288feb07d0924`; Deploy #164 / run `31739837957` succeeded.

The guard derives training dose from completed action history and existing effective-load evidence rather than treating current systemic fatigue as the whole training-memory model.

Current v1 budgets are deliberately bounded and simple:
- current-session limit: `90` effective minutes;
- session break: more than `120` simulated minutes without training;
- rolling 6-hour limit: `120` effective minutes;
- rolling 24-hour limit: `180` effective minutes.

Autonomous cognition receives the derived load status. Train-option duration is capped to the remaining budget; training options disappear when the remaining budget cannot support the minimum legal session; the final model-selected duration is checked again before scheduling.

This means short rest/fatigue recovery does not erase recent training dose. No schema v5, new canonical physiology field, universal injury model, or Mind Engine was introduced.

## Thorne Estate training environment

Status: COMPLETE / DEPLOYED.

- Interior-first Thorne Estate environment is implemented against `docs/DARIAN_MANSION_REFERENCE.md`.
- Top-Class Home Gym and Training Hall expose the richer bounded training-equipment surface.
- World revision is `thorne-estate-v3.2-training-environment`.
- Exterior estate grounds, private lake traversal, outdoor tactical course and broader Tahoe traversal remain deferred.

## Training Method Semantics v1

Status: COMPLETE / DEPLOYED.

`config/training_methods.v1.json` provides authored method metadata for current train-capable targets. It now also carries descriptive planning metadata for training methods without changing the canonical evidence source revision `training-method-semantics-v1`.

Equipment/method metadata describes workload evidence and planning context only. It does not own attribute progression formulas, recovery, decay or settlement.

## Dynamic Resource Awareness & Choice Breadth v1

Status: COMPLETE / CI VERIFIED / DEPLOYED.

PR #50 merged as `7516f6c09a371803508f67a1575d6ce83a170de2`; CI #557 succeeded; Deploy #161 succeeded.

Current cognition surface now:
- receives every legal current-room action/resource from the existing capability-driven action-option engine;
- receives one-hop reachable-location resource and training-method previews for purposeful movement planning;
- preserves move-first legality, so distant resources are visible for planning but not directly actionable;
- receives recent action-target usage metadata (`recent_uses`, latest simulated use time, repeated flag) as context rather than a hard repetition block;
- receives resource-aware autonomy guidance encouraging sensible variety when equivalent choices exist, without introducing a scoring/mind engine or forced rotation.

Focused tests prove all 10 Home Gym training resources reach cognition, Home Gym resources are visible from the connected Living Room as planning-only affordances, and repeated Free Weights use remains legal while being explicitly signaled as recent repetition.

## Physical progression state

### Strength

Status: ACTIVE / DEPLOYED / LIVE-CYCLE VALIDATED.

Free Weights remains the deliberate Strength stimulus source. Strength has its own level difficulty, saturation, recovery, detraining, idempotent settlement and completed-action activation semantics.

### Stamina

Status: ACTIVE / DEPLOYED.

Current pure-conditioning evidence sources:
- High-Speed Treadmill / `steady_state_cardio`
- Rowing Ergometer / `rowing_conditioning`
- Altitude Training Chamber / `altitude_conditioning`

Mixed movement/combat methods are not silently credited to Stamina.

### Agility

Status: ACTIVE / DEPLOYED.

Agility uses authored `speed_agility_drills` evidence from the Speed & Agility Station and has its own progression/recovery/saturation/detraining semantics. Agility Automatic Activation v1 is deployed.

## Grading state

- Strength grading exemplar — COMPLETE / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / DEPLOYED for compatible 0..100 attribute fields.
- IQ remains a separate scale.
- Skills grading/progression remains a separate family.
- Body composition/measurements remain a separate architecture family.

## Deferred boundaries

Not yet implemented as complete progression families:
- Speed progression;
- Reflexes progression;
- Endurance progression;
- Flexibility progression;
- skills progression;
- hypertrophy/body-measurement/body-composition progression;
- body-measurement grading evaluator;
- IQ/skills grading evaluators;
- inventory/resource depletion;
- richer memory/relationship engines;
- estate exterior / Tahoe traversal;
- schema v5.

## Current development policy

Persistent branch model:
- `main` = canonical/deployed line;
- `test` = reusable development/CI line.

Do not create feature/release branches by default. After a successful merge/deploy, synchronize `test` back to current `main` before the next slice.

For ordinary work, use focused tests + CI and the standard automatic deploy. Use disposable production-copy validation only when a concrete stateful risk justifies it.

## Exact resume point

Observe natural production behavior after **Training Session Load & Recovery Guard v1**.

The immediate question is whether Darian now ends or pauses training when his effective session/recent-load budget is exhausted and stays in recovery/non-training behavior even if systemic fatigue falls quickly afterward.

Continue observing resource/method variety at the same time, but do not add forced rotation or a Mind Engine merely to manufacture variety.

Speed progression remains a future candidate, but no Speed implementation is authorized by this roadmap state alone.
