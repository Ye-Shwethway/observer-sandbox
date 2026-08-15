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

Canonical docs:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`
- `docs/SKILL_CAPABILITY_RESOLUTION_V1.md`
- `docs/ACTOR_SKILL_CAPABILITY_ADAPTER_V1.md`
- `docs/REPRESENTED_SKILL_TASK_CONTRACT_V1.md`
- progression/evidence docs referenced by `ROADMAP.md`.

## Technology exemplar

Application: `diagnose_known_system_fault`.

Executable requirements:
- context all: `technical_system_represented`, `diagnostic_evidence_available`;
- resource any: `diagnostic_interface` or `diagnostic_instrumentation`;
- supporting resource: `technical_documentation`;
- Knowledge mode: `declarative_support_only`.

Supporting Attributes:
- `raps_ia.problem_solving`
- `raps_ma.focus`

Legacy `raps_ia.technological_aptitude` is compatibility provenance only, not a second Technology authority.

Pure capability resolution returns `supported / constrained / unsupported`. Definition anchors own challenge support. Knowledge is declarative/non-gating and Attributes are transparent/non-weighted until explicit modifier semantics exist. No probability, action authorization, second competency score, Skill mutation, or LLM deterministic authority.

Actor-backed assessment reads authoritative `character_skills.score` plus only definition-declared Attribute fields and performs no writes/evidence emission.

## Represented Skill Task Contract v1

The Skill Definition says what an application means. A Represented Skill Task Definition says how one concrete world task is bounded.

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

Validator prevents represented tasks from weakening application requirements, escaping the challenge/effect envelope, embedding actor state, or promoting `skill_practice:*` targets into application authority. Object names and model prose are never target authority.

The existing Systems Diagnostic Practice Console remains practice/learning evidence only and must not be reused as application authority.

## Current broad Skill set

Preserve umbrella Skills until justified decomposition:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Never fabricate child Skill scores from a parent value. If decomposition is introduced, parent/child authority, score migration, learning evidence, applications, and aggregation semantics must be explicit rather than inferred.

## Next canonical slice

**Represented Skill Task Instance Resolver v1 — read-only.**

Invariant:
`actor + task_id + target_entity_id + explicit available resource capabilities -> validate exact target type/definition/capabilities -> derive task challenge/context -> actor-backed Skill capability assessment -> read-only represented-task assessment`

Constraints:
- exact `definition_id`; no name/prose matching;
- fail closed on target mismatch;
- do not reuse the practice console;
- synthetic target/entity tests are sufficient; no production seed for proof;
- available resource capabilities remain explicit until represented resource ownership is separately proven;
- no writes, action authorization, events/evidence, XP, autonomy or Telegram integration.

After this read-only instance binding is proven, reassess whether the next move should be the first bounded Technology action integration or a batched refactor/expansion of the remaining umbrella Skill definitions so gameplay semantics are not built on description-only Skill rows.

## Exact resume point

**Represented Skill Task Contract v1 is complete/deployed through PR #119 / Deploy #203. Next implement one read-only Represented Skill Task Instance Resolver v1, then make an explicit architecture decision on umbrella Skill refactor/subskill expansion before broad gameplay integration.**
