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

Latest runtime deployment: **Deploy #200 / run `31872355878` SUCCESS**, Skill Application Requirements v1, PR #113 merge `7cfe07dc32764d322942b21748a0d26ebb8a46f7`.

Verified:
- PR CI #807 / run `31872236989`: SUCCESS;
- Skill Application Requirements Acceptance #1 / run `31872237030`: SUCCESS;
- Skill Definition Format Acceptance #3 / run `31872236960`: SUCCESS;
- Strength Live Cycle #37 / run `31872236988`: SUCCESS;
- Public Security #67 / run `31872236958`: SUCCESS;
- post-merge Application Requirements Acceptance #2 / run `31872355880`: SUCCESS;
- post-merge Skill Definition Format Acceptance #4 / run `31872355871`: SUCCESS;
- post-merge CI #808 / run `31872355861`: SUCCESS;
- service healthy, schema v5, autonomy normal 1.0x, Telegram/cognition intact;
- Technology remained `82.0 / A Advanced`.

No live capability/action behavior changed in PR #113; it adds executable requirement metadata only.

## Completed Skill foundation

Recent Skill checkpoints:
- Hand-to-Hand Skill Progression Foundation v1 — PR #104 / Deploy #196;
- Tactical Planning Skill Progression v1 — PR #106 / Deploy #197;
- Skill Evidence Semantics v1 / Technology practice — PR #108 / Deploy #198;
- Skill Definition & Capability Framework research/design — PR #110;
- Skill Creation Format v1 / Technology definition — PR #111 / Deploy #199;
- **Skill Application Requirements v1 — PR #113 / Deploy #200**.

Canonical docs:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`
- `docs/SKILL_EVIDENCE_SEMANTICS_V1.md`
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`

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

## Skill Creation Format + executable application requirements

Every first-class Skill Definition is validator-backed for identity, scope, relations, Knowledge/Ability dependencies, applications, E/D/C/B/A/S behavioral anchors, challenge classes, effects, risk, evidence, transfer, retention hooks, presentation and provenance.

Technology is the first definition and currently declares one application:
`diagnose_known_system_fault`.

Technology v1.1 executable requirements:
- context tags all: `technical_system_represented`, `diagnostic_evidence_available`;
- resource capabilities any: `diagnostic_interface`, `diagnostic_instrumentation`;
- supporting resource: `technical_documentation`;
- Knowledge mode: `declarative_support_only` with the Skill's declared Knowledge keys.

This prevents a future deterministic resolver from parsing prose or hiding equivalent constants. No Knowledge score is invented.

Underlying Technology supporting Attributes remain:
- `raps_ia.problem_solving`
- `raps_ma.focus`

Legacy `raps_ia.technological_aptitude` remains compatibility provenance only, not a second Technology authority.

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

1. **Technology Capability Resolution exemplar — NEXT**;
2. prove one deterministic assessment for `diagnose_known_system_fault`;
3. batch remaining current Skill Definitions by the proven format/resolution pattern;
4. resume missing Field Medicine/Survival/Weapons evidence/progression only after definitions exist;
5. Skill Retention/Reacquisition;
6. intellectual attributes, mental/emotion dynamics, broader social/relationship systems as later justified.

## Technology Capability Resolution exemplar — NEXT

Minimum invariant:
`declared Technology application + actor Technology proficiency + machine-readable context/resources + declared supporting Attributes + challenge -> deterministic capability assessment -> bounded outcome dimensions + immutable application evidence when actually applied`

First resolver boundary:
- one application only: `diagnose_known_system_fault`;
- definition-driven challenge eligibility from the actor's current E–S capability anchor;
- required context/resource checks from `requirements`, never prose parsing;
- Knowledge stays declarative support only; no hidden score/gate;
- supporting Attributes are exposed as declared inputs but must not alter eligibility through hidden weighting constants—add explicit modifier semantics first if/when needed;
- assessment class should be small and deterministic, e.g. `supported`, `constrained`, `unsupported`;
- no random success probability, second competency score, new XP formula, or LLM authority;
- no high-risk live authorization from Skill score alone;
- reusable actor/skill/application IDs only.

The assessment can be proven as a pure deterministic layer before adding a new live action/target if that keeps the exemplar bounded.

## Deferred boundaries

Do not add as side effects a full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior, deep crafting, partnered sexual behavior, detailed endocrine simulation, second production character solely for testing, or Tahoe exterior traversal.

## Exact resume point

**Skill Application Requirements v1 is complete/deployed through PR #113 / Deploy #200. Technology has a validated universal definition plus machine-readable executable requirements. Next: implement one bounded pure deterministic Technology Capability Resolution assessment for `diagnose_known_system_fault`, then decide the minimum safe integration point for actual application evidence.**
