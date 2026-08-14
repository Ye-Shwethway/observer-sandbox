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
- latest verified speed: `1.0x`
- cognition: Groq `openai/gpt-oss-20b`
- Telegram: connected

Latest verified runtime-affecting deployment: **Deploy #171 `31769893556` SUCCESS** from PR #63 merge `d8a3f770dd3c6f4293f5035d1085998ba0562bf7`.

Deploy #171 readback verified service active/healthy, schema v4, autonomy enabled/normal, `autonomy_retry=null`, cognition binding still Groq `openai/gpt-oss-20b`, Telegram API connected, and owner configuration present. Natural cognition had reached `decision_calls=334` at sim time `2025-05-04T17:38:00+00:00`. Deployment did not invoke the new model probe.

PR #62 / Deploy #170 added the next planned action's cognition reason to proactive Telegram Character Updates, so the Observer sees both what is next and why it was selected.

## P2.3 Telegram Creator AI Control v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

Delivery evidence:
- PR #63 tested head `f2e61d374dce1c3b493d27fb94e1024b9eb5a3fd`;
- primary CI #595 / run `31769832103` SUCCESS;
- merge `d8a3f770dd3c6f4293f5035d1085998ba0562bf7`;
- Deploy #171 / run `31769893556` SUCCESS.

One unrelated Stamina Progression disposable-production-copy acceptance run failed on an existing eligible-event assertion against the evolving copied production state. This slice did not touch Stamina/progression semantics; the primary full CI passed, Strength acceptance passed, and production-copy validation is non-mandatory for this non-state-sensitive control slice under current project policy.

Creator surface:
- `/start` -> `⚙️ Creator Settings` -> `🧠 AI Cognition`, with `/settings` and `/ai` as direct entry commands;
- current cognition provider/model display;
- provider list with credential presence/absence only;
- live provider model catalog fetch and cached pagination;
- server-side candidate selection so long/arbitrary model ids are not placed in Telegram callback payloads;
- one deliberately tiny real `Test Model` inference through the actual runtime adapter and structured cognition-response contract;
- friendly auth/permission, model availability, request-limit, quota/rate and timeout diagnostics;
- `Save & Activate` available/accepted only after a successful candidate probe.

Canonical test-before-save invariant:
- provider browsing, catalog refresh, candidate selection, failed probe, cancellation, and ordinary navigation do **not** change the current cognition binding;
- catalog success alone is not model-health proof because it cannot prove current inference quota/rate availability;
- only explicit `Save & Activate` enables the selected provider and writes the character cognition binding;
- probe execution never mutates world/profile/progression state or the current binding;
- a passing probe proves only that one minimal inference worked at that moment, not that future quota will remain available;
- API credential values are never displayed;
- CI/deploy readback must not trigger the real probe because it consumes provider inference quota.

Implementation surfaces:
- `src/observer_sandbox/ai_control.py`
- `src/observer_sandbox/telegram_ai_control.py`
- `src/observer_sandbox/telegram_creator_bot.py`
- `src/observer_sandbox/service.py`
- `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`
- `tests/test_telegram_ai_control_v1.py`

Explicit non-goals remain: automatic runtime provider failover, fallback-chain editing, Telegram API-key editing, model parameter tuning, schema v5, or world/profile/progression changes.

## Cognition resilience / Groq free-tier recovery

Status: **COMPLETE / CI VERIFIED / DEPLOYED / LIVE VERIFIED**.

The long idle stall was not one single provider-quota issue. The investigation found and corrected three bounded failure surfaces:

1. **Training-duration contradiction** — a runtime-shaped legal training duration could be narrower than the ordinary authored preferred duration, while later normalization could expand the model proposal back outside the remaining training-load budget and trigger repeated `ValueError` failures.
2. **Groq OpenAI-compatible bootstrap compatibility** — the first Groq deploy attempt reached `GET /openai/v1/models` but returned HTTP 403. Standard OpenAI-compatible request headers and better HTTP diagnostics were added, after which catalog fetch succeeded.
3. **Groq free-tier TPM pressure** — live cognition then reached Groq but returned HTTP 413 because the request was `8645` tokens against the account/model TPM limit of `8000`. The prompt contained duplicated derived metadata. Cognition context is now compacted without weakening authoritative action options or deterministic validation.

Relevant delivery chain:
- PR #55 — cognition duration-stall correction + generic OpenAI-compatible live decision adapter + Groq provider/bootstrap; CI #579 succeeded; merge `fb0e045686b129e5ecadb13e1f55c8fffb60e82f`.
- Deploy #166 — failed during first Groq catalog bootstrap; production service was not treated as a cognition acceptance.
- PR #56 — Groq catalog request hardening and deploy-resilient provider bootstrap; CI #581 succeeded; merge `33f79327e97790f3e3fca4c0317ef87da0eae8db`; Deploy #167 succeeded and bound Groq `openai/gpt-oss-20b`.
- PR #57 — live provider HTTP error detail preservation; CI #583 succeeded; merge `cfcd9f03fe660e8438bb2a74e2adac2b041a77f2`; Deploy #168 succeeded.
- PR #58/#59 — read-only latest autonomy-error observability and workflow syntax correction; final Runtime Read workflow is healthy and does not induce model traffic.
- PR #60 — semantic-preserving cognition prompt compaction for the 8000 TPM free-tier budget; CI #589 succeeded; merge `b813913ced1d51733e873b89dca2b04907dad353`; post-merge CI #590 and Deploy #169 succeeded.

Runtime action/target authority remains strict. Training-load validation remains deterministic. Provider HTTP failures remain `AIDecisionError`; deterministic invalid decisions are not disguised as provider fallback events.

## Environment and training methods

Thorne Estate interior training environment v3.2 is deployed. Training Hall and Top-Class Home Gym expose the richer bounded equipment surface; exterior/Tahoe traversal remains deferred.

Training Method Semantics v1 is deployed. `config/training_methods.v1.json` provides authored method/family/workload-channel metadata plus descriptive planning metadata. The canonical evidence revision remains `training-method-semantics-v1`, preserving Strength/Stamina/Agility evidence contracts.

## Dynamic Resource Awareness & Choice Breadth v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #50 merged as `7516f6c09a371803508f67a1575d6ce83a170de2`; CI #557 succeeded; Deploy #161 succeeded.

Cognition receives the full legal current-room resource/action set, one-hop reachable-location previews, strict move-first semantics for distant resources, and recent action-target usage metadata for sensible variety. No forced rotation or resource-scoring Mind Engine was added.

## Training Session Load & Recovery Guard v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #53 tested head `4c8d8f3caa3814f2def3c168e76b9d426bf37416`; CI #570 / run `31739634403` succeeded; merge `701599074e9e9824384e624f11c288feb07d0924`; Deploy #164 / run `31739837957` succeeded.

The guard derives recent training dose from completed action history and persisted effective-training-load evidence. Current v1 budgets are:
- current session: `90` effective minutes;
- session reset after more than `120` simulated minutes without training;
- rolling 6 hours: `120` effective minutes;
- rolling 24 hours: `180` effective minutes.

Train options are capped/removed based on remaining effective-load budget, and the selected duration is checked again before scheduling. Runtime-shaped duration bounds are now also authoritative during model planning/normalization, preventing the previously observed retry stall. No new schema field, injury model, or Mind Engine was introduced.

## Object Familiarity / Inspect Utility Guard v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #54 final tested head `674de824acf69fc4209e59e649364d0ece3696f5`; CI #575 / run `31765655658` succeeded; merge `d6742fcbaa06868ca7dbd58bac33ee09430d1a0d`; Deploy #165 / run `31765700369` succeeded. Post-merge CI #576 also succeeded.

This is a bounded bridge, not a full Character Memory Engine. Cognition derives inspection familiarity from existing world capabilities plus event history:
- established functional estate resources are treated as familiar and low-value routine `inspect` options are suppressed;
- genuinely unknown inspect-only objects may still receive a first-look inspection opportunity;
- prior interaction/history can establish familiarity without adding a new memory schema;
- the autonomy policy no longer advertises generic equipment checks as default midday productivity;
- guidance explicitly prefers meaningful non-training activity or ordinary downtime over manufacturing fake productive inspection loops when training is unavailable.

The first healthy post-recovery live decision selected ordinary `rest`, not a generic equipment inspection, which is directionally consistent with the intended guard. Continue observing naturally before claiming a long-run behavioral distribution.

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
- Do not silently fall back from deterministic validation failures by changing providers.
- Do not trigger a real AI probe for CI/deployment acceptance; probe execution is an explicit Creator action because it consumes provider inference quota.

## Exact resume point

P2.3 Telegram Creator AI Control v1 is deployed. Resume **natural read-only observation** of autonomous behavior.

Use the new `Creator Settings -> AI Cognition` flow only when the Creator intentionally wants to browse/fetch models, test a selected model, or activate a different cognition provider/model. Do not invoke `Test Model` merely as monitoring.

Do not build the full Character Memory Engine, automatic provider failover, forced equipment rotation, Speed progression, Telegram secret editing, model parameter tuning, or schema v5 without fresh Creator authorization.
