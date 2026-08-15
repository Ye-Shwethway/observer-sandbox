# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never manipulate production merely to manufacture evidence.
- Verification is focused-first. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes do not need the Python suite; do not deliberately repeat the full suite after merge.

## Strategic development mode — workflow completeness before depth

The Creator's vertical-completeness pass has reached its first major checkpoint:

`minimum unlock all Character Profile sections -> overall workflow/foundation review -> deepen highest-value systems later`

All Character Profile sections now meet the minimum-unlock standard from `docs/MINIMUM_PROFILE_UNLOCK_POLICY_V1.md`.

Do not reopen a section merely to add depth unless the upcoming foundation review finds a blocking cross-system requirement.

## Current verified deployment

Latest runtime deployment: **Deploy #228 / run `31896440459` SUCCESS**, Profile Minimum Unlock Sweep v1, PR #165 merge `736112054e3814f0f340ea5e919eb1729ea5837a`.

Final tested PR head: `2ebcfab51465ab4193e0bdcd0fee805ff196a442`.

Validation:
- **CI #930 / run `31896373252` SUCCESS**;
- **540 passed in 41.05s**;
- fresh DB init/status succeeded; schema remains v5;
- Cognition Capability Awareness, Research Action Semantics, Training Movement Contract Normalization, Eating Behavior, and Solo Regulation Naturalism acceptances all succeeded;
- no stale-contract fix cycle was needed and no deliberate duplicate full-suite run was performed.

Verified production readback after Deploy #228:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- runtime speed **3x** at readback;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy;
- world revision remains `thorne-estate-v3.4-private-activity-semantics`;
- live sim time `2025-05-07T12:49:00+00:00`;
- Darian was naturally resting in the Training Hall: energy 79.252, fatigue 20.402, hunger 29.743, cleanliness 82.46, sleepiness 29.65, thirst 37.935;
- no production action/state was fabricated for validation.

Deployment proves the new cognition context is installed. The regression proves Identity/Appearance/Background context reaches cognition input; do not claim a live decision specifically relied on one of those fields without separate evidence.

## Character Profile — MINIMUM-UNLOCKED v1

See `docs/PROFILE_MINIMUM_UNLOCK_SWEEP_V1.md`.

Current classification:
- **Identity** — minimum-unlocked; canonical identity is persisted/presented, DOB already participates in legitimate age-dependent runtime logic, and compact identity context reaches cognition.
- **Appearance** — minimum-unlocked; canonical appearance is persisted/presented and compact stable self/appearance context reaches cognition without granting mutation authority.
- **Body** — minimum-unlocked through authoritative measurements/composition, body/training effects, progression/readback, and profile presentation.
- **Attributes** — minimum-unlocked through authoritative scores, declared task/performance modifiers, progression where represented, and cognition/profile visibility.
- **Recovery** — minimum-unlocked; energy/fatigue/sleepiness and recovery state directly shape cognition, action availability, and training readiness.
- **Sexual** — minimum-unlocked; anatomy/physiology profile state plus Solo Sexual Regulation Naturalism v2 and deterministic private-action physiology are active.
- **Personality** — minimum-unlocked; traits, motivation, and complexity notes reach autonomous cognition.
- **Preferences** — minimum-unlocked; persisted preferences, hobbies, and habits reach autonomous cognition.
- **Background** — minimum-unlocked; canonical origins/history now reaches cognition as bounded stable context.
- **Skills** — minimum-unlocked / CLOSED v1; learned scores, represented applications, and legitimate progression paths are established.

The canonical-context closure is read-only. It does not create an Appearance Engine, biography engine, arbitrary profile mutation, cosmetic progression, relationship mechanics, or universal personality reward model.

## Skills — CLOSED v1

Frozen learned Skill surface:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` remains a derived/non-executable parent over Bladed Weapons + Firearms. Hidden legacy `weapons` is compatibility only. Do not deepen Skills during the foundation review unless a cross-system blocker requires it.

See `docs/SKILLS_CLOSURE_V1.md`.

## Solo Sexual Regulation Naturalism v2 — COMPLETE

The corrected baseline remains active:
- authored libido is primary;
- bounded young-adult/recovery/solitude contributions can be positive;
- release-recency recovery is libido-shaped;
- trailing-24h saturation resists loops without imposing a quota;
- anti-loop cooldown is 2 simulated hours;
- privacy suitability is authored separately from generic room access;
- reachable safe private locations use the normal location graph.

Cognition retains discretion; no daily/weekly quota exists.

See `docs/SOLO_SEXUAL_REGULATION_NATURALISM_V2.md`.

## Active next phase — Overall Workflow/Foundation Review

**REVIEW NEXT BEFORE IMPLEMENTING MORE DOMAIN DEPTH.**

Audit the current end-to-end simulation workflow and identify the highest-leverage missing or weak cross-cutting foundation. Review repository/source and verified production evidence rather than assuming every candidate needs implementation.

Candidate foundation areas:
- profile -> cognition influence and context generality;
- autonomy planning / goal continuity across decisions;
- generic action/task lifecycle and represented outcomes;
- environment/world context and purposeful movement;
- resources/inventory/consequences;
- knowledge/familiarity;
- inter-character participation contracts;
- event/lifecycle handling;
- long-horizon progression/decay.

For each candidate classify it as:
1. already sufficient for the current runnable workflow;
2. closure-only/documentation debt;
3. real missing foundation;
4. intentionally deferred domain depth.

Then select the **smallest highest-leverage runnable slice**. Prefer strengthening a reusable existing contract over creating a new engine.

## Deferred boundaries

No relationship-system expansion, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, arbitrary LLM profile mutation, or synthetic production actors/actions solely for proof.

## CI cadence

- focused task-relevant tests/gates while iterating;
- one final full CI checkpoint for code/runtime PRs by default;
- no deliberate second full-suite run merely because an already-tested PR merged;
- docs-only PRs skip the full Python suite;
- manual broad reruns only when structural risk genuinely warrants one.

## Exact resume point

**Profile Minimum Unlock Sweep v1 is complete through PR #165 final tested head `2ebcfab51465ab4193e0bdcd0fee805ff196a442`, merge `736112054e3814f0f340ea5e919eb1729ea5837a`, CI #930 with 540 passed, and Deploy #228 / run `31896440459` SUCCESS. Every Character Profile section is now minimum-unlocked; Skills remains CLOSED v1. Production is healthy at schema v5. At readback Darian was naturally resting in the Training Hall at `2025-05-07T12:49:00+00:00`, speed 3x. Resume with an Overall Workflow/Foundation Review, then choose one smallest highest-leverage cross-cutting slice before deepening any profile domain.**
