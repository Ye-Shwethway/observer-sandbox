# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-15

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified current production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

## Development workflow

Default:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use **exemplar-first, then batch-by-pattern**. Never move, train, practice or accelerate production merely to manufacture evidence. Darian/Thorne Estate are exemplars, not reusable-engine identity.

## Current verified deployment

Latest runtime deployment: **Deploy #199 / run `31871896715` SUCCESS**, Skill Creation Format v1 / Technology universal definition, PR #111 merge `a51c9f5980ba52883572397529d61889c856dbb6`.

Verified:
- PR CI #803 / run `31871844052`: SUCCESS;
- Skill Definition Format v1 Acceptance #1 / run `31871844138`: SUCCESS;
- Strength Live Cycle #36 / run `31871844050`: SUCCESS;
- Public Readiness Security Audit #65 / run `31871844057`: SUCCESS;
- post-merge Skill Definition Format Acceptance #2: SUCCESS;
- post-merge CI #804 / run `31871896720`: SUCCESS;
- service healthy/active, schema v5, autonomy normal 1.0x;
- Telegram/cognition bindings preserved;
- Technology remained `82.0 / A Advanced`.

The Skill Definition registry is deployed as a read-only application artifact. Live task capability resolution does **not** consume it yet, so PR #111 intentionally changed no actor score/XP/action capability.

## Current Skill authority

- `character_skills.score` = authoritative current learned proficiency;
- `character_skills.experience` = accumulated legitimate learning evidence;
- persisted `tier` = legacy compatibility only;
- grade = read-time `skill-proficiency-100-v1`;
- RAPS skill-like fields are not independent mutable Skill state;
- model prose/Telegram never mutate proficiency.

Current progression/evidence:
- Hand-to-Hand Combat — Training Method evidence;
- Tactical Planning — tactical Training Method evidence;
- Technology — explicit purpose-built `systems_diagnostic_practice` evidence.

Canonical progression/evidence docs:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`
- `docs/SKILL_EVIDENCE_SEMANTICS_V1.md`

## Skill Definition & Capability foundation

Canonical research/design:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`

Canonical machine-readable format/deployment checkpoint:
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `config/skill_definitions.v1.json`
- `src/observer_sandbox/skill_definitions.py`

Canonical ontology:
- **Ability / Attribute** — underlying capacity influencing learning/performance;
- **Knowledge** — facts/concepts/procedures known;
- **Skill** — learned capacity to apply relevant knowledge/abilities to observable task families;
- **Task / Application** — work attempted with its own challenge/context/resources/risk;
- **Competency / Demonstrated Capability** — evidence of reliable real-context application, not a second competing score;
- **Learning Evidence** — immutable evidence eligible under explicit progression policy;
- **Proficiency** — actor Skill score, generically graded but behaviorally interpreted by the universal Skill Definition.

Capability direction:
`Task Definition + Skill Definition + actor Skill state + relevant Knowledge/Abilities + tools/resources + context + reliability evidence -> deterministic capability resolution -> outcome + immutable evidence`

A Skill score alone is not complete gameplay authority.

## Skill Creation Format v1

Every first-class universal Skill Definition is validator-backed for:
1. stable identity/taxonomy/revision/status/reusability;
2. affirmative definition + explicit includes/excludes;
3. hierarchy/relations;
4. Knowledge dependencies;
5. Ability/Attribute dependencies;
6. observable applications/task families;
7. Skill-specific E/D/C/B/A/S behavioral anchors;
8. challenge classes: routine / standard / challenging / advanced / extreme;
9. allowed gameplay outcome dimensions;
10. risk/failure/consequence boundaries;
11. legitimate learning-evidence families;
12. bounded transfer/cross-training hooks;
13. deferred retention/reacquisition hooks;
14. grading/presentation metadata;
15. provenance/compatibility/migration rules.

Universal definitions cannot embed actor score/experience/tier/grade. Current E–S grading remains read-time presentation/proficiency interpretation; SS+ is not available on the current 0..100 scale.

### Technology exemplar

Technology is currently the only complete registry definition.

It covers represented technical diagnosis/configuration/maintenance/troubleshooting and explicitly excludes ordinary consumer use, weapon operation, medical treatment, unrepresented fabrication, offensive cybersecurity, and unsupported novel engineering.

First declared application:
- `diagnose_known_system_fault`

Declared supporting Attributes:
- `raps_ia.problem_solving`
- `raps_ma.focus`

Legacy `raps_ia.technological_aptitude` is compatibility provenance only and is not a second Technology proficiency authority.

Existing `systems_diagnostic_practice` remains the legitimate practice evidence method. The validator cross-checks that method against both the practice registry and Skill Progression whitelist.

## Current broad Skill set

Preserve these umbrella Skills until justified gameplay requires decomposition:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Never fabricate child Skill scores from parent values.

## Next canonical slice

**Technology Capability Resolution exemplar — `diagnose_known_system_fault`.**

Minimum invariant:
`declared Technology application + actor Technology proficiency + declared supporting Attributes + represented task challenge/context/resources -> deterministic capability assessment -> bounded outcome dimensions + immutable application evidence`

Before implementation, audit the current action/service/task architecture and verify that the definition registry contains enough machine-executable requirement metadata. If context/resources/Knowledge hooks are still too textual for deterministic resolution, strengthen the generic definition/task requirement contract first rather than hiding constants in the resolver.

Constraints:
- one Technology application family only;
- use the universal Skill Definition, not scattered hard-coded `skill >= N` checks;
- no full Knowledge Engine or invented hidden Knowledge scores;
- no second competency score;
- no new Skill XP formula;
- preserve current practice/progression authority;
- no actor-specific hard-coding;
- no high-risk live-system authorization from Skill score alone;
- no LLM authority over capability resolution;
- one bounded exemplar before generalizing resolution or defining the remaining Skills.

After the exemplar proves the pattern:
1. batch remaining current Skill Definitions;
2. resume missing Field Medicine/Survival/Weapons evidence/progression only after definitions exist;
3. add Retention/Reacquisition only when semantic/evidence coverage is broad enough.

## Deferred boundaries

Do not add a full Knowledge Engine, second competency score, giant speculative Skill tree, careers/jobs/quests/economy, broad Mind/Behavior, deep crafting, partnered sexual behavior, detailed endocrine simulation, second production character solely for testing, or Tahoe exterior traversal as side effects.

## Exact resume point

**Skill Creation Format v1 is complete/deployed as a read-only semantic foundation through PR #111 / Deploy #199. Technology has the first validated universal definition. Next audit and implement one bounded deterministic Technology Capability Resolution exemplar for `diagnose_known_system_fault`; strengthen generic machine-readable requirements first if the current definition is not executable enough.**
