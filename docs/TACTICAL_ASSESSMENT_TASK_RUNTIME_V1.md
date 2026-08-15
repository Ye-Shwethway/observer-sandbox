# Tactical Planning Represented Assessment Runtime v1

Status: **COMPLETE / DEPLOYED**
Date: 2026-08-15

## Evidence checkpoint

- PR: #131 — `add Tactical Planning represented assessment runtime v1`
- Tested head: `4e481e52ae1f068d8217640f8895b1a56fe95b0d`
- Merge: `aef123dc7840b69091c7264988b744c69d955396`
- Deploy: #210 / run `31878236282` — SUCCESS
- Full CI #846 — SUCCESS
- Represented Skill Task Contract v1 Acceptance #5 — SUCCESS
- Represented Skill Task Instance v1 Acceptance #3 — SUCCESS
- Cognitive Performance Modifier Contract v1 Acceptance #3 — SUCCESS
- Technology Diagnostic Task Runtime v1 Acceptance #3 — SUCCESS
- Skill Evidence / Skill Progression / Strength live-cycle regressions — SUCCESS

Production deploy verification confirmed service health, schema v5, normal autonomy with retry `null`, preserved cognition binding, and Telegram connectivity. No live Tactical action was forced for proof. The deployed production initialization path completed successfully; exact Tactical seed rows were proven by CI/fresh-DB tests rather than separately queried from the live DB in this checkpoint.

## Purpose

This is the second represented-Skill gameplay exemplar. Its purpose was not merely to add another action; it tested whether the Technology represented-runtime architecture generalizes to a cognitively heavy, non-tool-centric Skill application.

The result is positive. The common runtime pattern now has two materially different resource shapes and is ready for batch-by-pattern expansion where no new structural invariant is introduced.

## Canonical task

Task ID:
`tactical_situation_assessment_sim_v1`

Skill application:
`tactical_planning.assess_tactical_situation`

Challenge:
`standard`

Mode / risk:
`simulation_safe` / `low`

Action:
`assess`

Purpose-built target:
`obj_thorne_estate_intel_tactical_situation_assessment_simulator`

Exact target definition:
`represented_task:tactical_situation_assessment_simulator_v1`

Target capabilities:
- `inspect`
- `assess`
- `situational_intelligence`

The target is intentionally distinct from Tactical training/practice objects. Training evidence is not promoted into represented application authority.

## Resource-contract generalization

The Technology exemplar exposed only an `any` hard-resource shape. Tactical assessment legitimately requires no hard external resource, so PR #131 generalized represented-task resource contracts to:

`required_resource_mode: any | none`

The represented-task mode must preserve the underlying Skill application's resource mode.

For Tactical assessment:
- required mode: `none`
- required-any capabilities: none
- supporting capability: `situational_intelligence`

Missing supporting intelligence may produce a `constrained` eligible assessment; it does not become a hidden hard requirement.

## Deterministic capability flow

`cognition awareness -> legal colocated assess option -> exact task/target binding -> authoritative Tactical Planning Skill feasibility -> bounded cognitive-performance shaping -> deterministic outcome -> action completion -> immutable application evidence`

The LLM does not decide feasibility or mutate Skill state.

## Cognitive-performance contract

The Tactical assessment contract uses bounded task-specific factors only after feasibility:

### Reasoning quality
- Problem Solving: 0.45
- IQ: 0.30
- Focus: 0.25
- max absolute effect: 0.12

### Precision
- Focus: 0.50
- Problem Solving: 0.35
- IQ: 0.15
- max absolute effect: 0.10

### Adaptation
- Adaptability: 0.55
- Problem Solving: 0.30
- IQ: 0.15
- max absolute effect: 0.10

IQ is general reasoning context only. It cannot create Tactical Planning proficiency, hidden tactical Knowledge, represented information, target access, or command authority.

Legacy `raps_ia.tactical_thinking` is deliberately excluded from this contract because `character_skills.tactical_planning` is the learned-Skill authority; using both as proficiency inputs would double-count the same legacy concept.

## Outcome dimensions

The deterministic runtime resolves bounded indices for:
- `quality_precision`
- `information_gained`
- `partial_failure_recovery`

Feasibility remains owned by the represented-task/Skill capability resolver. Cognitive modifiers never upgrade an unsupported task to supported.

## Evidence semantics

Completed represented assessment emits immutable:
`skill_application_evidence`

It is explicitly:
`learning_evidence: false`

Application completion therefore does not automatically increase Tactical Planning score or experience.

Existing Tactical learning authority remains the already-authored VR Tactical Drills / AI Combat Simulation training evidence path.

## Acceptance invariants proven

Tests prove:
- distinct exact simulator/action seed;
- action visibility only when colocated;
- cognition receives both the concrete action and semantic Tactical capability awareness;
- Darian's authoritative Tactical Planning state resolves as 92 / S;
- deterministic repeatable outcome;
- bounded IQ / Problem Solving / Focus / Adaptability contributions;
- legacy tactical-thinking exclusion;
- supporting-resource constrained path;
- immutable application evidence without Tactical XP;
- completed-action idempotency;
- high IQ/attributes cannot substitute for an absent Tactical Planning Skill;
- wrong target definition fails closed and rolls back;
- Technology represented runtime remains compatible.

## Architectural conclusion

Technology and Tactical Planning now prove the represented-Skill runtime pattern across:
- hard-resource `any` and hard-resource `none` applications;
- tool-centric and cognition-centric task families;
- supported/constrained outcomes;
- immutable application evidence separated from learning evidence.

Therefore, under `AGENTS.md`, structurally equivalent low-risk follow-ons should be implemented as a **batch-by-pattern**, not as one bespoke exemplar PR per Skill.

A future application that introduces a genuinely new invariant — especially consequential H2H/Weapons safety, injury, target authorization, or other high-risk consequences — may still justify one bounded exemplar for that new invariant.
