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

Latest runtime deployment: **Deploy #201 / run `31872775593` SUCCESS**, Technology Capability Resolution v1, PR #115 merge `2609d4bde93d0a188db4ff398a90792b1cec759d`.

Verified:
- PR Technology Capability Resolution Acceptance #1 / run `31872730382`: SUCCESS;
- PR CI #811 / run `31872730342`: SUCCESS;
- Public Readiness Security Audit #69 / run `31872730326`: SUCCESS;
- post-merge Technology Capability Resolution Acceptance #2 / run `31872775640`: SUCCESS;
- post-merge CI #812 / run `31872775683`: SUCCESS;
- Deploy #201 / run `31872775593`: SUCCESS;
- service healthy/active, schema v5, autonomy normal 1.0x;
- Telegram/cognition intact;
- Technology remained `82.0 / A Advanced`.

The deployed resolver is a pure deterministic library. No live action authorization, target mutation, Skill XP/score mutation, or forced production capability event was added in PR #115.

## Completed Skill foundation

Recent Skill checkpoints:
- Hand-to-Hand Skill Progression Foundation v1 — PR #104 / Deploy #196;
- Tactical Planning Skill Progression v1 — PR #106 / Deploy #197;
- Skill Evidence Semantics v1 / Technology practice — PR #108 / Deploy #198;
- Skill Definition & Capability Framework research/design — PR #110;
- Skill Creation Format v1 / Technology definition — PR #111 / Deploy #199;
- Skill Application Requirements v1 — PR #113 / Deploy #200;
- **Technology Capability Resolution v1 — PR #115 / Deploy #201**.

Canonical docs:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`
- `docs/SKILL_EVIDENCE_SEMANTICS_V1.md`
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`
- `docs/SKILL_CAPABILITY_RESOLUTION_V1.md`

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

## Skill Definition + executable application requirements

Every first-class Skill Definition is validator-backed for identity, scope, relations, Knowledge/Ability dependencies, applications, E/D/C/B/A/S behavioral anchors, challenge classes, effects, risk, evidence, transfer, retention hooks, presentation and provenance.

Technology is the first definition and currently declares one application:
`diagnose_known_system_fault`.

Technology v1.1 executable requirements:
- context tags all: `technical_system_represented`, `diagnostic_evidence_available`;
- resource capabilities any: `diagnostic_interface`, `diagnostic_instrumentation`;
- supporting resource: `technical_documentation`;
- Knowledge mode: `declarative_support_only` with the Skill's declared Knowledge keys.

Underlying Technology supporting Attributes:
- `raps_ia.problem_solving`
- `raps_ma.focus`

Legacy `raps_ia.technological_aptitude` remains compatibility provenance only, not a second Technology authority.

## Technology Capability Resolution v1

Pure resolver:
`src/observer_sandbox/skill_capability.py`

Invariant:
`Skill Definition + proficiency + current grade anchor + requested challenge + executable context/resources + declared supporting inputs -> supported / constrained / unsupported`

Semantics:
- `supported`: mandatory gates and supporting resources are satisfied;
- `constrained`: mandatory gates pass but supporting resource capability is missing;
- `unsupported`: application challenge, proficiency-anchor challenge, required context, or required-any resource gate fails.

Important boundaries:
- no scattered numeric `skill >= N` capability thresholds;
- challenge support comes from the Skill Definition's current E–S anchor;
- Knowledge is exposed as declarative support and is not numerically assessed;
- declared Attributes are transparent inputs only in v1 and do not secretly alter status;
- no random success probability;
- no second competency score;
- no action authorization;
- no learning/XP mutation;
- no LLM authority.

`diagnose_known_system_fault` does not declare `extreme`; an S Technology score therefore does not make extreme work supported or authorized by itself.

## Current broad Skill set

Preserve as umbrella Skills until justified gameplay requires decomposition:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Never fabricate child Skill scores from a parent value.

## Next development sequence

1. **Actor-backed Skill Capability Assessment Adapter v1 — NEXT**;
2. prove read-only actor-state integration with the pure resolver;
3. then choose one represented Technology application/action evidence integration if a real task/target contract can supply truthful context/resources;
4. batch remaining current Skill Definitions by the proven format/resolution pattern;
5. resume missing Field Medicine/Survival/Weapons evidence/progression only after definitions exist;
6. Skill Retention/Reacquisition;
7. intellectual attributes, mental/emotion dynamics, broader social/relationship systems as later justified.

## Actor-backed Skill Capability Assessment Adapter v1 — NEXT

Minimum invariant:
`actor_id + skill_id + application_id + explicit challenge/context/resources -> authoritative actor Skill/Profile reads -> pure capability resolver -> read-only assessment`

Constraints:
- `character_skills.score` remains proficiency authority;
- only definition-declared Attribute fields may be read as supporting inputs;
- adapter must not mutate DB, action state, Skill score/XP, or profile values;
- assessment remains distinct from action authorization;
- explicit context/resource capabilities come from caller/task context, not guessed from names or prose;
- do not emit learning/application evidence merely because an assessment was requested;
- do not add an autonomous technical action in this slice;
- generic actor/skill/application IDs only; Darian may be a fixture, never implementation identity.

Before implementation, audit existing service/read accessor patterns and reuse the smallest appropriate layer rather than embedding a parallel persistence abstraction.

## Deferred boundaries

Do not add as side effects a full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior, deep crafting, partnered sexual behavior, detailed endocrine simulation, second production character solely for testing, or Tahoe exterior traversal.

## Exact resume point

**Technology Capability Resolution v1 is complete/deployed through PR #115 / Deploy #201. The pure resolver is proven and production-safe but is not wired to live actions. Next: one read-only actor-backed Skill Capability Assessment Adapter v1, then decide the minimum truthful represented-task integration before any live Technology application evidence.**
