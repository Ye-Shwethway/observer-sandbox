# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Runtime/code/config plus verified production are authoritative over remembered chat.
- AI proposes structured cognition; deterministic engines validate and mutate.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are exemplars, never reusable-engine identity.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never manipulate production merely to manufacture evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #203 / run `31873525050` SUCCESS**, Represented Skill Task Contract v1, PR #119 merge `5dd49824e75adce40f374822bf9dc5383ad7532e`.

Verified:
- PR Represented Task Acceptance #1 / `31873487399`: SUCCESS;
- PR CI #819 / `31873487361`: SUCCESS;
- Strength Live Cycle #38 / `31873487388`: SUCCESS;
- Public Security #73 / `31873487376`: SUCCESS;
- post-merge Represented Task Acceptance #2 / `31873525048`: SUCCESS;
- post-merge CI #820 / `31873525036`: SUCCESS;
- Deploy #203 / `31873525050`: SUCCESS;
- service healthy, schema v5, autonomy normal 1.0x, Telegram/cognition intact;
- Technology remained `82.0 / A Advanced`.

PR #119 added definition/validation artifacts only. No represented task entity or action was seeded, so production behavior intentionally remained unchanged.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. RAPS skill-like fields are not independent mutable Skill truth.

## Completed Skill execution chain

1. H2H Skill Progression v1 — PR #104 / Deploy #196
2. Tactical Planning Skill Progression — PR #106 / Deploy #197
3. Skill Evidence Semantics / Technology practice — PR #108 / Deploy #198
4. Skill Definition & Capability Framework — PR #110
5. Skill Creation Format / Technology definition — PR #111 / Deploy #199
6. Skill Application Requirements — PR #113 / Deploy #200
7. Technology Capability Resolution — PR #115 / Deploy #201
8. Actor-backed Skill Capability Adapter — PR #117 / Deploy #202
9. **Represented Skill Task Contract v1 — PR #119 / Deploy #203**

Canonical stack:
- `config/skill_definitions.v1.json`
- `src/observer_sandbox/skill_definitions.py`
- `src/observer_sandbox/skill_application_requirements.py`
- `src/observer_sandbox/skill_capability.py`
- `src/observer_sandbox/actor_skill_capability.py`
- `config/represented_skill_tasks.v1.json`
- `src/observer_sandbox/represented_skill_tasks.py`

Canonical docs include `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`, `SKILL_CREATION_FORMAT_V1.md`, `SKILL_APPLICATION_REQUIREMENTS_V1.md`, `SKILL_CAPABILITY_RESOLUTION_V1.md`, `ACTOR_SKILL_CAPABILITY_ADAPTER_V1.md`, and `REPRESENTED_SKILL_TASK_CONTRACT_V1.md`.

## Technology exemplar

Application: `diagnose_known_system_fault`.

Skill application requirements:
- context all: `technical_system_represented`, `diagnostic_evidence_available`;
- resource any: `diagnostic_interface` or `diagnostic_instrumentation`;
- supporting: `technical_documentation`;
- Knowledge: `declarative_support_only`;
- supporting Attributes: `raps_ia.problem_solving`, `raps_ma.focus`.

Pure capability resolver returns `supported / constrained / unsupported`; definition anchors own challenge support. Knowledge is non-gating; Attributes are transparent/non-weighted until explicit modifier semantics exist. No probability, action authorization, second competency score, XP mutation, or LLM authority.

Actor-backed adapter reads only authoritative `character_skills.score` and definition-declared Attribute fields. It is read-only, fails closed on missing Skill state, and never guesses task context/resources.

## Represented Skill Task Contract v1

The Skill Definition defines what an application means. The Represented Task Definition defines one concrete world-task contract.

First task:
`technology_known_system_fault_diagnostic_sim_v1`

- skill/application: `technology.diagnose_known_system_fault`
- challenge: `standard`
- mode/risk: `simulation_safe` / `low`
- exact target definition: `represented_task:technology_known_fault_diagnostic_simulator_v1`
- required target capability: `inspect`
- context: represented technical system + diagnostic evidence
- required resource: `diagnostic_interface`
- supporting resource: `technical_documentation`
- outcomes: feasibility, quality precision, information gained, partial failure recovery
- application evidence deferred; learning evidence explicitly false.

Validator prevents task definitions from weakening Skill application requirements, escaping challenge/effect envelopes, embedding actor state, or promoting `skill_practice:*` targets into application authority. Names/model prose are never target authority.

Existing Systems Diagnostic Practice Console remains **practice/learning evidence only** and must not be reused as application authority.

## Current broad Skill set / audit

Current actor Skill rows:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Audit result:
- Technology is the only current Skill with a complete validator-backed universal Skill Definition and executable application contract;
- Hand-to-Hand Combat and Tactical Planning have legitimate progression mechanics/evidence but do not yet have complete universal Skill Definitions/applications/behavioral anchors;
- Weapons, Survival, and Field Medicine currently have actor Skill state but no complete Skill Definition and no activated progression evidence path;
- therefore broad gameplay integration should not treat the remaining umbrella score names as sufficient task semantics.

Never fabricate child scores from parent values.

## Skill Definition Refactor Batch v1 — NEXT

Before broad gameplay integration, batch the five remaining current umbrella Skills through the already-proven Technology definition format:
- `hand_to_hand_combat`
- `weapons`
- `survival`
- `tactical_planning`
- `field_medicine`

Each definition should add:
- stable universal meaning and explicit scope includes/excludes;
- safe supporting Ability/Attribute dependencies without reusing legacy skill-like RAPS aliases as second Skill truth;
- E/D/C/B/A/S behavioral proficiency anchors;
- two bounded gameplay application families as the initial subskill-like surface;
- executable context/resource requirements for each application;
- allowed outcome dimensions and risk/consequence boundaries;
- explicit learning-evidence policy and compatibility provenance.

Initial application families should stay compact:
- H2H: unarmed striking; grappling/control/escape;
- Weapons: familiar melee weapon employment; familiar ranged weapon employment;
- Survival: field navigation; field sustainment;
- Tactical Planning: tactical situation assessment; tactical maneuver/contingency planning;
- Field Medicine: field casualty assessment; bounded stabilization/evacuation preparation.

These are **applications under the authoritative umbrella Skill score**, not new independently scored child Skill rows.

### Subskill policy

Do not split current parent scores into invented child scores. A true child Skill should be introduced only when:
1. its task family is meaningfully separable from the parent;
2. legitimate learning evidence can distinguish it;
3. progression/retention can be owned independently;
4. parent/child aggregation and migration semantics are explicit.

Until then, applications provide gameplay granularity without fabricating actor state. `component_skills` may remain empty in this batch.

Existing legitimate progression must remain intact:
- H2H existing eligible methods remain authoritative learning evidence;
- Tactical Planning existing eligible methods remain authoritative learning evidence;
- Technology remains unchanged except cross-registry validation as needed;
- Weapons/Survival/Field Medicine definitions must not invent learning evidence merely to make the batch symmetrical.

## Revised development sequence

1. **Skill Definition Refactor Batch v1 — NEXT**;
2. validate all six current umbrella Skills under one consistent definition/application contract while preserving actor scores and existing evidence;
3. Represented Skill Task Instance Resolver v1 — generic read-only target-instance binding;
4. add one distinct Technology simulator entity plus bounded action/application-evidence integration;
5. apply the proven represented-task/action pattern to other Skills by evidence/task pattern rather than one PR per Skill;
6. add missing Weapons/Survival/Field Medicine learning evidence/progression only when legitimate represented practice/task evidence exists;
7. later Skill retention/reacquisition and justified true subskill promotion;
8. later intellectual attributes, mental/emotion dynamics and broader social/relationship systems.

## Represented Skill Task Instance Resolver v1 — AFTER REFACTOR BATCH

Invariant:
`actor + task_id + target_entity_id + explicit available resource capabilities -> validate exact target type/definition/capabilities -> derive task challenge/context -> actor-backed Skill capability assessment -> read-only represented-task assessment`

Constraints remain:
- exact `definition_id`; no name/prose matching;
- fail closed on target mismatch;
- do not reuse practice console;
- synthetic target/entity tests are sufficient; no production seed for proof;
- available resource capabilities remain explicit until represented resource ownership is separately proven;
- no writes, action authorization, events/evidence, XP, autonomy or Telegram integration.

## Deferred boundaries

No full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior, deep crafting, partnered sexual behavior, detailed endocrine simulation, second production character solely for testing, or Tahoe exterior traversal as side effects.

## Exact resume point

**Represented Skill Task Contract v1 is complete/deployed through PR #119 / Deploy #203. Before broad task/action integration, implement Skill Definition Refactor Batch v1 for H2H, Weapons, Survival, Tactical Planning and Field Medicine using Technology as the proven exemplar. Preserve all current parent scores; use applications rather than fabricated scored subskills.**
