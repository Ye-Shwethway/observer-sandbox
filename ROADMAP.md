# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Current Creator instruction, current canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never manipulate production merely to manufacture evidence.
- Development verification is focused-first: use task-relevant tests/gates while iterating and reserve the full suite for the final code/runtime PR checkpoint unless broader risk justifies another run. Docs-only changes do not need the full Python suite.

## Strategic development mode — vertical completeness first

The Creator has explicitly prioritized **overall workflow completeness before subsystem depth**.

Canonical sequence:

`minimum unlock all Character Profile sections -> verify overall system workflow -> deepen highest-value systems later`

Follow `docs/MINIMUM_PROFILE_UNLOCK_POLICY_V1.md`.

Minimum unlock means real, not cosmetic: authoritative state + at least one meaningful runtime influence + persistence/presentation where relevant. It does not require exhaustive mechanics, deep taxonomies, multiple bespoke applications, or a dedicated subsystem for every field.

Batch structurally equivalent work. Do not return to one-field/one-PR or one-Skill-application/one-PR cadence unless a genuinely new invariant requires an exemplar.

## Current verified deployment

Latest runtime deployment: **Deploy #226 / run `31893586685` SUCCESS**, Skills Closure Batch v1, PR #161 merge `7cbc92a38ee8b3f5d8220c6e33ff0c4d00f157b4`.

Final tested PR head: `f502e7e0e0f438b2dfac9ffab01c547ef1b255b9`.

Validation:
- final **CI #923 / run `31893520852` SUCCESS**;
- fresh DB init/status succeeded; schema remains v5;
- Skill Progression Foundation, Skill Evidence Semantics, Skill Definition Format/Refactor, Tactical Planning progression, Strength Live Cycle, and Public Readiness Security gates all succeeded;
- the first full CI attempt had four stale progression-revision/set assertions after 531 passing tests; only those contract assertions were corrected;
- no manual repeated full-suite rerun was requested.

Verified production readback after Deploy #226:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- runtime speed **10x** at readback;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time `2025-05-07T06:24:00+00:00`;
- Darian was naturally training in the Top-Class Home Gym;
- Field Medicine remained 75/A, Bladed Weapons 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills 85.167/A;
- no production Field Medicine practice or casualty was fabricated for proof.

The live morning training state also confirms that the earlier Circadian Sleep Rhythm Stabilization has advanced beyond the previously pending early-evening sleep lock.

## Skills section — CLOSED v1 / minimum-unlocked

The Skills section is now **minimum-unlocked and closed for the vertical-completeness pass**. Do not deepen it further until the overall profile/workflow sweep is complete unless a blocking cross-system requirement is discovered.

Frozen learned Skill surface:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` is a derived/non-executable parent over Bladed Weapons + Firearms. Hidden legacy `weapons` remains only a compatibility projection. Neither receives direct progression XP.

Skill-like profile/Attribute compatibility fields such as combat skill, weapons proficiency, survival skill, powerlifting capacity, focus/precision, practical skills, technological aptitude, and medical knowledge are not independent Skills in this pass.

Minimum coverage:
- **Hand-to-Hand Combat** — represented applications + legitimate progression active; second-character sparring remains conditional on a distinct consenting colocated actor.
- **Bladed Weapons** — simulation-safe represented application + explicit practice progression complete.
- **Firearms** — simulation-safe represented application + explicit practice progression complete.
- **Survival** — represented navigation/sustainment + explicit progression complete.
- **Tactical Planning** — represented assessment/planning + progression complete.
- **Technology** — represented diagnostic + explicit progression complete.
- **Field Medicine** — casualty-context assessment/stabilization plus abstract simulation-safe `field_medicine_scenario_practice` progression complete.

Field Medicine scenario practice does not create casualty state or imply diagnosis/treatment mechanics. Real assessment/stabilization remain casualty-context-bound and application evidence remains separate from learning evidence.

See `docs/SKILLS_CLOSURE_V1.md`.

### Skills metadata debt

The active Field Medicine learning authority is the explicit Skill Progression + Skill Practice registries. The older universal Skill Definition `learning_evidence` description was not comprehensively refactored in the closure batch. It must not be interpreted as implicit application-to-XP authority. This is deferred metadata normalization, not a runtime blocker.

## Active next phase — Remaining Profile Minimum Unlock Sweep

**REVIEW/IMPLEMENT NEXT.** Leave Skills closed.

Target Character Profile sections:
- identity
- appearance
- body
- attributes
- recovery
- sexual
- personality
- preferences
- background

First inspect the current schema/profile/cognition/runtime influence for all nine sections and classify each as:
- already minimum-unlocked;
- closure-only gap;
- missing meaningful runtime influence.

Then batch by structural similarity rather than one section per PR.

Expected speed-first grouping, subject to fresh repo inspection:
1. **Mature closure group:** Body + Attributes + Recovery + Sexual — substantial foundations already exist; prefer audit/closure over rewrites.
2. **Canonical/context group:** Identity + Appearance + Personality + Preferences + Background — add only the smallest meaningful cognition/action influence necessary where one is missing.

Do not invent separate engines merely to make every field dynamic. Canonical/static fields may remain stable when their legitimate simulation role is contextual influence rather than mutation.

## After the profile sweep

Once every Character Profile section is minimum-unlocked, perform an overall workflow/foundation review before local deepening.

Likely cross-cutting foundation areas include:
- profile -> cognition influence;
- generic action/task lifecycle;
- resources/inventory/consequences;
- environment/world context;
- knowledge/familiarity;
- inter-character participation;
- event/lifecycle handling;
- long-horizon progression/decay;
- autonomy planning and goal continuity.

Ordering must be selected from repository/live evidence at that future checkpoint rather than prebuilding all of them now.

## CI cadence

- focused task-relevant tests/gates during implementation;
- one final full CI checkpoint for code/runtime PRs by default;
- no deliberate second full-suite run merely because an already-tested PR merged to `main`;
- docs-only pull requests skip the full Python suite;
- manual full reruns only when broader risk actually warrants one.

Some specialized acceptance workflows may still run automatically on matching pushes; do not mistake those for manually requested full-suite loops.

## Deferred boundaries

No relationship system expansion, casualty handoff consumer, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, full Knowledge Engine, H2H hierarchy rewrite, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, or synthetic production actors/actions solely for proof.

## Exact resume point

**Vertical-completeness mode is authoritative. Skills Closure Batch v1 is complete through PR #161 final tested head `f502e7e0e0f438b2dfac9ffab01c547ef1b255b9`, merge `7cbc92a38ee8b3f5d8220c6e33ff0c4d00f157b4`, CI #923, and Deploy #226 / run `31893586685` SUCCESS. Skills is CLOSED v1 / minimum-unlocked. Production is healthy at schema v5; at readback Darian was naturally training in the Home Gym at `2025-05-07T06:24:00+00:00`, speed 10x, with Field Medicine still 75/A and no fabricated practice/casualty. Review the nine remaining profile sections as one minimum-unlock sweep, batch gaps by pattern, and do not deepen Skills yet.**
