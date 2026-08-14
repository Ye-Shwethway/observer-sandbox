# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-14

## Operating principles

- Python/SQLite runtime and world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutations.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Preserve the composable runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian is the first richly specified exemplar, not the identity embedded in reusable universe engines.
- Character-specific profile/policy/world content is data; reusable simulation/cognition/progression/query/control logic must be actor/entity-id driven.
- Schema v4 remains the current foundation; do not introduce schema v5 without a concrete missing invariant.
- Prefer minimum-runnable, reversible slices.
- Use exemplar-first only for genuinely new invariants; batch structurally equivalent follow-ons.
- Default development flow:
  `test -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Keep only persistent `main` and reusable `test` branches unless a concrete exceptional need requires otherwise.
- Production-copy validation is optional and reserved for genuinely state-sensitive/migration-heavy work.
- New architecture/control surfaces must update their canonical contract plus this roadmap/bootstrap checkpoint in the same development cycle.

## Current verified production baseline

Latest runtime-affecting deployment: **Deploy #173 `31783391862` SUCCESS** from PR #67 merge `2aca8df01f3307d130844f4bcdc7cbbc18b9d66c`.

Deploy #173 readback verified:
- service active / healthy;
- schema v4;
- world revision `thorne-estate-v3.2-training-environment`;
- configured/default actor projection `char_darian`;
- autonomy enabled / normal, `paused=false`, `autonomy_retry=null`;
- speed **`1.0x`**;
- cognition primary Gemini `gemini-3.1-flash-lite`, preserved through normal deploy bootstrap;
- configured fallback Groq `qwen/qwen3.6-27b`, tested at `2026-08-14T07:27:42.290743+00:00`;
- Telegram API connected with owner/allowed-user configuration present;
- cognition `decision_calls=356` at the readback boundary;
- Darian was sleeping in the Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55 and Cleanliness 99.466.

No production acceleration, direct live profile/progression mutation, validation-induced model probe or intentionally induced provider failure was used for Deploy #173 acceptance.

## Completed foundation and observer/control layers

- Foundation schema v4 — COMPLETE.
- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 dynamic AI provider layer — COMPLETE; Gemini, Groq and generic OpenAI-compatible runtime support are deployed, with OpenAI/OpenRouter/NanoGPT provider surfaces retained.
- P1 Living Darian Minimum — CONTINUOUS AUTONOMY LIVE.
- P2 Telegram Observer MVP / browse / profile-control surfaces — COMPLETE / LIVE VERIFIED.
- Runtime speed control, action ETA, autonomy timing/observability, research/monitor semantics — DEPLOYED.
- Telegram proactive next-action cognition reason — DEPLOYED via PR #62 / Deploy #170.
- P2.3 Telegram Creator AI Control v1 — COMPLETE / CI VERIFIED / DEPLOYED / CREATOR-EXERCISED.
- Runtime Cognition Fallback v1 — COMPLETE / CI VERIFIED / DEPLOYED / CREATOR-CONFIGURED.
- Telegram Observer Home Message Lifecycle v1 — COMPLETE / CI VERIFIED / DEPLOYED.

### AI control/fallback invariant

Canonical contracts: `docs/AI_RUNTIME_FALLBACK.md`, `docs/TELEGRAM_HOME_LIFECYCLE.md`, `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.

- Provider catalogs can be fetched without changing bindings.
- A selected provider/model must pass one explicit real `Test Model` structured inference before save.
- Browse/refresh/select/test-failure/cancel do not mutate active configuration.
- Credential values are never displayed.
- Normal deploy/bootstrap preserves every existing explicit Creator-selected primary binding.
- One provider/model invocation failure may use the configured single fallback once.
- Fallback use never permanently rewrites primary cognition.
- Deterministic action/target/duration/runtime validation failure never triggers provider fallback.
- If primary and fallback both fail, existing autonomy retry/backoff remains authoritative.
- CI/deploy acceptance does not consume a model probe.

Explicitly deferred: multi-fallback chains, circuit breakers, provider-health scoring, automatic permanent rebinding, Telegram secret editing and model-parameter tuning.

## Universal Character Engine Contract

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

Canonical contract: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

Delivery:
- PR #67 tested head `d668823bb86a7b049fae10f8aab051ed80f11ae1`;
- primary CI #605 SUCCESS;
- merge `2aca8df01f3307d130844f4bcdc7cbbc18b9d66c`;
- post-merge CI #606 SUCCESS;
- Deploy #173 `31783391862` SUCCESS and live readback verified the default-actor projection and existing single-character behavior.

Current invariant:
- `config/characters/registry.json` resolves character-specific canonical/runtime-policy files as content, not engine identity;
- reusable actor selection is explicit actor -> configured valid `default_actor_id` -> sole existing character;
- ambiguous multi-character implicit selection fails closed;
- cognition loads the selected character's registered policy; another actor cannot silently inherit Darian's policy;
- reusable runtime/control/query/AI/simulation paths do not require a literal `char_darian` default;
- missing character location is invalid runtime state rather than an implicit Thorne Estate Master Suite;
- movement uses generic dynamic-location semantics;
- universe resume wakes every enabled idle actor at a decision boundary;
- synthetic non-Darian regression coverage catches identity leakage;
- Darian profile/config, Thorne Estate content and clearly named presentation aliases such as `/darian` remain valid exemplar content;
- no schema v5.

## Training and physiology foundation

- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE VERIFIED.
- P3.2 Targeted Training Session — COMPLETE.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED.
- P3.4 Training Effectiveness Outcome — COMPLETE / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / DEPLOYED.
- Minimum Training Stimulus v1 — COMPLETE / DEPLOYED.
- Training Session Load & Recovery Guard v1 — COMPLETE / CI VERIFIED / DEPLOYED.
- Causal hunger, thirst, energy, sleepiness, cleanliness and fatigue resolution — DEPLOYED.
- Sleep Pressure & Circadian Need v1 — COMPLETE / DEPLOYED.

Training Load Guard v1 budgets remain:
- current session: 90 effective minutes;
- session break: >120 simulated minutes without training;
- rolling 6 hours: 120 effective minutes;
- rolling 24 hours: 180 effective minutes.

Short fatigue recovery does not erase recent training dose. The model sees the derived remaining budget; deterministic validation remains final authority.

## Training environment and method semantics

Current production world: `thorne-estate-v3.2-training-environment`.

Training Hall and Top-Class Home Gym provide the bounded authored training-resource surface. Exterior estate grounds/private lake/outdoor tactical course/Tahoe traversal remain deferred.

`config/training_methods.v1.json` is the canonical Training Method Semantics v1 catalog. Equipment/method metadata describes causal workload/planning evidence; it does not own progression formulas or directly mutate attributes.

Object Familiarity / Inspect Utility Guard v1 and Dynamic Resource Awareness & Choice Breadth v1 are deployed. Familiar functional resources do not remain generic low-value inspect fallbacks; cognition can choose normal downtime instead of manufactured activity.

## Physical progression state

### Existing proven domains

**Strength — ACTIVE / DEPLOYED / LIVE-CYCLE VALIDATED.**
Free Weights remains the deliberate Strength stimulus source. Strength retains its proven level difficulty, saturation, recovery realization, detraining, idempotent settlement and completed-action activation semantics.

**Stamina — ACTIVE / DEPLOYED.**
Pure-conditioning evidence sources remain High-Speed Treadmill / `steady_state_cardio`, Rowing Ergometer / `rowing_conditioning`, and Altitude Training Chamber / `altitude_conditioning`. Mixed movement/combat methods are not silently credited to Stamina.

**Agility — ACTIVE / DEPLOYED.**
Agility uses `speed_agility_drills` from the Speed & Agility Station with its proven recovery/saturation/detraining semantics and automatic completed-action activation.

## Physical Attribute Progression Framework v1 — CURRENT ACTIVE SLICE

Canonical contract: `docs/PHYSICAL_ATTRIBUTE_PROGRESSION_FRAMEWORK.md`.

Status: **IMPLEMENTATION IN PROGRESS ON `test`**.

The proven Strength/Stamina/Agility lifecycle has been reconciled as:

`evidence scan -> consumed-event cursor -> recovery gate -> level/saturation gain -> detraining integration -> profile/history write -> settlement event`

The new framework uses one actor-generic policy-driven engine for the structurally equivalent remaining PA batch rather than four copy-paste engines. Existing Strength/Stamina/Agility implementations remain intact in v1 to avoid unnecessary migration risk.

Target batch and evidence policy:
- **Speed** — `speed_agility_drills`;
- **Reflexes** — `ai_combat_simulation` reactive work;
- **Endurance** — `heavy_bag_rounds`, `obstacle_conditioning`, `combat_pit_drills`; pure aerobic Stamina methods are intentionally excluded;
- **Flexibility** — new `mobility_stretching` evidence from a bounded Mobility & Stretching Area in the Home Gym.

Implementation invariants:
- policies live in `config/physical_attribute_progression.v1.json`;
- engine receives actor id/current field/evidence/recovery/policy and contains no Darian starting-value branch;
- first settlement bootstraps by consuming prior historical evidence without score mutation, preventing deployment-time retroactive gains;
- mature evidence is consumed only when recovery allows realization;
- each attribute owns distinct recovery/saturation/detraining policy;
- settlement/history evidence identifies the exact attribute/source;
- service activation occurs only at completed-action boundaries and creates no extra model calls;
- candidate world revision is `thorne-estate-v3.3-physical-attribute-training` with one additional train-capable Mobility & Stretching Area;
- no schema v5.

Validation hardening in the same slice:
- Minimum Training Stimulus Acceptance stages candidate `config/` alongside `src/`, fixing the prior missing `training_methods.v1.json` false failure;
- Strength Live Cycle validates each settlement against the profile value immediately before that settlement, fixing the prior evolving-production-copy baseline assertion.

Do not force live training to prove this batch. Deployment should verify health/world/config safely; natural completed actions establish bootstrap settlements, and later natural eligible training/recovery can provide live gain evidence.

## Grading state

- Strength grading exemplar — COMPLETE / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / DEPLOYED for compatible 0..100 attribute fields.
- IQ remains a separate scale.
- Skills grading/progression remains a separate family.
- Body composition/measurements remain a separate architecture family.

## Planned profile-unlock sequence after PA completion

1. body composition exemplar;
2. compatible body-measurement batch;
3. skill progression exemplar;
4. compatible skill batch;
5. intellectual attribute exemplar/batch;
6. mental/emotion dynamics.

## Deferred boundaries

Not authorized as side effects of the current work:
- full Character Memory Engine;
- multi-fallback chains/circuit breakers/provider-health scoring;
- Telegram API-key editing/model tuning;
- second production character solely for universalization testing;
- forced equipment rotation;
- generalized inventory/resource depletion;
- richer relationship engine;
- estate exterior/Tahoe traversal;
- schema v5.

## Exact resume point

Finish **Physical Attribute Progression Framework v1** on `test`: focused regression -> full CI and relevant corrected acceptance checks -> merge -> automatic deploy -> read-only production verification -> synchronize `test` to `main` and finalize canonical deployment evidence.

Then proceed directly to the **body composition progression exemplar** under the same universal actor-generic and minimum-runnable policy.
