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

Latest runtime deployment: **Deploy #197 / run `31870118116` SUCCESS**, Tactical Planning Skill Progression v1, PR #106 merge `fc0fb067681f1b6481eab330a21cc902ed44b497`.

Post-merge:
- CI #794 / run `31870118123`: SUCCESS;
- Tactical Planning Acceptance #2 / run `31870118233`: SUCCESS;
- Hand-to-Hand Skill Progression Foundation Acceptance #5 / run `31870118205`: SUCCESS.

Readback verified:
- service healthy/active;
- schema v5;
- autonomy enabled, normal mode, 1.0x;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback evidence preserved;
- Telegram connected with owner/allowed-user configuration;
- Tactical Planning remained at represented `92.0 / S Expert` after deployment, proving no retroactive activation jump.

Do not force live training to demonstrate progression. Natural future eligible practice may supply occurrence evidence.

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

Skill evidence direction:
`validated domain-specific practice/task + explicit skill relevance + bounded duration/quality/context -> immutable structured learning evidence -> generic Skill Progression settlement`

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
- **Tactical Planning Skill Progression v1 — PR #106 / Deploy #197**.

Detailed semantics/evidence are in the feature docs referenced by `ROADMAP.md`.

## Current authority map

Physical/profile:
- Weight/BF/FM/FFM — BC-2;
- circumferences — BC-3 + Training Anatomy + Regional Detraining;
- Height — Height Lifecycle;
- structural male sexual anatomy — Sexual Anatomy Lifecycle;
- long-term erectile baseline/cap — Sexual Physiology;
- current sexual state — context-driven runtime physiology;
- grades — read-time derived only;
- change ledgers/notification baselines — observer UX state only.

Skills:
- `character_skills.score` = authoritative current proficiency;
- `character_skills.experience` = legitimate accumulated post-activation learning evidence;
- persisted `tier` = legacy compatibility only;
- grade = read-time `skill-proficiency-100-v1`;
- RAPS skill-like fields are not independent mutable Skill progression truth.

Model prose, action reasons and Telegram never directly mutate skill proficiency.

## Grading / change presentation

Shared vocabulary:
`E Beginner -> D Novice -> C Capable -> B Skilled -> A Advanced -> S Expert -> SS Elite -> SSS Master -> X Mythic -> XX Transcendent`.

Current RAPS/Skill 0..100 schemes legitimately use E..S. Grades are derived, never persisted competing state.

Change observability currently uses cumulative significance including Skill/RAPS `0.10`, body circumference `0.05 in`, Height `0.10 in`, Weight `0.25 lb`, Body Fat `0.10` pp and ratio `0.01`. Grade transitions are immediately significant. Ordinary pushes are aggregated/debounced; Profile deltas remain available independently of notification state.

## Skill Progression — current live coverage

Canonical:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`;
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`.

Shared proven behavior:
- initialize/deploy zero-gain bootstrap consumes historical eligible evidence without retroactive score/XP;
- future eligible evidence can progress score/experience;
- recent-practice saturation + current-proficiency diminishing returns bound growth;
- action evidence cannot be double-counted;
- reseeding preserves earned/activated Skill state;
- generic grading/Profile delta/notification layers consume authoritative score changes automatically.

Live-enabled progression:
- Hand-to-Hand Combat — structured combat Training Method evidence;
- Tactical Planning — direct `vr_tactical_drills` plus reduced mixed `ai_combat_simulation` evidence.

## Remaining represented skill gap

Do not enable these from weak/generic evidence:
- Weapons — Armory inspect/use is not weapon practice;
- Survival — obstacle conditioning is not fieldcraft;
- Technology — generic terminal/workstation use or generic Research is not a technical task/topic/work product;
- Field Medicine — Diagnostic Station use is not medical practice/treatment.

Generic `research` currently has no topic/domain semantics and was explicitly introduced without Skill XP/progression. Never infer learning from action name or model reason prose.

## Next canonical slice

**Skill Evidence Semantics v1 — one bounded safe exemplar.**

Purpose: establish reusable structured evidence for a remaining learned skill when Training Method semantics are insufficient.

Candidate invariant:
`validated domain-specific practice/task + explicit skill relevance + bounded duration/quality/context -> immutable structured learning evidence -> existing generic Skill Progression settlement`

Constraints:
- one safe exemplar for the new evidence invariant, then batch equivalent mappings;
- no generic `use`/`inspect`/`research` XP;
- no actor-specific hard-coding;
- no new competing score/experience authority;
- reuse existing Skill Progression bootstrap, formula, idempotency, reseed safety, grading and change observability;
- no Skill Retention/Decay yet;
- keep any new object/action semantics abstract, simulation-safe and minimum-runnable.

## Deferred boundaries

Do not add economy/currency, careers/jobs/quests/salary, automatic restocking, deep crafting, Character Memory, broad Mind/Behavior, partnered sexual behavior, detailed endocrine simulation, a second production character solely for testing, or Tahoe exterior traversal as side effects.

## Exact resume point

First re-read verified production and the current canonical repository.

**Tactical Planning Skill Progression v1 is complete/deployed/live-activated through PR #106 / Deploy #197. Hand-to-Hand + Tactical Planning prove the generic Skill Progression engine. Next: Skill Evidence Semantics v1 using one bounded safe exemplar for a remaining represented skill that lacks legitimate structured practice evidence.**
