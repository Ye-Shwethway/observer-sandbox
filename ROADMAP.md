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

Current short-term training chain:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology -> session stimulus evidence`.

Minimum Training Stimulus v1 is deliberately narrow:
- action: `train`;
- target: Free Weights only;
- domain: Strength only;
- `stimulus_units = effective_minutes / 60`;
- evidence persists in action outcome + completion event;
- Heavy Bag and other targets emit no Strength stimulus in v1;
- raw Strength and derived grade do not change;
- no accumulated stimulus, adaptation, hypertrophy/body change, or schema v5.

Evidence: PR #14 merge `3578de12ebc750aca397b16f01f8bd368e1af11a`; CI #393 SUCCESS; Minimum Training Stimulus Acceptance #2 `31685799302` SUCCESS on a disposable copy of the live production DB; release `22f8a3d7776137cb72d2926caac37d1002e6d8ed`; Deploy #140 `31685928444` SUCCESS.

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

Evidence: Strength PR #12 / Deploy #138; Attribute Batch PR #13 / Deploy #139.

## Grading family rule

Do not use one numeric evaluator merely because multiple domains contain numbers.

- 0..100 compatible Attributes: current `raps-100-proof-v1` family.
- IQ: separate scale/evaluator if useful.
- Skills: separate family because progression/experience semantics may differ.
- Body measurements/composition: separate exemplar and batch; evaluator may need units, body composition, stature/proportion context and/or genetic ceilings rather than flat thresholds.

## Next planned sequence

Minimum Training Stimulus is now proven. The next progression work must not jump straight to attribute mutation.

1. Define/prove **Minimum Adaptation/Progression v1** only after explicitly specifying how session stimulus and recovery/time convert into adaptation.
2. Keep the first adaptation exemplar to Free Weights + Strength only.
3. Preserve raw-value authority, tiny deterministic changes, diminishing-return semantics, and auditable evidence.
4. Only after one adaptation exemplar is proven should equivalent progression expansion be batched by pattern.
5. Body grading remains a separate deferred family unless Creator explicitly prioritizes it.

## Deferred boundaries

Not implemented:
- accumulated stimulus store/history beyond action/event evidence;
- adaptation/progression mutation;
- skill/body-measurement progression;
- hypertrophy/body composition progression;
- body-measurement grading evaluator;
- IQ/skills grading evaluators;
- inventory/resource depletion;
- rich memory/relationship/environment engines;
- exterior/Tahoe traversal;
- schema v5.

## Current resume point

**Minimum Training Stimulus v1 is live.** Free Weights sessions can now produce auditable Strength stimulus evidence without changing Strength itself. The next bounded design/implementation candidate is **Minimum Adaptation/Progression v1 — Free Weights + Strength only**, but adaptation semantics must be defined before mutation is allowed.
