# Represented Skill Task Contract v1

Status: COMPLETE / DEPLOYED READ-ONLY TASK-DEFINITION FOUNDATION

## Purpose

The Skill Definition says what a Skill/application means. The Represented Skill Task Definition says how one concrete world task is bounded without turning names, model prose, or practice fixtures into gameplay authority.

Canonical registry:
- `config/represented_skill_tasks.v1.json`
- `src/observer_sandbox/represented_skill_tasks.py`

First exemplar:
`technology_known_system_fault_diagnostic_sim_v1`

## Invariant

`validated Skill application + represented task definition + exact target contract + task challenge/context/resources/outcome bounds -> machine-checkable represented task truth`

This layer defines task truth. It does not assess an actor, authorize an action, emit application evidence, or create learning evidence.

## Audit finding

Existing runtime already carries generic action `target`, `resources`, `conditions`, and `modifiers`; action instances persist them; entities expose `definition_id` and capabilities. However, no existing authority owned all of:
- Skill application id;
- challenge class;
- required context tags;
- task resource semantics;
- bounded outcome dimensions;
- target-system identity.

The existing Systems Diagnostic Practice Console is explicitly learning/practice authority (`skill_practice:systems_diagnostic_practice`) and therefore must not be silently promoted into real application authority.

## Technology exemplar

`technology_known_system_fault_diagnostic_sim_v1`:
- Skill: `technology`
- Application: `diagnose_known_system_fault`
- Challenge: `standard`
- Mode: `simulation_safe`
- Risk: `low`
- Exact target definition id: `represented_task:technology_known_fault_diagnostic_simulator_v1`
- Required target capability: `inspect`
- Context: `technical_system_represented`, `diagnostic_evidence_available`
- Required resource capability: `diagnostic_interface`
- Supporting resource capability: `technical_documentation`
- Outcome dimensions: `feasibility`, `quality_precision`, `information_gained`, `partial_failure_recovery`
- Application evidence: deferred until action integration
- Learning evidence: false

No target entity is seeded by this slice.

## Cross-layer validator locks

A represented task cannot:
- reference an unknown/non-executable Skill application;
- request a challenge outside the application envelope;
- weaken required application context;
- invent required resource capabilities outside the application contract;
- silently drop supporting resource semantics;
- add outcome dimensions outside application-declared gameplay effects;
- use a `skill_practice:*` definition as application target authority;
- embed actor score/experience/tier/grade/state;
- imply Skill learning evidence;
- claim `simulation_safe` while carrying non-low risk.

Target authority is exact `definition_id` based. Object names and model prose are never task authority.

## Validation / deployment

PR #119: `add represented Skill task contract v1`

Final tested head:
`f9d56817dc9a831113b78aeb4dee578947a294da`

Merge:
`5dd49824e75adce40f374822bf9dc5383ad7532e`

PR gates:
- Represented Skill Task Contract v1 Acceptance #1 / run `31873487399`: SUCCESS
- CI #819 / run `31873487361`: SUCCESS
- Strength Live Cycle Validation v1 #38 / run `31873487388`: SUCCESS
- Public Readiness Security Audit #73 / run `31873487376`: SUCCESS

Post-merge:
- Represented Skill Task Contract v1 Acceptance #2 / run `31873525048`: SUCCESS
- CI #820 / run `31873525036`: SUCCESS
- Deploy #203 / run `31873525050`: SUCCESS

Production readback after Deploy #203 verified:
- exact deployed commit `5dd49824e75adce40f374822bf9dc5383ad7532e`;
- service healthy/active;
- schema v5;
- autonomy normal at 1.0x;
- Telegram/cognition preserved;
- Technology remained `82.0 / A Advanced`;
- no represented task entity/action was introduced, so live behavior remained intentionally unchanged.

## Next minimum-runnable slice

**Represented Skill Task Instance Resolver v1 — read-only.**

Minimum invariant:
`actor + task_id + target_entity_id + explicit available resource capabilities -> validate target entity exact type/definition/capabilities -> derive challenge/context from represented task -> actor-backed Skill capability assessment -> read-only represented-task assessment`

Constraints:
- exact target entity binding only;
- no name/prose matching;
- do not reuse practice console;
- no entity seeding required to prove the generic resolver; tests may use synthetic entities;
- resource capabilities remain explicit caller/task inputs until represented resource ownership is separately proven;
- no action authorization, mutation, evidence, XP, autonomy, or Telegram integration;
- fail closed on target mismatch.

Only after this read-only instance binding is proven should one distinct represented Technology simulator entity and bounded action/evidence integration be considered.