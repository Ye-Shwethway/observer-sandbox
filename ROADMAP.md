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

Skills:
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

## Remaining skill evidence gap

Represented skills not yet enabled:
- **Field Medicine** — current Diagnostic Station use is not treatment/practice evidence;
- **Survival** — current obstacle work is conditioning/movement, not fieldcraft evidence;
- **Weapons** — current Armory affordances are inspect/use, not weapon-practice evidence.

Generic `research` has no topic/domain semantics and remains non-XP. Do not infer learning from action names or model prose.

## Next development sequence

1. **Skill Practice Coverage Batch v1 — Field Medicine + Survival — NEXT**;
2. Weapons evidence only if a clean abstract/simulation-safe mapping is justified without unnecessary operational scope;
3. Skill Retention / Reacquisition after acquisition-evidence coverage is broader;
4. intellectual attributes;
5. mental/emotion dynamics;
6. broader relationship/social systems and partnered/contextual sexual behavior;
7. broad Mind/Behavior architecture only after enough real feature families justify it.

## Skill Practice Coverage Batch v1 — NEXT

The new `practice` evidence invariant is proven. The next slice should batch structurally equivalent simulation-safe mappings rather than introducing new engines.

Planned bounded batch:
- **Field Medicine** — purpose-built medical scenario/simulation practice target in the existing Medical Bay; explicit `field_medicine` relevance;
- **Survival** — purpose-built fieldcraft scenario/simulation practice target in an existing appropriate training space; explicit `survival` relevance.

Both should reuse exactly:
`practice action -> registered practice target -> typed skill_practice evidence -> existing Skill Progression`.

Constraints:
- no ordinary Diagnostic Station/Obstacle Course reinterpretation;
- no model-prose XP;
- no new score/XP formula;
- no new Telegram path;
- no Skill Retention/Decay;
- purpose-built targets remain simulation/training abstractions rather than claims that ordinary object use constitutes expertise;
- one focused regression suite + one disposable production-copy batch validator should cover every batched mapping.

Weapons remains deferred unless the existing abstraction can support it without broadening into operational weapon mechanics.

## Deferred boundaries

Do not add economy/currency, careers/jobs/quests/salary, automatic restocking, deep crafting, Character Memory, broad Mind/Behavior, partnered sexual behavior, detailed endocrine simulation, a second production character solely for testing, or Tahoe exterior traversal as side effects.

## Exact resume point

Re-read current live production and canonical repository first.

**Skill Evidence Semantics v1 is complete/deployed/live-activated through PR #108 / Deploy #198. Technology now proves the generic purpose-built `practice` evidence path. The next canonical slice is Skill Practice Coverage Batch v1 for Field Medicine + Survival using the proven pattern, while Weapons stays deferred unless a clean safe abstraction is justified.**
