# Cognition Capability Awareness v1

Status: **COMPLETE / DEPLOYED**
Date: 2026-08-15
Implementation: PR #124
Merge: `29c4aa1f8fc46815786cc3871bd5998564314209`
Deployment: Deploy #206 SUCCESS

## Purpose

Observer Sandbox Skill semantics must be available to character cognition as well as deterministic runtime validation. A character that receives only a raw numeric Skill score cannot reason consistently about scope, applications, challenge limits, required context/resources, or boundaries.

Cognition Capability Awareness v1 provides a read-only semantic projection of authoritative actor Skill state plus universal Skill Definitions into model decision context.

## Invariant

Cognition receives enough semantic context to reason about what the actor plausibly knows how to attempt, while deterministic engines retain authority over legality, capability assessment, outcomes, evidence, progression, and state mutation.

The model may reason from capability context. It may not turn that context into authority.

## Skill awareness

For every actor Skill with a canonical definition, cognition receives:
- Skill identity/category and authoritative current score;
- current generic E-S grade and Skill-specific behavioral anchor;
- supported challenge classes and stated limits;
- definition scope plus explicit includes/excludes;
- executable application families;
- application challenge/context/resource/risk semantics;
- declared supporting Attribute values/relationships;
- declared Knowledge keys as semantic support context only.

An actor Skill row without a canonical definition is reported unresolved rather than interpreted from prose.

## Reasoning profile

V1 exposes bounded decision context including:
- `raps_ia.iq`
- `raps_ia.problem_solving`
- `raps_ma.focus`
- `raps_ma.adaptability`
- `raps_ia.creativity`
- `raps_ma.emotional_stability`
- `raps_ma.stress_management`
- `raps_ia.tactical_thinking`.

## IQ boundary

IQ is not Knowledge and is not learned Skill. It must not:
- create technical/medical/etc. Knowledge;
- change an authoritative Skill score by hidden arithmetic;
- authorize applications outside the Skill Definition;
- bypass target/resource/safety/challenge/consequence rules;
- become a universal bonus to unrelated tasks.

Numeric task effects are owned by explicit Cognitive / Performance Modifier contracts, not by this awareness projection.

## Knowledge boundary

Observer Sandbox does not yet have a first-class actor Knowledge subsystem. Skill-definition Knowledge dependencies remain declarative support only. Cognition may see relevant concepts, but runtime must not fabricate hidden Knowledge scores or numeric gates.

## In-world presentation boundary

Raw scores/grades are machine decision context, not an in-world UI. Character-grounded reasons should remain natural rather than exposing hidden game-stat phrasing.

## Integration

`ModelDecisionProvider._enrich_state()` adds `capability_awareness` to cognition state. Existing authoritative `action_options` remain the selectable action/target surface.

Separation:
`character cognition awareness -> proposes a plausible option`

while:
`deterministic action/task/capability engines -> validate and mutate`.

## Read-only boundary

The awareness builder writes nothing, emits no evidence/events, changes no Skill/profile value, and does not itself alter action availability or represented-task outcomes.

## Follow-on completed

Cognitive / Performance Modifier Contract v1 was deployed through PR #125 / Deploy #207, and Technology Represented Diagnostic Task Runtime v1 through PR #126 / Deploy #208. The next represented gameplay exemplar is Tactical Planning `assess_tactical_situation`.
