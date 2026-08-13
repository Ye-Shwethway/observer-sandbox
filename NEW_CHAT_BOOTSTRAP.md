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
- latest verified speed: `2.0x` at Deploy #161 readback; re-read whenever exact cadence matters
- cognition: Gemini `gemini-3.5-flash-lite`
- Telegram: connected

Latest deployment: **Deploy #161 `31734036894` SUCCESS** from main merge `7516f6c09a371803508f67a1575d6ce83a170de2`.

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

Pause for Creator discussion and observe autonomous choice breadth after the resource-awareness deployment.

First determine from actual post-deploy behavior whether Darian begins using more of the resources/methods he can now perceive. If the legal option breadth is visible but choices still collapse onto Free Weights/Heavy Bag, inspect real decision history before proposing a choice-policy or future Mind Engine layer.

Do not start Speed progression or forced equipment rotation without fresh Creator authorization.
