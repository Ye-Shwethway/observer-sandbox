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
- New architecture/control surfaces must update their canonical contract plus this roadmap/bootstrap checkpoint in the same development cycle.

## Current production baseline

- Repository: `Ye-Shwethway/observer-sandbox`
- VPS application: `/opt/observer-sandbox`
- Production DB: `/var/lib/observer-sandbox/observer.sqlite3`
- Service: `observer-sandbox`
- Schema: v4
- World revision: `thorne-estate-v3.2-training-environment`
- Autonomy: enabled / normal
- Cognition: Gemini `gemini-3.1-flash-lite`
- Telegram: connected
- Latest verified speed: `3.0x` at Deploy #172 readback.
- Latest verified runtime-affecting deployment: Deploy #172 `31779629810` SUCCESS from PR #65 merge `20c01b82a1ebacbd05d5a12cdccef009c7284981`.
- Deploy #172 readback: service active/healthy, schema v4, autonomy enabled/normal, `autonomy_retry=null`, Creator-selected Gemini binding preserved, Telegram API connected, Creator owner configuration present.
- Post-merge CI #602 / run `31779629861` SUCCESS.
- PR #62 / Deploy #170 added the next planned action reason to proactive Telegram Character Updates.

Post-Deploy169 live acceptance cleared the prior retry-cap stall on a natural decision boundary: cognition `decision_calls` advanced `331 -> 332`, `autonomy_retry` became `null`, and Darian scheduled a 10-minute `rest` action in the Training Hall. By Deploy #172 readback natural cognition had advanced to `decision_calls=352` at sim time `2025-05-04T21:32:00+00:00`; Darian was showering in the Master Bathroom. No production acceleration, direct live state mutation, validation-induced model probe, or intentionally induced provider failure was used for this deployment.

## Completed foundation and observer layers

- Foundation schema v4 — COMPLETE.
- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 AI Provider Layer foundation — COMPLETE; Gemini plus generic OpenAI-compatible live cognition are deployed.
- P1 Living Darian Minimum — CONTINUOUS AUTONOMY LIVE.
- P2 Telegram Observer MVP / browse / profile-control surfaces — COMPLETE / LIVE VERIFIED.
- Runtime speed control, action ETA, autonomy timing/observability, research/monitor semantics — DEPLOYED.
- Telegram proactive next-action reason visibility — DEPLOYED via PR #62 / Deploy #170.

## P2.3 Telegram Creator AI Control v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED / CREATOR-EXERCISED**.

Delivery:
- PR #63 tested head `f2e61d374dce1c3b493d27fb94e1024b9eb5a3fd`;
- primary CI #595 / run `31769832103` SUCCESS;
- merged as `d8a3f770dd3c6f4293f5035d1085998ba0562bf7`;
- Deploy #171 / run `31769893556` SUCCESS;
- Creator later reported a successful real Gemini model probe and successful activation back to Gemini through Telegram;
- Deploy #172 independently verified that the selected Gemini binding is `gemini-3.1-flash-lite` and remains preserved across normal deployment bootstrap.

One unrelated Stamina Progression production-copy acceptance workflow failed during PR #63 on an existing eligible-event assertion against the evolving disposable production copy. That control slice did not touch Stamina/progression semantics; primary full CI and Strength acceptance succeeded, and production-copy validation is non-mandatory for non-state-sensitive control-plane changes under current project policy.

Current minimum-runnable surface:
- owner-only `Creator Settings -> AI Cognition` navigation plus `/settings` and `/ai` entry points;
- display the current cognition provider/model binding;
- list built-in providers while revealing only credential presence/absence, never credential values;
- fetch a provider's live model catalog without changing active cognition configuration as a side effect;
- cache and paginate fetched models;
- stage provider/model candidates server-side so arbitrary/full model ids do not need to fit Telegram callback payloads;
- run one deliberately tiny **real inference probe** through the selected model's actual runtime adapter and structured cognition-response path;
- report useful auth/permission, model availability, request-limit, rate/quota, timeout, or bounded provider errors;
- require a successful probe before primary or fallback save becomes available or is accepted server-side;
- preserve bindings on browse, refresh, candidate selection, test failure, cancellation, and navigation;
- only explicit Creator save changes primary/fallback configuration.

Architecture split:
- reusable provider/catalog/probe/binding/fallback orchestration lives in `src/observer_sandbox/ai_control.py` plus `src/observer_sandbox/ai_fallback.py`;
- Telegram candidate session/navigation/presentation lives in `src/observer_sandbox/telegram_ai_control.py`;
- the existing polling shell is extended through `src/observer_sandbox/telegram_creator_bot.py` rather than duplicating the base bot/runtime;
- `service.py` routes Telegram polling through that extension;
- canonical behavior is defined in `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`, `docs/AI_RUNTIME_FALLBACK.md`, and `docs/TELEGRAM_HOME_LIFECYCLE.md`.

Probe semantics:
- catalog fetch is not treated as an inference health check;
- the probe consumes one intentionally minimal real provider inference call and therefore can detect a current quota/rate/auth/model failure before activation;
- a passing probe proves only that the selected model worked at that moment; it does not guarantee future quota availability;
- probe execution never mutates world/profile/progression state or the current cognition binding;
- deployment/CI verification must not invoke the probe; it is an explicit Creator action.

## Runtime Cognition Fallback v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

Canonical contract: `docs/AI_RUNTIME_FALLBACK.md`.

Delivery:
- PR #65 final tested head `ddfcd757fb94d270a5b20db1bd1601d92b050903`;
- primary CI #601 / run `31779586802` SUCCESS;
- merge `20c01b82a1ebacbd05d5a12cdccef009c7284981`;
- Deploy #172 / run `31779629810` SUCCESS;
- post-merge CI #602 / run `31779629861` SUCCESS;
- readback verified service health and preservation of Creator-selected Gemini `gemini-3.1-flash-lite` through the legacy Groq bootstrap entry point (`changed=false`, `existing_binding_preserved`).

Current invariant:
- one ordinary primary cognition binding plus at most one tested fallback provider/model;
- fallback selection from Telegram uses the same `fetch -> select -> Test Model -> Save Fallback` safety pattern;
- primary binding never changes merely because fallback is used;
- provider/model invocation failure may trigger one fallback attempt;
- deterministic action/target/duration/runtime validation failure never triggers provider fallback;
- if both primary and fallback fail, existing autonomy retry/backoff remains authoritative;
- successful fallback use records bounded provider/model/error metadata for observability;
- normal deploy/bootstrap preserves every existing explicit Creator-selected primary binding; `force=True` remains an explicit administrative migration only;
- no schema v5; fallback configuration uses runtime control state.

v1 deliberately does **not** add an ordered multi-fallback chain, circuit breaker, provider-health scoring, permanent automatic rebinding, or Telegram API-key editing.

## Telegram Observer Home Message Lifecycle v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

Canonical contract: `docs/TELEGRAM_HOME_LIFECYCLE.md`.

Current behavior:
- `/start` Home board includes `✕ Close`;
- Close deletes the message rather than editing it into a placeholder;
- newly sent `/start` Home boards auto-delete after 5 minutes by default;
- TTL can be configured through `OBSERVER_TELEGRAM_HOME_TTL_SECONDS`, bounded to 30..3600 seconds;
- the TTL remains active only while the message displays Observer Home; navigating away cancels it and returning Home re-arms it;
- deletion failures are presentation-only and cannot affect autonomy/simulation;
- timer state is intentionally in-process, so service restart may forget outstanding timers while manual Close remains available;
- no persistent world/schema field is added for ephemeral Telegram cleanup.

## Cognition resilience / Groq free-tier recovery

Status: **COMPLETE / CI VERIFIED / DEPLOYED / LIVE VERIFIED**.

The August 14 idle stall had multiple bounded causes rather than a single Gemini quota failure:

1. Runtime-shaped training durations could be narrower than ordinary authored preferred durations, while later normalization could expand the selected duration and repeatedly fail the final training-load check with `ValueError`.
2. Initial Groq catalog bootstrap returned HTTP 403 until OpenAI-compatible request headers/diagnostics were hardened.
3. After Groq bound successfully, live cognition returned HTTP 413 because the free/on-demand TPM limit was `8000` while the prompt requested `8645` tokens. The prompt contained duplicated derived runtime metadata.

Delivered corrections:
- PR #55 — duration-stall correction, generic OpenAI-compatible live decision adapter, Groq provider/bootstrap; CI #579 SUCCESS; merge `fb0e045686b129e5ecadb13e1f55c8fffb60e82f`.
- Deploy #166 — failed at first Groq catalog bootstrap; did not establish cognition acceptance.
- PR #56 — catalog request hardening and deploy-resilient provider bootstrap; CI #581 SUCCESS; merge `33f79327e97790f3e3fca4c0317ef87da0eae8db`; Deploy #167 SUCCESS and Groq `openai/gpt-oss-20b` bound.
- PR #57 — live provider HTTP error detail preservation; CI #583 SUCCESS; merge `cfcd9f03fe660e8438bb2a74e2adac2b041a77f2`; Deploy #168 SUCCESS.
- PR #58/#59 — read-only latest autonomy-error observability plus workflow syntax correction; current Runtime Read is healthy and does not induce model traffic.
- PR #60 — semantic-preserving cognition prompt compaction for the `8000` TPM budget; CI #589 SUCCESS; merge `b813913ced1d51733e873b89dca2b04907dad353`; post-merge CI #590 and Deploy #169 SUCCESS.

Current semantics:
- provider HTTP/quota/transport failures surface as `AIDecisionError` with bounded diagnostics and may use the configured single fallback;
- authoritative action/target pairs remain strict;
- runtime-shaped duration bounds remain authoritative during planning and normalization;
- deterministic training-load validation remains final authority;
- deterministic validation failures never trigger provider fallback;
- prompt compaction removes duplicated derived context while preserving decision principles, action authority, top-level load status, resource context, and character grounding.

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

Autonomous cognition receives the derived load status. Train-option duration is capped to the remaining budget; training options disappear when the remaining budget cannot support the minimum legal session; the final model-selected duration is checked again before scheduling. Runtime-shaped legal duration bounds now also override ordinary authored planning preferences when tighter.

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

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #54 final tested head `674de824acf69fc4209e59e649364d0ece3696f5`; CI #575 / run `31765655658` succeeded; merge `d6742fcbaa06868ca7dbd58bac33ee09430d1a0d`; Deploy #165 / run `31765700369` succeeded; post-merge CI #576 succeeded.

This is a bounded familiarity bridge rather than a full Character Memory Engine.

Current semantics:
- established functional estate resources are treated as familiar and do not remain generic low-value `inspect` fallbacks;
- genuinely unknown inspect-only objects can remain available for a first-look inspection;
- existing interaction/event history can establish familiarity without a schema change;
- the midday autonomy policy no longer advertises generic equipment checks as productive default behavior;
- cognition is explicitly allowed to choose ordinary non-training activity or downtime instead of manufacturing fake productivity when training is unavailable.

The first healthy post-recovery live decision selected ordinary `rest`, not a generic equipment inspection. This is directionally consistent with the intended guard; longer-run behavior should still be observed naturally before declaring a behavioral distribution.

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
- multi-fallback chains, provider circuit breakers and provider-health scoring;
- Telegram API-key editing and model-parameter tuning;
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

Runtime Cognition Fallback v1 and Telegram Observer Home Message Lifecycle v1 are deployed. Resume **natural read-only observation** of autonomous behavior.

The fallback is configuration-ready but should be saved/tested through Telegram only when the Creator intentionally chooses a fallback model. Do not intentionally induce a provider failure or model probe for monitoring; observe fallback use only if an ordinary primary provider/model call naturally fails.

Current production readback after Deploy #172: Gemini `gemini-3.1-flash-lite`, autonomy enabled/normal, speed `3.0x`, `autonomy_retry=null`, Telegram connected, decision calls `352`.

Do not build the full Character Memory Engine, multi-fallback chains/circuit breakers, forced equipment rotation, Speed progression, Telegram secret editing, model parameter tuning, or schema v5 without fresh Creator authorization.
