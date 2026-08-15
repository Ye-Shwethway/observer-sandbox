# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Python/SQLite runtime and verified live world state are authoritative.
- AI proposes structured cognition; deterministic engines validate and mutate.
- Telegram is an observer/control adapter, never a simulation engine.
- Preserve the LEGO contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are production exemplars, never reusable-engine identity.
- Reusable mechanics are actor/entity/definition-id driven.
- Prefer minimum-runnable reversible slices.
- Use **exemplar-first, then batch-by-pattern**: prove one new structural invariant, then batch equivalent follow-ons.
- Default flow: `branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Use disposable production-copy validation for stateful/migration risk; never move, accelerate or mutate production merely to manufacture evidence.
- Internal engine receipts are audit evidence, not character activity.

## Current verified deployment baseline

Latest runtime deployment: **Deploy #198 / run `31870737488` SUCCESS**, Skill Evidence Semantics v1 with Technology Systems Diagnostic Practice exemplar, PR #108 merge `3cd35cb1480533c0c2258ee72d2726cfe24b586b`.

Post-merge:
- main CI #798 / run `31870737278`: SUCCESS;
- Skill Evidence Semantics Acceptance #2 / run `31870737515`: SUCCESS;
- Tactical Planning Acceptance #4 / run `31870737546`: SUCCESS.

Deploy readback verified:
- service healthy/active;
- schema version 5;
- autonomy enabled, normal mode, 1.0x;
- Telegram connected with owner/allowed-user configuration present;
- Gemini `gemini-3.1-flash-lite` primary cognition preserved;
- Groq `qwen/qwen3.6-27b` tested fallback preserved;
- live Technology remained at represented `82.0 / A Advanced` after activation, proving no retroactive score jump.

No live Technology practice was forced or accelerated for evidence.

## Completed foundations

Major completed families include:
- P0/P0.5 runtime/provider foundation, P1 continuous autonomy, P2 Telegram Observer/Profile/Control, P2.3 Creator AI Control;
- Runtime Cognition Fallback, Telegram Home, Universal Character Engine, Dynamic Resource Awareness / Choice Breadth, Object Familiarity / Inspect Utility Guard;
- fatigue/recovery, targeted training, readiness/effectiveness/effective load, Minimum Training Stimulus and Session Load/Recovery Guard;
- causal needs + sleep/circadian behavior;
- Physical Attribute Progression Framework v1;
- Inventory/Eating/Nutrition through Meal Choice Intelligence;
- BC-2 Body Composition — PR #78 / Deploy #182;
- BC-3 Body Measurement — PR #82 / Deploy #183;
- Training Method Semantics v2 — PR #84 / Deploy #184;
- Training Anatomy / Movement Semantics v1 — PR #86 / Deploy #185;
- Regional Measurement Detraining — PR #88 / Deploy #186;
- Height Lifecycle;
- Sexual Anatomy & Physiology Lifecycle and Male Erectile Physiology Canonical Contract;
- Physical Profile Coverage Audit and Physical Presentation Closure;
- Telegram Profile Schema-Driven UX;
- Solo Sexual Regulation v1 — PR #97 / Deploy #193;
- Universal Profile Grading Framework v1 — PR #100 / Deploy #194;
- Character Change Observability & Notification Foundation v1 — PR #102 / Deploy #195;
- Hand-to-Hand Skill Progression Foundation v1 — PR #104 / Deploy #196;
- Tactical Planning Skill Progression v1 — PR #106 / Deploy #197;
- **Skill Evidence Semantics v1 / Technology exemplar — PR #108 / Deploy #198**.

Detailed contracts and historical validation evidence live in the corresponding canonical feature docs.

## Current authority map

Physical/profile:
- Weight/BF/FM/FFM — BC-2;
- circumferences — BC-3 + Training Anatomy + Regional Detraining;
- Height — Height Lifecycle;
- structural male sexual anatomy — Sexual Anatomy Lifecycle;
- long-term erectile baseline/cap — Sexual Physiology contract;
- current sexual state — context-driven runtime physiology;
- grades — read-time derived interpretation only;
- profile-change ledgers/notification baselines — observer UX state only.

Skills today:
- `character_skills.score` — authoritative current proficiency;
- `character_skills.experience` — accumulated legitimate post-activation learning evidence;
- persisted `tier` — legacy/compatibility only;
- grade — read-time `skill-proficiency-100-v1`;
- RAPS skill-like fields are not independent live progression authorities;
- model prose, action reason text and Telegram are never Skill progression authority.

## Profile grading / change observability

Universal grading vocabulary remains:
`E Beginner -> D Novice -> C Capable -> B Skilled -> A Advanced -> S Expert -> SS Elite -> SSS Master -> X Mythic -> XX Transcendent`.

Current 0..100 RAPS/Skill schemes legitimately reach E..S only. Grades are never persisted competing truth. Raw body dimensions remain descriptive rather than `larger = better`.

Change observability remains generic: Skill/RAPS `0.10` cumulative significance, body circumference `0.05 in`, Height `0.10 in`, Weight `0.25 lb`, Body Fat `0.10` pp and ratio `0.01`; grade transitions are immediately significant; ordinary push debounce is 5 real minutes per recipient/character.

## Skill Progression + Skill Evidence

Canonical:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`;
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`;
- `docs/SKILL_EVIDENCE_SEMANTICS_V1.md`.

Progression invariant:
`completed skill-relevant structured evidence + effective duration + explicit relevance + current proficiency + recent-practice saturation -> effective learning units -> bounded score/experience settlement + immutable audit event`

Skill Evidence invariant:
`validated domain-specific practice target + explicit practice method + bounded duration/context -> immutable structured skill-practice evidence -> existing generic Skill Progression settlement`

Shared behavior:
- initialize/deploy zero-gain bootstrap consumes historical eligible evidence without retroactive XP/score;
- future eligible evidence may progress score/experience;
- 24-sim-hour saturation + current-proficiency diminishing returns bound growth;
- consumed action event IDs cannot be credited twice;
- reseeding preserves progression-active/experienced skill state;
- authoritative score changes inherit generic grading/Profile deltas/notifications;
- no skill-specific Telegram subsystem.

Current live-enabled progression:
- Hand-to-Hand Combat — structured Training Method evidence;
- Tactical Planning — `vr_tactical_drills` direct evidence + reduced mixed `ai_combat_simulation` evidence;
- Technology — purpose-built `Systems Diagnostic Practice Console` / `systems_diagnostic_practice` typed Skill Evidence.

The explicit generic `practice` action is object-targeted, colocated and capability-gated. Only purpose-built registered practice targets advertise it. Ordinary `use`, `inspect`, `research`, `monitor` or generic terminal/medical-station activity does not become XP.

## Newly identified structural gap — Skill meaning and creation contract

The current runtime can **store and progress a skill score**, but it does not yet have a canonical reusable definition for what a skill *means*.

Current `character_skills` rows primarily carry:
- `skill_key`;
- broad `category`;
- current `score`;
- legacy `tier`;
- `experience`;
- free-form metadata.

Current character seeds likewise name represented skills and scores but do not define authoritative scope or capability semantics.

Therefore the engine cannot yet answer in a generic deterministic way:
- what tasks/activities are inside vs outside a skill;
- which knowledge/abilities/subskills compose it;
- what prerequisite skills or knowledge are required;
- what a proficiency score means behaviorally;
- what difficulty/challenge levels the actor can attempt reliably;
- how the skill modifies action validation, quality, speed, resource use, success/failure or consequences;
- what kinds of evidence can legitimately teach/improve the skill;
- how practice, live application and related-skill transfer differ;
- what can decay, be retained, reacquired or transfer to another skill;
- how broad umbrella skills relate to narrower component skills;
- how future skill categories can be created consistently without bespoke engine code.

This gap is now higher priority than adding more progression mappings. **Do not expand Field Medicine, Survival or Weapons progression until the Skill Definition/Capability contract is designed and accepted.**

## Research direction — Skill Definition & Capability Framework

Research/design should precede runtime implementation. Use established skill/competency taxonomies as references, but adapt them to Observer Sandbox rather than copying any one framework.

The target should separate at least:
- **knowledge** — facts/concepts/procedures known;
- **skill** — ability to perform bounded tasks effectively;
- **competency / demonstrated capability** — reliable application under contextual responsibility/risk;
- **attributes/abilities** — underlying capacities that influence learning/performance but are not the skill itself.

A reusable skill definition should be capable of expressing:
1. stable identity and taxonomy;
2. plain-language definition and explicit scope boundaries;
3. parent/category and optional child/component relations;
4. prerequisite knowledge/skills/attributes;
5. task/action/application domains;
6. proficiency-level behavioral descriptors or capability bands;
7. difficulty/challenge model;
8. deterministic gameplay effects and limits;
9. legitimate acquisition/practice/application evidence families;
10. learning/transfer/saturation/retention hooks;
11. risk/failure/consequence semantics where relevant;
12. observability/grading/presentation metadata;
13. version/revision/source provenance.

Avoid a giant universal skill engine in the first implementation. The first deliverable should be a **docs/research-backed canonical Skill Definition Format + validation rules**, followed by one bounded exemplar migrated into that format before batching the remaining current skills.

## Current represented skills awaiting semantic definition review

- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Technology
- Field Medicine

Existing score/progression evidence remains valid unless the later semantic migration explicitly finds a conflict. Do not silently reinterpret historical evidence.

## Next development sequence

1. **Skill Definition & Capability Framework — research + canonical design — NEXT**;
2. define the minimum reusable Skill Creation Format and validation rules;
3. migrate **one bounded exemplar** to prove the format and gameplay-consumption contract;
4. batch structurally equivalent definitions for the other represented skills;
5. only then resume missing Skill Evidence/Progression coverage (Field Medicine, Survival, Weapons as justified);
6. Skill Retention / Reacquisition after semantic + acquisition-evidence coverage is broad enough;
7. intellectual attributes;
8. mental/emotion dynamics;
9. broader relationship/social systems and partnered/contextual sexual behavior;
10. broad Mind/Behavior architecture only after enough real feature families justify it.

## Next checkpoint — proposal/design stage

No runtime/schema implementation of the new Skill Definition architecture is yet canonical in this checkpoint.

Immediate work:
- research authoritative real-world skill/competency frameworks;
- audit current Observer Sandbox skill consumers/producers;
- propose the minimum canonical Skill Creation Format;
- identify what belongs in definition data vs generic engines vs per-domain adapters;
- define migration compatibility for existing `character_skills` and progression evidence;
- choose the first exemplar only after the definition contract is coherent.

## Deferred boundaries

Do not add economy/currency, careers/jobs/quests/salary, automatic restocking, deep crafting, Character Memory, broad Mind/Behavior, partnered sexual behavior, detailed endocrine simulation, a second production character solely for testing, or Tahoe exterior traversal as side effects.

## Exact resume point

Re-read current live production and canonical repository first.

**Skill Evidence Semantics v1 is complete/deployed/live-activated through PR #108 / Deploy #198. Technology proves the generic explicit-practice evidence path. Before adding more skill progression mappings, the next canonical priority is research/design of a reusable Skill Definition & Capability Framework so every current and future skill has explicit meaning, scope, prerequisites, capability/application semantics and learning evidence rules.**
