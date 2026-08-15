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

Latest runtime deployment: **Deploy #192 / run `31856295920` SUCCESS**, Telegram Profile Schema-Driven UX + Grading Display, PR #95 merge `78037276a8ebceb96dc1784f60e1f3bf6a2fe1c5`.

Post-merge main **CI #746 / run `31856295912` SUCCESS**.

The immediately preceding physical/profile runtime checkpoint is Physical Presentation Closure v1, PR #94 merge `acfbd0b4a25b3ea1c4a587c9be9a2f4898bcc92b`, Deploy #191 SUCCESS.

Sensitive production profile values are intentionally not dumped into public GitHub Actions evidence. Runtime deployment health is green; intimate-value correctness/visibility is covered by local/disposable validation and the owner-only Telegram query contract.

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
- Telegram Profile Schema-Driven UX + dynamic grading presentation.

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

The earlier gate is closed. Physical/profile mechanics were intentionally completed before crossing into Skill Progression because body composition, structural growth, circumferences, sexual physiology and skills require materially different evidence/lifecycle rules.

Authority map:
- Weight/BF/FM/FFM — BC-2;
- circumferences — BC-3 + Training Anatomy + Regional Detraining;
- structural Height — Height Lifecycle;
- male structural sexual anatomy — Sexual Anatomy Lifecycle;
- long-term erectile baseline — Sexual Physiology Lifecycle/canonical male profile contract;
- current sexual state — context-driven runtime state, intentionally not invented without evidence;
- composition-linked visible abdominal definition — derived presentation;
- stable appearance anchors remain canonical until a real dynamic owner exists;
- broader health vitals/injury/illness are explicit future domains, not fake static simulation.

Male canonical profiles require structural sexual anatomy/genetic targets plus long-term `baseline_erectile_function` and `erection_firmness_cap`. These are per-character inputs; Darian is only the first rich exemplar.

Relevant completed slices:
- Male Erectile Physiology Canonical Contract — PR #92 / Deploy #189;
- Physical Profile Coverage Audit — PR #93;
- Physical Presentation Closure — PR #94 / Deploy #191.

Canonical: `docs/PHYSICAL_PROFILE_COVERAGE_AUDIT_V1.md`.

## Telegram Profile Schema-Driven UX — COMPLETE / DEPLOYED

Canonical: `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`.

PR #95 / Deploy #192 replaced the fixed profile section registry with `config/profile_sections.v1.json` metadata:

`domain/collection -> section id + label + icon + order + visibility + renderer kind + sensitivity`

Acceptance proves a new ordinary section can be added through config metadata without a Telegram handler branch. Special renderers format genuinely different shapes but do not own section existence.

### Sexual Anatomy & Physiology section

An owner-only Telegram profile section now exposes represented sexual-anatomy/long-term physiology/RAPS-SA information and any genuinely materialized current sexual state.

Security is enforced below the button layer:
- owner-only section visibility;
- allowed non-owner menu omission;
- direct non-owner callback fails closed;
- private/intimate sensitivity is authoritative;
- no momentary erection/arousal values are invented merely to fill a UI.

Do not expose intimate production values in public CI logs merely for evidence.

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

The accepted `raps-100-proof-v1` scheme preserves its existing 0..100 thresholds and legitimately reaches E through S only. Higher tiers remain available for future named schemes with appropriate scale semantics; they are not squeezed into 0..100.

Telegram row format:
`Strength 90 (S) · Expert`

Attributes also display read-time group and overall grades. Compatible values are averaged arithmetically and the mean is evaluated through the same named scheme. IQ remains visible but excluded from this aggregate because its scale differs.

No individual/group/overall grade is persisted; values are recomputed on every read.

PR #95 tested fixture evidence:
- Strength 90 -> S · Expert;
- Physical mean 86.538 -> A · Advanced;
- compatible Attributes overall mean 86.583 -> A · Advanced.

These are tested read-time values, not immutable labels.

Final PR #95 evidence:
- tested head `2683f7f9ced8ee43c14088912b85f709cc2747d5`;
- CI #745 / `31856247078` SUCCESS;
- Read-Only Grading Proof #17 / `31856247076` SUCCESS;
- Attribute Grading Batch 1 #16 / `31856247111` SUCCESS;
- Public Readiness Security Audit #38 / `31856247097` SUCCESS;
- Inventory Operations Acceptance #30 / `31856247203` SUCCESS;
- merge `78037276a8ebceb96dc1784f60e1f3bf6a2fe1c5`;
- Deploy #192 / `31856295920` SUCCESS;
- main CI #746 / `31856295912` SUCCESS.

Grading production-copy acceptances are now state-aware instead of assuming Strength remains fixed at 90 after progression.

## Public Repository Security — COMPLETE / PUBLIC

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md`, `SECURITY.md`.

Public hardening is complete. Manual UI verification remains opportunistic where the GitHub App cannot fully read settings: outside-contributor workflow approval, Secret scanning/Push protection, and `main` branch/ruleset protection.

## Next development sequence

1. **Skill Progression Family**;
2. intellectual attributes;
3. mental/emotion dynamics;
4. broader relationship/social systems, including context-driven sexual physiology where justified;
5. broad Mind/Behavior architecture only after enough real feature signals justify it.

Post-public GitHub settings verification remains opportunistic and non-blocking.

## Skill Progression Family — NEXT

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
- estate exterior/Tahoe traversal.

## Exact resume point

Re-read live production and current canonical repository first.

**Physical Profile Completion and Telegram Profile Schema-Driven UX are complete/deployed. The next canonical development family is Skill Progression.**

Start by establishing skill-specific evidence/progression semantics from existing schema and action evidence rather than copying body/attribute progression formulas by convenience.
