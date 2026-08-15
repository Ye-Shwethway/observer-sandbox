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

Latest runtime deployment: **Deploy #227 / run `31895171211` SUCCESS**, Solo Sexual Regulation Naturalism v2, PR #163 merge `13c57933b8136c014f6940b2647c2acdbc3b8eac`.

Final tested PR head: `b9d7ee05f52555417afb9fc1272e0d921657be6b`.

Validation:
- final **CI #929 / run `31895111772` SUCCESS** with **538 passed**;
- fresh DB init/status succeeded; schema remains v5;
- Solo Regulation Naturalism v2 Acceptance #23, Thorne Estate Training Environment v1 Acceptance #9, Research Action Semantics Acceptance #29, Strength Live Cycle Validation v1 #82, and Public Readiness Security Audit #113 all succeeded;
- an earlier final-CI attempt exposed only stale world-revision assertions plus one incorrect older-age fixture after 535 passing tests; those assertions were corrected narrowly, without changing the runtime model;
- no deliberate duplicate full-suite run was performed after merge.

Verified production readback after Deploy #227:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- runtime speed **5x** at readback;
- world revision `thorne-estate-v3.4-private-activity-semantics` active;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time `2025-05-07T10:54:00+00:00`;
- Darian was in the Top-Class Home Gym, current action `idle`, energy 81.586, fatigue 24.277, sleepiness 23.9;
- no production self-satisfaction action was forced or accelerated for proof.

## Solo Sexual Regulation Naturalism v2 — COMPLETE

This bounded correction fixes the over-conservative v1 pacing model while preserving cognition discretion and avoiding any daily/weekly quota.

Current drive authority combines:
- authored libido as the primary stable input;
- bounded adult life-stage contribution;
- positive recovery contribution for good energy / low fatigue / low sleepiness;
- represented resident-scope solitude contribution;
- libido-shaped release-recency recovery;
- trailing-24-hour saturation penalty after completed releases;
- adverse-state penalties only when recovery state is meaningfully poor.

The anti-loop behavioral cooldown is now 2 simulated hours. It is a pacing guard, not a clinical refractory-period claim. For Darian's authored young/high-libido/healthy/solitary state, same-day repeat can become legal when current state supports it; cognition still chooses whether to act.

Privacy suitability is now separate from generic `world.access`. `world.metadata.private_activity` can mark appropriate personal/secluded spaces. Darian's Master Suite/Bathroom remain valid, while Library, Training Hall, Home Gym and other authored secluded estate spaces can also qualify when authorized and alone. Quasi's Room and Guest Rooms are explicitly excluded despite generic `access=private`.

Reachable safe private locations are discovered through the normal location graph with breadth-first search rather than only direct neighbors. Normal movement remains required.

See `docs/SOLO_SEXUAL_REGULATION_NATURALISM_V2.md`.

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

**REVIEW/IMPLEMENT NEXT.** Leave Skills closed. Solo Sexual Regulation Naturalism v2 is now a corrected baseline for the Sexual section review.

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

**Vertical-completeness mode is authoritative. Solo Sexual Regulation Naturalism v2 is complete through PR #163 final tested head `b9d7ee05f52555417afb9fc1272e0d921657be6b`, merge `13c57933b8136c014f6940b2647c2acdbc3b8eac`, CI #929 with 538 passed, and Deploy #227 / run `31895171211` SUCCESS. Production is healthy at schema v5 and world revision `thorne-estate-v3.4-private-activity-semantics`; at readback Darian was in the Home Gym at `2025-05-07T10:54:00+00:00`, speed 5x, with no fabricated private action. Skills remains CLOSED v1. Resume with the Remaining Profile Minimum Unlock Sweep, treating Naturalism v2 as the Sexual-section baseline.**
