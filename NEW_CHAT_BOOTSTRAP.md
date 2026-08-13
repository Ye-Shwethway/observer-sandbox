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
- latest verified speed: `1.0x` at Deploy #164 readback; re-read whenever exact cadence matters
- cognition: Gemini `gemini-3.5-flash-lite`
- Telegram: connected

Latest deployment: **Deploy #164 `31739837957` SUCCESS** from PR #53 merge `701599074e9e9824384e624f11c288feb07d0924`.

Deploy #164 readback verified service active/healthy, schema v4, autonomy enabled/normal, Gemini binding preserved, Telegram connected, and Darian at `2025-05-04T15:26:00+00:00` in the Living Room reading with fatigue `38.235`.

## Environment and training methods

Thorne Estate interior training environment v3.2 is deployed. Training Hall and Top-Class Home Gym expose the richer bounded equipment surface; exterior/Tahoe traversal remains deferred.

Training Method Semantics v1 is deployed. `config/training_methods.v1.json` provides authored method/family/workload-channel metadata plus descriptive planning metadata. The canonical evidence revision remains `training-method-semantics-v1`, preserving Strength/Stamina/Agility evidence contracts.

## Dynamic Resource Awareness & Choice Breadth v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #50 merged as `7516f6c09a371803508f67a1575d6ce83a170de2`; CI #557 succeeded; Deploy #161 succeeded.

Cognition now receives:
- the full legal current-room action/resource option set produced by generic capability matching;
- one-hop reachable-location resource/action/training-method previews for movement planning;
- strict move-first semantics for distant resources;
- recent action-target usage metadata as context (`recent_uses`, last simulated use, repeated flag), never as a hard repetition ban;
- resource-aware guidance to consider sensible variety when equivalent choices exist.

Focused tests prove all 10 Home Gym training resources are exposed to cognition, connected-room resources are visible for planning without becoming directly actionable, and repeated Free Weights use remains legal while being marked as recently repeated.

No Mind Engine, resource scoring system, forced rotation, schema change, or progression formula change was added.

## Training Session Load & Recovery Guard v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #53 tested head `4c8d8f3caa3814f2def3c168e76b9d426bf37416`; CI #570 / run `31739634403` succeeded; merge `701599074e9e9824384e624f11c288feb07d0924`; Deploy #164 / run `31739837957` succeeded.

The guard derives recent training dose from completed `action_instances` and persisted effective-training-load evidence. It adds no new canonical physiology field and no schema change.

Current v1 budgets:
- current session: `90` effective minutes;
- a session resets after more than `120` simulated minutes without training;
- rolling 6 hours: `120` effective minutes;
- rolling 24 hours: `180` effective minutes.

Cognition receives a `training_load_guard` view. Train options are capped to the remaining effective-load budget or removed when even the minimum legal train duration cannot fit. A chosen training duration is checked again against the same budget before becoming an autonomous action.

Short-term fatigue recovery therefore no longer erases recent training dose. This is a deterministic behavior guard, not a Mind Engine or long-horizon workout planner.

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

Observe autonomous behavior with the deployed **Training Session Load & Recovery Guard v1**.

Verify from natural production behavior that Darian stops or shifts to recovery/non-training activity when his effective session/recent-load budget is exhausted, and that a temporary fall in systemic fatigue does not immediately reopen an excessive training burst.

Do not add a Mind Engine, forced equipment rotation, or Speed progression without fresh Creator authorization.
