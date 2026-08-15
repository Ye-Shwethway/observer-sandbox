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
- Never mutate or accelerate production merely to manufacture evidence.

## Current verified deployment baseline

Latest runtime deployment: **Deploy #199 / run `31871896715` SUCCESS**, Skill Creation Format v1 / Technology universal definition, PR #111 merge `a51c9f5980ba52883572397529d61889c856dbb6`.

Verified:
- PR CI #803 / run `31871844052`: SUCCESS;
- Skill Definition Format v1 Acceptance #1 / run `31871844138`: SUCCESS;
- Strength Live Cycle #36 / run `31871844050`: SUCCESS;
- Public Readiness Security Audit #65 / run `31871844057`: SUCCESS;
- post-merge Skill Definition Format Acceptance #2: SUCCESS;
- post-merge CI #804 / run `31871896720`: SUCCESS;
- service healthy/active, schema v5, autonomy normal 1.0x;
- Telegram connected, cognition bindings preserved;
- Technology remained `82.0 / A Advanced` after deployment.

Skill definitions are deployed application artifacts but are **not yet consumed by live task capability resolution**. No actor score/XP/action capability changed in this slice.

## Completed major foundations

Major completed families include runtime/provider foundation, continuous autonomy, Telegram Observer/Profile/Control + Creator AI Control, cognition fallback, Universal Character Engine, training fatigue/recovery/readiness/effective load, needs/sleep, Physical Attribute Progression, Inventory/Eating/Nutrition, Body Composition/Measurements, Training Method/Anatomy semantics, Regional Detraining, Height Lifecycle, Sexual Anatomy/Physiology + Solo Sexual Regulation, Universal Profile Grading, Character Change Observability, and the current Skill foundations.

Recent Skill checkpoints:
- Hand-to-Hand Skill Progression Foundation v1 — PR #104 / Deploy #196;
- Tactical Planning Skill Progression v1 — PR #106 / Deploy #197;
- Skill Evidence Semantics v1 / Technology practice exemplar — PR #108 / Deploy #198;
- Skill Definition & Capability Framework research/design — PR #110;
- **Skill Creation Format v1 / Technology definition — PR #111 / Deploy #199**.

## Current Skill authority

- `character_skills.score` — authoritative current learned proficiency;
- `character_skills.experience` — accumulated legitimate learning evidence;
- persisted `tier` — legacy compatibility only;
- grade — read-time `skill-proficiency-100-v1`;
- RAPS skill-like fields are not independent mutable Skill truth;
- model prose, action reason text and Telegram never directly mutate Skill state.

Universal Skill meaning is now separate from actor state:
- registry: `config/skill_definitions.v1.json`;
- loader/validator: `src/observer_sandbox/skill_definitions.py`;
- canonical format/evidence: `docs/SKILL_CREATION_FORMAT_V1.md`;
- canonical research/design: `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`.

## Skill ontology

Canonical distinctions:
- **Ability / Attribute** — underlying capacity influencing learning/performance;
- **Knowledge** — facts/concepts/procedures known;
- **Skill** — learned capacity to apply relevant knowledge/abilities to observable task families;
- **Task / Application** — the work attempted, with challenge/context/resources/risk;
- **Competency / Demonstrated Capability** — real-context reliability evidence, not a second score;
- **Learning Evidence** — immutable evidence eligible under explicit policy;
- **Proficiency** — actor Skill score, generically graded but behaviorally interpreted by the Skill Definition.

A Skill score alone is not complete gameplay authority.

## Skill Creation Format v1

Every first-class Skill Definition now has a validator-backed contract covering:
1. stable identity/taxonomy/revision/status/reusability;
2. affirmative definition plus explicit includes/excludes;
3. hierarchy/relations;
4. Knowledge dependencies;
5. Ability/Attribute dependencies;
6. observable applications;
7. Skill-specific E/D/C/B/A/S behavioral anchors;
8. challenge classes: routine / standard / challenging / advanced / extreme;
9. whitelisted gameplay effects;
10. risk/failure/consequence boundaries;
11. legitimate learning evidence;
12. bounded transfer hooks;
13. deferred retention/reacquisition hooks;
14. grading/presentation metadata;
15. provenance/compatibility/migration policy.

The validator cross-checks practice evidence against both `skill_practice_methods.v1.json` and `skill_progression.v1.json`. Universal definitions cannot embed actor score/experience/tier/grade.

### Technology exemplar

Technology is currently the only registry definition.

It explicitly covers represented technical diagnosis/configuration/maintenance/troubleshooting and excludes ordinary consumer use, weapons operation, medical treatment, unrepresented fabrication, offensive cybersecurity, and unsupported novel engineering.

Its first declared application is `diagnose_known_system_fault`.

Underlying modifiers currently reference `raps_ia.problem_solving` and `raps_ma.focus`; legacy `raps_ia.technological_aptitude` is compatibility provenance only and is not a second Technology authority.

Existing `systems_diagnostic_practice` remains the legitimate practice evidence method. Generic use/inspect/research/monitor and model prose remain non-evidence by implication.

## Current broad Skill set

Preserve as umbrella Skills until real gameplay requires justified decomposition:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Do not fabricate child Skill scores from parent scores.

## Next development sequence

1. **Technology Capability Resolution exemplar — NEXT**;
2. prove one bounded deterministic application using `diagnose_known_system_fault`;
3. batch remaining current Skill Definitions by the proven creation format;
4. resume missing Field Medicine/Survival/Weapons evidence/progression only after their definitions exist;
5. Skill Retention/Reacquisition;
6. intellectual attributes;
7. mental/emotion dynamics;
8. broader relationship/social systems;
9. broad Mind/Behavior only when enough real feature families justify it.

## Technology Capability Resolution exemplar — NEXT

Minimum invariant:
`declared Technology application + actor Technology proficiency + declared supporting Attributes + represented task challenge/context/resources -> deterministic capability assessment -> bounded outcome dimensions + immutable application evidence`

Constraints:
- one application family only: `diagnose_known_system_fault`;
- reuse the universal Skill Definition rather than hard-coded Technology thresholds scattered through code;
- no full Knowledge Engine; unresolved Knowledge requirements remain explicit/declarative context rather than hidden invented scores;
- no second competency score;
- no new Skill XP formula;
- no change to existing practice evidence/progression authority;
- no actor-specific hard-coding;
- no high-risk live-system authorization from Skill score alone;
- no LLM authority over deterministic capability resolution;
- one bounded exemplar before generalizing task resolution across all Skills.

## Deferred boundaries

Do not add as side effects:
- full Knowledge Engine;
- second competency score;
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

**Skill Creation Format v1 is complete/deployed as a read-only semantic foundation through PR #111 / Deploy #199. Technology has the first validated universal definition. Next: one bounded deterministic Technology Capability Resolution exemplar for `diagnose_known_system_fault`; do not yet batch other Skills or resume their progression coverage.**
