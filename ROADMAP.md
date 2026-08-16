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
- Character-specific behavioral hard-coding is forbidden.
- Persistent repository branches are only `main` and `test`; normal development occurs on `test` and is promoted to `main` after validation.

## Current production checkpoint

**W1 — Environment / Weather Foundation v1 is COMPLETE / DEPLOYED.**

Evidence:
- PR #218 — `Add Environment / Weather Foundation v1`
- final tested head `432cdabeee8c099b13fe70545498cf6730abe751`
- CI #985 / run `31953779921`: SUCCESS
- Inventory Foundation v1 Acceptance #70: SUCCESS
- merge `7279fc15dc2e83ba1703913db649e9968fdb9fdd`
- Deploy #256 / run `31953861367`: SUCCESS
- final sync/install/configure cognition/restart/verify: SUCCESS
- schema v10
- environment schema v1
- world-input schema v1
- mind schema v1

Production intentionally contains **no fabricated current weather**. W1 is source-neutral until an authoritative environment producer/source writes a state.

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
- World Stimulus / Exposure Foundation v1;
- **Environment / Weather Foundation v1**.

South Lake Tahoe remains intentionally paused.

## Canonical cognition / world-input chain

Canonical docs:
- `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
- `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve:

`world/event truth != stimulus availability != exposure != perception/interpretation != memory != mind state/thought != intention/plan != action proposal != action authority`.

No later subsystem may collapse these layers merely to simplify prompting.

## MIND-F0 — Intelligent Mind Engine Foundation — DEPLOYED

Generic persistence exists for:
- bounded `mental_cycles`;
- typed `mental_episodes`;
- persistent/semi-persistent `mental_artifacts`;
- typed `mental_links`.

MIND-F0 remains behavior-neutral. Current autonomy does not automatically create mental cycles or thoughts.

## W0 — World Stimulus / Exposure Foundation — DEPLOYED

W0 is the shared world-input boundary for weather, media, money, obligations, communications and other external cognition inputs.

Deployed schema/API:
- `world_stimuli`;
- `world_stimulus_scopes`;
- `character_exposures`;
- bounded eligibility queries;
- explicit exposure recording/readback.

Authority guarantees:
- eligibility != exposure;
- exposure != perception/belief/memory/thought;
- exposure never grants action authority.

## W1 — Environment / Weather Foundation — DEPLOYED

Canonical contract:
`docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`

Implementation/acceptance companions:
- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1_IMPLEMENTATION_NOTES.md`
- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1_ACCEPTANCE.md`

Deployed runtime:
- authoritative historical `environment_states`;
- weather condition, temperature, precipitation, wind, visibility, cloud cover and daylight/light fields;
- simulation-time validity and source provenance;
- represented-containment environment resolution;
- most-specific location state override;
- W0 direct ambient stimulus publication;
- direct ambient exposure only at explicit `world.spatial_container.exposure="outdoor"` locations;
- generic second-character/location support;
- same-scope state supersession with old direct-ambient W0 stimulus retirement.

Canonical flow:

`environment truth -> location applicability -> W0 environment stimulus -> direct outdoor exposure -> future perception/appraisal -> Mind`.

Explicit non-effects:
- no weather-to-mood arithmetic;
- no weather-to-action steering;
- no automatic Memory or Mind records;
- no default live weather fabrication;
- no live weather API, forecast engine or stochastic climate simulation yet.

Indoor locations may resolve geographic environment truth for future mediated consumers, but they do not receive direct ambient exposure.

## World element expansion policy

Phones, televisions, radios, computers, internet/network access, accounts, calendars, communication endpoints and similar elements are represented world entities/resources when possession, location, access, availability or capability matters.

Add them in the bounded slice where a concrete producer/consumer requires them. Do not prebuild decorative complexity and do not treat devices/internet as omniscient cognition channels.

For environment information specifically:
`weather truth != forecast publication != device/service availability != character exposure != belief`.

## Active phase — remaining minimum World Input producers

### W2 — Commitments / Obligations Foundation — NEXT

Goal: represent factual future obligations before planning so the character can later distinguish what is desired from what is expected/promised/scheduled.

Minimum target:
- obligation/commitment records;
- types such as appointment, promise, deadline and scheduled responsibility;
- start/due simulation times;
- optional represented person/entity/location target;
- status/lifecycle;
- flexibility/reschedulability metadata;
- provenance/source;
- W0 reminder/notice stimulus production when represented;
- no automatic Mind concern, intention or plan creation.

Potential world expansion when needed:
- calendar/reminder representation;
- communication endpoint/source for externally delivered commitments;
- devices only if a concrete reminder/delivery path requires them.

Keep commitment truth separate from reminder exposure and separate again from the actor mentally prioritizing it.

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

Use exemplar-first, then batch-by-pattern. W2-W5 do not need giant parallel architectures if they share the proven W0 pattern.

## MIND-F2 — Mental Episode Runtime — AFTER MINIMUM WORLD INPUTS

At meaningful cognition/action boundaries, one cognition call may emit a small structured mental-episode bundle alongside an action proposal.

No continuous per-minute LLM polling.

Mind input should consume bounded actor-relative exposure/perception handoffs, not global world tables.

## MIND-F3 — Attention / Appraisal / Active Concerns

Add small persistent mental context above raw prompt data. External facts flow through exposure/perception and character-relative appraisal rather than direct arbitrary mental modifiers.

## MIND-F4 — Intention Foundation

Introduce near-term future direction distinct from prospective thought and distinct from a multi-step plan.

## MIND-F5 — Planning

Planning consumes authoritative current state plus currently recallable memory and active Mind artifacts. Plans remain interruptible and never bypass action validation.

First useful consumers remain:
- multi-day training/recovery balance;
- purposeful destination + activity selection.

## MIND-F6 — Social Cognition / Communication

Target:
`utterance -> exposure/perception -> memory/person context -> appraisal/social inference -> internal thought -> response intention -> utterance proposal`.

## MIND-F7 — Relationship Adaptation

Relationship state should consume represented interpreted social evidence rather than arbitrary direct dialogue-to-trust increments.

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
- full unused device/media/economy ecosystems before a consumer needs them;
- fabricated weather simply to avoid an empty environment state.

## World / spatial lock

Current Estate boundary remains closed:
- no public-road edge from Main Security Gate;
- no Tahoe-backcountry edge from Concealed Forest Passage;
- no water-travel edge from Hidden Dock;
- legacy Estate Exterior remains locked/non-traversable.

Known geography never grants executable movement by itself.

## Current exact resume point

**W1 Environment / Weather Foundation v1 is deployed. Implement W2 Commitments / Obligations Foundation next on `test`, aligned with W0 and the Mind Engine contract. Expand calendars/devices/communication endpoints only when the active obligation/reminder consumer requires them. Do not activate the Mental Episode/Planning runtime yet.**
