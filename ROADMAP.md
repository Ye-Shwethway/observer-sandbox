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

Latest runtime deployment: **Deploy #197 / run `31870118116` SUCCESS**, Tactical Planning Skill Progression v1, PR #106 merge `fc0fb067681f1b6481eab330a21cc902ed44b497`.

Post-merge:
- main CI #794 / run `31870118123`: SUCCESS;
- Tactical Planning Acceptance #2 / run `31870118233`: SUCCESS;
- Hand-to-Hand Skill Progression Foundation Acceptance #5 / run `31870118205`: SUCCESS.

Deploy readback verified:
- service healthy/active;
- schema version 5;
- autonomy enabled, normal mode, 1.0x;
- Telegram connected with owner/allowed-user configuration present;
- Gemini `gemini-3.1-flash-lite` primary cognition preserved;
- Groq `qwen/qwen3.6-27b` tested fallback preserved;
- live Tactical Planning remained at represented `92.0 / S Expert` after activation, proving no retroactive score jump.

No live Tactical/Combat practice was forced or accelerated for evidence.

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
- Skill Progression Foundation v1 — Hand-to-Hand Combat — PR #104 / Deploy #196;
- **Tactical Planning Skill Progression v1 — PR #106 / Deploy #197**.

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

Skills:
- `character_skills.score` — authoritative current proficiency;
- `character_skills.experience` — accumulated legitimate post-activation learning evidence;
- persisted `tier` — legacy/compatibility only;
- grade — read-time `skill-proficiency-100-v1`;
- RAPS skill-like fields (`combat_skill`, `weapons_proficiency`, `survival_skill`, etc.) are not independent live progression authorities.

## Profile grading / change observability

Universal grading vocabulary remains:
`E Beginner -> D Novice -> C Capable -> B Skilled -> A Advanced -> S Expert -> SS Elite -> SSS Master -> X Mythic -> XX Transcendent`.

Current 0..100 RAPS/Skill schemes legitimately reach E..S only. Grades are never persisted competing truth. Raw body dimensions remain descriptive rather than `larger = better`.

Change observability remains generic:
- Skill/RAPS significance `0.10` cumulative;
- body circumference `0.05 in`, Height `0.10 in`, Weight `0.25 lb`, Body Fat `0.10` pp, ratios `0.01`;
- grade transitions immediately significant;
- Profile `▲/▼`; benefit color only where semantics justify it;
- ordinary push debounce 5 real minutes per recipient/character;
- `/statnotify` + Character toggle provide per-character notification control.

Canonical: `docs/UNIVERSAL_PROFILE_GRADING_FRAMEWORK_V1.md`, `docs/PROFILE_GRADING_COVERAGE_V1.md`, `docs/CHARACTER_CHANGE_OBSERVABILITY_V1.md`.

## Skill Progression family

Canonical:
- `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`;
- `docs/SKILL_PROGRESSION_TACTICAL_V1.md`.

Proven invariant:
`completed skill-relevant structured evidence + effective duration + explicit method relevance + current proficiency + recent-practice saturation -> effective learning units -> bounded score/experience settlement + immutable audit event`

Shared behavior:
- zero-gain initialize/deploy bootstrap consumes historical eligible evidence without retroactive XP/score;
- future eligible practice may progress score/experience;
- 24-sim-hour saturation + current-proficiency diminishing returns bound growth;
- consumed action event IDs cannot be credited twice;
- reseeding preserves progression-active/experienced and extra learned skills;
- authoritative score changes inherit generic grading/Profile deltas/notifications;
- no skill-specific Telegram subsystem.

Current live-enabled skills:
- Hand-to-Hand Combat — structured combat Training Method evidence;
- Tactical Planning — `vr_tactical_drills` direct evidence and mixed `ai_combat_simulation` cross-training.

## Remaining skill evidence gap

Represented skills still lacking sufficiently specific structured learning evidence:
- **Weapons** — current Armory affordances are inspect/use, not weapon-practice evidence;
- **Survival** — current obstacle work is conditioning/movement, not fieldcraft evidence;
- **Technology** — terminal/workstation use and generic Research do not encode a technical task/topic/work product;
- **Field Medicine** — Diagnostic Station use does not encode medical practice/treatment evidence.

Generic `research` has no topic/domain semantics and was explicitly introduced without skill progression. Do not infer XP from action names or model reason prose.

## Next development sequence

1. **Skill Evidence Semantics v1 — one bounded safe exemplar — NEXT**;
2. batch remaining skills by proven evidence pattern where structurally equivalent;
3. Skill Retention / Reacquisition after acquisition-evidence coverage is broader;
4. intellectual attributes;
5. mental/emotion dynamics;
6. broader relationship/social systems and partnered/contextual sexual behavior;
7. broad Mind/Behavior architecture only after enough real feature families justify it.

## Skill Evidence Semantics v1 — NEXT

Purpose: create a reusable structured contract for legitimate skill-improving practice/task evidence that current Training Method semantics do not cover.

Minimum invariant candidate:
`validated domain-specific practice/task + explicit skill relevance + bounded duration/quality/context -> immutable structured learning evidence -> existing generic Skill Progression settlement`

Constraints:
- one safe exemplar first; do not simultaneously invent four unrelated evidence families;
- no learning from generic `use`, `inspect`, `research` or free-form model prose;
- no actor-specific hard-coding;
- no second Skill score/XP authority;
- existing Skill Progression formula/bootstrap/idempotency/reseed/observability must be reused;
- do not add Retention/Decay in this slice;
- if an exemplar needs a new object/action definition, keep it abstract, simulation-safe and minimum-runnable.

After the exemplar proves the evidence contract, structurally equivalent evidence mappings should be batched.

## Deferred boundaries

Do not add as side effects:
- economy/currency, careers/jobs/quests/salary;
- automatic restocking, deep crafting;
- Character Memory or broad Mind/Behavior;
- partnered sexual behavior;
- detailed endocrine/micronutrient/organ simulation;
- second production character solely for testing;
- Tahoe exterior traversal.

## Exact resume point

Re-read current live production and canonical repository first.

**Tactical Planning Skill Progression v1 is complete/deployed/live-activated through PR #106 / Deploy #197. Hand-to-Hand and Tactical Planning now prove the generic Skill Progression engine. The next canonical slice is Skill Evidence Semantics v1 using one bounded safe exemplar for a remaining skill whose current runtime lacks legitimate structured practice evidence.**
