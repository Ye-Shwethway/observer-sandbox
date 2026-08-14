# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
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

Latest verified runtime-affecting deployment remains **Deploy #172 `31779629810` SUCCESS** from PR #65 merge `20c01b82a1ebacbd05d5a12cdccef009c7284981` until the current universalization slice is merged and deployed.

Deploy #172 readback verified service active/healthy, schema v4, autonomy enabled/normal, `autonomy_retry=null`, Creator-selected Gemini `gemini-3.1-flash-lite` preserved across the Groq bootstrap entry point (`changed=false`, `existing_binding_preserved`), Telegram API connected, and owner configuration present. Natural cognition had reached `decision_calls=352` at sim time `2025-05-04T21:32:00+00:00`; Darian was showering in the Master Bathroom. Deployment did not invoke a real model probe or intentionally induce provider failure. Post-merge CI #602 / run `31779629861` also succeeded.

Creator subsequently selected **Groq Qwen 3.6 27B** as the single fallback model through Telegram and reported the required real `Test Model` probe green. Treat that as proof the candidate worked at selection time only. Do not deliberately fail Gemini or consume a probe merely to force fallback acceptance; wait for natural provider-layer failure if runtime fallback evidence is needed.

## Universal Character Engine Contract — CURRENT ACTIVE SLICE

Canonical contract: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

Creator clarified that Darian is an exemplar because his detailed canonical facts already exist; universe rules and engines must remain universally reusable rather than fixed around Darian.

Current `test` implementation is hardening this boundary before further profile simulation unlocks:
- `config/characters/registry.json` resolves Darian's canonical/runtime-default/autonomy-policy files as character content rather than engine identity;
- `actor_selection.py` resolves explicit actor -> configured valid `default_actor_id` -> sole actor only; multiple actors without a valid default fail closed;
- legacy actor-runtime migration requires an explicitly resolved actor;
- autonomy, runtime status, CLI, AI bootstrap/control/fallback, simulation and observer-query paths no longer rely on a literal `char_darian` default for reusable behavior;
- character cognition resolves that character's own registered policy; an unregistered synthetic actor must fail rather than inherit Darian's autonomy policy;
- missing character location is an explicit invalid runtime state rather than silently becoming the Thorne Estate Master Suite;
- movement uses generic dynamic-location semantics;
- global resume wakes every enabled idle actor at a real decision boundary rather than only a selected exemplar;
- Darian canonical/config files, Thorne Estate content and clearly named convenience aliases such as `/darian` remain valid exemplar/presentation content;
- no schema v5.

Regression coverage includes a synthetic non-Darian actor specifically to catch character-identity leakage before a second production character is introduced.

**State at this checkpoint:** implementation/docs are on `test`, but CI/merge/deploy evidence has not yet been established. Do not describe this slice as deployed until those gates pass.

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

Status: **COMPLETE / CI VERIFIED / DEPLOYED / CREATOR-CONFIGURED**.

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

## Progression state and next authorized expansion

Current active/deployed progression:
- Strength — live-cycle validated; Free Weights deliberate source.
- Stamina — pure-conditioning sources: treadmill, rowing ergometer, altitude chamber.
- Agility — `speed_agility_drills` from Speed & Agility Station.

After Universal Character Engine hardening is green/deployed, continue immediately with **Physical Attribute Progression Framework v1** for:
- Speed
- Reflexes
- Endurance
- Flexibility

Do not create four independent character-specific engines. Reconcile the shared Strength/Stamina/Agility lifecycle into an actor-generic/policy-driven progression contract, while preserving attribute-specific evidence and physiology where needed. Current Darian values are exemplar inputs only.

Important semantic separation: Stamina is cardiovascular/work-capacity reserve; Endurance must measure sustained performance under accumulated workload/fatigue rather than duplicate Stamina. If Flexibility lacks valid current evidence, add the smallest reusable mobility/stretching method rather than fabricating progression from unrelated training.

After PA completion, planned profile-unlock sequence is body composition exemplar -> measurement batch -> skill exemplar/batch -> intellectual attribute exemplar/batch -> mental/emotion dynamics.

## Core safety boundaries that remain

- Do not intentionally accelerate production for testing.
- Do not directly edit live profile/progression/world state as a test fixture.
- Keep LLM cognition proposal-only; deterministic engines own mutations.
- Creator controls remain typed/audited and follow `docs/CREATOR_CONTROL_POLICY.md`.
- Post-deploy verification is read-only unless a concrete live control change is explicitly requested.
- Never trigger provider fallback from deterministic validation failure.
- Do not trigger a real AI probe for CI/deployment acceptance; it consumes provider inference quota.
- Do not add a second production character merely to validate universalization; use synthetic disposable test fixtures until single-character profile expansion is substantially further along.

## Exact resume point

Finish the current **Universal Character Engine Contract** hardening on `test`: focused regression/full CI -> merge -> standard deploy -> read-only production verification. Until that evidence exists, production remains at Deploy #172.

Then continue autonomously with **Physical Attribute Progression Framework v1** and the Speed/Reflexes/Endurance/Flexibility batch under the exemplar-first-then-batch policy.

Do not build the full Character Memory Engine, multi-fallback chains/circuit breakers, forced equipment rotation, Telegram secret editing, model parameter tuning, a second production character, or schema v5 as side effects.
