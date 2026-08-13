# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Development policy

Use minimum runnable expansion plus **exemplar-first, then batch-by-pattern**. Prove one structural pattern end-to-end; once green/deployed, equivalent follow-ons should normally use one branch/PR, one focused test suite, one pre-merge disposable production-copy dry-run covering the whole batch, iterative fixes if needed, then one merge and one deploy/readback.

## Production baseline

- repo `Ye-Shwethway/observer-sandbox`
- VPS `/opt/observer-sandbox`
- DB `/var/lib/observer-sandbox/observer.sqlite3`
- systemd `observer-sandbox`
- SQLite schema v4
- world root `world_observer_universe`
- estate `loc_thorne_estate`
- world revision `thorne-estate-v3.0-scoped-ids`
- Darian autonomy enabled / normal / wake-on-demand
- global speed is Creator-controlled and must be re-read live
- Gemini cognition binding preserved
- Telegram connected private Creator observer

Production continues autonomously. Re-read live state whenever exact current action/stats/speed matter.

## Canonical runtime rule

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

LLMs propose structured actions only. Deterministic runtime owns legality and mutation.

## Proven feature state

- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.
- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.
- P3.4 Training Effectiveness Outcome — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Minimum Training Stimulus v1 — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.
- Adaptation Curve v1 — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / READ-ONLY.
- Stimulus Saturation / Diminishing Returns v1 — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / READ-ONLY.
- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Research Action Semantics v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Activity Semantics Batch 1 (`monitor`) — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.
- Read-Only Grading Strength Exemplar — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.

## Training progression state

Current evidence chain:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology -> session stimulus evidence -> read-only level/ceiling factor -> read-only recent-stimulus saturation factor`.

Minimum Training Stimulus v1:
- Free Weights train session only;
- Strength domain only;
- `stimulus_units = effective_minutes / 60`;
- Heavy Bag and other targets emit no Strength stimulus in v1;
- raw Strength remains unchanged.

Adaptation Curve v1:
- curve id `strength-level-curve-v1`;
- `effective_ceiling = natural_ceiling * ceiling_multiplier`;
- `level_factor = clamp((effective_ceiling-current)/effective_ceiling,0,1)^2` by default;
- default natural ceiling 100;
- Strength 90 -> 0.01, 95 -> 0.0025, 99 -> 0.0001;
- raw Strength/grade remain unchanged.

Stimulus Saturation v1:
- curve id `strength-stimulus-saturation-v1`;
- source existing action-completion training-stimulus event evidence;
- 72 simulated-hour rolling window;
- Strength domain only;
- `saturation_factor = 1 / (1 + 0.3 * recent_strength_stimulus_units)`;
- 0 units -> 1.0, 1 -> ~0.7692, 2 -> 0.625, 4 -> ~0.4545;
- no stimulus consumption/event mutation/raw Strength mutation;
- event insertion IDs are not treated as simulated-time chronology.

Evidence: Adaptation Curve PR #15 merge `52644bfcbb8b7b9cb4196d8b5f253a32e053aaf2`, acceptance `31686888383`, Deploy #141 `31686957768`; Stimulus Saturation PR #16 merge `f02f2407957872dad192701b3726c3f2d8ff096d`, CI #405 SUCCESS, acceptance #2 `31687327606`, release `052931125b23f1f50166bea8142f8da358b694ec`, Deploy #142 `31687401802` SUCCESS.

## Stat mutation gate

Raw stat mutation is **not authorized**.

Mandatory sequence:
1. Adaptation Curve v1 — COMPLETE / read-only.
2. Stimulus Saturation / Diminishing Returns v1 — COMPLETE / read-only.
3. Recovery Realization v1 — pending.
4. Detraining / Prolonged-Untrained Decay v1 — pending and mandatory.
5. Adaptation Preview v1 — pending; compose projected positive/negative delta with no mutation.
6. Stat Mutation Gate v1 — only after all prior gates are accepted; tiny audited decimal mutation only.

Positive path:
`eligible stimulus -> level/ceiling difficulty -> saturation/diminishing return -> recovery realization -> previewed positive delta`.

Regression path:
`elapsed relevant untrained time -> detraining eligibility -> decay curve -> previewed negative delta`.

Special modifiers stay abstract/factorized (effective-ceiling, adaptation-rate, recovery, etc.); no real-world drug dosing or medical guidance.

Canonical progression contract: `docs/TRAINING_PROGRESSION_GATES.md`.

## Grading state

`raps-100-proof-v1` is derived-only for 36 explicitly opted-in compatible 0..100 Attributes fields. Raw values remain authoritative.

Separate grading families remain mandatory:
- IQ excluded because its scale differs;
- Skills excluded because score/progression/experience semantics may differ;
- Body measurements/composition require a **separate exemplar + batch** and must not inherit flat attribute thresholds by default.

## Time and planning state

Action duration remains integer simulated minutes with minimum 1 minute. `1 sim min @ 3600x` remains a positive `1/60` real-second due interval. Sleep remains intentionally unclamped until nap/night-sleep semantics are separated.

## Exact resume point

**Adaptation Curve v1 + Stimulus Saturation v1 are live/read-only.** Resume with **Recovery Realization v1 — Free Weights + Strength only**. Do not mutate Strength. After recovery, implement mandatory Detraining/Prolonged-Untrained Decay, then Adaptation Preview. Only after all are accepted may Stat Mutation Gate v1 be considered.
