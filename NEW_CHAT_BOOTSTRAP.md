# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-14

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical contracts/source files
5. current live production evidence before implementation decisions

Current Creator instruction and newer repository/CI/deploy/live-runtime evidence override older chat memory.

## Development workflow

Default flow:

`test -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Keep only persistent `main` and reusable `test` branches unless an exceptional need is concrete. After merge/deploy, fast-forward `test` back to current `main` before the next slice.

Production-copy validation is optional. Use it when a stateful/migration risk needs production-shaped data; otherwise prefer focused regression + full CI. Never accelerate production or mutate live profile/world/progression merely to manufacture acceptance evidence.

Whenever a slice introduces a new architecture/control invariant, update its canonical contract plus `ROADMAP.md` and this bootstrap in the same development cycle.

## Current verified production baseline

Latest runtime-affecting deployment: **Deploy #173 `31783391862` SUCCESS**, PR #67 merge `2aca8df01f3307d130844f4bcdc7cbbc18b9d66c`.

Deploy #173 readback:
- service active / healthy;
- schema v4;
- world revision `thorne-estate-v3.2-training-environment`;
- default actor projection `char_darian`;
- autonomy enabled / normal, `paused=false`, `autonomy_retry=null`;
- speed **`1.0x`**;
- primary cognition Gemini `gemini-3.1-flash-lite`;
- normal Groq bootstrap preserved that explicit Creator-selected primary (`existing_binding_preserved`);
- fallback Groq `qwen/qwen3.6-27b`, configured/tested through Telegram;
- Telegram API connected; owner and allowed-user config present;
- cognition `decision_calls=356` at readback;
- Darian was sleeping in the Master Suite; Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

No model probe/provider failure/live-state mutation was induced for Deploy #173 acceptance.

## Universal Character Engine Contract

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.
Canonical contract: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

PR #67:
- tested head `d668823bb86a7b049fae10f8aab051ed80f11ae1`;
- primary CI #605 SUCCESS;
- merge `2aca8df01f3307d130844f4bcdc7cbbc18b9d66c`;
- post-merge CI #606 SUCCESS;
- Deploy #173 SUCCESS.

Invariant:
- Darian is exemplar content, not reusable engine identity;
- character config registry owns character-specific canonical/runtime/autonomy-policy files;
- actor selection is explicit actor -> valid configured `default_actor_id` -> sole actor;
- multi-character ambiguity fails closed;
- another actor cannot silently inherit Darian cognition policy;
- reusable runtime/autonomy/query/AI/simulation APIs do not rely on literal `char_darian` defaults;
- missing actor location is invalid state, not implicit Master Suite;
- global resume wakes all enabled idle actors;
- synthetic non-Darian regression guards identity leakage;
- no schema v5.

Named Darian/Thorne content and `/darian` convenience presentation remain valid exemplar surfaces.

## AI / Telegram control state

P2.3 Telegram Creator AI Control v1, Runtime Cognition Fallback v1 and Telegram Observer Home Message Lifecycle v1 are deployed.

Key invariants:
- catalog fetch does not mutate cognition binding;
- selected model requires explicit real `Test Model` before save;
- test failure/cancel/navigation do not mutate config;
- credential values never display;
- CI/deploy never performs a model probe;
- one eligible provider-layer failure may try one configured fallback;
- fallback never rewrites primary;
- deterministic action/target/duration/runtime validation never triggers fallback;
- both provider calls failing returns to ordinary autonomy retry/backoff;
- `/start` Home has manual Close plus bounded 5-minute default auto-delete lifecycle.

Do not deliberately fail Gemini or spend inference simply to prove fallback monitoring.

## Training / physiology state

Deployed:
- systemic fatigue/recovery;
- targeted training sessions;
- readiness/effectiveness/effective training load;
- minimum Strength stimulus;
- training-session load/recovery guard;
- causal needs and sleep-pressure/circadian behavior;
- Training Method Semantics v1;
- Dynamic Resource Awareness / Choice Breadth;
- Object Familiarity / Inspect Utility Guard.

Existing physical progression:
- Strength — deployed/live-cycle validated; Free Weights source;
- Stamina — deployed; treadmill, rowing ergometer, altitude chamber pure-conditioning sources;
- Agility — deployed; `speed_agility_drills` source.

## Physical Attribute Progression Framework v1 — CURRENT ACTIVE SLICE

Canonical contract: `docs/PHYSICAL_ATTRIBUTE_PROGRESSION_FRAMEWORK.md`.

The shared lifecycle reconciled from Strength/Stamina/Agility is:

`evidence scan -> consumed-event cursor -> recovery gate -> level/saturation gain -> detraining integration -> profile/history write -> settlement event`

Current `test` work implements one actor-generic policy-driven engine for:
- **Speed** -> `speed_agility_drills`;
- **Reflexes** -> `ai_combat_simulation`;
- **Endurance** -> `heavy_bag_rounds`, `obstacle_conditioning`, `combat_pit_drills`;
- **Flexibility** -> new `mobility_stretching` method from a Mobility & Stretching Area.

Important semantics:
- Stamina remains cardiovascular/work-capacity reserve; pure aerobic Stamina evidence is not Endurance evidence;
- Flexibility receives a real authored resource/method rather than fabricated credit from unrelated sessions;
- policy/config is `config/physical_attribute_progression.v1.json`;
- engine contains no Darian-specific score branch;
- first settlement is bootstrap-only: consume historical evidence without retroactive score gain;
- service activates the four-attribute batch only at completed-action boundaries;
- existing Strength/Stamina/Agility implementations remain intact in this slice;
- candidate world revision is `thorne-estate-v3.3-physical-attribute-training`;
- no schema v5 and no extra model calls.

The same slice corrects two validation harness defects discovered during PR #67:
- Minimum Training Stimulus Acceptance now stages candidate `config/` with `src/` so `training_methods.v1.json` exists;
- Strength Live Cycle compares a settlement delta to the score immediately before that exact settlement, not to the start of a loop that may contain earlier valid settlements.

## Exact resume point

Finish the current PA framework batch on `test`: focused regression -> full CI + relevant corrected acceptance checks -> merge -> deploy -> read-only production verification -> sync `test` to `main` -> finalize deployment evidence in canonical docs.

Do not force a live training session merely to prove progression. Natural completed actions will bootstrap the four new attributes first; later natural eligible training/recovery can provide live gain evidence.

After PA completion, proceed to **body composition progression exemplar**, then compatible body-measurement batch, skill exemplar/batch, intellectual attributes, and later mental/emotion dynamics.

Do not add full Character Memory, multi-fallback/circuit-breaker architecture, forced equipment rotation, Telegram secret editing/model tuning, a second production character merely for testing, or schema v5 as side effects.
