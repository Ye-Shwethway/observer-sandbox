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
- Repeated expansion follows **exemplar-first, then batch-by-pattern**: prove one genuinely new structural pattern, then batch equivalent follow-ons into one PR, one focused regression suite, one pre-merge disposable production-copy dry-run covering every batched item, and one deploy/readback.
- Dry-run, acceptance, tuning, and accelerated simulation use a disposable copy of the production DB. Production is reserved for all-green merge/deploy and read-only post-deploy verification; validation must not accelerate or otherwise mutate the live runtime.

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

Current training/progression chain:
`Free Weights -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology -> Strength stimulus -> level/ceiling difficulty -> saturation -> recovery -> detraining -> preview -> idempotent settlement -> automatic action-boundary activation`.

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
Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / LIVE BOOTSTRAP VERIFIED.

Activation policy:
- progression is checked only at completed-action simulation boundaries, never on the tight service poll;
- bootstrap once if no settlement cursor exists;
- eligible unconsumed Strength stimulus (>=48 sim hours and recovery allowed) settles at the next action-completion boundary;
- otherwise pure detraining checkpoints occur at most once per 24 simulated hours and only when Strength-training history exists;
- short/same boundaries skip without writing progression events;
- progression failure remains downstream of action completion and must not roll back the action or stop autonomy.

Evidence: PR #21 merge `71f00e2850c9c47f0875f012fd68bb131e4b6247`; CI #425 SUCCESS; acceptance #1 `31689247542` SUCCESS; release `8d8eeee737cd901dd229090ec26eba099d9350fa`; Deploy #147 `31689319524` SUCCESS.

The Strength progression mutation flow is ACTIVE.

## Strength Progression Observability v1

Status: COMPLETE / DEPLOYED / CREATOR LIVE UX VERIFIED.

`Profile -> Recovery` now exposes read-only Strength progression diagnostics:
- six-decimal raw Strength;
- recent qualifying Strength stimulus / 72h;
- level adaptation factor;
- saturation yield;
- recovery realization and adaptation status;
- latest settlement delta/time;
- detraining/grace status;
- next progression boundary.

Creator live-verified the initial no-stimulus/bootstrap state. Wording polish subsequently clarified bootstrap/no-history semantics without changing math or state.

Evidence:
- PR #25 merge `d291e77f4c290bc4b0487888e52a4c6063349f36`, CI #457 `31699319018` SUCCESS, Deploy #151 `31699394074` SUCCESS;
- wording polish PR #26 merge `ebf18df5cc728ea600490f4b23da6e8bc35096ef`, CI #462 `31700255690` SUCCESS, release `fb45466d61494dbe066c47a39f17a48ef240ddd3`, Deploy #152 `31700418122` SUCCESS.

## Causal physiological need resolution

- Hunger resolver v1 — DEPLOYED / CREATOR LIVE VERIFIED.
- Thirst/hunger causal resolver v2 — DEPLOYED / CREATOR LIVE VERIFIED.
- Complete five-need causal resolver v3 — COMPLETE / CI VERIFIED / PRODUCTION-COPY COMPATIBILITY VERIFIED / DEPLOYED.
- Fatigue Causal Recovery + Inspect Loop Guard v1 — COMPLETE / CI VERIFIED / PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / LIVE HEALTH VERIFIED.

v3 used the accelerated development rule correctly:
- Energy was the directionality exemplar;
- Sleepiness + Cleanliness were expanded in the same PR;
- Hunger/Thirst remained green;
- one PR / one deploy.

Fatigue follow-on reuses the existing physiological/training thresholds instead of inventing a parallel scale:
- fatigue >=55 is a strong recovery need;
- fatigue >=70 is a critical recovery need and matches the existing hard training gate;
- `rest` / `sleep` are the causal resolvers;
- high-fatigue cognition cannot substitute training-adjacent `inspect` / `use` for recovery;
- immediate repeated inspect/use pairs and serial same-room inspect/use loops are deterministically suppressed using recent event evidence, without a new schema counter.

Current authored priority is:
`sleepiness -> energy -> fatigue -> thirst -> hunger -> cleanliness`, with critical needs ahead of strong needs.

Evidence for v3: PR #24 merge `e1e6d79479fa4d2ae837c395ec3b2fdb7391dc8f`; CI #451 `31698384623` SUCCESS; production-copy compatibility acceptance #12 `31698384587` SUCCESS; Deploy #150 `31698521410` SUCCESS.

Evidence for Fatigue Causal Recovery + Inspect Loop Guard v1:
- final PR #27 head `cb500d9319aa6247c7db2132dbc52f70fa917aec`;
- CI #471 run `31703588016` SUCCESS;
- Fatigue Causal Recovery v1 Acceptance #5 run `31703588566` SUCCESS;
- Causal Need Resolution v2 compatibility Acceptance #17 run `31703587998` SUCCESS;
- copied production baseline: fatigue `71.285` at sim `2025-05-02T14:59:00+00:00` in Training Hall;
- reproduced disposable-copy fatigue `72.4` yielded only `rest`; 180 sim-min natural rest reduced fatigue to `46.9`;
- production mutation `false`, model calls `0`;
- PR #27 merge `31484c561948d84e97d5c677f15cd1ced7f8ad89`;
- release `9121904f3db9009af32e30dbb925c5c60cd837cb`;
- post-release CI #473 run `31703753642` SUCCESS;
- Deploy #153 run `31703753498` SUCCESS;
- post-deploy service active/healthy, schema v4, Gemini binding preserved, Telegram connected.

Post-deploy readback also reported speed `2.0x`, fatigue `70.91`, and a pre-existing pending `inspect` action at sim `2025-05-02T15:14:00+00:00`. Deployment preserves already-planned actions, so that pending inspect is not evidence against the new next-boundary selection guard. The live `2.0x` speed was not changed by this slice and must not be silently altered by validation tooling.

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

## Next proposed slice — Strength Progression Live Cycle Validation & Tuning v1

Before adding another progression domain, validate one complete real Strength cycle while preserving production safety.

Required validation:
1. read live production baseline evidence for Strength, fatigue/readiness, recent stimulus, speed and pending action without mutation;
2. copy the current production DB to a disposable validation DB;
3. use real copied Free Weights completion/stimulus evidence where available; do not fabricate Strength stimulus or directly set Strength;
4. inspect copied Profile/Recovery diagnostics immediately after the qualifying stimulus;
5. let recovery proceed through ordinary action semantics on the disposable copy; accelerated simulated observation is permitted only on the copy;
6. inspect the <=6h, 6..48h and >=48h recovery boundaries on the copy when practical;
7. verify the first eligible automatic settlement only at an action-completion boundary;
8. compare actual stimulus, level factor, saturation, recovery factor and settlement delta with the v1 formulas;
9. verify raw Strength history/event evidence, consumed IDs, duplicate-credit suppression and same-boundary idempotency;
10. tune constants only if concrete evidence shows a mismatch; otherwise preserve formulas and mark the cycle validated;
11. after all-green merge/deploy, perform read-only production health/runtime readback only.

This slice is validation/tuning, not a new progression-domain implementation. Production runtime acceleration, direct progression edits, fabricated stimulus, and validation-induced Telegram activity are prohibited.

## Current resume point

Resume **Strength Progression Live Cycle Validation & Tuning v1** under the disposable production-copy validation policy. First treat live production only as a read-only source of baseline/evidence and reconcile the observed live speed `2.0x` before assuming any wall-time cadence. After the Strength cycle is validated, propose the next physical progression domain and first prove its domain-specific stimulus/recovery/decay semantics before any batch expansion.

Body measurements/composition remain a separate architecture line.
