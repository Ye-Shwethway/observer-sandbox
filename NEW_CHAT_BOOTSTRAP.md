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

Latest runtime deployment: **Deploy #200 / run `31872355878` SUCCESS**, Skill Application Requirements v1, PR #113 merge `7cfe07dc32764d322942b21748a0d26ebb8a46f7`.

Verified:
- PR CI #807 SUCCESS;
- Application Requirements Acceptance #1 SUCCESS;
- Skill Definition Format Acceptance #3 SUCCESS;
- Strength Live Cycle #37 SUCCESS;
- Public Security #67 SUCCESS;
- post-merge Application Requirements Acceptance #2 SUCCESS;
- post-merge Skill Definition Format Acceptance #4 SUCCESS;
- post-merge CI #808 SUCCESS;
- service healthy, schema v5, autonomy normal 1x, Telegram/cognition intact;
- Technology remained `82.0 / A Advanced`.

PR #113 changes executable metadata only; live capability/action behavior is not wired yet.

## Skill foundation / authority

Actor Skill state:
- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = accumulated legitimate learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Universal Skill meaning:
- `config/skill_definitions.v1.json`
- `src/observer_sandbox/skill_definitions.py`
- `src/observer_sandbox/skill_application_requirements.py`

Canonical docs:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`
- progression/evidence docs referenced by `ROADMAP.md`.

Ontology remains:
Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated real-context reliability. No second competency score exists.

## Technology definition

Technology is the first complete universal Skill Definition. It covers represented technical diagnosis/configuration/maintenance/troubleshooting and explicitly excludes ordinary consumer use, weapon operation, medical treatment, unrepresented fabrication, offensive cybersecurity, and unsupported novel engineering.

First application:
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

**Technology Capability Resolution exemplar — pure deterministic assessment for `diagnose_known_system_fault`.**

Minimum direction:
`Skill Definition + actor Technology score + current proficiency anchor + requested challenge + machine-readable context/resources + declared supporting Attributes -> supported/constrained/unsupported assessment`

Constraints:
- no prose parsing or scattered `skill >= N` constants;
- challenge support comes from the definition's current proficiency anchor;
- required context/resource checks come from the executable requirements contract;
- Knowledge remains declarative support only—no hidden Knowledge score/gate;
- declared Attributes may be reported as inputs, but must not modify eligibility via hidden weighting constants; strengthen the definition first if real modifier semantics are needed;
- no random probability, second competency score, new XP formula, or LLM authority;
- no high-risk live authorization from Skill score alone;
- one pure assessment exemplar before adding a live skill-application action/target.

After this exemplar proves the resolution pattern, choose the minimum safe application-evidence integration, then batch remaining current Skill Definitions before resuming their progression coverage.

## Exact resume point

**Skill Application Requirements v1 is complete/deployed through PR #113 / Deploy #200. Next implement the pure deterministic Technology Capability Resolution assessment for `diagnose_known_system_fault`; do not yet add other Skill definitions or a full live skill-application system.**
