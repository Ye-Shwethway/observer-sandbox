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

## Production baseline

- repo: `Ye-Shwethway/observer-sandbox`
- VPS: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- service: `observer-sandbox`
- schema: v4
- world revision: `thorne-estate-v3.2-training-environment`
- autonomy: enabled / normal
- latest verified speed: `1.0x` at Deploy #169 readback
- cognition: Groq `openai/gpt-oss-20b`
- Telegram: connected

Latest runtime-affecting deployment: **Deploy #169 `31767701373` SUCCESS** from PR #60 merge `b813913ced1d51733e873b89dca2b04907dad353`.

Post-Deploy169 natural runtime acceptance verified service active/healthy, schema v4, autonomy enabled/normal, Groq credential/binding active, and the stalled retry state cleared on a fresh autonomous decision. Cognition `decision_calls` advanced `331 -> 332`, `autonomy_retry` became `null`, and Darian naturally scheduled a 10-minute `rest` action in the Training Hall with reason `Brief rest to restore energy and reduce fatigue before winding down.` No simulation acceleration or direct live state mutation was used.

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

## Exact resume point

Continue **natural read-only observation** of autonomous behavior after the cognition-recovery/Groq migration.

Verify over ordinary decisions that:
- the old retry-cap stall does not recur;
- Groq remains healthy under normal free-tier request limits;
- Object Familiarity continues to prevent familiar-equipment inspect-room-hopping when training is unavailable;
- Darian naturally uses meaningful non-training activity or downtime where appropriate.

Do not build the full Character Memory Engine, forced equipment rotation, Speed progression, or schema v5 without fresh Creator authorization.
