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

Latest runtime deployment: **Deploy #201 / run `31872775593` SUCCESS**, Technology Capability Resolution v1, PR #115 merge `2609d4bde93d0a188db4ff398a90792b1cec759d`.

Verified:
- Technology Capability Resolution Acceptance #1 / run `31872730382`: SUCCESS;
- PR CI #811 / run `31872730342`: SUCCESS;
- Public Security #69 / run `31872730326`: SUCCESS;
- post-merge Technology Capability Resolution Acceptance #2 / run `31872775640`: SUCCESS;
- post-merge CI #812 / run `31872775683`: SUCCESS;
- Deploy #201 / run `31872775593`: SUCCESS;
- service healthy, schema v5, autonomy normal 1x, Telegram/cognition intact;
- Technology remained `82.0 / A Advanced`.

The resolver is deployed as a pure deterministic library. It is not yet live action authorization and did not mutate actor progression or manufacture production evidence.

## Skill foundation / authority

Actor Skill state:
- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = accumulated legitimate learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Universal Skill meaning / execution contracts:
- `config/skill_definitions.v1.json`
- `src/observer_sandbox/skill_definitions.py`
- `src/observer_sandbox/skill_application_requirements.py`
- `src/observer_sandbox/skill_capability.py`

Canonical docs:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`
- `docs/SKILL_CAPABILITY_RESOLUTION_V1.md`
- progression/evidence docs referenced by `ROADMAP.md`.

Ontology remains:
Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated real-context reliability. No second competency score exists.

## Technology definition

Technology is the first complete universal Skill Definition. First application:
`diagnose_known_system_fault`.

Machine-readable requirements:
- all context tags: `technical_system_represented`, `diagnostic_evidence_available`;
- any required resource capability: `diagnostic_interface` or `diagnostic_instrumentation`;
- supporting resource capability: `technical_documentation`;
- Knowledge mode: `declarative_support_only` using declared Technology Knowledge keys.

Supporting Attributes:
- `raps_ia.problem_solving`
- `raps_ma.focus`

Legacy `raps_ia.technological_aptitude` is compatibility provenance only, not a second Technology authority.

Existing `systems_diagnostic_practice` remains learning evidence. Generic use/inspect/research/monitor/model prose remain non-evidence by implication.

## Technology Capability Resolution v1

Pure deterministic direction:
`Skill Definition + actor proficiency + grade-specific behavioral anchor + requested challenge + executable context/resources + declared supporting inputs -> supported / constrained / unsupported`

Status semantics:
- `supported`: required gates and supporting resources satisfied;
- `constrained`: required gates pass but supporting resource capability missing;
- `unsupported`: application challenge, proficiency-anchor challenge, required context, or required-any resource gate fails.

Locks:
- challenge support comes from Skill Definition anchors, not scattered numeric thresholds;
- Knowledge remains declarative support only and `knowledge_assessed` is false;
- declared Attributes are reported transparently but do not alter v1 status through hidden weights;
- no probability/random roll;
- no second competency score;
- no Skill score/XP mutation;
- no action authorization;
- no LLM deterministic authority.

An S score does not override application scope: `diagnose_known_system_fault` does not declare `extreme`.

## Current broad Skill set

Preserve as umbrella Skills until justified decomposition:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Never fabricate child scores from parent values.

## Next canonical slice

**Actor-backed Skill Capability Assessment Adapter v1.**

Minimum invariant:
`actor_id + skill_id + application_id + explicit challenge/context/resources -> read authoritative actor Skill/Profile inputs -> pure Skill Capability Resolver -> read-only assessment`

Constraints:
- read `character_skills.score` as proficiency authority;
- read only definition-declared Attribute fields;
- no DB/profile/action/Skill mutation;
- assessment is not authorization;
- caller/task context supplies explicit context/resource capability tokens; adapter does not infer them from prose or object names;
- no learning/application evidence emitted merely for assessment;
- no autonomous technical action in this slice;
- generic actor/skill/application IDs only.

Before implementation, audit existing repository/service accessor patterns and use the smallest existing read layer. After the adapter is proven, consider one represented Technology application/action evidence integration only if truthful target/task context already exists or is added as its own bounded contract.

## Exact resume point

**Technology Capability Resolution v1 is complete/deployed through PR #115 / Deploy #201. Next implement one read-only actor-backed Skill Capability Assessment Adapter v1; do not yet batch other Skill definitions or add a live autonomous Technology action.**
