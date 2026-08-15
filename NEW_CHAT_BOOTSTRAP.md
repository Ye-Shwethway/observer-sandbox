# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-15

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical contracts/source files
5. current live production evidence before implementation decisions.

Current Creator instruction and newer repository/CI/deploy/live evidence override older chat memory.

## Development workflow

Default:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use production-copy validation for concrete stateful/migration risk. Never accelerate/mutate production merely to manufacture acceptance evidence. New architecture/control/security invariants update their canonical contract + ROADMAP + bootstrap in the same development cycle.

## Current verified deployment checkpoint

Latest runtime deployment: **Deploy #194 / run `31865693609` SUCCESS**, Universal Profile Grading Framework v1 + current Profile Grading Coverage, PR #100 merge `2c28dbdd4b32084fd13df97290c7793e63f91d33`.

Post-merge main **CI #768 / run `31865693605` SUCCESS**.

Deploy readback at `2026-08-15T04:56:53Z` verified:
- service healthy/active;
- schema version 5;
- autonomy enabled, normal mode, 1.0x;
- Darian remained in ordinary autonomous state in the Master Suite; production was not manipulated for grading evidence;
- Telegram API connected, owner/allowed-user configuration present;
- Gemini `gemini-3.1-flash-lite` remains primary cognition;
- Groq `qwen/qwen3.6-27b` remains tested fallback evidence.

Grading is read-only interpretation; no production profile/skill/body mutation was used to prove it.

## Universal invariants

Darian/Thorne Estate are production exemplars, never reusable-engine identity.

Cognition:
`deterministic state/context -> one model proposal -> authoritative validation -> deterministic mutation`

Inventory/eating:
`universal definition -> concrete stack -> reachable action context -> structured quantity -> deterministic validation -> state transition + immutable evidence`

Body composition:
`bounded nutrition/energy evidence + current FM/FFM + resistance evidence + recovery + genetic envelope -> deterministic settlement -> coupled Weight/BF history + audit`

Body measurements:
`BC-2 settlement + regional resistance evidence + authored anatomy/genetic envelope + inactivity context -> bounded circumference settlement -> profile history + event`

Training:
`concrete target -> reusable method -> optional movement pattern(s) -> effective load -> deterministic method/anatomy evidence -> independent downstream progression engines`

Profile presentation:
`profile schema + section metadata + current represented values + caller role/sensitivity -> generic query -> read-only derived interpretation -> Telegram`

Profile grading:
`authoritative current value(s) + explicit named grading scheme + scheme-specific context -> derived grade metadata -> generic consumers`

Solo sexual regulation v1:
`adult actor + authored libido + release recency + recovery state + authorized private/alone context -> bounded drive -> cognition may propose self_satisfaction -> deterministic validation -> temporary sexual physiology + immutable action evidence -> rolling 7-day count`

Long-term sexual-drive direction:
`baseline libido + transient sexual arousal/cues + release recency/satiety + current physiology + later contextual/relationship/endocrine modifiers -> current sexual drive -> cognition chooses among legal actions`

Stress is not a prerequisite. No single hormone/media/cue/relationship variable is a mandatory trigger. Current v1 has no special deterministic stress/mood/fatigue/sleep/endocrine bonus.

## Completed current-scope foundations

Physical/profile/runtime foundations include:
- BC-2 Body Composition — PR #78 / Deploy #182;
- BC-3 Body Measurement — PR #82 / Deploy #183;
- Training Method Semantics v2 — PR #84 / Deploy #184;
- Training Anatomy / Movement Semantics v1 — PR #86 / Deploy #185;
- Regional Measurement Detraining v1 — PR #88 / Deploy #186;
- Height Lifecycle v1;
- Sexual Anatomy & Physiology Lifecycle v1;
- Male Erectile Physiology Canonical Contract — PR #92 / Deploy #189;
- Physical Profile Coverage Audit — PR #93;
- Physical Presentation Closure — PR #94 / Deploy #191;
- Telegram Profile Schema-Driven UX — PR #95 / Deploy #192;
- Solo Sexual Regulation v1 — PR #97 / Deploy #193;
- **Universal Profile Grading Framework v1 + Profile Grading Coverage — PR #100 / Deploy #194**.

Body authority remains:
- Weight/BF/FM/FFM — BC-2;
- circumferences — BC-3 + Training Anatomy + Regional Detraining;
- structural height — Height Lifecycle;
- structural male sexual anatomy — Sexual Anatomy Lifecycle;
- long-term erectile baseline — Sexual Physiology/canonical male profile contract;
- current sexual state — context-driven runtime physiology;
- grades — derived query-layer interpretation only, never body/progression authority.

## Universal Profile Grading Framework v1 — COMPLETE / DEPLOYED

Canonical:
- `docs/UNIVERSAL_PROFILE_GRADING_FRAMEWORK_V1.md`
- `docs/PROFILE_GRADING_COVERAGE_V1.md`
- `docs/READ_ONLY_GRADING_PROOF.md`

Shared vocabulary:
`E Beginner -> D Novice -> C Capable -> B Skilled -> A Advanced -> S Expert -> SS Elite -> SSS Master -> X Mythic -> XX Transcendent`.

Current scheme registry:
- `raps-100-proof-v1`: explicit compatible 0..100 Attributes, E..S only;
- `skill-proficiency-100-v1`: represented `character_skills.score`, E..S only;
- `body-aesthetic-proportion-v1`: selected aesthetics-oriented body target ranges;
- `body-central-adiposity-v1`: health-oriented waist/height target range;
- `body-physique-composite-v1`: read-time composite across compatible Body references.

Key contracts:
- grades never persist as competing truth;
- numeric field != automatically gradeable;
- IQ remains outside RAPS grading;
- Skills grade from current score while legacy `tier` is not grading authority;
- raw Body dimensions remain descriptive/ungraded;
- Body v1 grades derived waist/shoulders, waist/hips and waist/height references;
- chest/waist is context-only in v1;
- no `larger = better` body rule;
- no hard-coded popularized golden ratio;
- health, general aesthetics, bodybuilding/classic-physique and modelling may later use different named schemes over the same raw state;
- Telegram consumes generic grade metadata from the query layer.

Body v1 reference bands:
- waist/shoulders `0.55..0.65` (bounded around the ~0.6 adult-male preference reported in selected attractiveness literature);
- waist/hips `0.80..0.90` (selected adult-male attractiveness evidence);
- waist/height `0.40..0.49` (NICE adult central-adiposity guidance).

Current coverage classification:
- Attributes — graded;
- Skills — graded;
- Body — partially/compositely graded from explicit derived references;
- Appearance / Recovery — contextual-only;
- Personality / Preferences / Habits / Background — not gradeable by default;
- Sexual Anatomy & Physiology — contextual/not quality-graded by default.

PR #100 final tested head `4425c9b2d4bc0f5ee421f37c2031739cc7813f9e`:
- CI #767 / `31865642768` SUCCESS;
- Attribute Grading Batch 1 Acceptance #29 / `31865642781` SUCCESS on disposable production copy;
- Read-Only Grading Proof #30 / `31865642762` SUCCESS;
- Public Readiness Security Audit #54 / `31865642765` SUCCESS;
- merge `2c28dbdd4b32084fd13df97290c7793e63f91d33`;
- Deploy #194 / `31865693609` SUCCESS;
- main CI #768 / `31865693605` SUCCESS.

The production-copy acceptance proved current Attributes, derived Body grading, separate Skills grading, Telegram rendering, zero model calls, and unchanged persisted profile/skill state.

## Solo Sexual Regulation v1 — COMPLETE / DEPLOYED

Canonical: `docs/SOLO_SEXUAL_REGULATION_V1.md`.

The runtime has a bounded adult-only private/alone solo behavior loop independent of the future Relationship System. `self_satisfaction` is intimate at the observer policy layer, owner-visible and non-owner-redacted/hidden as appropriate. Structural anatomy and long-term erectile capacity are unchanged by ordinary sexual activity.

Current drive uses authored libido, release recency and immediate recovery state. Future sexual media/cues, relationships or endocrine context may become modifiers only when their own real evidence/authority exists. Do not invent testosterone from training/physique/Strength.

## Public repository security

`Ye-Shwethway/observer-sandbox` is PUBLIC. Public hardening remains in force. Sensitive/intimate production values must not be dumped into public CI logs merely for acceptance evidence. VPS-backed PR validation must fail closed for fork-originated PRs.

## Next development sequence

1. **Skill Progression Foundation v1 — Hand-to-Hand Combat exemplar**;
2. structurally equivalent Skill Progression batches;
3. Skill Retention / Reacquisition when justified;
4. intellectual attributes;
5. mental/emotion dynamics, including later contextual Solo Regulation stress/mood feedback when a real state authority exists;
6. broader relationship/social systems and partnered/contextual sexual behavior;
7. broad Mind/Behavior architecture only after enough real feature families justify it.

## Skill Progression resume constraints

Before mutation, inspect/reconcile:
- `character_skills.score` as current demonstrated proficiency;
- `experience` as accumulated legitimate learning/practice history rather than a duplicate score;
- persisted `tier` as legacy/compatibility data, not independent grade authority;
- duplicated skill-like RAPS fields (`combat_skill`, `weapons_proficiency`, `survival_skill`, etc.) so progression does not become split-brain;
- action/training/research evidence channels by skill type;
- retention/decay/reacquisition boundaries;
- generic actor/skill IDs.

Recommended first exemplar: **Hand-to-Hand Combat**.

Proposed invariant:
`skill-relevant completed practice + duration + challenge/quality + current proficiency + readiness/fatigue + recent practice history -> effective learning stimulus -> bounded proficiency adaptation + immutable evidence`

Reuse existing immutable action/training evidence. Physiology/body progression and Skill progression may consume the same evidence independently; neither should secretly own/call the other.

Do not invent historical XP on activation. Darian's represented current score is the baseline. Do not force live production training merely to produce acceptance evidence. Skill decay/retention remains a later bounded slice.

## Exact resume point

First re-read current live production and canonical repository.

**Universal Profile Grading Framework v1 and current Profile Grading Coverage are complete/deployed through PR #100 / Deploy #194. The next canonical development slice is Skill Progression Foundation v1 — Hand-to-Hand Combat exemplar.**

Do not add economy/currency, careers/jobs/quests/salary, automatic restocking, deep crafting, Character Memory, broad Mind/Behavior, partnered sexual behavior, detailed endocrine simulation, a second production character, or Tahoe exterior traversal as side effects.
