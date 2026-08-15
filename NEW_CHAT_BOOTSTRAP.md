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

Use **exemplar-first, then batch-by-pattern**. Do not force production movement, training, practice or acceleration merely for evidence. Darian/Thorne Estate remain exemplars, not reusable-engine identity.

## Current verified deployment

Latest runtime deployment: **Deploy #198 / run `31870737488` SUCCESS**, Skill Evidence Semantics v1 / Technology practice exemplar, PR #108 merge `3cd35cb1480533c0c2258ee72d2726cfe24b586b`.

Verified:
- CI #798 SUCCESS;
- Skill Evidence Acceptance #2 SUCCESS;
- Tactical Planning Acceptance #4 SUCCESS;
- service healthy, schema v5, autonomy normal 1.0x;
- Telegram/cognition bindings preserved;
- Technology remained `82.0 / A Advanced` after activation, with no retroactive score gain.

## Current Skill authority

- `character_skills.score` = authoritative current learned proficiency;
- `character_skills.experience` = accumulated legitimate learning evidence;
- persisted `tier` = legacy compatibility only;
- grade = read-time `skill-proficiency-100-v1`;
- RAPS skill-like fields are not independent mutable Skill state;
- model prose/Telegram do not mutate proficiency.

Current progression/evidence:
- Hand-to-Hand Combat — Training Method evidence;
- Tactical Planning — tactical Training Method evidence;
- Technology — explicit purpose-built `systems_diagnostic_practice` evidence.

Canonical progression/evidence docs:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`
- `docs/SKILL_EVIDENCE_SEMANTICS_V1.md`

## Skill Definition & Capability Framework v1

Canonical design:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`

Research basis: O*NET, NIST NICE, ESCO and SFIA, adapted to the Observer Sandbox runtime rather than copied literally.

Canonical ontology:
- **Ability / Attribute** — underlying capacity influencing learning/performance;
- **Knowledge** — facts/concepts/procedures known;
- **Skill** — learned capacity to apply relevant knowledge/abilities to observable task families;
- **Task / Application** — work attempted with its own challenge/context/resources/risk;
- **Competency / Demonstrated Capability** — evidence of reliable real-context application, not a second competing score;
- **Learning Evidence** — immutable evidence eligible under an explicit progression policy;
- **Proficiency** — actor `character_skills.score`, generically graded but behaviorally interpreted by each Skill Definition.

Capability direction:
`Task Definition + Skill Definition + actor Skill state + relevant Knowledge/Abilities + tools/resources + context + reliability evidence -> deterministic capability resolution -> outcome + immutable evidence`

A Skill score alone must not become the whole gameplay authority.

## Skill Creation Format v1 — required semantic coverage

Every first-class Skill Definition must support:
1. stable identity/taxonomy/revision/status/reusability;
2. definition + explicit included/excluded scope;
3. parent/component/related-skill relations;
4. knowledge dependencies;
5. ability/attribute dependencies;
6. observable task/application families;
7. Skill-specific E/D/C/B/A/S behavioral capability anchors;
8. challenge classes: routine / standard / challenging / advanced / extreme;
9. allowed gameplay outcome dimensions;
10. risk/failure/consequence boundaries;
11. legitimate learning evidence families;
12. explicit bounded transfer/cross-training;
13. future retention/reacquisition hooks;
14. grading/observability metadata;
15. provenance/compatibility/migration rules.

Current E–S grading thresholds remain presentation/proficiency interpretation. Capability anchors add domain-specific behavioral meaning; SS+ is not available on the current 0..100 scale.

Current broad Skill review set:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Do not explode these into speculative child Skills or fabricate child scores. Decompose only when real gameplay/evidence requires it.

## Next canonical slice

**Skill Creation Format v1 + validator — Technology definition exemplar.**

Provisional registry: `config/skill_definitions.v1.json`.

The validator should reject invalid/duplicate identities, missing scope, broken/cyclic relations, incomplete E–S capability anchors, meaningless task families, missing high-risk consequence boundaries, unknown learning-evidence references, implicit prose/action-name XP, unsupported SS+ anchors, actor state embedded in universal definitions, score-fabricating transfer rules and silent semantic reinterpretation of historical evidence.

Technology should be the first complete definition because its typed practice evidence is already proven. This next slice should establish a machine-readable registry + validation only; do **not** change live task capability resolution yet.

After the registry/validator is proven:
1. wire one bounded Technology application into deterministic capability resolution;
2. batch remaining current Skill definitions;
3. resume missing Field Medicine/Survival/Weapons evidence/progression;
4. add Retention/Reacquisition only after semantic/evidence coverage is broad enough.

## Deferred boundaries

Do not add a full Knowledge Engine, second competency score, giant Skill tree, careers/jobs/quests/economy, broad Mind/Behavior, deep crafting, partnered sexual behavior, detailed endocrine simulation, second production character solely for testing, or Tahoe exterior traversal as side effects.

## Exact resume point

**Skill Definition & Capability Framework v1 research/ontology/design is the current canonical design. Next implement only the machine-readable Skill Creation Format v1 + validator with one Technology definition; runtime capability resolution remains the following exemplar slice.**
