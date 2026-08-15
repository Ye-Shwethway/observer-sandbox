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

Use production-copy validation for concrete stateful/migration risk. Never accelerate/mutate production merely to manufacture acceptance evidence. New architecture/control/security invariants update their canonical contract + ROADMAP + bootstrap in the same cycle.

## Current verified deployment checkpoint

Latest runtime deployment: **Deploy #192 / run `31856295920` SUCCESS** for Telegram Profile Schema-Driven UX + Grading Display, PR #95 merge `78037276a8ebceb96dc1784f60e1f3bf6a2fe1c5`.

Post-merge main **CI #746 / run `31856295912` SUCCESS**.

The immediately preceding physical/profile checkpoint is Physical Presentation Closure v1, PR #94 merge `acfbd0b4a25b3ea1c4a587c9be9a2f4898bcc92b`, Deploy #191 SUCCESS.

Latest safe production verification for this UI slice intentionally does **not** print intimate profile values into public GitHub Actions logs. Deploy health and CI are green; intimate values were validated on disposable/local test databases and are inspectable by the configured Telegram owner.

## Universal invariants

Darian/Thorne Estate are production exemplars, never reusable-engine identity.

Inventory/eating:
`Universal definition -> concrete stack -> reachable action context -> structured quantity -> deterministic validation -> state transition + immutable evidence`

Cognition:
`deterministic state/context -> one model proposal -> authoritative validation -> deterministic mutation`

Body composition:
`complete bounded energy/nutrition evidence + current FM/FFM + resistance evidence + recovery + genetic envelope -> deterministic settlement -> coupled Weight/BF history + audit`

Body measurements:
`BC-2 settlement + regional resistance evidence + authored anatomy/genetic envelope + regional inactivity context -> bounded regional circumference settlement -> atomic profile history + event`

Training:
`concrete target -> reusable method -> optional selected reusable movement patterns -> effective load -> deterministic method/anatomy evidence -> domain progression engines`

Profile presentation:
`profile schema + section metadata + current represented values + caller role/sensitivity -> generic profile query -> read-only derived grading/presentation -> Telegram`

## Physical/profile family — COMPLETE FOR CURRENT SCOPE

Completed and deployed:
- BC-2 Body Composition — PR #78 / Deploy #182;
- BC-3 Body Measurement — PR #82 / Deploy #183;
- Training Method Semantics v2 — PR #84 / Deploy #184;
- Training Anatomy / Movement Semantics v1 — PR #86 / Deploy #185;
- Regional Measurement Detraining v1 — PR #88 / Deploy #186;
- Height Lifecycle v1 — deployed before the current checkpoint;
- Sexual Anatomy & Physiology Lifecycle v1 — deployed before the current checkpoint;
- Male Erectile Physiology Canonical Contract — PR #92 / Deploy #189;
- Physical Profile Coverage Audit v1 — PR #93;
- Physical Presentation Closure v1 — PR #94 / Deploy #191;
- Telegram Profile Schema-Driven UX + Grading Display — PR #95 / Deploy #192.

Canonical physical/profile docs include:
- `docs/BODY_COMPOSITION_PROGRESSION_V1.md`
- `docs/BODY_MEASUREMENT_PROGRESSION_V1.md`
- `docs/TRAINING_METHOD_SEMANTICS_V2.md`
- `docs/TRAINING_ANATOMY_V1.md`
- `docs/REGIONAL_MEASUREMENT_DETRAINING_V1.md`
- `docs/PHYSICAL_PROFILE_COVERAGE_AUDIT_V1.md`
- `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`
- `docs/READ_ONLY_GRADING_PROOF.md`

### Body/height/sexual authority summary

- Weight/BF/FM/FFM are owned by BC-2; do **not** add a competing Weight decay authority.
- Eleven circumferences are owned by BC-3 with movement-aware regional evidence and regional detraining.
- Structural height is owned by Height Lifecycle; adult stability is a valid normal outcome.
- Structural male sexual anatomy is lifecycle-driven and distinct from momentary sexual state.
- Represented male canonical profiles require structural anatomy/genetic targets plus long-term `baseline_erectile_function` and `erection_firmness_cap`.
- Momentary arousal/erectile state/firmness remain context-driven runtime state rather than invented static defaults.
- Darian-specific values remain exemplar profile data, never universal engine constants.

### Physical presentation closure

- authored abdominal structure is distinct from current visible abdominal definition;
- visible definition follows current composition relative to authored sustainable BF floor;
- stable appearance anchors such as PARS remain truthful canonical anchors unless/until a real dynamic appearance engine exists;
- broader health vitals and sexual-context transitions remain explicit future domains rather than fake static simulation.

## Telegram Profile Schema-Driven UX — COMPLETE / DEPLOYED

Canonical: `docs/TELEGRAM_PROFILE_SCHEMA_DRIVEN_UX.md`.

Section metadata is now externalized in `config/profile_sections.v1.json`:
`domain/collection -> section id + label + icon + order + visibility + renderer kind + sensitivity`

Ordinary new sections can be added through metadata/config without a Telegram handler branch. Special renderers only own formatting, not section existence.

### Sexual Anatomy & Physiology observer section

Telegram owner now receives an owner-only **Sexual Anatomy & Physiology** profile section combining represented sexual-anatomy/RAPS-SA values and any genuinely materialized runtime sexual state.

Security is query-layer enforced:
- allowed non-owner users do not receive the section in the menu;
- direct non-owner callback attempts fail closed;
- private/intimate fields are not exposed merely because they exist;
- no fake current erection/arousal state is invented for display.

### Grading presentation

Shared vocabulary is retained:
`E Beginner -> D Novice -> C Capable -> B Skilled -> A Advanced -> S Expert -> SS Elite -> SSS Master -> X Mythic -> XX Transcendent`.

The existing `raps-100-proof-v1` scheme preserves its proven E..S thresholds; higher tiers are not artificially compressed into the 0..100 RAPS scale.

Telegram individual display is now:
`Strength 90 (S) · Expert`

Attributes also derive read-time group and overall grades from the arithmetic mean of current compatible values, then evaluate through the same named scheme. IQ remains excluded because its scale semantics differ.

Grades/group averages are **not persisted state**; they recompute on every read when underlying values change.

For the canonical Darian test fixture at PR #95:
- Strength 90 -> S · Expert;
- Physical mean 86.538 -> A · Advanced;
- overall compatible Attributes mean 86.583 -> A · Advanced.

These are evidence from the tested fixture, not immutable character labels.

PR #95 final tested head: `2683f7f9ced8ee43c14088912b85f709cc2747d5`.
Validation:
- CI #745 / `31856247078` SUCCESS;
- Read-Only Grading Proof #17 / `31856247076` SUCCESS on disposable production copy;
- Attribute Grading Batch 1 #16 / `31856247111` SUCCESS on disposable production copy;
- Public Readiness Security Audit #38 / `31856247097` SUCCESS;
- Inventory Operations v1 Acceptance #30 / `31856247203` SUCCESS;
- merge `78037276a8ebceb96dc1784f60e1f3bf6a2fe1c5`;
- Deploy #192 / `31856295920` SUCCESS;
- main CI #746 / `31856295912` SUCCESS.

Legacy grading acceptances were also made state-aware: they stage the profile-section config and grade the current production-copy raw value rather than assuming Strength remains exactly 90 forever.

## Public repository security checkpoint

`Ye-Shwethway/observer-sandbox` is PUBLIC. Public hardening remains in force. Intimate production values must not be dumped into public CI logs merely for acceptance evidence.

Manual GitHub UI verification remains opportunistic for outside-contributor workflow approval, Secret scanning/Push protection, and `main` branch/ruleset protection where the GitHub App cannot fully read account-level settings.

## Later sequence

1. **Skill Progression Family**;
2. intellectual attributes;
3. mental/emotion dynamics;
4. later broader relationship/social systems, including contextual sexual-state behavior where justified;
5. broad Mind/Behavior architecture only after enough real feature families justify it.

## Exact resume point

First re-read current live production and canonical repository.

The physical/profile completion gate and required Telegram schema-driven profile debt are closed for current scope. **The next canonical development family is Skill Progression.**

Before implementing it, inspect existing `character_skills`, current skill/Profile UX, training/action evidence contracts, and the universal grading/progression boundaries. Preserve the exemplar-first-then-batch policy and do not make Skills a renamed copy of physical-attribute progression without proving skill-specific evidence and lifecycle semantics.

Do not add economy/currency, automatic restocking, deep recipes/crafting, Character Memory, broad Mind/Behavior engines, or a second production character merely for testing as side effects.
