# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-15

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

## Workflow

Default:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use **exemplar-first, then batch-by-pattern**. Never manipulate production merely to manufacture evidence. Darian/Thorne Estate are exemplars only.

## Current verified deployment

Latest runtime deployment: **Deploy #203 / run `31873525050` SUCCESS**, Represented Skill Task Contract v1, PR #119 merge `5dd49824e75adce40f374822bf9dc5383ad7532e`.

Verified:
- PR Represented Skill Task Contract v1 Acceptance #1 / `31873487399`: SUCCESS;
- PR CI #819 / `31873487361`: SUCCESS;
- Strength Live Cycle #38 / `31873487388`: SUCCESS;
- Public Security #73 / `31873487376`: SUCCESS;
- post-merge Represented Task Acceptance #2 / `31873525048`: SUCCESS;
- post-merge CI #820 / `31873525036`: SUCCESS;
- Deploy #203 / `31873525050`: SUCCESS;
- service healthy, schema v5, autonomy normal 1x, Telegram/cognition intact;
- Technology remained `82.0 / A Advanced`.

PR #119 introduced definition/validation artifacts only. No represented task entity or live action was seeded, so production behavior intentionally remained unchanged.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. RAPS skill-like fields are not independent mutable Skill truth.

## Current Skill execution stack

- `config/skill_definitions.v1.json`
- `src/observer_sandbox/skill_definitions.py`
- `src/observer_sandbox/skill_application_requirements.py`
- `src/observer_sandbox/skill_capability.py`
- `src/observer_sandbox/actor_skill_capability.py`
- `config/represented_skill_tasks.v1.json`
- `src/observer_sandbox/represented_skill_tasks.py`

Canonical docs include the Skill framework/creation/application/capability/actor-adapter docs plus `docs/REPRESENTED_SKILL_TASK_CONTRACT_V1.md` and the progression/evidence docs referenced by `ROADMAP.md`.

## Technology exemplar

Technology is the first complete gameplay-grade universal Skill Definition. Its first application is `diagnose_known_system_fault`.

Executable requirements:
- context all: `technical_system_represented`, `diagnostic_evidence_available`;
- resource any: `diagnostic_interface` or `diagnostic_instrumentation`;
- supporting resource: `technical_documentation`;
- Knowledge mode: `declarative_support_only`;
- supporting Attributes: `raps_ia.problem_solving`, `raps_ma.focus`.

Pure capability resolution returns `supported / constrained / unsupported`. Definition anchors own challenge support. Knowledge is declarative/non-gating and Attributes are transparent/non-weighted until explicit modifier semantics exist. Actor-backed assessment reads authoritative Skill/Profile state and is read-only.

## Represented Skill Task Contract v1

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
- bounded outcomes: feasibility, quality precision, information gained, partial failure recovery
- application evidence deferred; learning evidence explicitly false.

Names/model prose are never target authority. Existing Systems Diagnostic Practice Console remains practice/learning evidence only and must not be reused as application authority.

## Current Skill audit

Actor umbrella Skill rows:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Current implementation maturity:
- Technology: complete validator-backed universal definition/application contract plus progression practice;
- Hand-to-Hand Combat: legitimate progression evidence exists, but no complete universal definition/application contract yet;
- Tactical Planning: legitimate progression evidence exists, but no complete universal definition/application contract yet;
- Weapons / Survival / Field Medicine: authoritative actor scores exist, but no complete universal definition and no activated progression evidence path yet.

Therefore broad gameplay integration should not treat the remaining umbrella names/scores as sufficient task semantics.

## Next canonical slice

**Skill Definition Refactor Batch v1.**

Batch the five remaining umbrella Skills through the Technology-proven format:
- `hand_to_hand_combat`
- `weapons`
- `survival`
- `tactical_planning`
- `field_medicine`

Each receives stable meaning/scope, safe Attribute dependencies, E/D/C/B/A/S behavioral anchors, two bounded gameplay application families, executable application context/resource requirements, allowed outcome/risk boundaries, learning-evidence policy, presentation and compatibility provenance.

Initial application families:
- H2H: unarmed striking; grappling/control/escape;
- Weapons: familiar melee weapon employment; familiar ranged weapon employment;
- Survival: field navigation; field sustainment;
- Tactical Planning: tactical situation assessment; tactical maneuver/contingency planning;
- Field Medicine: field casualty assessment; bounded stabilization/evacuation preparation.

These applications are the initial subskill-like gameplay surface. **Do not create independent child Skill scores yet.** Parent `character_skills.score` remains authoritative.

True scored subskills require independently distinguishable learning evidence, progression/retention ownership, and explicit parent/child aggregation + migration semantics. Never split current parent scores into invented child values.

Existing H2H/Tactical/Technology learning evidence must remain intact. Weapons/Survival/Field Medicine definitions must not invent learning evidence merely for symmetry.

## After the refactor batch

Implement **Represented Skill Task Instance Resolver v1** as the next read-only generic runtime seam, then one distinct Technology simulator/action evidence integration. Apply later task/action integration by proven pattern rather than one PR per Skill.

## Exact resume point

**Represented Skill Task Contract v1 is complete/deployed through PR #119 / Deploy #203. Next implement Skill Definition Refactor Batch v1 for H2H, Weapons, Survival, Tactical Planning and Field Medicine, preserving all existing actor scores and using applications rather than fabricated scored subskills.**
