# Represented Skill Task Instance Resolver v1

Status: **COMPLETE / DEPLOYED**
Date: 2026-08-15
Implementation: PR #123
Merge: `a5e7f268e5ecbffc0101eb20ee1daaa9723d0b90`
Deployment: Deploy #205 / run `31875288660` SUCCESS

## Purpose

Bind one validated represented Skill task definition to one concrete world entity and one actor's authoritative Skill state without authorizing or executing an action.

Canonical module:
`src/observer_sandbox/represented_skill_task_instance.py`

## Invariant

`actor + represented task + exact target entity + explicit available resource capabilities -> target contract validation -> task resource envelope -> actor-backed Skill capability assessment -> read-only represented-task assessment`

## Authority boundaries

The represented task owns Skill/application id, challenge class, required context tags, target type/definition/capability contract, and task-specific required/supporting resource envelope.

The concrete entity owns its id, entity type, exact `definition_id`, and advertised capabilities.

The actor-backed Skill adapter owns authoritative `character_skills.score`, definition-declared supporting Attribute reads, and pure Skill application capability resolution.

The caller owns the explicit resource capabilities available for assessment. V1 does not infer resources from inventory, location, object names, prose, or model output.

## Target binding

Binding fails closed before Skill assessment unless:
- the target exists;
- entity type exactly matches;
- `definition_id` exactly matches;
- all task-required target capabilities are advertised.

Names and model prose are never target authority. A `skill_practice:*` target cannot satisfy the represented Technology task.

## Task resource envelope

The Skill application may be broader than one represented task. Caller resource capabilities are therefore filtered through the represented task's required + supporting envelope before actor Skill resolution.

For the Technology exemplar, the generic application accepts `diagnostic_interface` or `diagnostic_instrumentation`, while the represented task intentionally requires `diagnostic_interface`. Generic instrumentation cannot bypass that narrower task contract.

## Status semantics

- `unsupported` — required context/resource or proficiency/challenge support is missing;
- `constrained` — hard gates pass but supporting resources are absent;
- `supported` — hard gates pass and declared support resources are available.

Target-binding mismatches are contract errors and fail closed. The resolver introduces no second score or probability model.

## Read-only boundary

This resolver performs no writes and emits no events/history/application evidence/learning evidence. It does not authorize actions, seed targets, change Skill score/experience, mutate targets, or change autonomy/Telegram state.

## Acceptance

Focused acceptance proved:
- exact target + required/supporting resources -> supported;
- missing required task resource -> unsupported;
- missing support -> constrained;
- broader application resource cannot bypass task requirements;
- wrong definition/type/capability/missing target -> fail closed;
- practice target cannot masquerade as application target;
- assessment leaves events, profile history, Skill score and target state unchanged.

## Follow-on completed

This read-only seam became the foundation for Cognition Capability Awareness, bounded Cognitive / Performance Modifiers, and Technology Represented Diagnostic Task Runtime v1. The Technology runtime was later deployed through PR #126 / Deploy #208 without changing this resolver's read-only assessment contract.
