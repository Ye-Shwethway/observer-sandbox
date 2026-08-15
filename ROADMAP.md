# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Python/SQLite runtime and live world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutation.
- Telegram is an observer/control adapter, never a simulation engine.
- Preserve the LEGO runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are first rich production exemplars, never reusable-engine identity.
- Reusable runtime/cognition/progression/query/control/inventory/nutrition/training logic is actor/entity/definition-id driven.
- Prefer minimum-runnable reversible slices.
- Use one bounded exemplar for a genuinely new invariant, then batch structurally equivalent follow-ons.
- Default flow: `branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Use production-copy validation for concrete stateful/migration risk; never accelerate or directly mutate production merely to manufacture acceptance evidence.

## Current verified deployment baseline

Latest runtime deployment: **Deploy #194 / run `31865693609` SUCCESS**, Universal Profile Grading Framework v1 + current grading coverage closure, PR #100 merge `2c28dbdd4b32084fd13df97290c7793e63f91d33`.

Post-merge main **CI #768 / run `31865693605` SUCCESS**.

Deploy readback at `2026-08-15T04:56:53Z` verified:
- service healthy/active;
- schema version 5;
- autonomy enabled in normal mode at 1.0x;
- Darian remained in the Master Suite and continued ordinary autonomous state rather than being manipulated for grading evidence;
- Telegram API connected with owner/allowed-user configuration present;
- Gemini `gemini-3.1-flash-lite` remained the primary cognition binding;
- Groq `qwen/qwen3.6-27b` remained tested fallback evidence.

Grading validation is read-only. No live production profile/skill/body state was mutated to manufacture evidence.

## Completed foundations

- schema v4 composable runtime foundation, operationally extended by schema v5 inventory stacks;
- P0/P0.5 foundation + dynamic provider layer;
- P1 continuous autonomy;
- P2 Telegram Observer/Profile/Control;
- P2.3 Creator AI Control v1;
- Runtime Cognition Fallback v1;
- Telegram Home lifecycle;
- Universal Character Engine;
- Dynamic Resource Awareness / Choice Breadth;
- Object Familiarity / Inspect Utility Guard;
- fatigue/recovery, targeted training, readiness/effectiveness/effective load;
- Minimum Training Stimulus + Session Load/Recovery Guard;
- causal needs + sleep/circadian behavior;
- Physical Attribute Progression Framework v1 for Strength, Stamina, Agility, Speed, Reflexes, Endurance and Flexibility;
- universal inventory/eating/nutrition slices through Meal Choice Intelligence;
- BC-2 Body Composition and BC-3 Body Measurement progression;
- Training Method Semantics v2;
- Training Anatomy / Movement Semantics v1;
- Regional Measurement Detraining v1;
- Height Lifecycle v1;
- Sexual Anatomy & Physiology Lifecycle v1;
- Male Erectile Physiology Canonical Contract;
- Physical Profile Coverage Audit v1;
- Physical Presentation Closure v1;
- Telegram Profile Schema-Driven UX;
- Solo Sexual Regulation v1;
- **Universal Profile Grading Framework v1 + Profile Grading Coverage v1**.

## Universal Item / Eating Program

Invariant:
`Universal definition -> concrete stack -> reachable action context -> structured quantity -> deterministic validation -> state transition + immutable evidence`

- Inventory Foundation v1 — COMPLETE / DEPLOYED via PR #71 / Deploy #177.
- Inventory Operations v1 — COMPLETE / DEPLOYED via PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — COMPLETE / DEPLOYED via PR #74 / Deploy #179.
- Eating Behavior v1 — COMPLETE / DEPLOYED via PR #76 / Deploy #180.
- Meal Choice Intelligence v1 — COMPLETE / DEPLOYED via PR #77 / Deploy #181.

## Body Composition / Measurement Program

Research locks:
- no static universal `3500 kcal = 1 lb` rule;
- Weight/FM/FFM/BF% are coupled;
- genetics are character-specific potential envelopes;
- protein/energy availability constrain lean adaptation;
- circumference progression combines body composition with regional resistance context;
- regional detraining may reverse post-activation training-acquired excess but never reinterpret authored activation anatomy as untrained;
- detailed fluid/glycogen/endocrine/micronutrient simulation remains deferred.

### BC-2 — Body Composition Progression

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #78 / Deploy #182.

Invariant:
`complete bounded nutrition/energy evidence + current FM/FFM + resistance evidence + recovery + genetic envelope -> deterministic settlement -> coupled Weight/BF history + event`

Weight progression/decline is already owned by BC-2. Do not add a second Weight decay authority.

### BC-3 — Body Measurement Progression

**COMPLETE / DEPLOYED / LIVE-ACTIVATED** via PR #82 / Deploy #183.

Covers neck, shoulders, chest, waist, hips, biceps relaxed/flexed, triceps, forearms, thighs and calves. Regional adaptation consumes movement-aware training evidence; Darian's authored measurements/genetic envelopes remain exemplar data, not universal formulas.

### Regional Measurement Detraining v1

**COMPLETE / DEPLOYED** via PR #88 / Deploy #186.

Invariant:
`BC-3 activation baseline + immutable regional resistance history + bounded BC-2 settlement -> inactivity pressure -> reversible post-activation regional excess decay`

No second body progression authority and no double-counting of systemic FFM loss.

## Training semantics foundation

### Training Method Semantics v2

**COMPLETE / DEPLOYED** via PR #84 / Deploy #184.

`concrete training target -> target binding -> reusable method definition -> effective-load evidence -> downstream progression`

### Training Anatomy / Movement Semantics v1

**COMPLETE / DEPLOYED** via PR #86 / Deploy #185.

`train target -> reusable method -> validated movement pattern(s) -> regional anatomy evidence -> downstream progression`

Reusable methods/movements contain no actor identity. Historical method-level fallback remains for old/no-selection evidence.

## Physical Profile Completion Gate — COMPLETE FOR CURRENT SCOPE

Authority map:
- Weight/BF/FM/FFM — BC-2;
- circumferences — BC-3 + Training Anatomy + Regional Detraining;
- structural Height — Height Lifecycle;
- male structural sexual anatomy — Sexual Anatomy Lifecycle;
- long-term erectile baseline — Sexual Physiology Lifecycle/canonical male profile contract;
- current sexual state — context-driven runtime physiology, with Solo Regulation as the first implemented explicit behavior driver;
- composition-linked visible abdominal definition — derived presentation;
- stable appearance anchors remain canonical until a real dynamic owner exists;
- broader health vitals/injury/illness are explicit future domains, not fake static simulation.

Male canonical profiles require structural sexual anatomy/genetic targets plus long-term `baseline_erectile_function` and `erection_firmness_cap`. These are per-character inputs; Darian is only the first rich exemplar.

Relevant completed slices:
- Male Erectile Physiology Canonical Contract — PR #92 / Deploy #189;
- Physical Profile Coverage Audit — PR #93;
- Physical Presentation Closure — PR #94 / Deploy #191;
- Telegram Profile Schema-Driven UX — PR #95 / Deploy #192;
- Solo Sexual Regulation v1 — PR #97 / Deploy #193;
- Universal Profile Grading Framework v1 — PR #100 / Deploy #194.

## Telegram Profile Schema-Driven UX — COMPLETE / DEPLOYED

Canonical: `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`.

`config/profile_sections.v1.json` externalizes:
`domain/collection -> section id + label + icon + order + visibility + renderer kind + sensitivity`

Ordinary sections are metadata-driven. The owner-only Sexual Anatomy & Physiology section exposes represented sexual anatomy/long-term physiology/RAPS-SA information and genuinely materialized current sexual state. Non-owner direct access fails closed.

## Universal Profile Grading Framework v1 — COMPLETE / DEPLOYED

Canonical:
- `docs/UNIVERSAL_PROFILE_GRADING_FRAMEWORK_V1.md`
- `docs/PROFILE_GRADING_COVERAGE_V1.md`
- historical Attribute proof: `docs/READ_ONLY_GRADING_PROOF.md`

Core invariant:
`authoritative current value(s) + explicit named grading scheme + scheme-specific context -> derived grade metadata -> generic consumers`

Shared vocabulary remains:
`E Beginner -> D Novice -> C Capable -> B Skilled -> A Advanced -> S Expert -> SS Elite -> SSS Master -> X Mythic -> XX Transcendent`.

Current scheme registry:
- `raps-100-proof-v1` — explicit compatible 0..100 Attributes, E..S only;
- `skill-proficiency-100-v1` — represented learned-skill scores, E..S only;
- `body-aesthetic-proportion-v1` — selected aesthetics-oriented target ranges;
- `body-central-adiposity-v1` — health-oriented waist/height reference;
- `body-physique-composite-v1` — read-time compatible Body composite.

Rules locked by PR #100:
- grades are never persisted state;
- numeric fields do not automatically become gradeable;
- IQ remains outside the RAPS scheme;
- Skills grade from `character_skills.score`; persisted `tier` is not grading authority;
- raw Body measurements remain descriptive/ungraded rather than `larger = better`;
- Body v1 derives waist/shoulders, waist/hips and waist/height graded references plus chest/waist context;
- no popularized golden-ratio constant is encoded as universal truth;
- health, general aesthetics, bodybuilding/classic-physique and modelling may later be separate named interpretations over the same authoritative body state;
- Telegram consumes generic query-layer grade metadata.

Body v1 references:
- waist/shoulders `0.55..0.65`, centered around the ~0.6 adult-male preference reported by the selected attractiveness evidence;
- waist/hips `0.80..0.90` from selected adult-male attractiveness evidence;
- waist/height `0.40..0.49` from NICE adult central-adiposity guidance;
- chest/waist remains context-only because v1 does not encode an unsupported single universal optimum.

Current grading coverage:
- Attributes — graded;
- Skills — graded;
- Body — partially/compositely graded through explicit derived references;
- Appearance and Recovery — contextual only;
- Personality, Preferences/Habits and Background — not gradeable by default;
- Sexual Anatomy & Physiology — contextual/not quality-graded by default.

Final PR #100 tested head `4425c9b2d4bc0f5ee421f37c2031739cc7813f9e`:
- CI #767 / `31865642768` SUCCESS;
- Attribute Grading Batch 1 Acceptance #29 / `31865642781` SUCCESS on disposable production copy;
- Read-Only Grading Proof Acceptance #30 / `31865642762` SUCCESS;
- Public Readiness Security Audit #54 / `31865642765` SUCCESS;
- merge `2c28dbdd4b32084fd13df97290c7793e63f91d33`;
- Deploy #194 / `31865693609` SUCCESS;
- main CI #768 / `31865693605` SUCCESS.

The production-copy acceptance proves raw profile and skill persistence remain unchanged while derived Body/Skill grading and Telegram rendering work against copied production state. No model call is needed.

## Solo Sexual Regulation v1 — COMPLETE / DEPLOYED

Canonical: `docs/SOLO_SEXUAL_REGULATION_V1.md`.

Current v1 invariant:
`adult actor + authored libido + release recency + recovery state + authorized private/alone context -> bounded solo-regulation drive -> cognition may propose self_satisfaction -> deterministic validation -> temporary sexual physiology + immutable action evidence -> rolling 7-day count`

Long-term drive contract:
`baseline libido + transient sexual arousal/cues + release recency/satiety + current physiological state + later contextual/relationship/endocrine modifiers -> current sexual drive -> cognition may choose among legal actions`

Key boundaries:
- adult-only;
- private authored location + resident authorization + no colocated represented character;
- bounded drive threshold and anti-loop pacing guard;
- no fixed weekly quota;
- stress is not a prerequisite or mandatory trigger;
- no single hormone/media/cue/relationship variable is a mandatory trigger;
- no testosterone surrogate inferred from training/body composition;
- future sexual-media/cue exposure may modulate transient arousal only when real content/event evidence exists;
- future endocrine effects require an explicit endocrine authority rather than invented testosterone values;
- current v1 does not apply action-specific stress reduction, mood/fatigue/sleep bonus or endocrine cascade;
- later stress/mood feedback must be contextual and conditional, not a reason to manufacture stress;
- no partnered sexual behavior or Relationship System dependency in v1;
- no structural anatomy or long-term erectile-capacity mutation from ordinary sexual activity.

## Public Repository Security — COMPLETE / PUBLIC

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md`, `SECURITY.md`.

Public hardening remains in force. VPS-backed PR validation must fail closed for fork-originated PRs, and sensitive/intimate production values must not be dumped into public logs merely for evidence.

## Next development sequence

1. **Skill Progression Foundation v1 — Hand-to-Hand Combat exemplar**;
2. Skill Progression follow-on batches by proven structural pattern;
3. Skill Retention / Reacquisition when justified;
4. intellectual attributes;
5. mental/emotion dynamics, including later contextual Solo Regulation stress/mood feedback when a real state authority exists;
6. broader relationship/social systems and partnered/contextual sexual behavior;
7. broad Mind/Behavior architecture only after enough real feature signals justify it.

Post-public GitHub settings verification remains opportunistic and non-blocking.

## Skill Progression Family — NEXT

Do not treat Skills as merely renamed RAPS physical attributes.

Existing grading is presentation only. Before progression mutation, reconcile:
- `character_skills` schema/current data and Telegram Skills view;
- `character_skills.score` as current proficiency authority;
- accumulated `experience` as learning/practice evidence rather than a duplicate score;
- persisted `tier` as legacy/compatibility data, not an independently mutable grade authority;
- duplicated skill-like RAPS fields such as combat/weapons/survival so they do not become split-brain progression authorities;
- action/training/research evidence that can legitimately improve each skill;
- retention/decay/reacquisition semantics;
- generic actor/skill IDs rather than Darian-specific logic.

Recommended first bounded exemplar:
**Hand-to-Hand Combat**.

Proposed invariant:
`skill-relevant completed practice + duration + challenge/quality + current proficiency + readiness/fatigue + recent practice history -> effective learning stimulus -> bounded proficiency adaptation + immutable evidence`

Use existing training/action evidence as the shared event source. Skill progression and physiology/body progression may consume the same immutable action evidence independently; they must not call one another as hidden authorities.

Do not invent historical experience on activation. Darian's represented current score is the baseline; future legitimate completed actions create new progression evidence naturally. Do not force live production training merely to prove an occurrence.

Decay/retention remains a later bounded slice after acquisition/progression semantics are proven.

## Future universal object/inventory expansion

When justified: movable containers/carried inventory; fixed storage capacity; training equipment instances; tools/electronics/books/medical supplies; clothing/equipped state; materials/crafting; eventually economy/ownership/pricing/currency.

## Deferred boundaries

Do not add as side effects:
- broad Mind/Behavior Engine;
- Character Memory Engine;
- multi-fallback/circuit-breaker/provider-health expansion;
- Telegram secret/model-parameter editing;
- second production character solely for testing;
- automatic restocking, deep recipes, economy/currency, generalized crafting;
- detailed endocrine/micronutrient/organ simulation;
- partnered sexual behavior / relationship sexual mechanics before that family is explicitly entered;
- estate exterior/Tahoe traversal.

## Exact resume point

Re-read live production and current canonical repository first.

**Universal Profile Grading Framework v1 and current Profile Grading Coverage are complete/deployed through PR #100 / Deploy #194. The next canonical development slice is Skill Progression Foundation v1 using Hand-to-Hand Combat as the bounded exemplar.**

Start by resolving skill authority (`score` / `experience` / legacy `tier` and duplicated RAPS skill-like fields), then establish skill-specific immutable learning evidence and one minimum-runnable progression invariant before batching other skills.
