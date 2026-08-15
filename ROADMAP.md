# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Python/SQLite runtime and verified live world state are authoritative.
- AI proposes structured cognition; deterministic engines validate and mutate.
- Telegram is an observer/control adapter, never a simulation engine.
- Preserve the LEGO contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are exemplars, never reusable-engine identity.
- Reusable mechanics are actor/entity/definition-id driven.
- Prefer minimum-runnable reversible slices.
- Use **exemplar-first, then batch-by-pattern**.
- Default flow: `branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Never mutate or accelerate production merely to manufacture evidence.

## Current verified deployment baseline

Latest runtime deployment: **Deploy #198 / run `31870737488` SUCCESS**, Skill Evidence Semantics v1 with Technology Systems Diagnostic Practice exemplar, PR #108 merge `3cd35cb1480533c0c2258ee72d2726cfe24b586b`.

Verified after deployment:
- main CI #798 / run `31870737278`: SUCCESS;
- Skill Evidence Semantics Acceptance #2 / run `31870737515`: SUCCESS;
- Tactical Planning Acceptance #4 / run `31870737546`: SUCCESS;
- service healthy/active, schema v5, autonomy normal 1.0x;
- Telegram connected;
- Gemini `gemini-3.1-flash-lite` primary and Groq `qwen/qwen3.6-27b` fallback preserved;
- Technology remained `82.0 / A Advanced`, proving no retroactive score jump.

No live Technology practice was forced for evidence.

## Completed major foundations

Major completed families include runtime/provider foundation, continuous autonomy, Telegram Observer/Profile/Control + Creator AI Control, cognition fallback, Universal Character Engine, training fatigue/recovery/readiness/effective load, needs/sleep, Physical Attribute Progression, Inventory/Eating/Nutrition, Body Composition/Measurements, Training Method/Anatomy semantics, Regional Detraining, Height Lifecycle, Sexual Anatomy/Physiology + Solo Sexual Regulation, Universal Profile Grading, Character Change Observability, and the current Skill progression/evidence foundations.

Recent Skill checkpoints:
- Hand-to-Hand Skill Progression Foundation v1 — PR #104 / Deploy #196;
- Tactical Planning Skill Progression v1 — PR #106 / Deploy #197;
- Skill Evidence Semantics v1 / Technology exemplar — PR #108 / Deploy #198.

## Current Skill authority

- `character_skills.score` — authoritative current learned proficiency;
- `character_skills.experience` — accumulated legitimate learning evidence;
- persisted `tier` — legacy compatibility only;
- grade — read-time `skill-proficiency-100-v1`;
- RAPS skill-like fields are not independent mutable Skill truth;
- model prose, action reason text and Telegram never directly mutate Skill state.

Live-enabled progression:
- Hand-to-Hand Combat — structured Training Method evidence;
- Tactical Planning — `vr_tactical_drills` + reduced mixed `ai_combat_simulation` evidence;
- Technology — explicit `systems_diagnostic_practice` Skill Evidence.

Canonical:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`;
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`;
- `docs/SKILL_EVIDENCE_SEMANTICS_V1.md`.

## Skill Definition & Capability Framework — researched design complete

Canonical design:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`.

Research basis includes O*NET, NIST NICE, ESCO and SFIA. The accepted ontology separates:
- **Ability / Attribute** — underlying capacity influencing learning/performance;
- **Knowledge** — facts/concepts/procedures known;
- **Skill** — learned capacity to apply knowledge/abilities to observable task families;
- **Task / Application** — the work being attempted, with difficulty/context/resources/risk;
- **Competency / Demonstrated Capability** — evidence of reliable real-context application, not a second competing numeric score;
- **Learning Evidence** — immutable evidence that may contribute to progression under explicit policy;
- **Proficiency** — `character_skills.score`, generically graded but behaviorally interpreted by each Skill Definition.

Core direction:
`Task Definition + Skill Definition + actor Skill state + relevant Knowledge/Abilities + tools/resources + context + reliability evidence -> deterministic capability resolution -> outcome dimensions + immutable application evidence`

A Skill score alone is not the complete gameplay authority.

## Skill Creation Format v1 contract

Every first-class Skill Definition must support:
1. stable identity/taxonomy/version/status/reusability;
2. affirmative definition plus explicit `scope_includes` and `scope_excludes`;
3. parent/component/related-skill relations;
4. knowledge dependencies;
5. ability/attribute dependencies;
6. observable task/application families;
7. skill-specific behavioral capability anchors for current E/D/C/B/A/S bands;
8. task challenge classes: routine / standard / challenging / advanced / extreme;
9. whitelisted gameplay outcome dimensions the Skill may influence;
10. failure/risk/consequence boundaries;
11. legitimate acquisition/practice/application evidence families;
12. explicit bounded transfer/cross-training hooks;
13. future retention/reacquisition hooks;
14. grading/observability/presentation metadata;
15. provenance/compatibility/migration policy.

The current 0..100 grading scheme still uses E..S only. Capability anchors add Skill-specific behavioral meaning; they do not create SS+ grades or replace the generic grading scheme.

The six current Skills remain broad umbrella Skills until gameplay actually requires narrower first-class component Skills:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Do not fabricate child scores when an umbrella Skill is later decomposed.

## Next development sequence

1. **Skill Creation Format v1 + validator — NEXT**;
2. create one complete machine-readable **Technology** definition as exemplar;
3. keep the registry read-only with respect to gameplay until schema/validator checks are green;
4. wire one bounded Technology application into deterministic capability resolution;
5. batch remaining current Skill definitions by proven pattern;
6. resume missing Field Medicine/Survival/Weapons evidence/progression only after their semantics exist;
7. Skill Retention/Reacquisition;
8. intellectual attributes;
9. mental/emotion dynamics;
10. broader relationship/social systems;
11. broad Mind/Behavior architecture only when justified.

## Phase B — NEXT

Provisional registry: `config/skill_definitions.v1.json`.

Add a reusable loader/validator that rejects at least:
- invalid/duplicate Skill identities;
- missing definition/scope/category/type;
- broken/cyclic hierarchy;
- missing or inconsistent E–S capability anchors;
- application families without observable outcome meaning;
- high-risk applications without consequence boundaries;
- unknown learning-evidence method references;
- implicit XP from generic action names/model prose;
- unsupported SS+ anchors on the current 0..100 scheme;
- actor score/XP/grade embedded in universal definitions;
- transfer rules that fabricate new Skill state;
- semantic revisions that silently reinterpret historical evidence.

The first registry entry should be **Technology**, because its explicit practice evidence already exists and therefore minimizes new variables while proving the definition format.

No database/schema migration is required merely to prove the registry/validator. Runtime task-resolution wiring belongs to the following exemplar slice.

## Deferred boundaries

Do not add as side effects:
- a full Knowledge Engine;
- a second competency score;
- giant speculative Skill trees;
- economy/currency/careers/jobs/quests/salary;
- deep crafting;
- Character Memory or broad Mind/Behavior;
- partnered sexual behavior;
- detailed endocrine simulation;
- second production character solely for testing;
- Tahoe exterior traversal.

## Exact resume point

Re-read current live production and canonical repository first.

**Skill Definition & Capability Framework v1 research/ontology/design is complete as a canonical design candidate. Next: implement the machine-readable Skill Creation Format v1 + validator with one Technology definition, without yet changing live gameplay capability resolution.**
