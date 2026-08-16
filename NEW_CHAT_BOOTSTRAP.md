# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-16

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches are only `main` and `test`.

Default workflow:
`develop on test -> focused tests + final PR CI -> merge test into main -> automatic deploy when runtime-affecting -> production verification -> sync test to final main checkpoint`.

Do not create per-slice `agent/*` branches unless the Creator explicitly approves an exceptional isolation need.

## Current canonical checkpoint

**W1 — Environment / Weather Foundation v1 is COMPLETE / DEPLOYED.**

Latest runtime evidence:
- PR #218 — `Add Environment / Weather Foundation v1`
- final tested PR head: `432cdabeee8c099b13fe70545498cf6730abe751`
- CI #985 / run `31953779921`: SUCCESS
- Inventory Foundation v1 Acceptance #70: SUCCESS
- merge: `7279fc15dc2e83ba1703913db649e9968fdb9fdd`
- Deploy #256 / run `31953861367`: SUCCESS
- deployment verification (`sync -> install/configure cognition -> restart -> verify`): SUCCESS
- schema: **v10**
- environment schema: **v1**
- world-input schema: **v1**
- mind schema: **v1**

Important production state: **W1 does not invent or seed current weather.** Until an authoritative producer/source writes an environment state, production correctly has no represented current weather condition.

## Required cognition / world-input read order

1. `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
2. `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
3. `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`
4. `docs/HUMAN_MEMORY_DYNAMICS_V1.md`
5. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
6. task-relevant world/profile/runtime docs only.

## Canonical layer separation

Preserve:

`world/event truth != stimulus availability != character exposure != perception != memory != mind/thought != intention/plan != action proposal != action authority`.

The Mind Engine remains the shared actor-owned cognition substrate. MIND-F0 is still behavior-neutral: current autonomy does not automatically generate mental cycles/thoughts and no planner is active.

## W0 — World Stimulus / Exposure Foundation

Canonical contract:
`docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`

Deployed generic persistence:
- `world_stimuli`
- `world_stimulus_scopes`
- `character_exposures`

Key rules:
- world existence is not character knowledge;
- stimulus eligibility is not exposure;
- exposure is not perception, belief, memory, thought or behavior;
- producers route cognition-facing external signals through W0 instead of bespoke hidden exposure stores.

## W1 — Environment / Weather Foundation v1

Canonical contract:
`docs/ENVIRONMENT_WEATHER_FOUNDATION_V1.md`

Implementation companions:
- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1_IMPLEMENTATION_NOTES.md`
- `docs/ENVIRONMENT_WEATHER_FOUNDATION_V1_ACCEPTANCE.md`

Deployed authoritative table:
- `environment_states`

Represented environment fields include:
- weather condition;
- temperature C;
- precipitation kind/intensity;
- wind speed;
- visibility;
- cloud cover;
- daylight state/light level;
- simulation-time validity;
- source provenance and lifecycle.

Canonical W1 flow:

`environment truth -> containment-based location applicability -> W0 environment stimulus -> actual direct outdoor exposure -> future perception/appraisal -> possible thought/memory/intention -> validated action`.

Important rules:
- authoritative environment state is separate from W0 stimulus/exposure;
- most-specific represented containment scope wins;
- direct ambient exposure requires `world.spatial_container.exposure = "outdoor"` on the actor's current location;
- indoor locations may resolve geographic environment truth for future windows/apps/media consumers but do not receive direct ambient exposure;
- no hard-coded Estate outdoor ID list exists in the weather algorithm;
- replacement same-scope states preserve history by superseding prior rows and retiring prior direct-ambient stimuli;
- W1 does not auto-create Events, Memory, Mind cycles, relationship changes, mood values or action steering;
- no direct rules such as `rain -> mood -5` or `snow -> stay inside`.

## Device / internet weather rule

Direct ambient weather requires no device.

Forecasts, alerts, phone weather widgets, TV reports, websites or internet weather services are later **information/media** producers. They must use represented device/network/media access plus W0 exposure and retain source provenance where appropriate.

Preserve:

`weather exists != forecast exists != character received forecast != character believes forecast`.

Add phones/TV/computers/network/services only when an active producer/consumer needs them; do not treat them as omniscient cognition channels.

## Memory / Mind rules remain authoritative

Memory retains actor-owned experience/knowledge and dynamic recallability. Exposure is not memory; thought is not automatically memory; prospective thought is not automatically intention or plan.

External facts should eventually flow:

`authoritative fact -> stimulus -> exposure -> perception -> character-relative appraisal -> mental episode/artifact -> possible intention/action`.

## Next world-input sequence

Completed:
1. W0 World Stimulus / Exposure Foundation
2. W1 Environment / Weather Foundation

Next:
3. **W2 Commitments / Obligations Foundation**
4. W3 Money / Economy Minimum Foundation
5. W4 Information / Media Foundation
6. W5 Communication Exposure Foundation
7. MIND-F2 Mental Episode Runtime after minimum external-input foundations are sufficient.

Use exemplar-first, then batch-by-pattern. Do not turn each producer into a giant isolated subsystem.

## W2 direction

Commitments/obligations should represent the external/factual side of things a character has agreed, is expected, or is scheduled to do without automatically turning them into intentions or plans.

Likely minimum scope:
- appointment / promise / deadline / scheduled obligation facts;
- start/due simulation time;
- target/person/location where represented;
- status, priority/significance metadata and flexibility;
- reminder/notice production through W0 when appropriate;
- no automatic Mind concern/intention/plan creation.

## Estate boundary

Estate-first scope remains active. South Lake Tahoe/public-road/backcountry/water expansion remains paused.

No traversable continuation exists from:
- Main Security Gate to public road;
- Concealed Forest Passage to Tahoe backcountry;
- Hidden Dock to water travel.

## Exact resume point

**W1 Environment / Weather Foundation v1 is deployed and production contains no fabricated current weather. Build W2 Commitments / Obligations Foundation next against the W0 + Mind contracts. Expand concrete devices/calendars/communication endpoints only when W2 or another active producer actually needs them. Do not activate the Mental Episode/Planning runtime yet.**
