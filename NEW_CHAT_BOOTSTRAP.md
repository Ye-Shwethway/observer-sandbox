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

Use **exemplar-first, then batch-by-pattern**: one bounded exemplar proves a genuinely new invariant; structurally equivalent follow-ons must be batched rather than split into repetitive PR/deploy cycles.

## Current verified deployment checkpoint

Latest runtime deployment: **Deploy #196 / run `31869399038` SUCCESS**, Skill Progression Foundation v1 — Hand-to-Hand Combat exemplar, PR #104 merge `a8c86705700f689024c75fe91e00be9361ae557a`.

Post-merge:
- CI #790 / run `31869399041`: SUCCESS;
- Skill Progression Foundation v1 Acceptance #3 / run `31869399147`: SUCCESS on main.

Deploy readback verified:
- service healthy/active;
- schema version 5;
- autonomy enabled, normal mode, 1.0x;
- Telegram API connected with owner/allowed-user configuration present;
- Gemini `gemini-3.1-flash-lite` remains primary cognition;
- Groq `qwen/qwen3.6-27b` remains tested fallback evidence;
- live Hand-to-Hand query presentation remained at its represented baseline after bootstrap, so deployment did not create a retroactive skill-score jump.

Do not force or accelerate combat training merely to demonstrate Skill Progression. Natural future eligible practice may provide live occurrence evidence.

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

Profile change observability:
`authoritative mutation/history -> domain-aware cumulative delta -> significance policy -> grade-transition check -> presentation ledger -> Profile delta UX + eligible aggregated notification`

Skill progression:
`completed skill-relevant evidence + effective duration/quality + explicit skill relevance + current proficiency + recent-practice saturation -> effective learning units -> bounded score/experience settlement + immutable audit event`

Solo sexual regulation v1:
`adult actor + authored libido + release recency + recovery state + authorized private/alone context -> bounded drive -> cognition may propose self_satisfaction -> deterministic validation -> temporary sexual physiology + immutable action evidence -> rolling 7-day count`

## Completed current-scope foundations

Current major completed slices include:
- P0/P0.5 runtime/provider foundation;
- P1 continuous autonomy;
- P2 Telegram Observer/Profile/Control;
- P2.3 Creator AI Control v1;
- Runtime Cognition Fallback v1;
- Universal Character Engine;
- Dynamic Resource Awareness / Choice Breadth;
- Object Familiarity / Inspect Utility Guard;
- fatigue/recovery, targeted training, readiness/effectiveness/effective load;
- Minimum Training Stimulus + Session Load/Recovery Guard;
- causal needs + sleep/circadian behavior;
- Physical Attribute Progression Framework v1;
- inventory/eating/nutrition through Meal Choice Intelligence;
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
- Universal Profile Grading Framework v1 — PR #100 / Deploy #194;
- Character Change Observability & Notification Foundation v1 — PR #102 / Deploy #195;
- **Skill Progression Foundation v1 — Hand-to-Hand Combat — PR #104 / Deploy #196**.

## Current authority map

Physical/profile:
- Weight/BF/FM/FFM — BC-2;
- circumferences — BC-3 + Training Anatomy + Regional Detraining;
- structural height — Height Lifecycle;
- structural male sexual anatomy — Sexual Anatomy Lifecycle;
- long-term erectile baseline/cap — Sexual Physiology/canonical male profile contract;
- current sexual state — context-driven runtime physiology;
- grades — derived query-layer interpretation only;
- change ledgers/notification baselines — derived UX/preference state only.

Skills:
- `character_skills.score` — authoritative current proficiency;
- `character_skills.experience` — accumulated legitimate post-activation learning evidence;
- persisted `tier` — legacy/compatibility only;
- read-time grade — `skill-proficiency-100-v1`;
- RAPS skill-like fields such as `combat_skill`, `weapons_proficiency`, `survival_skill` are not independent live progression authorities.

## Universal Profile Grading — COMPLETE / DEPLOYED

Canonical:
- `docs/UNIVERSAL_PROFILE_GRADING_FRAMEWORK_V1.md`
- `docs/PROFILE_GRADING_COVERAGE_V1.md`
- `docs/READ_ONLY_GRADING_PROOF.md`

Shared vocabulary:
`E Beginner -> D Novice -> C Capable -> B Skilled -> A Advanced -> S Expert -> SS Elite -> SSS Master -> X Mythic -> XX Transcendent`.

Grades are derived only. Numeric fields are not automatically gradeable. IQ remains outside current RAPS grading. Skills grade from authoritative `character_skills.score`. Raw Body dimensions remain descriptive; Body v1 uses explicitly named derived reference schemes rather than `larger = better` or a universal golden-ratio constant.

Checkpoint: PR #100 / Deploy #194.

## Character Change Observability — COMPLETE / DEPLOYED

Canonical: `docs/CHARACTER_CHANGE_OBSERVABILITY_V1.md`.

Current behavior:
- microscopic changes accumulate against display/notification baselines;
- Skill/RAPS significance default `0.10` points;
- Body circumference `0.05 in`, Height `0.10 in`, Weight `0.25 lb`, Body Fat `0.10` pp, ratio `0.01`;
- grade transitions are immediately significant;
- Profile deltas remain visible even when notifications are off;
- ordinary pushes are aggregated and debounced to one per recipient/character per 5 real minutes;
- grade transitions bypass ordinary debounce;
- `/statnotify` + Character detail provide per-character gate;
- OFF→ON/global toggles reset baselines and do not replay backlog;
- profile-less actors no-op safely.

Checkpoint: PR #102 / Deploy #195.

## Skill Progression Foundation v1 — COMPLETE / DEPLOYED / LIVE-ACTIVATED

Canonical: `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`.

Hand-to-Hand exemplar:
- consumes immutable `action_completed` evidence reconstructed through Training Method Semantics;
- currently recognizes configured combat methods such as Heavy Bag, Combat Mat, Technical Dummy, AI Combat Simulation and Combat Pit drills;
- non-combat training such as free weights does not improve Hand-to-Hand merely because it is a `train` action;
- zero-gain bootstrap occurs at initialize/deploy and cursor-consumes historical eligible evidence without retroactive XP/score;
- future eligible practice progresses `score` and `experience` with recent-practice saturation and current-proficiency diminishing returns;
- consumed action event IDs cannot be credited twice;
- canonical reseeding preserves progression-active/experienced skill state and extra learned skills;
- internal progression receipts remain audit evidence and are excluded from user-facing Recent Activity;
- authoritative score changes automatically inherit existing grading/Profile delta/notification behavior.

Validation checkpoint:
- PR #104 final tested head `bc0dd277013c9cbed727fa48880dc2ff1258cc20`;
- CI #789 SUCCESS;
- focused production-copy acceptance #2 SUCCESS;
- Public Readiness Security Audit #58 SUCCESS;
- merge `a8c86705700f689024c75fe91e00be9361ae557a`;
- Deploy #196 SUCCESS;
- post-merge CI #790 SUCCESS;
- main focused acceptance #3 SUCCESS.

Production was not moved/trained/accelerated to manufacture evidence.

## Solo Sexual Regulation v1 — COMPLETE / DEPLOYED

Canonical: `docs/SOLO_SEXUAL_REGULATION_V1.md`.

Current drive uses authored libido, release recency and immediate recovery state. Stress is not a prerequisite. No fixed weekly quota, testosterone surrogate, partnered behavior, structural-anatomy mutation or special deterministic stress/mood/sleep reward exists in v1.

Its production-copy acceptance now establishes deterministic eligible preconditions only inside the disposable copy rather than assuming current live cooldown/recovery state.

## Public repository security

`Ye-Shwethway/observer-sandbox` is PUBLIC. Public hardening remains in force. Sensitive/intimate production values must not be dumped into public CI logs merely for acceptance evidence. VPS-backed PR validation must fail closed for fork-originated PRs.

## Next development sequence

1. **Skill Progression follow-on batch by proven evidence pattern — NEXT**;
2. additional Skill Progression batches only where legitimate existing evidence supports them;
3. Skill Retention / Reacquisition when justified;
4. intellectual attributes;
5. mental/emotion dynamics;
6. broader relationship/social systems and partnered/contextual sexual behavior;
7. broad Mind/Behavior architecture only after enough real feature families justify it.

## Next slice constraints

The Hand-to-Hand exemplar has proven the structural invariant. Do not implement one PR/deploy per remaining skill.

Before mutation:
- inventory represented remaining skills against current immutable evidence sources;
- group only structurally equivalent mappings;
- use existing Training Method evidence for combat-practice mappings where legitimate;
- use existing Research/action evidence for technical/cognitive skills only where current semantics are concrete enough;
- require real fieldcraft/practical action evidence for Survival-like skills;
- defer any skill that would require inventing a major new subsystem;
- keep the same `score`/`experience` authority, bootstrap, idempotency and reseed-safety contracts;
- do not add Skill Retention/Decay yet;
- do not create mutable split-brain RAPS aliases;
- reuse generic grading/change-observability/notification layers rather than skill-specific Telegram code.

## Exact resume point

First re-read current live production and canonical repository.

**Skill Progression Foundation v1 — Hand-to-Hand Combat exemplar is complete/deployed through PR #104 / Deploy #196. The next canonical development slice is a Skill Progression follow-on batch by proven evidence pattern.**

Start by inventorying the remaining represented skills against already-existing immutable training/action/research evidence. Batch only mappings that can be justified now; defer the rest.

Do not add economy/currency, careers/jobs/quests/salary, automatic restocking, deep crafting, Character Memory, broad Mind/Behavior, partnered sexual behavior, detailed endocrine simulation, a second production character or Tahoe exterior traversal as side effects.
