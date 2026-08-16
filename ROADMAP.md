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
- Persistent repository branches are only `main` and `test`; normal development occurs on `test` and is promoted to `main` after validation.

## Current production checkpoint

**Intelligent Mind Engine Foundation v1 is COMPLETE / DEPLOYED.**

Evidence:
- PR #214 — `Add Intelligent Mind Engine Foundation v1`
- final tested head `a08faaeaf5852ec44ea4aab92f78c746db5d18e8`
- CI #982 / run `31951775815`: SUCCESS
- Public Readiness Security Audit #139: SUCCESS
- Inventory Foundation v1 Acceptance #67: SUCCESS
- merge `71b280191e91c7314180e992bb0beaf0c734d97a`
- Deploy #254 / run `31951861684`: SUCCESS
- final sync/install/configure cognition/restart/verify: SUCCESS
- schema v8
- mind schema v1

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
- Human Memory Dynamics v1;
- **Intelligent Mind Engine Foundation v1**.

South Lake Tahoe remains intentionally paused.

## Memory architecture lock

Canonical docs:
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve:
`event/world truth != actor memory trace != currently recalled cognition context != current action authority`

Memory provides actor-owned episodic/semantic records, dynamic strength/detail/lifecycle, simulation-time forgetting, sleep-bounded consolidation, cue-driven recall, bounded reinforcement, generic spatial semantic knowledge and Telegram observability.

Character Profile has separate Working Memory / Encoding / Retention / Recall traits. Memory behavior may not branch on character identity.

## Canonical Mind Engine architecture

Canonical contract:
`docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`

The Mind Engine is the shared internal cognition substrate above raw injected context and below future intention/planning/social behavior.

Preserve:

`world truth != perception != memory != mind state/thought != intention/plan != action proposal != action authority`

Every future system that can materially influence character perception, interpretation, thought, affect, active concerns, goals, intentions, planning, social cognition, communication or relationship appraisal must read and align with the Mind Engine contract before implementation.

Do not create parallel hidden mind/planner/thought stores. Use the shared typed Mind sockets or explicitly document why a subsystem is outside mental cognition.

## MIND-F0 — Foundation Schema / Socket Contract — DEPLOYED

Generic persistence exists for:
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

**MIND-F0 is behavior-neutral.** Current autonomy does not automatically create mental cycles or thoughts. No planner or thought generator was activated by the foundation deployment.

## W0 — World Stimulus / Exposure Foundation — AUTHORIZED / IN IMPLEMENTATION

Canonical contract:
`docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`

Purpose: create one shared world-input boundary before weather/media/money/communication systems begin feeding cognition.

Preserve:

`world/event truth != stimulus availability != character exposure != perception/interpretation != appraisal/thought != memory != action authority`

W0 minimum schema/API:
- `world_stimuli` — externally available signals with source provenance, category, channel, salience and simulation-time availability;
- `world_stimulus_scopes` — explicit world/location/entity/character/audience availability scopes;
- `character_exposures` — proof that a represented signal actually reached one character through an implemented channel;
- bounded eligibility queries that do not record exposure;
- generic exposure recording that does not create Memory, Mind state, relationship changes or world mutations.

Initial stimulus categories:
- environment;
- information;
- communication;
- financial;
- obligation;
- social;
- system;
- other.

Initial channel vocabulary:
- visual;
- auditory;
- tactile;
- environmental;
- device;
- media;
- direct;
- mixed;
- other.

### World element expansion policy

Add phones, televisions, radios, computers, internet/network access, accounts, calendars, communication endpoints and similar world elements **when a concrete W0 producer/consumer needs them**.

They must be represented through normal world/entity/resource/relationship contracts when possession, location, access, availability or capabilities matter. Do not treat devices or the internet as magical omniscient cognition channels.

Example:
`media item -> represented TV/device output -> actor/location compatibility -> exposure -> future perception/appraisal`

## World-input producer sequence after W0

### W1 — Environment / Weather Foundation

Minimum target:
- weather condition;
- temperature;
- precipitation;
- wind;
- light/daylight context;
- indoor/outdoor exposure boundary;
- deterministic environment/affordance inputs where represented;
- no direct mood modifier.

### W2 — Commitments / Obligations Foundation

Minimum target:
- appointments/deadlines/promises/scheduled obligations;
- start/due times, status and flexibility;
- reminders through W0;
- no automatic intention or plan creation.

### W3 — Money / Economy Minimum Foundation

Minimum target:
- character financial resources/balances;
- transactions;
- income/expenses/obligations;
- deterministic affordability;
- financial notices through W0;
- no direct anxiety/behavior modifier.

### W4 — Information / Media Foundation

Minimum target:
- information/media items;
- source/publisher and publication/availability;
- credibility/source metadata;
- represented device/media exposure through W0;
- `world knows != character knows`.

### W5 — Communication Exposure Foundation

Minimum target:
- sender/recipient/channel/content/delivery boundary;
- utterance/message stimulus creation;
- actual exposure/read-or-heard boundary;
- later interpretation/response through Social Cognition, not direct chatbot ping-pong.

Use exemplar-first, then batch-by-pattern. These do not have to become five oversized isolated architectures if multiple producers share the proven W0 contract.

## MIND-F2 — Mental Episode Runtime — AFTER MINIMUM WORLD INPUTS

At meaningful cognition/action boundaries, allow one model call to emit a small structured bundle of mental episodes alongside an action proposal.

No continuous per-minute LLM polling.

Mind input should consume bounded actor-relative perception/exposure handoffs, not global world tables.

## MIND-F3 — Attention / Appraisal / Active Concerns

Add small persistent mental context above raw prompt data.

External facts should flow through represented exposure/perception and character-relative appraisal rather than direct arbitrary mental modifiers.

## MIND-F4 — Intention Foundation

Introduce near-term future direction distinct from prospective thought and distinct from a multi-step plan.

## MIND-F5 — Planning

Planning consumes authoritative current state plus currently recallable memory and active mind artifacts. Plans remain interruptible and never bypass action validation.

First useful consumers remain:
- multi-day training/recovery balance;
- purposeful destination + activity selection.

## MIND-F6 — Social Cognition / Communication

Target:
`utterance -> exposure/perception -> memory/person context -> appraisal/social inference -> internal thought -> response intention -> utterance proposal`

## MIND-F7 — Relationship Adaptation

Relationship state should consume represented interpreted social evidence rather than arbitrary direct dialogue-to-trust increments.

## Why Cognition Context remains separate

Current `Cognition Context` is the read-only inspector for actual bounded model injection. It is useful and intentionally raw; it is not represented Mind state.

Future observability should distinguish:
- World / Environment — objective facts;
- Exposure — externally available signals that reached the actor;
- Profile — represented character facts;
- Memory — retained knowledge/experience;
- Mind — structured mental episodes and active artifacts;
- Cognition Context — exact model-injection snapshots.

## Universal autonomy semantic lock

A character-specific source may define factual identity/profile, biography, initial skills, possessions, relationships, preferences/hobbies, factual goals, memory ability or factual initial knowledge.

It may not define future behavior scripts such as named autonomy prompts/policies, fixed daily routines/training schedules, bespoke destination steering or identity-keyed code branches.

Generic cognition derives behavior from represented state:
`profile + physiology + time + environment + affordances + goals + relationships + currently recallable memories + active mental context + deterministic constraints`.

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
- character-specific mental scripts;
- full unused device/media/economy ecosystems before a consumer needs them.

## World / spatial lock

Current Estate boundary remains closed:
- no public-road edge from Main Security Gate;
- no Tahoe-backcountry edge from Concealed Forest Passage;
- no water-travel edge from Hidden Dock;
- legacy Estate Exterior remains locked/non-traversable.

Known geography never grants executable movement by itself.

## Current exact resume point

**Implement and validate W0 — World Stimulus / Exposure Foundation v1 on `test`, promote it to `main`, deploy schema/API, then build the first minimum world-input producer (normally W1 Weather/Environment) against the canonical W0 + Mind contracts. Expand concrete world elements such as devices/network access only when the active producer/consumer requires them.**
