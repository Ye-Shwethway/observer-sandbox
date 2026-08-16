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

**W0 — World Stimulus / Exposure Foundation v1 is COMPLETE / DEPLOYED.**

Evidence:
- PR #216 — `Add World Stimulus / Exposure Foundation v1`
- final tested head `c73343188c5a1891c445dae565c48220c1a12736`
- CI #984 / run `31953100474`: SUCCESS
- Public Readiness Security Audit #142: SUCCESS
- Inventory Foundation v1 Acceptance #69: SUCCESS
- merge `76a2929358ac0ac765e80703efd4fa4e5b2bfe48`
- Deploy #255 / run `31953211583`: SUCCESS
- final sync/install/configure cognition/restart/verify: SUCCESS
- schema v9
- world-input schema v1
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
- Intelligent Mind Engine Foundation v1;
- **World Stimulus / Exposure Foundation v1**.

South Lake Tahoe remains intentionally paused.

## Canonical cognition chain

Canonical docs:
- `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
- `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve the full separation:

`world/event truth != stimulus availability != exposure != perception/interpretation != memory != mind state/thought != intention/plan != action proposal != action authority`

No later subsystem may collapse these layers merely to simplify prompting.

## Memory architecture lock

Memory provides actor-owned episodic/semantic records, dynamic strength/detail/lifecycle, simulation-time forgetting, sleep-bounded consolidation, cue-driven recall, bounded reinforcement, generic spatial semantic knowledge and Telegram observability.

Character Profile has separate Working Memory / Encoding / Retention / Recall traits. Memory behavior may not branch on character identity.

Exposure is not memory. Thought is not automatically memory.

## MIND-F0 — Intelligent Mind Engine Foundation — DEPLOYED

Generic persistence exists for:
- bounded `mental_cycles`;
- typed `mental_episodes`;
- persistent/semi-persistent `mental_artifacts`;
- typed `mental_links`.

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

MIND-F0 remains behavior-neutral. Current autonomy does not automatically create mental cycles or thoughts.

## W0 — World Stimulus / Exposure Foundation — DEPLOYED

Canonical contract:
`docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`

W0 is the shared world-input boundary for future weather, media, money, obligations, communications and other external cognition inputs.

Deployed schema/API:
- `world_stimuli` — externally available signals with category, channel, source provenance, salience and simulation-time availability;
- `world_stimulus_scopes` — explicit world/location/entity/character/audience availability scopes;
- `character_exposures` — actor-specific proof that a signal reached the actor boundary;
- bounded eligibility query that does not itself record exposure;
- explicit exposure recording/readback;
- bounded validation for categories/channels/scopes;
- generic second-character support.

Authority guarantees:
- eligibility != exposure;
- exposure != perception;
- exposure != belief;
- exposure != memory;
- exposure != thought/appraisal;
- exposure != behavior/action authority;
- W0 APIs do not auto-create events, Character Memory or Mind cycles.

## World element expansion policy

Phones, televisions, radios, computers, internet/network access, accounts, calendars, communication endpoints and similar elements are represented world entities/resources when possession, location, access, availability or capability matters.

Add them in the bounded slice where a concrete producer/consumer requires them. Do not prebuild decorative complexity and do not treat devices/internet as omniscient cognition channels.

Examples:
- `message -> represented phone/device -> actual exposure -> future perception/appraisal`
- `media item -> represented TV/device output -> location/action compatibility -> exposure`
- `internet item -> represented publication + network/service + accessible device -> interaction/exposure`

## Active phase — first concrete World Input producers

### W1 — Environment / Weather Foundation — NEXT

Build the first concrete W0 producer.

Minimum target:
- represented weather state;
- condition;
- temperature;
- precipitation;
- wind;
- light/daylight context;
- simulation-time validity;
- location/area applicability;
- outdoor vs indoor exposure boundary;
- W0 environment stimulus generation;
- deterministic environment/affordance inputs where represented;
- no direct mood modifier.

Weather should not write `sadness`, `motivation`, `training desire` or similar Mind state directly.

Preferred flow:
`weather truth -> environment stimulus -> exposure eligibility/actual exposure -> future perception/appraisal -> Mind`

Estate-first scope is sufficient; W1 does not require opening South Lake Tahoe traversal.

### W2 — Commitments / Obligations Foundation

Minimum target:
- appointments/deadlines/promises/scheduled obligations;
- start/due times;
- status/flexibility;
- reminders through W0;
- no automatic intention/plan creation.

### W3 — Money / Economy Minimum Foundation

Minimum target:
- balances/financial resources;
- transactions;
- income/expenses/obligations;
- deterministic affordability;
- financial notices through W0;
- no direct anxiety/behavior modifier.

### W4 — Information / Media Foundation

Minimum target:
- information/media items;
- sources/publishers;
- publication/availability;
- credibility/source metadata;
- represented device/media exposure through W0;
- `world knows != character knows`.

### W5 — Communication Exposure Foundation

Minimum target:
- sender/recipient/channel/content/delivery boundary;
- utterance/message stimulus creation;
- actual read/heard/exposure boundary;
- later interpretation/response through Social Cognition, not direct chatbot ping-pong.

Use exemplar-first, then batch-by-pattern. W1-W5 do not need five giant parallel architectures if multiple producers share the proven W0 pattern.

## MIND-F2 — Mental Episode Runtime — AFTER MINIMUM WORLD INPUTS

At meaningful cognition/action boundaries, one cognition call may emit a small structured mental-episode bundle alongside an action proposal.

No continuous per-minute LLM polling.

Mind input should consume bounded actor-relative exposure/perception handoffs, not global world tables.

## MIND-F3 — Attention / Appraisal / Active Concerns

Add small persistent mental context above raw prompt data.

External facts should flow through exposure/perception and character-relative appraisal rather than arbitrary direct mental modifiers.

## MIND-F4 — Intention Foundation

Introduce near-term future direction distinct from prospective thought and distinct from a multi-step plan.

## MIND-F5 — Planning

Planning consumes authoritative current state plus currently recallable memory and active Mind artifacts. Plans remain interruptible and never bypass action validation.

First useful consumers remain:
- multi-day training/recovery balance;
- purposeful destination + activity selection.

## MIND-F6 — Social Cognition / Communication

Target:
`utterance -> exposure/perception -> memory/person context -> appraisal/social inference -> internal thought -> response intention -> utterance proposal`

## MIND-F7 — Relationship Adaptation

Relationship state should consume represented interpreted social evidence rather than arbitrary direct dialogue-to-trust increments.

## Observability separation

Future observer surfaces should distinguish:
- World / Environment — objective facts;
- Exposure — external signals that reached the actor;
- Profile — represented character facts;
- Memory — retained knowledge/experience;
- Mind — structured mental episodes/artifacts;
- Cognition Context — exact model-injection snapshots.

## Universal autonomy semantic lock

Character-specific factual seeds are allowed. Character-specific behavioral scripts are not.

No named-character autonomy prompt, routine, destination steering, anti-repetition counter-prompt, memory formula, world-input interpretation or mental script may be introduced.

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
- full unused device/media/economy ecosystems before a consumer needs them.

## World / spatial lock

Current Estate boundary remains closed:
- no public-road edge from Main Security Gate;
- no Tahoe-backcountry edge from Concealed Forest Passage;
- no water-travel edge from Hidden Dock;
- legacy Estate Exterior remains locked/non-traversable.

Known geography never grants executable movement by itself.

## Current exact resume point

**W0 World Stimulus / Exposure Foundation v1 is deployed. Implement W1 Environment / Weather Foundation next on `test`, aligned with both W0 and the Mind Engine contract. Expand concrete world entities such as devices/network access only when an active producer/consumer requires them. Do not activate a giant Mind/Planning system yet.**
