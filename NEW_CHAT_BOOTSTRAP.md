# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-15

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical contracts/source files
5. verified current live production before implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

## Development workflow

Default:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use disposable production-copy validation for concrete stateful/migration risk. Never accelerate or directly mutate production merely to manufacture acceptance evidence.

Use **exemplar-first, then batch-by-pattern**: one bounded exemplar proves a genuinely new invariant; structurally equivalent follow-ons are batched rather than split into repetitive PR/deploy cycles.

Darian/Thorne Estate are exemplars, never reusable-engine identity. Reusable mechanics are actor/entity/definition-id driven.

## Current verified deployment checkpoint

Latest runtime deployment: **Deploy #198 / run `31870737488` SUCCESS**, Skill Evidence Semantics v1 with Technology Systems Diagnostic Practice exemplar, PR #108 merge `3cd35cb1480533c0c2258ee72d2726cfe24b586b`.

Post-merge:
- CI #798 / run `31870737278`: SUCCESS;
- Skill Evidence Semantics Acceptance #2 / run `31870737515`: SUCCESS;
- Tactical Planning Acceptance #4 / run `31870737546`: SUCCESS.

Readback verified:
- service healthy/active;
- schema v5;
- autonomy enabled, normal mode, 1.0x;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` tested fallback preserved;
- Telegram connected with owner/allowed-user configuration;
- Technology remained represented at `82.0 / A Advanced`, proving no retroactive activation jump.

Do not force live practice to demonstrate progression. Natural future eligible practice may supply occurrence evidence.

## Universal invariants

Cognition:
`deterministic state/context -> one model proposal -> authoritative validation -> deterministic mutation`

Training:
`concrete target -> reusable method -> optional movement pattern(s) -> effective load -> immutable structured evidence -> independent downstream progression engines`

Profile grading:
`authoritative current value(s) + explicit named grading scheme + scheme-specific context -> derived grade metadata -> generic consumers`

Profile change observability:
`authoritative mutation/history -> cumulative domain-aware delta -> significance/grade-transition check -> Profile delta UX + eligible aggregated notification`

Skill progression:
`completed skill-relevant structured evidence + effective duration + explicit relevance + current proficiency + recent-practice saturation -> effective learning units -> bounded score/experience settlement + immutable audit event`

Skill evidence:
`validated domain-specific practice target + explicit practice method + bounded duration/context -> immutable structured skill-practice evidence -> existing generic Skill Progression settlement`

## Completed major foundations

Current major completed families include:
- runtime/provider foundation, continuous autonomy, Telegram Observer/Profile/Control + Creator AI Control;
- cognition fallback, Universal Character Engine, choice/resource awareness, object familiarity/inspect utility;
- fatigue/recovery, targeted training, readiness/effectiveness/effective load, minimum stimulus and load/recovery guards;
- causal needs + sleep/circadian behavior;
- Physical Attribute Progression Framework v1;
- inventory/eating/nutrition through Meal Choice Intelligence;
- BC-2 Body Composition / BC-3 Body Measurements;
- Training Method Semantics v2 + Training Anatomy/Movement Semantics;
- Regional Measurement Detraining + Height Lifecycle;
- Sexual Anatomy/Physiology + Solo Sexual Regulation v1;
- Physical Profile Coverage/Presentation + Telegram Profile Schema-Driven UX;
- Universal Profile Grading Framework v1 — PR #100 / Deploy #194;
- Character Change Observability & Notification Foundation v1 — PR #102 / Deploy #195;
- Hand-to-Hand Skill Progression Foundation v1 — PR #104 / Deploy #196;
- Tactical Planning Skill Progression v1 — PR #106 / Deploy #197;
- **Skill Evidence Semantics v1 / Technology exemplar — PR #108 / Deploy #198**.

Detailed semantics/evidence are in the feature docs referenced by `ROADMAP.md`.

## Current Skill authority map

- `character_skills.score` = authoritative current proficiency;
- `character_skills.experience` = accumulated legitimate post-activation learning evidence;
- persisted `tier` = legacy compatibility only;
- grade = read-time `skill-proficiency-100-v1`;
- RAPS skill-like fields are not independent mutable Skill truth;
- model prose, action reason text and Telegram never directly mutate proficiency.

Live-enabled progression:
- Hand-to-Hand Combat — structured combat Training Method evidence;
- Tactical Planning — direct `vr_tactical_drills` plus reduced mixed `ai_combat_simulation` evidence;
- Technology — purpose-built `Systems Diagnostic Practice Console` / `systems_diagnostic_practice` Skill Evidence.

Ordinary `use`, `inspect`, `research`, `monitor` or generic terminal/medical-station activity does not become XP.

Canonical:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`;
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`;
- `docs/SKILL_EVIDENCE_SEMANTICS_V1.md`.

## Important newly identified gap — Skill meaning itself

The current engine can store, grade and progress a named Skill, but there is no canonical reusable **Skill Definition / Creation Format** that tells the runtime what the skill actually means.

Current `character_skills` storage is largely:
- `skill_key`;
- broad `category`;
- `score`;
- legacy `tier`;
- `experience`;
- free-form metadata.

Current character seeds similarly provide skill key/category/score without authoritative task scope, prerequisites, component skills, difficulty/capability semantics, deterministic gameplay effects, acquisition rules, transfer rules or failure/consequence boundaries.

As a result, a score such as Technology 82 or Field Medicine 75 currently has a grade/proficiency value but not a complete generic deterministic answer to **what the actor can reliably do with it**.

Do **not** add more Field Medicine, Survival or Weapons progression mappings before this semantic foundation is designed and accepted.

## Next canonical priority

**Skill Definition & Capability Framework — research + canonical design.**

Research first, then design a minimum reusable Skill Creation Format that can express:
1. identity/taxonomy;
2. definition + explicit scope boundaries;
3. parent/category and optional child/component relations;
4. prerequisite knowledge/skills/attributes;
5. action/task/application domains;
6. proficiency-level behavioral/capability descriptors;
7. difficulty/challenge semantics;
8. deterministic gameplay effects and limits;
9. legitimate acquisition/practice/application evidence families;
10. learning/transfer/saturation/retention hooks;
11. risk/failure/consequence semantics where relevant;
12. grading/observability/presentation metadata;
13. version/revision/source provenance.

The design should explicitly separate:
- **knowledge** — facts/concepts/procedures known;
- **skill** — ability to apply knowledge and perform tasks;
- **competency / demonstrated capability** — reliable application in contextual/operational conditions;
- **attributes/abilities** — underlying capacities that influence learning/performance but are not the skill itself.

Do not build a giant universal engine immediately. First produce the research-backed canonical contract/format and validation rules. Then migrate one bounded existing skill as the exemplar. Once proven, batch equivalent current skills.

Current represented skills needing semantic-definition review:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Existing progression/evidence remains valid unless later semantic migration explicitly demonstrates a conflict. Never silently reinterpret historical evidence.

## Next development sequence

1. **Skill Definition & Capability Framework research/design — NEXT**;
2. minimum Skill Creation Format + validation rules;
3. one bounded exemplar migration;
4. batch remaining current skill definitions by pattern;
5. resume missing Skill Evidence/Progression coverage;
6. Skill Retention / Reacquisition after semantic/evidence coverage is broad enough;
7. intellectual attributes;
8. mental/emotion dynamics;
9. broader relationship/social systems and partnered/contextual sexual behavior;
10. broad Mind/Behavior architecture only after enough real feature families justify it.

## Deferred boundaries

Do not add economy/currency, careers/jobs/quests/salary, automatic restocking, deep crafting, Character Memory, broad Mind/Behavior, partnered sexual behavior, detailed endocrine simulation, a second production character solely for testing, or Tahoe exterior traversal as side effects.

## Exact resume point

First re-read verified production and current canonical repository.

**Skill Evidence Semantics v1 is complete/deployed/live-activated through PR #108 / Deploy #198. Technology proves the explicit-practice evidence path. The next priority is no longer immediate Field Medicine/Survival progression coverage; it is research/design of the reusable Skill Definition & Capability Framework so current and future skills have explicit meaning, scope, prerequisites, capability/application semantics and learning evidence rules.**
