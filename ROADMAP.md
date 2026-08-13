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

Current short-term chain:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology -> session Strength stimulus evidence`.

Minimum Training Stimulus v1 remains narrow: Free Weights + Strength only; `stimulus_units = effective_minutes / 60`; Heavy Bag and other targets do not emit Strength stimulus in v1.

## Strength progression math gates

All pre-mutation math gates are now COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.

### Adaptation Curve v1 — READ-ONLY
- curve `strength-level-curve-v1`;
- `effective_ceiling = natural_ceiling * ceiling_multiplier`;
- `level_factor = clamp((effective_ceiling-current)/effective_ceiling,0,1)^2`;
- default natural ceiling 100;
- Strength 90 -> 0.01, 95 -> 0.0025, 99 -> 0.0001.

### Stimulus Saturation / Diminishing Returns v1 — READ-ONLY
- 72 simulated-hour Strength-stimulus window from existing completion-event evidence;
- `saturation_factor = 1 / (1 + 0.3 * recent_strength_stimulus_units)`;
- no mutable saturation counter; event insertion id is not treated as simulated-time chronology.

### Recovery Realization v1 — READ-ONLY
- latest positive Strength stimulus establishes the recovery boundary;
- <=6 sim hours -> zero time realization;
- 6..48h -> linear ramp;
- >=48h -> full time eligibility;
- state quality uses energy, alertness and systemic-fatigue recovery;
- fatigue >=70 hard-blocks realization;
- `recovery_factor = clamp(time_factor * state_quality * recovery_multiplier,0,1)`.

### Detraining / Prolonged-Untrained Decay v1 — READ-ONLY
- no Strength-training history -> no invented decay start;
- first 14 simulated days untrained -> zero decay pressure;
- after grace: `time_factor = 1 - exp(-overdue_days/60)`;
- high-level exposure `= clamp(current/effective_ceiling,0,1)^2`;
- decay pressure stays bounded and does not mutate Strength.

### Adaptation Preview v1 — READ-ONLY
- positive proof scale `0.25` raw Strength points per fully-realized low-level stimulus unit before level/saturation/recovery factors;
- positive preview: `0.25 * recent_stimulus * level_factor * saturation_factor * recovery_factor * adaptation_rate_multiplier`;
- at Strength 90, one recent fully recovered 1.0 stimulus unit projects about `+0.001923` with default modifiers;
- negative proof rate: `0.02 * decay_pressure * preview_days * decay_rate_multiplier`;
- default preview horizon 1 simulated day;
- no raw mutation or stimulus consumption.

Special modifiers remain factorized: effective-ceiling, adaptation-rate, recovery, detraining-pressure and decay-rate are distinct simulation sockets. No real-world drug dosing/medical guidance is modeled.

## Stat Mutation Gate v1

### Strength Progression Settlement v1 Core
Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / **NOT AUTOMATICALLY ACTIVE**.

Core safety invariants:
1. first settlement is non-mutating bootstrap; historical pre-feature Strength stimulus is marked consumed so deployment cannot retroactively jump Strength;
2. consumed stimulus event ids are persisted in `strength_progression_settled` audit events and cannot be credited twice;
3. positive stimulus requires >=48 simulated hours and fatigue below the existing 70 hard block; blocked/too-young stimulus remains pending;
4. detraining uses an analytic integral across the exact unsettled simulated-time interval and resets at Strength-training events;
5. every cursor advance is audited; every actual raw Strength mutation is also written to `character_profile_history`;
6. replay at the same simulated settlement boundary is a no-op;
7. mutation authority becomes `strength-progression-settlement-v1`, mode `simulated`, six-decimal raw precision, bounded to 0..100.

Evidence: PR #20 merge `d6c94c90aec354faedd42656c42d078cb5bd42a3`; CI #420 SUCCESS; Strength Progression Settlement v1 Acceptance #2 `31688789743` SUCCESS on a disposable live production DB copy; release `028f1bf4506f2a0192a2df987d1c3cb24b8a4fe5`; Deploy #146 `31688891757` SUCCESS.

The core is deliberately not called by the production service yet. Production Strength therefore must not change merely because this code is deployed.

## Activation rule

The next bounded slice is **Strength Progression Automatic Activation v1**. Activation must remain separate from the mutation-core PR and must prove on a disposable production copy that:
- the first automatic settlement is bootstrap-only and preserves live Strength;
- automatic scheduling cannot double-consume stimulus or double-apply detraining;
- no-op/cursor event volume is bounded rather than emitted every tight service tick;
- future eligible Strength stimulus settles without manual DB edits;
- production deployment/readback preserves Telegram/Gemini/autonomy/runtime health.

Preferred activation policy: evaluate after action-completion boundaries, but only call settlement when either (a) an eligible unconsumed Strength stimulus exists or (b) a bounded detraining checkpoint is due (target: at most once per simulated day for pure time-decay settlement). Bootstrap is the one explicit exception.

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

- Strength grading exemplar — COMPLETE / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / DEPLOYED; 36 explicitly opted-in compatible 0..100 Attributes fields.
- IQ remains excluded because its scale differs.
- Skills remain a separate grading/progression family.
- Body measurements/composition remain a **separate exemplar + batch** because units, stature/proportion, composition and calculation semantics differ materially.

## Deferred boundaries

Not implemented:
- automatic production Strength settlement activation;
- progression for non-Strength attributes, skills, body measurements or composition;
- hypertrophy/body-composition progression;
- body-measurement grading evaluator;
- IQ/skills grading evaluators;
- inventory/resource depletion;
- rich memory/relationship/environment engines;
- exterior/Tahoe traversal;
- schema v5.

## Current resume point

All required Strength progression formulas plus the idempotent settlement core are proven. Resume with **Strength Progression Automatic Activation v1**. Keep activation bounded and separately accepted; do not batch other attributes into this first mutation activation exemplar.
