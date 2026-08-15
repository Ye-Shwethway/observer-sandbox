# Technology Represented Diagnostic Task Runtime v1

Status: **COMPLETE / DEPLOYED**
Date: 2026-08-15
Implementation: PR #126
Merge: `6009fe5805843418d3590c2929476f600dfcadea`
Deployment: Deploy #208 SUCCESS

## Purpose

This slice is the first end-to-end gameplay consumer of the Skill Definition / Capability foundation. It turns the read-only Technology diagnostic exemplar into a represented selectable deterministic simulation action without making model prose or raw Skill scores state-mutation authority.

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

Capabilities:
- `inspect`
- `diagnose`
- `diagnostic_interface`
- `technical_documentation`.

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
→ `immutable skill_application_evidence`.

The model may choose a displayed `diagnose` option, but cannot invent a target or bypass deterministic task/Skill settlement.

## Deterministic outcome v1

V1 uses no random success roll.

After the represented task is supported or constrained, authoritative Technology proficiency becomes a bounded base factor:
`base = Technology score / 100`

Declared cognitive/performance dimensions shape only allowed outcome fields:
- `quality_precision = base × precision multiplier`
- `information_gained = base × reasoning_quality multiplier`
- `partial_failure_recovery = base × mean(reasoning_quality, adaptation multipliers)`.

Indices clamp to `0..1`.

If the task is constrained solely by absent supporting resource, this represented runtime uses explicit support multiplier `0.92`. This does not modify learned Skill and cannot bypass a missing required resource.

Outcome class is deterministic from the minimum resolved index:
- `strong` >= 0.80
- `solid` >= 0.65
- `limited` >= 0.45
- otherwise `poor`.

These are task-result labels, not Skill grades or a second competency score.

## IQ / supporting-factor boundary

IQ participates only through the explicit Technology modifier contract. It cannot create Technology proficiency/Knowledge, satisfy missing target/resource/context requirements, upgrade unsupported capability, or create action access.

A high-IQ actor with no authoritative Technology Skill row fails closed.

## Evidence

A completed valid diagnostic action records:
1. normal immutable `action_completed`, enriched with represented-task outcome and `skill_application` payload;
2. distinct immutable `skill_application_evidence` linked to the same action/completion event.

Evidence includes task identity/revision, Skill/application, exact target, challenge, capability status, outcome class/indices and duration.

`learning_evidence` is explicitly false. This runtime does not award XP, modify Technology score, reinterpret historical actions, or turn generic application into progression.

## Transaction safety

Represented-task settlement occurs before action completion commits. Invalid exact target binding or unsupported Skill capability causes rollback so action-instance, time, physiology and evidence mutations are not persisted.

Completed `action_id` retries remain idempotent and do not duplicate application evidence.

## Cognition boundary

Cognition receives semantic Skill/application awareness and reasoning context. A concrete legal `diagnose` action appears only when the actor is colocated with the exact represented target. In-world reasons remain natural rather than exposing hidden scores/grades.

## Production verification

Deploy #208 seeded the simulator/action without moving the live actor or forcing a diagnostic action. Later sanitized readback confirmed the simulator/action remained present through Deploy #209. Parent Skill values remained unchanged.

## Follow-on direction

Technology is now the proven first represented gameplay exemplar. The next slice is Tactical Planning `assess_tactical_situation`, using a distinct represented tactical scenario/simulator. It should reuse only structurally proven runtime seams, declare its own relevant cognitive factors/outcomes, keep application evidence separate from learning evidence, and avoid child Skill creation or forced production action proof.
