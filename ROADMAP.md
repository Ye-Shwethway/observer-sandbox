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

Latest runtime deployment: **Deploy #193 / run `31860951081` SUCCESS**, Solo Sexual Regulation v1, PR #97 merge `60e1e3949631e1284e41ae0940a03fb02421fef8`.

Post-merge main **CI #757 / run `31860951093` SUCCESS**.

Deploy readback verified service healthy/active, autonomy enabled in normal mode at 1.0x, Darian sleeping in the Master Suite at sim time `2025-05-05T19:49:00+00:00`, Telegram API connected, Gemini primary cognition preserved and Groq fallback available.

Sensitive production profile/action values are intentionally not dumped into public GitHub Actions evidence. Do not accelerate production merely to manufacture a Solo Regulation occurrence.

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
- Telegram Profile Schema-Driven UX + dynamic grading presentation;
- **Solo Sexual Regulation v1**.

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

Weight progression/decline is already owned by BC-2. **Do not add a second Weight decay authority.**

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
- current sexual state — context-driven runtime physiology, now with Solo Regulation as the first implemented explicit behavior driver;
- composition-linked visible abdominal definition — derived presentation;
- stable appearance anchors remain canonical until a real dynamic owner exists;
- broader health vitals/injury/illness are explicit future domains, not fake static simulation.

Male canonical profiles require structural sexual anatomy/genetic targets plus long-term `baseline_erectile_function` and `erection_firmness_cap`. These are per-character inputs; Darian is only the first rich exemplar.

Relevant completed slices:
- Male Erectile Physiology Canonical Contract — PR #92 / Deploy #189;
- Physical Profile Coverage Audit — PR #93;
- Physical Presentation Closure — PR #94 / Deploy #191;
- Telegram Profile Schema-Driven UX — PR #95 / Deploy #192;
- Solo Sexual Regulation v1 — PR #97 / Deploy #193.

## Telegram Profile Schema-Driven UX — COMPLETE / DEPLOYED

Canonical: `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`.

`config/profile_sections.v1.json` externalizes:
`domain/collection -> section id + label + icon + order + visibility + renderer kind + sensitivity`

Ordinary sections are metadata-driven. The owner-only Sexual Anatomy & Physiology section exposes represented sexual anatomy/long-term physiology/RAPS-SA information and genuinely materialized current sexual state. Non-owner direct access fails closed.

## Read-Only Grading / Telegram Grading Presentation

Canonical: `docs/READ_ONLY_GRADING_PROOF.md`.

Shared vocabulary:
- E — Beginner
- D — Novice
- C — Capable
- B — Skilled
- A — Advanced
- S — Expert
- SS — Elite
- SSS — Master
- X — Mythic
- XX — Transcendent

The accepted `raps-100-proof-v1` scheme preserves its 0..100 E..S thresholds; higher tiers remain available for future schemes with appropriate scale semantics. Telegram rows use `Strength 90 (S) · Expert`. Compatible group/overall values are arithmetic means evaluated at read time; IQ is excluded because its scale differs. Grades are never persisted state.

## Universal Profile Grading Framework v1 — NEXT

Canonical planning contract: `docs/UNIVERSAL_PROFILE_GRADING_FRAMEWORK_V1.md`.

**This grading closure now precedes Skill Progression.**

Goal: extend grading from the current Attribute-only implementation into a reusable profile-wide interpretation layer without making grades authoritative state.

Planned principles:
- explicit named grading schemes rather than one universal formula;
- a numeric field is not automatically gradeable;
- Attributes preserve the proven RAPS 0..100 scheme;
- Skills receive monotonic proficiency grading from authoritative skill scores once score/tier/experience ownership is reconciled;
- Body uses proportional/contextual grading rather than `larger = better`;
- physique grading may use evidence-backed derived ratios/balance/composition and composite evaluation;
- health, general aesthetics, bodybuilding and modelling may later be separate named schemes over the same authoritative body state;
- popularized golden-ratio claims must not be hard-coded as universal truth without evidence;
- Telegram consumes generic derived grade metadata;
- future career/quest/job/salary systems may consume grade results without owning or persisting them.

Before closure, profile areas should be classified `graded`, `derived-grade candidate`, `contextual-only`, or `not gradeable` so recovery/personality/preferences/intimate frequency/anatomy fields do not receive meaningless grades merely because they are numeric.

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
- stress is **not** a prerequisite or mandatory trigger;
- no single hormone/media/cue/relationship variable is a mandatory trigger;
- no testosterone surrogate inferred from training/body composition;
- future sexual-media/cue exposure may modulate transient arousal only when real content/event evidence exists;
- future endocrine effects require an explicit endocrine authority rather than invented testosterone values;
- current v1 does not apply action-specific stress reduction, mood/fatigue/sleep bonus or endocrine cascade;
- later stress/mood feedback must be contextual and conditional, not a reason to manufacture stress;
- no partnered sexual behavior or Relationship System dependency in v1;
- no structural anatomy or long-term erectile-capacity mutation from ordinary sexual activity.

Cognition receives current drive, release recency, trailing-seven-day evidence, current private/aloneness status and reachable safe private rooms. Prompting explicitly permits the behavior as discretionary when authoritative `action_options` expose it and permits ordinary movement toward a reachable private room when context supports that choice. Stronger safety/physiology needs remain higher priority.

At validated action start, deterministic runtime may materialize current arousal/erectile physiology; completion moves it through bounded subsiding state and updates `raps_sa.self_satisfaction_weekly` from completed action evidence. Later ordinary action boundaries refresh drive and return temporary physiology toward baseline.

Actors without represented adult sexual-profile data remain composable; this domain is a no-op for them rather than inventing missing sexual facts.

Observer privacy:
- action sensitivity is `intimate`;
- owner can inspect appropriate owner-only profile/current/history/pending surfaces and receive eligible notifications;
- allowed non-owner history/recent-location views omit the action;
- non-owner current/pending state is redacted to `Private Activity`;
- public validation must not print intimate production values.

PR #97 evidence:
- final candidate head `6904171d59b5b022f902ce837916a4654d597845`;
- candidate CI #756 / `31860327090` SUCCESS;
- Solo Regulation Acceptance #8 / `31860327100` SUCCESS;
- Sexual Anatomy Physiology Lifecycle Acceptance #16 / `31860327174` SUCCESS;
- Public Readiness Security Audit #47 / `31860327029` SUCCESS;
- Strength Live Cycle Validation run `31860327058` retry SUCCESS;
- merge `60e1e3949631e1284e41ae0940a03fb02421fef8`;
- Deploy #193 / `31860951081` SUCCESS;
- main CI #757 / `31860951093` SUCCESS.

A legacy Research Action Semantics acceptance surfaced an obsolete exact-singleton target assumption on the post-merge main matrix. The reusable invariant is that the Research Desk remains valid and the Bookshelf remains invalid; the world is allowed to gain additional research-capable targets. The checkpoint sync generalizes that validator rather than constraining future composition.

## Public Repository Security — COMPLETE / PUBLIC

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md`, `SECURITY.md`.

Public hardening is complete. Manual UI verification remains opportunistic where the GitHub App cannot fully read settings: outside-contributor workflow approval, Secret scanning/Push protection, and `main` branch/ruleset protection.

## Next development sequence

1. **Universal Profile Grading Framework v1**;
2. **Profile Grading Coverage Closure**;
3. **Skill Progression Foundation v1**;
4. Skill Progression follow-on batches/retention as justified;
5. intellectual attributes;
6. mental/emotion dynamics, including later contextual Solo Regulation stress/mood feedback when a real state authority exists;
7. broader relationship/social systems and partnered/contextual sexual behavior;
8. broad Mind/Behavior architecture only after enough real feature signals justify it.

Post-public GitHub settings verification remains opportunistic and non-blocking.

## Skill Progression Family — AFTER GRADING CLOSURE

Do not treat Skills as merely renamed RAPS physical attributes.

Before implementation, reconcile:
- `character_skills` schema/current data and Telegram Skills view;
- action/training/research evidence that can legitimately improve a skill;
- current skill scores/tier/experience semantics;
- grading boundaries versus actual progression state;
- decay/retention semantics where appropriate;
- generic actor/skill IDs rather than Darian-specific logic.

Minimum-runnable policy still applies: prove one genuinely new skill progression invariant with a bounded exemplar, then batch structurally equivalent skills by pattern once the invariant is green.

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

**Physical Profile Completion, Telegram Profile Schema-Driven UX, and Solo Sexual Regulation v1 are complete/deployed. The next canonical development slice is Universal Profile Grading Framework v1, followed by Profile Grading Coverage Closure; Skill Progression starts only after that grading foundation is complete.**

Start by designing/implementing the explicit grading-scheme registry and preserving existing Attribute behavior, then add Skills grading presentation and evidence-backed Body/Physique grading without mutating underlying progression state.
