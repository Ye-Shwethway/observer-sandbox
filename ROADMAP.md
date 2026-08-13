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

Current training chain:
`Free Weights -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology -> Strength stimulus -> level/ceiling difficulty -> saturation -> recovery -> detraining -> preview -> idempotent settlement`.

## Strength progression math gates

All pre-mutation math gates are COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

### Adaptation Curve v1
- `effective_ceiling = natural_ceiling * ceiling_multiplier`;
- `level_factor = clamp((effective_ceiling-current)/effective_ceiling,0,1)^2`;
- default ceiling 100; Strength 90 -> 0.01, 95 -> 0.0025, 99 -> 0.0001.

### Stimulus Saturation / Diminishing Returns v1
- 72 simulated-hour Strength-stimulus window from completion-event evidence;
- `saturation_factor = 1 / (1 + 0.3 * recent_strength_stimulus_units)`;
- no mutable saturation counter; event id ordering is not treated as sim-time chronology.

### Recovery Realization v1
- <=6 sim hours after latest Strength stimulus -> zero time realization;
- 6..48h -> linear ramp; >=48h -> full time eligibility;
- state quality uses energy, alertness and systemic-fatigue recovery;
- fatigue >=70 hard-blocks positive realization.

### Detraining / Prolonged-Untrained Decay v1
- no Strength-training history -> no invented decay start;
- first 14 simulated days untrained -> zero decay pressure;
- after grace: `time_factor = 1 - exp(-overdue_days/60)`;
- high-level exposure `= clamp(current/effective_ceiling,0,1)^2`.

### Adaptation Preview v1
- positive proof scale: `0.25 * recent_stimulus * level_factor * saturation_factor * recovery_factor * adaptation_rate_multiplier`;
- at Strength 90, one recent fully recovered 1.0 stimulus projects about `+0.001923` with default modifiers;
- negative proof rate: `0.02 * decay_pressure * preview_days * decay_rate_multiplier`;
- modifiers remain factorized: ceiling, positive rate, recovery, detraining pressure and negative rate are separate sockets.

No real-world drug dosing/medical guidance is modeled; special conditions use abstract simulation modifiers only.

## Stat Mutation Gate v1 — Strength exemplar

### Strength Progression Settlement v1 Core
Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.

Safety invariants:
1. first settlement is non-mutating bootstrap; pre-feature Strength stimulus cannot cause a retroactive stat jump;
2. consumed stimulus event ids cannot be credited twice;
3. positive stimulus requires >=48 simulated hours and fatigue below 70; blocked/too-young evidence remains pending;
4. detraining is analytically integrated over the exact unsettled sim-time interval and resets at Strength-training events;
5. every cursor advance is audited and every actual mutation is historized;
6. replay at the same simulated settlement boundary is a no-op;
7. actual mutation uses six-decimal raw precision, bounded 0..100, authority `strength-progression-settlement-v1`.

Evidence: PR #20 merge `d6c94c90aec354faedd42656c42d078cb5bd42a3`; CI #420 SUCCESS; acceptance #2 `31688789743` SUCCESS; Deploy #146 `31688891757` SUCCESS.

### Strength Progression Automatic Activation v1
Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / **LIVE BOOTSTRAP VERIFIED**.

Activation policy:
- progression is checked only at completed-action simulation boundaries, never on the tight 2-second service poll;
- bootstrap once if no settlement cursor exists;
- eligible unconsumed Strength stimulus (>=48 sim hours and recovery allowed) settles at the next action-completion boundary;
- otherwise pure detraining checkpoints occur at most once per 24 simulated hours and only when Strength-training history exists;
- short/same boundaries skip without writing progression events;
- progression failure remains downstream of action completion and must not roll back the action or stop autonomy.

Evidence: PR #21 merge `71f00e2850c9c47f0875f012fd68bb131e4b6247`; CI #425 SUCCESS; Strength Progression Auto Activation v1 Acceptance #1 `31689247542` SUCCESS; release `8d8eeee737cd901dd229090ec26eba099d9350fa`; Deploy #147 `31689319524` SUCCESS.

Live verification:
- automatic production service established the first `strength_progression_settled` event before the explicit verifier could do so;
- first settlement event id `161`, bootstrap `true`, sim time `2025-05-02T09:23:00+00:00`;
- Strength remained exactly `90.0 -> 90.0` and retained pre-mutation static/attribute-engine authority;
- explicit bootstrap verifier then returned `same_or_older_boundary`, proving duplicate bootstrap suppression;
- live service remained active/healthy, schema v4, autonomy enabled/normal.

The Strength progression mutation flow is therefore **ACTIVE**. Future eligible Free Weights Strength stimulus may create tiny decimal raw Strength changes automatically after recovery; prolonged untrained periods may create bounded negative changes after the detraining grace/curve.

## Post-P3.5 stabilization

- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Minimum action timing invariant — CI VERIFIED.

## Selective Activity/Action Semantics

- Research v1 exemplar — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Activity Semantics Batch 1 (`monitor`) — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.

## Read-only grading

- Strength grading exemplar — COMPLETE / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / DEPLOYED; 36 explicitly opted-in compatible 0..100 Attributes fields.
- IQ remains separate because its scale differs.
- Skills remain a separate grading/progression family.
- Body measurements/composition remain a **separate exemplar + batch** because units, stature/proportion, composition and calculation semantics differ materially.

## Deferred boundaries

Not implemented:
- progression stimulus/mutation for non-Strength attributes;
- skill progression;
- hypertrophy/body-measurement/body-composition progression;
- body-measurement grading evaluator;
- IQ/skills grading evaluators;
- inventory/resource depletion;
- rich memory/relationship/environment engines;
- exterior/Tahoe traversal;
- schema v5.

## Current resume point

**Strength progression v1 is live as the first complete mutation exemplar.** Do not immediately batch other attributes merely because the settlement pattern exists: each new progression domain first needs an explicit stimulus mapping and any domain-specific recovery/decay semantics. Recommended next decision is either:
1. add Creator-facing Strength progression observability (last stimulus, recovery state, next eligibility, latest settlement/delta), then observe/tune the live exemplar; or
2. choose the next compatible physical progression domain and prove its stimulus mapping before any batch expansion.

Body measurements/composition remain a separate architecture line.
