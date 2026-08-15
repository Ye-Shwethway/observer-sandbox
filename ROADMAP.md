# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Runtime/code/config plus verified live production are authoritative over remembered chat.
- AI proposes structured cognition; deterministic engines validate and mutate.
- Telegram is observer/control, never simulation authority.
- Preserve the LEGO contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are exemplars, never reusable-engine identity.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never mutate or accelerate production merely to manufacture evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #202 / run `31873159944` SUCCESS**, Actor-backed Skill Capability Assessment Adapter v1, PR #117 merge `07b43a20f28c75cccb150f01cd8f071a5a3a08d9`.

Verified:
- PR Actor Skill Capability Adapter Acceptance #1 / run `31873122885`: SUCCESS;
- PR CI #815 / run `31873122797`: SUCCESS;
- Public Readiness Security Audit #71 / run `31873122839`: SUCCESS;
- post-merge Actor Skill Capability Adapter Acceptance #2 / run `31873159937`: SUCCESS;
- post-merge CI #816 / run `31873159939`: SUCCESS;
- Deploy #202 / run `31873159944`: SUCCESS;
- service healthy/active, schema v5, autonomy normal 1.0x;
- Telegram/cognition intact;
- Technology remained `82.0 / A Advanced`.

The adapter is deployed as a read-only library and is not called by the autonomy/service loop. No live action capability, Skill score/XP, profile value, or evidence was mutated merely to prove it.

## Completed Skill foundation

Recent Skill checkpoints:
- Hand-to-Hand Skill Progression Foundation v1 — PR #104 / Deploy #196;
- Tactical Planning Skill Progression v1 — PR #106 / Deploy #197;
- Skill Evidence Semantics v1 / Technology practice — PR #108 / Deploy #198;
- Skill Definition & Capability Framework research/design — PR #110;
- Skill Creation Format v1 / Technology definition — PR #111 / Deploy #199;
- Skill Application Requirements v1 — PR #113 / Deploy #200;
- Technology Capability Resolution v1 — PR #115 / Deploy #201;
- **Actor-backed Skill Capability Assessment Adapter v1 — PR #117 / Deploy #202**.

Canonical docs:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`
- `docs/SKILL_EVIDENCE_SEMANTICS_V1.md`
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`
- `docs/SKILL_CAPABILITY_RESOLUTION_V1.md`
- `docs/ACTOR_SKILL_CAPABILITY_ADAPTER_V1.md`

## Skill authority / ontology

Actor state:
- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = accumulated legitimate learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Universal meaning:
- `config/skill_definitions.v1.json` + validator-backed definitions.

Canonical distinctions remain:
- Ability/Attribute = underlying capacity;
- Knowledge = facts/concepts/procedures known;
- Skill = learned capacity to apply knowledge/abilities to observable task families;
- Task/Application = work attempted with challenge/context/resources/risk;
- Competency/Demonstrated Capability = real-context reliability evidence, not a second score;
- Learning Evidence = immutable progression-eligible evidence;
- Proficiency = actor Skill score interpreted by skill-specific behavioral anchors.

RAPS skill-like fields are not independent mutable Skill truth. Model prose and Telegram do not mutate proficiency.

## Technology executable definition

Technology is the first complete universal Skill Definition. First application:
`diagnose_known_system_fault`.

Technology v1.1 executable requirements:
- all context tags: `technical_system_represented`, `diagnostic_evidence_available`;
- any required resource capability: `diagnostic_interface`, `diagnostic_instrumentation`;
- supporting resource: `technical_documentation`;
- Knowledge mode: `declarative_support_only`.

Supporting Attributes:
- `raps_ia.problem_solving`
- `raps_ma.focus`

Legacy `raps_ia.technological_aptitude` is compatibility provenance only, not a second Technology authority.

## Capability Resolution v1

Pure resolver:
`src/observer_sandbox/skill_capability.py`

Invariant:
`Skill Definition + proficiency + grade anchor + requested challenge + explicit context/resources + declared supporting inputs -> supported / constrained / unsupported`

Locks:
- no scattered numeric capability thresholds;
- challenge support comes from definition anchors;
- Knowledge is declarative/non-gating;
- Attributes are transparent non-weighted inputs until explicit modifier semantics exist;
- no probability, second competency score, action authorization, learning mutation, or LLM authority.

## Actor-backed Capability Adapter v1

Read-only adapter:
`src/observer_sandbox/actor_skill_capability.py`

Invariant:
`actor_id + skill_id + application_id + explicit challenge/context/resources -> authoritative actor Skill/Profile reads -> pure resolver -> read-only assessment`

Behavior:
- reads `character_skills.score` only for Skill proficiency;
- reads only definition-declared Attribute fields;
- ignores unrelated profile fields;
- missing declared Attribute rows remain explicit `None` under current non-gating semantics;
- malformed declared numeric fields fail clearly;
- missing authoritative Skill state fails closed instead of fabricating a score;
- caller/task contract owns challenge/context/resource tokens; adapter does not guess them from inventory, location, names or prose;
- assessments emit no events/history/evidence and perform no writes.

Focused tests use a generic synthetic actor, not Darian as implementation identity.

## Current broad Skill set

Preserve as umbrella Skills until justified decomposition:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Never fabricate child Skill scores from a parent value.

## Next development sequence

1. **Represented Technology Task Contract audit/exemplar — NEXT**;
2. determine whether existing object/action semantics can truthfully supply application id, challenge, context/resource capabilities and target identity;
3. if not, add the smallest generic represented-task contract first;
4. then implement one bounded `diagnose_known_system_fault` application/action evidence integration;
5. batch remaining current Skill Definitions after the full definition->assessment->represented-task pattern is proven;
6. resume missing Field Medicine/Survival/Weapons evidence/progression only after definitions exist;
7. Skill Retention/Reacquisition;
8. later intellectual attributes, mental/emotion dynamics and broader social/relationship systems as justified.

## Represented Technology Task Contract — NEXT

Audit existing actions, object capabilities/definitions, conditions/resources/modifiers and target validation before mutation.

Required task facts for a truthful `diagnose_known_system_fault` exemplar:
- stable application id;
- represented target/system identity;
- challenge class;
- explicit required context tags;
- explicit resource capability tokens;
- bounded outcome dimensions and evidence semantics.

Do not infer these facts from object names or LLM prose. Do not make Skill assessment itself action authorization. If the existing action/object architecture lacks a generic machine-readable source for these facts, add one minimum contract rather than hiding Technology constants in the action engine.

## Deferred boundaries

Do not add as side effects a full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior, deep crafting, partnered sexual behavior, detailed endocrine simulation, second production character solely for testing, or Tahoe exterior traversal.

## Exact resume point

**Actor-backed Skill Capability Assessment Adapter v1 is complete/deployed through PR #117 / Deploy #202. Next audit and prove the minimum represented Technology task contract for `diagnose_known_system_fault`; do not yet wire a generic Skill action engine or batch other Skill definitions.**
