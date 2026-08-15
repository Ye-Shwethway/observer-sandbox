# Represented Skill Task Instance Resolver v1

Status: IMPLEMENTATION CANDIDATE
Date: 2026-08-15

## Purpose

Bind one validated represented Skill task definition to one concrete world entity and one actor's authoritative Skill state without authorizing or executing an action.

Canonical module:
`src/observer_sandbox/represented_skill_task_instance.py`

## Invariant

`actor + represented task + exact target entity + explicit available resource capabilities -> target contract validation -> task resource envelope -> actor-backed Skill capability assessment -> read-only represented-task assessment`

## Authority boundaries

The represented task owns:
- Skill/application id;
- challenge class;
- required context tags;
- target type/definition/capability contract;
- task-specific required/supporting resource capability envelope.

The concrete entity owns:
- entity id;
- entity type;
- exact `definition_id`;
- advertised capabilities.

The actor-backed Skill adapter owns:
- authoritative `character_skills.score` read;
- definition-declared Attribute reads;
- pure Skill application capability resolution.

The caller owns the explicit set of resource capabilities currently available for the assessment. v1 deliberately does not infer them from inventory, location, object names, prose, or model output.

## Target binding

Target binding is fail-closed before Skill assessment:
- target entity must exist;
- entity type must exactly match task contract;
- `definition_id` must exactly match task contract;
- all task-required target capabilities must be advertised.

Object names and model prose are never target authority. A `skill_practice:*` target cannot satisfy the Technology represented task because its definition id does not equal the represented application target definition.

## Task resource envelope

The Skill application may be broader than one represented task. Therefore caller-supplied resource capabilities are filtered through the represented task's own required + supporting resource envelope before actor Skill resolution.

For the Technology exemplar, the generic application accepts `diagnostic_interface` or `diagnostic_instrumentation`, while the represented simulator task intentionally narrows the required capability to `diagnostic_interface`. Supplying only `diagnostic_instrumentation` cannot bypass that task-specific contract.

## Status semantics

Target binding errors are contract errors and fail closed.

After a valid target binding, capability assessment remains:
- `unsupported` — required context/resource or proficiency/challenge support is missing;
- `constrained` — hard gates pass but one or more supporting resources are absent;
- `supported` — hard gates pass and declared support resources are available.

The resolver does not introduce a second score or probability model.

## Read-only boundary

v1 performs no writes and emits no events, history, action evidence, or learning evidence. It does not:
- authorize or start an action;
- seed a simulator entity;
- change Skill score or experience;
- alter target state;
- change autonomy or Telegram behavior.

Synthetic entity tests are sufficient proof for this slice.

## Acceptance

Focused acceptance proves:
- exact synthetic target + required/supporting resources -> supported;
- missing required task resource -> unsupported;
- missing supporting documentation -> constrained;
- broader application resource outside the task envelope cannot bypass task requirements;
- wrong `definition_id` -> fail closed;
- practice-console definition -> fail closed;
- wrong entity type -> fail closed;
- missing target capability -> fail closed;
- missing target -> fail closed;
- assessment leaves events, profile history, Skill score, and target contract state unchanged.

## Next

After this read-only seam is deployed and verified, the next bounded slice may seed one distinct Technology diagnostic simulator entity and integrate one represented diagnostic action/application-evidence path. Learning evidence remains separate unless explicitly justified later.
