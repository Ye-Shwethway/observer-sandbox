# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-13

## Product principles

- Python/SQLite runtime/world state is authoritative.
- AI proposes structured cognition; it never directly mutates arbitrary world state.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Cognition remains wake-on-demand; no periodic LLM heartbeat by default.
- Canonical runtime composition:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Schema v4 remains the current composable foundation. Do not introduce schema v5 without a concrete missing invariant.
- Repeated expansion follows **exemplar-first, then batch-by-pattern**: prove one structural pattern, then batch equivalent follow-ons into one PR, one pre-merge disposable production-copy dry-run, and one deploy/readback.

## Foundation / P0 / P1

- Foundation schema v4 — COMPLETE.
- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 AI Provider Layer — FOUNDATION COMPLETE; Darian preserves configured Gemini cognition.
- P1 Living Darian Minimum — CONTINUOUS AUTONOMY LIVE / ENGINE HARDENING PASSED.

## P2 — Telegram Observer

- P2.1 Mobile Observer MVP — LIVE.
- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.

## P3 — Richer Simulation Vertical Slices

- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.
- P3.4 Training Effectiveness Outcome — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Minimum Training Stimulus v1 — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.
- Adaptation Curve v1 — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / READ-ONLY.

Current progression evidence chain:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology -> session stimulus evidence -> read-only level/ceiling adaptation factor`.

Minimum Training Stimulus v1 remains deliberately narrow:
- action: `train`;
- target: Free Weights only;
- domain: Strength only;
- `stimulus_units = effective_minutes / 60`;
- evidence persists in action outcome + completion event;
- Heavy Bag and other targets emit no Strength stimulus in v1;
- raw Strength and derived grade do not change.

Adaptation Curve v1 is also read-only:
- curve id `strength-level-curve-v1`;
- `effective_ceiling = natural_ceiling * ceiling_multiplier`;
- `remaining_fraction = clamp((effective_ceiling - current) / effective_ceiling, 0, 1)`;
- `level_factor = remaining_fraction ^ 2` by default;
- default natural ceiling `100`, default ceiling multiplier `1.0`;
- Strength 90 -> factor `0.01`; 95 -> `0.0025`; 99 -> `0.0001`;
- an abstract ceiling modifier changes effective headroom without mutating raw Strength;
- no accumulated stimulus, recovery realization, detraining, adaptation mutation, hypertrophy/body change, or schema v5.

Evidence: Minimum Training Stimulus PR #14 merge `3578de12ebc750aca397b16f01f8bd368e1af11a`, acceptance `31685799302`, Deploy #140 `31685928444`; Adaptation Curve PR #15 merge `52644bfcbb8b7b9cb4196d8b5f253a32e053aaf2`, acceptance `31686888383`, release `abfe82d279fb1c85a027109185b1d28ae859fbd1`, Deploy #141 `31686957768` SUCCESS.

## Progression mutation gates

Raw Strength/stat mutation is **not authorized** yet.

Required order before Stat Mutation Gate v1:
1. Adaptation Curve v1 — COMPLETE / read-only.
2. Stimulus Saturation / Diminishing Returns v1 — pending.
3. Recovery Realization v1 — pending.
4. Detraining / Prolonged-Untrained Decay v1 — pending and mandatory before mutation.
5. Adaptation Preview v1 — pending; compose positive and negative projected deltas without mutation.
6. Stat Mutation Gate v1 — only after all prior gates are accepted; tiny audited decimal raw-stat updates only.

Positive path:
`eligible stimulus -> level/ceiling difficulty -> saturation/diminishing return -> recovery realization -> previewed positive delta`.

Regression path:
`elapsed relevant untrained time -> detraining eligibility -> decay curve -> previewed negative delta`.

Special modifiers stay abstract and factorized (for example effective-ceiling, adaptation-rate, or recovery multipliers). Do not implement real-world drug dosing/medical guidance.

Canonical contract: `docs/TRAINING_PROGRESSION_GATES.md`.

## Post-P3.5 stabilization

- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Minimum action timing invariant — CI VERIFIED.

## Selective Activity/Action Semantics

- Research v1 exemplar — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Activity Semantics Batch 1 (`monitor`) — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.

Do not add more verbs merely for breadth. A verb requiring new state/consequences becomes a new exemplar.

## Read-only grading

### Strength exemplar
Status: COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.

- raw `raps_pa.strength = 90` remains authoritative;
- named proof scheme `raps-100-proof-v1` derives Grade S;
- grade is query/presentation metadata only;
- no schema change.

### Attribute Grading Batch 1
Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.

- 36 explicitly opted-in compatible 0..100 Attributes fields are graded;
- IQ is excluded because it uses a different scale;
- Skills require their own family;
- Body measurements/composition require a **separate exemplar + batch** because their normalization/calculation semantics differ materially;
- raw profile values remain unchanged.

## Grading family rule

Do not use one numeric evaluator merely because multiple domains contain numbers.

- 0..100 compatible Attributes: current `raps-100-proof-v1` family.
- IQ: separate scale/evaluator if useful.
- Skills: separate family because progression/experience semantics may differ.
- Body measurements/composition: separate exemplar and batch; evaluator may need units, body composition, stature/proportion context and/or genetic ceilings rather than flat thresholds.

## Deferred boundaries

Not implemented:
- accumulated/recent stimulus state beyond current action/event evidence;
- stimulus saturation/diminishing-return state;
- recovery realization state;
- detraining/prolonged-untrained decay;
- raw attribute/skill/body-measurement progression mutation;
- hypertrophy/body composition progression;
- body-measurement grading evaluator;
- IQ/skills grading evaluators;
- inventory/resource depletion;
- rich memory/relationship/environment engines;
- exterior/Tahoe traversal;
- schema v5.

## Current resume point

**Adaptation Curve v1 is live and read-only.** The next bounded implementation slice is **Stimulus Saturation / Diminishing Returns v1 — Free Weights + Strength only**. Do not mutate Strength. After saturation, implement Recovery Realization, then mandatory Detraining/Prolonged-Untrained Decay, then a composed Adaptation Preview. Only after all are accepted may Stat Mutation Gate v1 be considered.
