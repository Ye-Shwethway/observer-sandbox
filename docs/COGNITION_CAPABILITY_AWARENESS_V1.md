# Cognition Capability Awareness v1

Status: implementation candidate

## Purpose

Observer Sandbox Skill semantics must be available to character cognition as well as deterministic runtime validation. A character that has an authoritative Skill state but receives only a raw numeric score in model context cannot reason consistently about the Skill's scope, applications, challenge limits, required context, resources, or failure boundaries.

Cognition Capability Awareness v1 provides a read-only semantic projection of authoritative actor Skill state plus universal Skill Definitions into model decision context.

## Invariant

Cognition receives enough semantic context to reason about what the actor plausibly knows how to attempt, while deterministic engines retain authority over legality, capability assessment, outcomes, evidence, progression, and state mutation.

The model may reason from capability context. The model may not turn that context into authority.

## Skill awareness

For every actor Skill with a canonical Skill Definition, cognition receives:

- Skill identity, category, and authoritative current score;
- current generic E-S grade and Skill-specific behavioral anchor;
- supported challenge classes and stated limits at that anchor;
- affirmative Skill definition plus explicit includes/excludes;
- executable application families;
- application challenge classes, required context, resource contracts, and risk/failure context;
- declared supporting Attribute values and relationships;
- declared Knowledge keys as semantic support context only.

An actor Skill row without a canonical definition is reported as unresolved rather than being invented or interpreted from prose.

## Reasoning profile

V1 also exposes a bounded reasoning profile to cognition:

- `raps_ia.iq` — general reasoning capacity;
- `raps_ia.problem_solving`;
- `raps_ma.focus`;
- `raps_ma.adaptability`;
- `raps_ia.creativity`;
- `raps_ma.emotional_stability`;
- `raps_ma.stress_management`;
- `raps_ia.tactical_thinking`.

These values are decision context only in v1.

### IQ boundary

IQ is not Knowledge and is not a learned Skill. A high IQ may later participate in explicitly authored planning/reasoning modifier contracts, but it must not:

- create technical or medical Knowledge the actor does not have;
- increase an authoritative Skill score by hidden arithmetic;
- authorize an application outside the Skill Definition;
- bypass target, resource, safety, challenge, or consequence rules;
- become a universal bonus to unrelated tasks.

No IQ normalization or outcome formula is introduced by this slice.

## Knowledge boundary

Observer Sandbox does not yet have a first-class actor Knowledge subsystem. Skill Definition Knowledge dependencies therefore remain `declarative_support_only`. Cognition may see the relevant Knowledge concepts, but the runtime must not fabricate hidden actor Knowledge scores or numeric Knowledge gates.

## In-world presentation boundary

Raw scores and grade letters are machine decision context. Model reasoning should use them to calibrate plausibility, not speak as though the simulated character sees a game UI. In-world action reasons should remain natural and character-grounded rather than saying, for example, "my Technology is 82/A."

## Read-only boundary

The awareness builder:

- performs no writes;
- emits no events;
- emits no application or learning evidence;
- changes no Skill score/experience;
- changes no profile value;
- changes no action availability by itself;
- changes no represented task result by itself.

## Cognition integration

`ModelDecisionProvider._enrich_state()` adds `capability_awareness` to the state serialized into the cognition request. Existing `action_options` remain authoritative for selectable action/target pairs.

This creates the intended separation:

`character cognition awareness -> proposes a plausible option`

while:

`deterministic action/task/capability engines -> validate and mutate`

## Next slice

After this slice is proven and deployed, add **Cognitive / Performance Modifier Contract v1** before using IQ or supporting Attributes numerically in represented task outcomes. The contract must be explicit, bounded, task/Skill-specific, and must preserve learned Skill authority.

The first end-to-end consumer remains **Technology Represented Diagnostic Task Runtime v1**.
