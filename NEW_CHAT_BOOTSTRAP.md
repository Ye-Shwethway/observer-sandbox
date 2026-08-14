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
- latest verified speed: `1.0x` at Deploy #165 readback; re-read whenever exact cadence matters
- cognition: Gemini `gemini-3.5-flash-lite`
- Telegram: connected

Latest deployment: **Deploy #165 `31765700369` SUCCESS** from PR #54 merge `d6742fcbaa06868ca7dbd58bac33ee09430d1a0d`.

Deploy #165 readback verified service active/healthy, schema v4, autonomy enabled/normal, Gemini binding preserved, Telegram connected, and Darian at `2025-05-04T17:18:00+00:00` in the Training Hall, idle, with fatigue `34.935`.

The readback also preserved a pre-deploy autonomy retry record (`failures=8`, `last_error=ValueError`, no pending action). Treat that as an observation item rather than evidence of a failed deployment. If it persists across fresh post-deploy decision boundaries, inspect the decision error separately.

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

Train options are capped/removed based on remaining effective-load budget, and the selected duration is checked again before scheduling. Short-term fatigue recovery therefore does not erase recent training dose. No new schema field, injury model, or Mind Engine was introduced.

## Object Familiarity / Inspect Utility Guard v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #54 final tested head `674de824acf69fc4209e59e649364d0ece3696f5`; CI #575 / run `31765655658` succeeded; merge `d6742fcbaa06868ca7dbd58bac33ee09430d1a0d`; Deploy #165 / run `31765700369` succeeded. Post-merge CI #576 also succeeded.

This is a bounded bridge, not a full Character Memory Engine. Cognition now derives inspection familiarity from existing world capabilities plus event history:
- established functional estate resources are treated as familiar and low-value routine `inspect` options are suppressed;
- genuinely unknown inspect-only objects may still receive a first-look inspection opportunity;
- prior interaction/history can establish familiarity without adding a new memory schema;
- the autonomy policy no longer advertises generic equipment checks as default midday productivity;
- guidance explicitly prefers meaningful non-training activity or ordinary downtime over manufacturing fake productive inspection loops when training is unavailable.

Focused tests cover the observed room-hopping fallback pattern while preserving first-look inspection for an unknown inspect-only object.

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

## Exact resume point

Observe autonomous behavior after **Object Familiarity / Inspect Utility Guard v1**.

Verify naturally that training-load blocking no longer causes Darian to roam through familiar estate resources performing generic equipment inspections. Familiar stable equipment should normally disappear as low-value `inspect` choices, while genuinely novel/unknown inspect-only objects remain discoverable.

Also watch whether the pre-deploy `ValueError` retry record clears on fresh autonomous decisions. Investigate it only if it persists or causes observable stalls.

Do not build the full Character Memory Engine, forced equipment rotation, or Speed progression without fresh Creator authorization.
