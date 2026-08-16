# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-16

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Prefer vertical completeness before local depth.
- Never manipulate production merely to manufacture evidence.
- Code/runtime PRs get one final full CI checkpoint by default; docs-only changes do not need the Python suite.
- **Character-specific behavioral hard-coding is forbidden.** Character-specific authoring may seed represented facts/state; autonomous behavior must emerge from universal systems.

## Current production checkpoint

**Human Memory Dynamics v1 is COMPLETE / DEPLOYED.**

Evidence:
- PR #212
- final tested head `1cad8d9188e49f42f9c00b8026eccd917a9fc073`
- CI #980 / run `31950039890`: SUCCESS
- all triggered acceptance gates on the final head: SUCCESS
- merge `b8343d12b5204a0f3a049cbfb7632b617df77495`
- Deploy #253 / run `31950111179`: SUCCESS
- final install/configure cognition/restart/verify: SUCCESS
- schema v7

## Completed foundation stack

The current deployed minimum foundation includes:
- Character Profile / Skills minimum foundations;
- adaptive dispositions/habits/preferences/personality foundations;
- Estate spatial-container and reachability foundation;
- Outdoor Spatial Affordance Cognition v1;
- Universal Character Autonomy v1;
- Universal action satiation / movement-cycle shaping;
- Character Memory Foundation v1;
- Semantic Spatial Memory Migration;
- Human Memory Dynamics v1.

South Lake Tahoe remains intentionally paused.

## Memory architecture lock

Canonical docs:
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve:
`event/world truth != actor memory trace != currently recalled cognition context != current action authority`

Memory now provides actor-owned episodic/semantic records, dynamic strength/detail/lifecycle, simulation-time forgetting, sleep-bounded consolidation, cue-driven recall, bounded reinforcement, generic spatial semantic knowledge and Telegram observability.

Character Profile has separate Working Memory / Encoding / Retention / Recall traits. Memory behavior may not branch on character identity.

## Canonical Mind Engine architecture

Canonical contract:
`docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`

The Mind Engine is the shared internal cognition substrate above raw injected context and below future intention/planning/social behavior.

Preserve:

`world truth != perception != memory != mind state/thought != intention/plan != action proposal != action authority`

### Mandatory future alignment rule

Every future system that can materially influence character perception, interpretation, thought, affect, active concerns, goals, intentions, planning, social cognition, communication or relationship appraisal **must read and align with the Mind Engine contract before implementation**.

This rule includes external-world systems when they feed cognition, especially:
- weather/environment appraisal;
- economy/money concerns;
- media/information exposure;
- communications;
- schedules/commitments/obligations;
- social/relationship systems.

Do not create parallel hidden mind/planner/thought stores. Use the shared typed Mind sockets or explicitly document why a subsystem is outside mental cognition.

### Foundation schema target

Mind Foundation v1 establishes generic persistence for:
- bounded `mental_cycles`;
- typed `mental_episodes`;
- persistent/semi-persistent `mental_artifacts`;
- typed `mental_links` to represented memories/events/entities/actions/other mental artifacts.

Initial episode vocabulary:
- task-focused;
- spontaneous;
- reflective;
- prospective;
- social;
- evaluative.

Reserved artifact vocabulary:
- concern;
- goal;
- intention;
- plan;
- social inference;
- appraisal;
- working item.

Foundation schema is not permission to activate every reserved subsystem immediately.

## Why Cognition Context remains separate

Current `Cognition Context` is the read-only inspector for the actual bounded model injection. It remains useful and intentionally raw.

It is not the represented mind.

Future observability should distinguish:
- Profile — represented character facts;
- Memory — retained knowledge/experience;
- Mind — structured mental episodes and active artifacts;
- Cognition Context — exact model-injection snapshots.

## Universal autonomy semantic lock

A character-specific source may define factual identity/profile, biography, initial skills, possessions, relationships, preferences/hobbies, factual goals, memory ability or factual initial knowledge.

It may not define future behavior scripts such as named autonomy prompts/policies, fixed daily routines/training schedules, bespoke destination steering or identity-keyed code branches.

Generic cognition derives behavior from represented state:
`profile + physiology + time + environment + affordances + goals + relationships + currently recallable memories + active mental context + deterministic constraints`.

## External world input direction

Mind does not exist in a vacuum, but the project does not need to finish every possible world system before continuing cognition work.

Build minimum reusable world-input foundations as evidence requires them. External facts should feed cognition through represented exposure/perception and character-relative appraisal rather than direct arbitrary mental modifiers.

Examples:
- weather fact -> perception/comfort/affordance context -> appraisal;
- financial state -> represented affordability/obligation exposure -> concern/appraisal;
- media item -> source/publication -> character exposure -> interpretation/memory;
- utterance -> perception -> social interpretation -> response intention.

Avoid rules such as `rain -> mood -5` or `low cash -> anxiety +10`.

## Active phase — Intelligent Mind Engine Foundation

### MIND-F0 — Foundation Schema / Socket Contract — AUTHORIZED

Goal: create the stable generic persistence and integration envelope without changing current autonomous behavior.

Required:
1. canonical architecture contract;
2. mandatory future-system alignment rule in repository instructions;
3. schema for mental cycles, episodes, artifacts and typed links;
4. versioned generic runtime API to create/read those records;
5. idempotent migration and character-generic tests;
6. preserve current action/memory/world authority;
7. do not auto-generate thoughts yet.

### MIND-F1 — World Input Foundations — AFTER F0 / evidence-driven

Candidate minimum channels:
- weather/environment state and perception-ready exposure;
- money/economy minimum character state;
- media/information items + exposure;
- communication exposure/event boundary;
- commitments/obligations as needed.

Do not build giant complete world simulations merely to unblock Mind.

### MIND-F2 — Mental Episode Runtime

At meaningful cognition/action boundaries, allow one model call to emit a small structured bundle of mental episodes alongside an action proposal.

No continuous per-minute LLM polling.

### MIND-F3 — Attention / Appraisal / Active Concerns

Add small persistent mental context above raw prompt data.

### MIND-F4 — Intention Foundation

Introduce near-term future direction distinct from prospective thought and distinct from a multi-step plan.

### MIND-F5 — Planning

Planning consumes authoritative current state plus currently recallable memory and active mind artifacts. Plans remain interruptible and never bypass action validation.

First useful consumers remain:
- multi-day training/recovery balance;
- purposeful destination + activity selection.

### MIND-F6 — Social Cognition / Communication

Target:
`utterance -> perception -> memory/person context -> appraisal/social inference -> internal thought -> response intention -> utterance proposal`

### MIND-F7 — Relationship Adaptation

Relationship state should consume represented interpreted social evidence rather than arbitrary direct dialogue-to-trust increments.

## Deferred depth

Do not silently add:
- artificial-consciousness claims;
- full human emotion taxonomy;
- false-memory fabrication;
- clinical psychiatric simulation;
- dreams/detailed sleep-stage modeling;
- vector/embedding memory;
- continuous thought polling;
- giant monolithic Mind module;
- character-specific mental scripts.

## World / spatial lock

Current Estate boundary remains closed:
- no public-road edge from Main Security Gate;
- no Tahoe-backcountry edge from Concealed Forest Passage;
- no water-travel edge from Hidden Dock;
- legacy Estate Exterior remains locked/non-traversable.

Known geography never grants executable movement by itself.

## Current exact resume point

**Implement MIND-F0 — Intelligent Mind Engine Foundation Schema / Socket Contract. Keep behavior unchanged. After deployment, inspect and discuss which minimum world-input foundations should precede the first Mental Episode Runtime. All future cognition-affect-planning-social systems must align with the canonical Mind Engine contract.**
