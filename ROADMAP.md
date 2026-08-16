# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-16

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Prefer **vertical completeness before local depth**.
- Never manipulate production merely to manufacture evidence.
- Verification is focused-first. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes do not need the Python suite.

## Character Profile checkpoint

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1.

Adaptive Character Disposition Foundation is COMPLETE v1:
`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> Slow Personality Plasticity`.

Do not reopen local psychology merely for depth.

## Skills — CLOSED v1

Frozen learned Skill surface:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` is derived/non-executable; hidden legacy `weapons` is compatibility only.

## Overall Workflow/Foundation Review — COMPLETE / CLOSED v1

See `docs/OVERALL_WORKFLOW_FOUNDATION_REVIEW_V1.md`.

The bounded final closure pass found **no additional blocking foundation gap**. Do not continue open-ended gap hunting by default.

Four evidence-selected structural gaps were closed during the review:
1. **Autonomy Intent Continuity v1** — PR #178 / Deploy #236.
2. **Active Modifier Runtime Foundation v1** — PR #180 / Deploy #237.
3. **Action Condition Runtime Foundation v1** — PR #182 / Deploy #238.
4. **Participant-Aware Recent Event Context v1** — PR #184 / Deploy #239.

Current minimum foundation classifications:
- generic action/task lifecycle: CLOSED v1;
- resources/inventory/state consequences: CLOSED v1;
- environment/world context: CLOSED v1 minimum;
- knowledge/object familiarity: CLOSED v1 minimum;
- inter-character participation: CLOSED v1 socket;
- event/lifecycle handling: CLOSED v1;
- participant-aware recent event cognition: CLOSED v1 minimum;
- longer-horizon progression/decay: CLOSED v1 exemplars;
- profile -> cognition/runtime integration: CLOSED v1;
- autonomy purpose continuity: CLOSED v1 minimum;
- persistent temporary modifier lifecycle: CLOSED v1 minimum;
- action-definition prerequisite runtime: CLOSED v1 minimum.

Routine/schedule reinspection found meaningful authored time-window + simulation-time + physiological-priority influence already present. A full sequence ledger remains later depth.

## Active phase — Creator Feature Planning

The project has moved from foundation-gap review to explicit product feature planning and minimum-runnable feature slices.

For each desired feature:
1. define the user-visible capability and why it matters;
2. identify dependencies on current runtime contracts;
3. separate minimum-runnable behavior from later depth;
4. rank against other requested features by value, dependency, implementation cost and runtime risk;
5. use one bounded exemplar only for a genuinely new invariant, then batch equivalent follow-ons.

A deferred capability is not a foundation defect. Reopen the foundation review only if a concrete feature exposes a cross-system invariant that cannot currently be represented or executed safely.

### Completed Creator feature — Telegram Cognition Context Inspector v1

Status: **COMPLETE / DEPLOYED**.

See `docs/TELEGRAM_COGNITION_CONTEXT_INSPECTOR_V1.md`.

The owner-only Telegram viewer exposes the actual compact cognition context captured immediately before production model injection, retains the latest three actor-scoped snapshots, distinguishes primary and corrective-retry injections, recursively renders future context keys, and pages long snapshots without message splitting.

Runtime PR #187:
- final tested head `b4e0248b5fbf1d4fbc65c62181b8d1bfb74dc8ff`;
- CI #950 / run `31929295850`: SUCCESS, **605 passed in 45.27s**;
- merge `c1ee61ad335ea3fd37509e868c8b406e20d714b7`;
- Deploy #240 / run `31929343421`: SUCCESS.

No production cognition call was fabricated solely to populate the viewer.

### Latest completed Creator feature — Cognition Context Efficiency v1

Status: **COMPLETE / DEPLOYED / CLOSED**.

See `docs/COGNITION_CONTEXT_EFFICIENCY_V1.md`.

The cognition inspector exposed excessive model-facing metadata. The read-only production baseline audit before compaction measured:
- full prompt **66,952 characters**;
- runtime context **64,575 characters**;
- `capability_awareness` **24,404 characters (37.8%)**;
- `action_options` **17,866 characters (27.7%)**;
- repeated `training_method` metadata **8,411 characters**.

PR #191 compacted the model-facing projection only. It removes repeated capability definition/application prose and repeated training catalog/planning metadata while retaining executable action/target/duration/resource contracts, exact movement IDs, proficiency/behavioral anchors, machine-relevant requirements, risk and supporting knowledge/attributes. Deterministic engine state and validation/mutation paths remain unchanged.

Runtime PR #191:
- final tested head `b4febc29ad7ba37d67547346abd5bb9fff73b772`;
- CI #954: SUCCESS, **613 passed in 53.34s**;
- fresh DB init/status healthy; schema v5;
- task-relevant acceptance workflows green;
- merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6`;
- Deploy #243 / run `31931381264`: **SUCCESS**, including production cognition-context audit execution.

The GitHub connector confirmed successful deploy/audit execution but did not expose the raw redirected job-log body. Therefore the canonical checkpoint records no fabricated post-deploy percentage. Closure is supported by the measured production baseline, deterministic serialized-size reduction regression, semantic-preservation regression, full CI and successful deployment.

Do not continue speculative trimming by default. Reopen cognition-context efficiency only when measured prompt size, provider cost/latency, or observed cognition quality justifies another bounded slice.

## Current verified deployment

Latest runtime deployment: **Deploy #243 / run `31931381264` SUCCESS**, Cognition Context Efficiency v1.

Verified deployment evidence:
- runtime merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6` deployed;
- install/configure/restart/verify completed successfully;
- production cognition-context audit execution succeeded;
- schema remains v5;
- no schema migration or synthetic production cognition call was required for this slice.

## Deferred boundaries

No giant planner/task graph, relationship-system expansion by default, universal episodic-memory engine, witness model, weather/economy/vehicle systems merely for completeness, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, deep weapon taxonomy, quests/jobs, arbitrary LLM profile mutation, synthetic production actors/actions solely for proof, modifier authoring UI, status-effect taxonomy, arbitrary universal bonus engine, or universal condition/expression language.

These may become explicit feature candidates where appropriate; they are not automatically authorized by foundation closure.

## Exact resume point

**Overall Workflow/Foundation Review v1 remains COMPLETE / CLOSED. Telegram Cognition Context Inspector v1 and Cognition Context Efficiency v1 are COMPLETE / DEPLOYED. Latest runtime checkpoint: PR #191, final tested head `b4febc29ad7ba37d67547346abd5bb9fff73b772`, CI #954 with 613 passing tests, merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6`, Deploy #243 SUCCESS. Prompt compaction v1 is closed after targeting the measured dominant duplicate metadata while preserving deterministic/runtime semantics. Next work is the next Creator-prioritized product feature, not generic gap hunting or speculative context trimming.**