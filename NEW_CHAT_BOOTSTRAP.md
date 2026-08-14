# Observer Sandbox — New Chat Bootstrap

Status: **READY**
Last synchronized: 2026-08-14

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts. Current Creator instruction and newer repository/runtime evidence override older chat memory.

## Development workflow

Default flow is intentionally minimal:

`test -> focused tests + CI -> merge to main -> automatic deploy when runtime-affecting -> read-only production check`

Keep only persistent `main` and reusable `test` branches unless a concrete exceptional need requires otherwise. After merge/deploy, fast-forward `test` back to current `main` before the next slice.

Production-copy validation is optional, not mandatory. Use it only for genuinely state-sensitive, migration-heavy, or otherwise high-risk changes that local tests/CI cannot cover well enough. Prefer small reversible changes and Git rollback over layered release ceremony.

When a slice introduces a new architecture/control invariant, update the task-relevant canonical contract plus `ROADMAP.md` and this bootstrap checkpoint during the same development cycle.

## Production baseline

- repo: `Ye-Shwethway/observer-sandbox`
- VPS: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- service: `observer-sandbox`
- schema: v4
- world revision: `thorne-estate-v3.2-training-environment`
- autonomy: enabled / normal
- latest verified speed: `3.0x`
- cognition: Gemini `gemini-3.1-flash-lite`
- Telegram: connected

Latest verified runtime-affecting deployment: **Deploy #172 `31779629810` SUCCESS** from PR #65 merge `20c01b82a1ebacbd05d5a12cdccef009c7284981`.

Deploy #172 readback verified service active/healthy, schema v4, autonomy enabled/normal, `autonomy_retry=null`, Creator-selected Gemini `gemini-3.1-flash-lite` preserved across the Groq bootstrap entry point (`changed=false`, `existing_binding_preserved`), Telegram API connected, and owner configuration present. Natural cognition had reached `decision_calls=352` at sim time `2025-05-04T21:32:00+00:00`; Darian was showering in the Master Bathroom. Deployment did not invoke a real model probe or intentionally induce provider failure. Post-merge CI #602 / run `31779629861` also succeeded.

PR #62 / Deploy #170 added the next planned action's cognition reason to proactive Telegram Character Updates.

## P2.3 Telegram Creator AI Control v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED / CREATOR-EXERCISED**.

Delivery evidence:
- PR #63 tested head `f2e61d374dce1c3b493d27fb94e1024b9eb5a3fd`;
- primary CI #595 / run `31769832103` SUCCESS;
- merge `d8a3f770dd3c6f4293f5035d1085998ba0562bf7`;
- Deploy #171 / run `31769893556` SUCCESS;
- Creator later reported a successful real Gemini probe and successful activation back to Gemini through Telegram;
- Deploy #172 independently verified the selected Gemini binding and that normal deployment now preserves it.

Creator surface:
- `/start` -> `⚙️ Creator Settings` -> AI cognition controls, with `/settings` and `/ai` direct entries;
- current primary and fallback provider/model display;
- provider list with credential presence/absence only;
- live catalog fetch and cached pagination;
- server-side candidate selection;
- real `Test Model` inference through the runtime adapter and structured response contract;
- friendly auth/model/quota/rate/timeout diagnostics;
- save only after a successful probe.

Canonical test-before-save invariant:
- browsing, catalog refresh, selection, failed probe, cancellation and navigation do not mutate cognition configuration;
- catalog success alone is not inference-health proof;
- only explicit Creator save changes a primary/fallback selection;
- API credential values are never displayed;
- CI/deploy readback must not trigger real model probes.

## Runtime Cognition Fallback v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

Canonical contract: `docs/AI_RUNTIME_FALLBACK.md`.

Delivery evidence:
- PR #65 final tested head `ddfcd757fb94d270a5b20db1bd1601d92b050903`;
- primary CI #601 / run `31779586802` SUCCESS;
- merge `20c01b82a1ebacbd05d5a12cdccef009c7284981`;
- Deploy #172 / run `31779629810` SUCCESS;
- post-merge CI #602 / run `31779629861` SUCCESS.

Current v1 invariant:
- one primary cognition binding plus at most one tested fallback provider/model;
- fallback is configured through Telegram with the same fetch/select/Test Model/save safety pattern;
- a provider/model invocation failure may trigger one fallback attempt;
- primary binding remains unchanged when fallback is used;
- deterministic action/target/duration/runtime validation failures never trigger fallback;
- if primary and fallback both fail, existing autonomy retry/backoff handles the combined provider failure;
- successful fallback usage records bounded runtime observability metadata;
- normal deployment/bootstrap preserves any existing explicit Creator-selected primary binding; `force=True` is reserved for explicit administrative migration;
- no schema v5.

Explicitly deferred: multi-fallback chains, circuit breakers, health scoring, permanent automatic rebinding, Telegram API-key editing and model-parameter tuning.

## Telegram Observer Home Message Lifecycle v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

Canonical contract: `docs/TELEGRAM_HOME_LIFECYCLE.md`.

Current behavior:
- `/start` Home board includes `✕ Close`;
- Close deletes the Home message through Telegram `deleteMessage`;
- newly sent `/start` boards auto-delete after 5 minutes by default;
- `OBSERVER_TELEGRAM_HOME_TTL_SECONDS` may override the TTL, bounded to 30..3600 seconds;
- Home TTL is active only while that message is displaying Observer Home; navigating away cancels the timer and returning Home re-arms it;
- lifecycle cleanup is Telegram presentation state only and cannot mutate simulation/autonomy;
- timer state is intentionally in-process; service restart may forget outstanding timers, while manual Close remains available.

## Cognition resilience / Groq free-tier recovery

Status: **COMPLETE / CI VERIFIED / DEPLOYED / LIVE VERIFIED**.

The long idle stall had multiple bounded causes:

1. **Training-duration contradiction** — runtime-shaped legal training duration could be narrower than ordinary authored preferred duration, while normalization could expand a proposal back outside remaining load budget and trigger repeated `ValueError` failures.
2. **Groq bootstrap compatibility** — initial model catalog request returned HTTP 403 until OpenAI-compatible request headers/diagnostics were hardened.
3. **Groq free-tier TPM pressure** — live cognition then returned HTTP 413 because request size exceeded the model/account TPM budget; duplicated derived prompt metadata was compacted without weakening deterministic authority.

Relevant delivery chain:
- PR #55 — duration correction + generic OpenAI-compatible runtime + Groq provider/bootstrap; CI #579; merge `fb0e045686b129e5ecadb13e1f55c8fffb60e82f`.
- PR #56 — Groq catalog hardening/deploy resilience; CI #581; merge `33f79327e97790f3e3fca4c0317ef87da0eae8db`; Deploy #167.
- PR #57 — provider HTTP error detail preservation; CI #583; merge `cfcd9f03fe660e8438bb2a74e2adac2b041a77f2`; Deploy #168.
- PR #58/#59 — read-only autonomy error observability/workflow correction.
- PR #60 — prompt compaction for free-tier budget; CI #589; merge `b813913ced1d51733e873b89dca2b04907dad353`; Deploy #169.

Runtime action/target authority remains strict. Training-load validation remains deterministic. Provider fallback must never disguise deterministic invalid decisions.

## Environment and training methods

Thorne Estate interior training environment v3.2 is deployed. Training Hall and Top-Class Home Gym expose the richer bounded equipment surface; exterior/Tahoe traversal remains deferred.

Training Method Semantics v1 is deployed. `config/training_methods.v1.json` provides authored method/family/workload-channel metadata plus descriptive planning metadata. The canonical evidence revision remains `training-method-semantics-v1`.

## Dynamic Resource Awareness & Choice Breadth v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #50 merged as `7516f6c09a371803508f67a1575d6ce83a170de2`; CI #557 succeeded; Deploy #161 succeeded.

Cognition receives the full legal current-room resource/action set, one-hop reachable-location previews, strict move-first semantics for distant resources, and recent action-target usage metadata for sensible variety. No forced rotation or resource-scoring Mind Engine was added.

## Training Session Load & Recovery Guard v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #53 tested head `4c8d8f3caa3814f2def3c168e76b9d426bf37416`; CI #570 / run `31739634403` succeeded; merge `701599074e9e9824384e624f11c288feb07d0924`; Deploy #164 / run `31739837957` succeeded.

Current v1 budgets:
- current session: `90` effective minutes;
- session reset after more than `120` simulated minutes without training;
- rolling 6 hours: `120` effective minutes;
- rolling 24 hours: `180` effective minutes.

Train options are capped/removed based on remaining effective-load budget and the selected duration is checked again before scheduling. No new schema field, injury model, or Mind Engine was introduced.

## Object Familiarity / Inspect Utility Guard v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #54 final tested head `674de824acf69fc4209e59e649364d0ece3696f5`; CI #575 succeeded; merge `d6742fcbaa06868ca7dbd58bac33ee09430d1a0d`; Deploy #165 succeeded.

This is a bounded bridge, not a full Character Memory Engine. Established functional estate resources suppress low-value routine inspect fallback while genuinely unknown inspect-only objects may still receive a first-look opportunity.

## Progression state

- Strength: active/deployed/live-cycle validated; Free Weights remains the deliberate Strength source.
- Stamina: active/deployed; pure-conditioning sources are treadmill, rowing ergometer, and altitude chamber.
- Agility: active/deployed; `speed_agility_drills` from the Speed & Agility Station is the authored evidence surface.

## Core safety boundaries that remain

- Do not intentionally accelerate production for testing.
- Do not directly edit live profile/progression/world state as a test fixture.
- Keep LLM cognition proposal-only; deterministic engines own mutations.
- Creator controls remain typed/audited and follow `docs/CREATOR_CONTROL_POLICY.md`.
- Post-deploy verification is read-only unless a concrete live control change is explicitly requested.
- Never trigger provider fallback from deterministic validation failure.
- Do not trigger a real AI probe for CI/deployment acceptance; it consumes provider inference quota.

## Exact resume point

Runtime Cognition Fallback v1 and Telegram Observer Home Message Lifecycle v1 are deployed. Resume **natural read-only observation** of autonomous behavior.

The fallback is configuration-ready but should be selected/tested/saved through Telegram only when the Creator intentionally chooses a fallback model. Do not intentionally induce a provider failure or real model probe merely for monitoring. Observe fallback behavior naturally if the primary provider/model later fails.

Current production readback after Deploy #172: Gemini `gemini-3.1-flash-lite`, autonomy enabled/normal, speed `3.0x`, `autonomy_retry=null`, Telegram connected, decision calls `352`.

Do not build the full Character Memory Engine, multi-fallback chains/circuit breakers, forced equipment rotation, Speed progression, Telegram secret editing, model parameter tuning, or schema v5 without fresh Creator authorization.
