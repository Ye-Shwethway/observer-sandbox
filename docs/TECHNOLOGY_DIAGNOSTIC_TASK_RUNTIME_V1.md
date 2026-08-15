# Technology Represented Diagnostic Task Runtime v1

Status: implementation candidate

## Purpose

This slice is the first end-to-end gameplay consumer of the Skill Definition / Capability foundation. It turns the previously read-only Technology diagnostic exemplar into a represented, selectable, deterministic simulation action without making model prose or raw Skill scores state-mutation authority.

## Runtime exemplar

Task:

`technology_known_system_fault_diagnostic_sim_v1`

Action:

`diagnose`

Purpose-built target:

`obj_thorne_estate_intel_known_fault_diagnostic_simulator`

Exact definition:

`represented_task:technology_known_fault_diagnostic_simulator_v1`

Location:

`loc_thorne_estate_intelligence_hub`

The simulator advertises:

- `inspect`
- `diagnose`
- `diagnostic_interface`
- `technical_documentation`

The integrated interface/documentation are represented resources for this first low-risk exemplar. External inventory/tool capability resolution remains future work.

## Gameplay flow

`cognition capability awareness`
→ `authoritative diagnose action option`
→ `generic action lifecycle / colocation validation`
→ `exact represented-task instance binding`
→ `authoritative Technology Skill capability assessment`
→ `bounded Cognitive / Performance Modifier resolution`
→ `deterministic diagnostic outcome`
→ `action_completed`
→ `immutable skill_application_evidence`

The model may choose a displayed `diagnose` option, but cannot invent a target or bypass deterministic task/Skill settlement.

## Deterministic outcome v1

V1 intentionally uses no random success roll.

After the represented task is `supported` or `constrained`, authoritative Technology proficiency is converted to a bounded base factor:

`base = Technology score / 100`

The already-declared Cognitive / Performance Modifier contract shapes only allowed outcome dimensions:

- `quality_precision = base × precision multiplier`
- `information_gained = base × reasoning_quality multiplier`
- `partial_failure_recovery = base × mean(reasoning_quality, adaptation multipliers)`

All indices are clamped to `0..1`.

If a task is `constrained` solely because a supporting resource is absent, this specific represented runtime applies an explicit `0.92` support multiplier to outcome indices. This does not modify the learned Skill score and does not turn a missing required resource into a pass.

Outcome class is deterministic from the minimum resolved index:

- `strong` at or above `0.80`
- `solid` at or above `0.65`
- `limited` at or above `0.45`
- otherwise `poor`

These are gameplay result labels, not new Skill grades or competency scores.

## IQ and supporting factors

IQ participates only through the explicit Technology cognitive-performance contract. It cannot:

- create Technology proficiency;
- create technical Knowledge;
- satisfy missing task/resource/target requirements;
- upgrade an unsupported task to supported;
- create a new action option by itself.

A very high-IQ actor with no authoritative Technology Skill row must fail closed.

## Evidence

A completed valid diagnostic action records:

1. the normal immutable `action_completed` event, enriched with the represented-task outcome and `skill_application` payload;
2. a distinct immutable `skill_application_evidence` event linked to the same action and caused by the completion event.

The application evidence contains task identity/revision, Skill/application, target identity/definition, challenge class, capability status, outcome class/indices, and duration.

`learning_evidence` is explicitly `false`.

This slice does not award XP, change Technology score, reinterpret historical actions, or activate implicit progression from generic application evidence.

## Transaction safety

Technology represented-task settlement occurs before the action completion transaction commits. Invalid exact target binding or missing authoritative Skill capability causes an explicit rollback so action-instance, simulation-time, physiology, and evidence mutations are not persisted.

Reusing an already completed `action_id` remains idempotent through the existing action lifecycle and does not duplicate application evidence.

## Cognition boundary

Cognition already receives full Skill/application semantics, current behavioral anchors, supporting Attributes, and general reasoning context from Cognition Capability Awareness v1. When the actor is colocated with the simulator, the ordinary authoritative `action_options` surface exposes `diagnose` against the exact target.

The character therefore has both:

- semantic awareness of what the represented Technology application means;
- a concrete legal world action when the relevant target is physically available.

In-world reasons should remain natural rather than referring to hidden game scores/grades.

## Production safety

Deployment may seed the simulator/action definition, but validation must not move the live actor or force a diagnostic action. Production verification is read-only: service health, seeded object/action presence where available, unchanged Skill state, and intact autonomy/cognition configuration.

## Follow-on direction

After this exemplar is proven:

1. close the runtime/docs checkpoint;
2. generalize the represented Skill application settlement pattern where structural equivalence is proven;
3. batch additional low-risk represented Skill tasks by pattern rather than repeating bespoke one-off plumbing;
4. consider true scored child Skills only when application-level evidence demonstrates independent progression/retention needs.
