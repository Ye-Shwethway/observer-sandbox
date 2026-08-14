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
- Latest verified speed: `1.0x` at Deploy #165 readback; speed is Creator-controlled and must be re-read whenever exact cadence matters.
- Latest deployment: Deploy #165 `31765700369` SUCCESS from PR #54 merge `d6742fcbaa06868ca7dbd58bac33ee09430d1a0d`.

Deploy #165 readback was healthy with schema v4 and preserved Gemini/Telegram configuration. Darian was idle in the Training Hall at `2025-05-04T17:18:00+00:00`, fatigue `34.935`. A pre-deploy retry record (`failures=8`, `last_error=ValueError`, no pending action) was still present; re-check only if it persists across fresh post-deploy decisions or causes a visible stall.

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
- Sleep Pressure & Circadian Need v1 — COMPLETE / DEPLOYED.

### Training Session Load & Recovery Guard v1

PR #53 tested head `4c8d8f3caa3814f2def3c168e76b9d426bf37416`; CI #570 / run `31739634403` succeeded; merged as `701599074e9e9824384e624f11c288feb07d0924`; Deploy #164 / run `31739837957` succeeded.

The guard derives training dose from completed action history and existing effective-load evidence rather than treating current systemic fatigue as the whole training-memory model.

Current v1 budgets:
- current-session limit: `90` effective minutes;
- session break: more than `120` simulated minutes without training;
- rolling 6-hour limit: `120` effective minutes;
- rolling 24-hour limit: `180` effective minutes.

Autonomous cognition receives the derived load status. Train-option duration is capped to the remaining budget; training options disappear when the remaining budget cannot support the minimum legal session; the final model-selected duration is checked again before scheduling.

Short rest/fatigue recovery therefore does not erase recent training dose. No schema v5, new canonical physiology field, universal injury model, or Mind Engine was introduced.

## Thorne Estate training environment

Status: COMPLETE / DEPLOYED.

- Interior-first Thorne Estate environment is implemented against `docs/DARIAN_MANSION_REFERENCE.md`.
- Top-Class Home Gym and Training Hall expose the richer bounded training-equipment surface.
- World revision is `thorne-estate-v3.2-training-environment`.
- Exterior estate grounds, private lake traversal, outdoor tactical course and broader Tahoe traversal remain deferred.

## Training Method Semantics v1

Status: COMPLETE / DEPLOYED.

`config/training_methods.v1.json` provides authored method metadata for current train-capable targets. It also carries descriptive planning metadata without changing the canonical evidence source revision `training-method-semantics-v1`.

Equipment/method metadata describes workload evidence and planning context only. It does not own attribute progression formulas, recovery, decay or settlement.

## Dynamic Resource Awareness & Choice Breadth v1

Status: COMPLETE / CI VERIFIED / DEPLOYED.

PR #50 merged as `7516f6c09a371803508f67a1575d6ce83a170de2`; CI #557 succeeded; Deploy #161 succeeded.

Cognition receives every legal current-room action/resource from generic capability matching, one-hop reachable-location previews, move-first legality, and recent action-target usage metadata. Resource awareness encourages sensible variety without a forced-rotation or scoring engine.

## Object Familiarity / Inspect Utility Guard v1

Status: COMPLETE / CI VERIFIED / DEPLOYED.

PR #54 final tested head `674de824acf69fc4209e59e649364d0ece3696f5`; CI #575 / run `31765655658` succeeded; merge `d6742fcbaa06868ca7dbd58bac33ee09430d1a0d`; Deploy #165 / run `31765700369` succeeded; post-merge CI #576 succeeded.

This is a bounded familiarity bridge rather than a full Character Memory Engine.

Current semantics:
- established functional estate resources are treated as familiar and do not remain generic low-value `inspect` fallbacks;
- genuinely unknown inspect-only objects can remain available for a first-look inspection;
- existing interaction/event history can establish familiarity without a schema change;
- the midday autonomy policy no longer advertises generic equipment checks as productive default behavior;
- cognition is explicitly allowed to choose ordinary non-training activity or downtime instead of manufacturing fake productivity when training is unavailable.

Focused tests cover the observed room-hopping inspection fallback while preserving discovery of unknown inspect-only objects.

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

Not yet implemented as complete families:
- full Character Memory Engine / richer episodic-semantic memory;
- Speed progression;
- Reflexes progression;
- Endurance progression;
- Flexibility progression;
- skills progression;
- hypertrophy/body-measurement/body-composition progression;
- body-measurement grading evaluator;
- IQ/skills grading evaluators;
- inventory/resource depletion;
- richer relationship engine;
- estate exterior / Tahoe traversal;
- schema v5.

## Current development policy

Persistent branch model:
- `main` = canonical/deployed line;
- `test` = reusable development/CI line.

Do not create feature/release branches by default. After a successful merge/deploy, synchronize `test` back to current `main` before the next slice.

For ordinary work, use focused tests + CI and the standard automatic deploy. Use disposable production-copy validation only when a concrete stateful risk justifies it.

## Exact resume point

Observe natural production behavior after **Object Familiarity / Inspect Utility Guard v1**.

The immediate question is whether Darian now avoids room-hopping through familiar equipment for generic inspections when his training-load budget blocks further exercise, and instead chooses meaningful non-training activity or ordinary downtime.

Also verify whether the pre-deploy `ValueError` retry record clears on fresh autonomous decisions. Investigate only if it persists or causes observable stalling.

Do not build the full Character Memory Engine merely to solve familiarity, and do not start Speed progression without fresh Creator authorization.
