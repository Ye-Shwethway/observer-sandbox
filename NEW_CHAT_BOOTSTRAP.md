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

Latest runtime deployment: **Deploy #202 / run `31873159944` SUCCESS**, Actor-backed Skill Capability Assessment Adapter v1, PR #117 merge `07b43a20f28c75cccb150f01cd8f071a5a3a08d9`.

Verified:
- Adapter Acceptance #1 / run `31873122885`: SUCCESS;
- PR CI #815 / run `31873122797`: SUCCESS;
- Public Security #71 / run `31873122839`: SUCCESS;
- post-merge Adapter Acceptance #2 / run `31873159937`: SUCCESS;
- post-merge CI #816 / run `31873159939`: SUCCESS;
- Deploy #202 / run `31873159944`: SUCCESS;
- service healthy, schema v5, autonomy normal 1x, Telegram/cognition intact;
- Technology remained `82.0 / A Advanced`.

The adapter is deployed read-only and is not called by autonomy/service. No live action capability, Skill progression or evidence was forced.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. RAPS skill-like fields are not independent mutable Skill truth.

Canonical execution stack:
- `config/skill_definitions.v1.json`
- `src/observer_sandbox/skill_definitions.py`
- `src/observer_sandbox/skill_application_requirements.py`
- `src/observer_sandbox/skill_capability.py`
- `src/observer_sandbox/actor_skill_capability.py`

Canonical docs:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`
- `docs/SKILL_CAPABILITY_RESOLUTION_V1.md`
- `docs/ACTOR_SKILL_CAPABILITY_ADAPTER_V1.md`
- progression/evidence docs referenced by `ROADMAP.md`.

## Technology definition

First application: `diagnose_known_system_fault`.

Executable requirements:
- context all: `technical_system_represented`, `diagnostic_evidence_available`;
- resource any: `diagnostic_interface` or `diagnostic_instrumentation`;
- supporting resource: `technical_documentation`;
- Knowledge mode: `declarative_support_only`.

Supporting Attributes:
- `raps_ia.problem_solving`
- `raps_ma.focus`

Legacy `raps_ia.technological_aptitude` is compatibility provenance only, not a second Technology authority.

## Capability Resolution v1

`Skill Definition + proficiency + grade anchor + requested challenge + explicit context/resources + declared inputs -> supported / constrained / unsupported`

Locks:
- definition anchors own challenge support;
- Knowledge is declarative/non-gating;
- Attributes are transparent non-weighted inputs until explicit modifier semantics exist;
- no probability, second competency score, Skill mutation, action authorization, or LLM deterministic authority.

## Actor-backed Adapter v1

`actor_id + skill_id + application_id + explicit challenge/context/resources -> authoritative actor Skill/Profile reads -> pure resolver -> read-only assessment`

Behavior:
- reads requested `character_skills.score`;
- reads only definition-declared Attribute fields;
- ignores undeclared profile fields;
- missing declared Attribute rows remain transparent `None` under current non-gating semantics;
- malformed declared numeric data fails clearly;
- missing authoritative Skill row fails closed with no fabricated score;
- caller owns task challenge/context/resource tokens; adapter does not infer them from inventory, location, names or prose;
- emits no events/history/evidence and performs no writes.

Focused acceptance uses a generic synthetic actor rather than Darian as implementation identity.

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

**Represented Technology Task Contract audit/exemplar for `diagnose_known_system_fault`.**

Audit existing actions, object definitions/capabilities, conditions/resources/modifiers and target validation. Determine whether current architecture truthfully supplies:
- stable application id;
- target/system identity;
- challenge class;
- explicit context tags;
- explicit resource capability tokens;
- bounded outcome/evidence semantics.

Do not infer these facts from object names or model prose. Skill assessment is not action authorization. If existing architecture lacks a generic machine-readable owner for these task facts, add the smallest represented-task contract first. Only then implement one bounded Technology application/action evidence integration.

Do not yet batch other Skill definitions or build a generic Skill action engine.

## Exact resume point

**Actor-backed Skill Capability Assessment Adapter v1 is complete/deployed through PR #117 / Deploy #202. Next audit/prove the minimum represented Technology task contract for `diagnose_known_system_fault`.**
