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
`develop on test -> focused tests + final PR CI -> merge test into main -> automatic deploy when runtime-affecting -> production verification -> sync test to final main checkpoint`

Do not create per-slice `agent/*` branches unless the Creator explicitly approves an exceptional isolation need.

## Current canonical checkpoint

**W0 — World Stimulus / Exposure Foundation v1 is COMPLETE / DEPLOYED.**

Latest runtime evidence:
- PR #216 — `Add World Stimulus / Exposure Foundation v1`
- final tested PR head: `c73343188c5a1891c445dae565c48220c1a12736`
- CI #984 / run `31953100474`: SUCCESS
- Public Readiness Security Audit #142: SUCCESS
- Inventory Foundation v1 Acceptance #69: SUCCESS
- merge: `76a2929358ac0ac765e80703efd4fa4e5b2bfe48`
- Deploy #255 / run `31953211583`: SUCCESS
- deployment verification (`sync -> install/configure cognition -> restart -> verify`): SUCCESS
- schema: **v9**
- world-input schema: **v1**
- mind schema remains **v1**

`test` was fast-forwarded to the runtime merge before this docs-only continuity update.

## Required cognition / world-input / memory read order

1. `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
2. `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
3. `docs/HUMAN_MEMORY_DYNAMICS_V1.md`
4. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
5. `docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md`
6. task-relevant world/profile/runtime docs only.

## Canonical Mind Engine rule

The Mind Engine is the shared character-owned substrate for future internal cognition.

Preserve:

`world truth != perception != memory != mind state/thought != intention/plan != action proposal != action authority`

Every future subsystem that can materially influence character perception, interpretation, thought, affect, active concerns, goals, intentions, planning, social cognition, communication or relationship appraisal must read and align with `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md` before implementation.

MIND-F0 remains behavior-neutral: current autonomy does not automatically create mental cycles or thoughts yet.

## W0 World Stimulus / Exposure Foundation v1

Canonical contract:
`docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`

W0 creates the shared boundary between objective world truth and future actor-relative perception.

Preserve:

`world/event truth != stimulus availability != character exposure != perception/interpretation != appraisal/thought != memory != action authority`

Deployed generic schema:
- `world_stimuli` — externally available signals with source provenance, category/channel, salience and simulation-time availability;
- `world_stimulus_scopes` — explicit world/location/entity/character/audience availability scopes;
- `character_exposures` — proof that a signal actually reached one represented actor through an implemented channel.

Initial stimulus categories:
- `environment`
- `information`
- `communication`
- `financial`
- `obligation`
- `social`
- `system`
- `other`

Initial channels:
- `visual`
- `auditory`
- `tactile`
- `environmental`
- `device`
- `media`
- `direct`
- `mixed`
- `other`

Important rules:
- a world fact is not character knowledge merely because it exists;
- eligibility queries do not record exposure;
- exposure does not prove understanding, belief, emotional importance, memory or behavior change;
- W0 does not auto-create Memory rows, mental cycles, relationship changes or world mutations;
- global world-input tables must not be dumped wholesale into cognition.

## Devices / media / internet expansion rule

Phones, televisions, radios, computers, internet/network access, accounts, calendars and communication endpoints are represented world entities/resources when possession, location, access, availability or capabilities matter.

Add them when a concrete producer/consumer needs them, in the same bounded world slice. Do not prebuild unused complexity and do not treat devices or the internet as magical omniscient cognition channels.

Examples:
- `message truth -> represented phone/device -> exposure -> future perception/appraisal`
- `media item -> represented TV/device output -> location/action compatibility -> exposure`
- `published information -> represented network/service + device access -> interaction/exposure`

## Memory architecture remains authoritative

Preserve:
`event/world truth != actor memory trace != currently recalled cognition context != action authority`.

Human Memory Dynamics v1 remains deployed with recent/consolidated/remote/faded lifecycle, strength/detail decay, sleep-bounded consolidation, cue-driven recall and individual Memory Ability traits.

Exposure is not memory. Thought is not automatically memory. Prospective thought is not automatically intention or plan.

## External world / mental appraisal rule

Do not implement direct arbitrary mental modifiers such as:
- `rain -> mood -5`
- `low cash -> anxiety +10`
- `negative news -> sadness +20`

Preferred flow:

`authoritative external fact -> stimulus -> exposure -> perception -> character-relative appraisal -> mental episode/artifact/affect -> possible intention/action`

World systems own their facts; Mind owns internal interpretation.

## Current world-input sequence

W0 is deployed. Preferred next minimum producer sequence:
1. **W1 Environment / Weather Foundation**
2. W2 Commitments / Obligations Foundation
3. W3 Money / Economy Minimum Foundation
4. W4 Information / Media Foundation
5. W5 Communication Exposure Foundation
6. then MIND-F2 Mental Episode Runtime once actor-relative external inputs are rich enough.

Use exemplar-first, then batch-by-pattern. These do not need to become five oversized isolated architectures if they share proven W0 patterns.

## W1 direction

Weather/environment should become the first concrete W0 producer because it is continuous external state with clear location/exposure boundaries.

Minimum target:
- weather condition;
- temperature;
- precipitation;
- wind;
- light/daylight context;
- indoor/outdoor exposure distinction;
- deterministic environmental affordance/comfort inputs where represented;
- W0 stimulus/exposure integration;
- no direct mood or behavior modifier.

Do not expand South Lake Tahoe merely to build weather. Estate-first scope remains active.

## Cognition Context vs Mind vs Exposure

Keep distinct:
- **Exposure** — external signals that actually reached the actor boundary;
- **Memory** — what the actor retained/knows;
- **Mind** — structured actor-owned internal mental activity/state;
- **Cognition Context** — the raw compact data actually injected into a model call.

No Telegram Exposure/Mind browser is required yet; current persistence/query contracts make future observer surfaces possible without redesign.

## Universal autonomy invariant

Character-specific authoring may seed represented facts/state but must not command future behavior.

No named-character autonomy policy, bespoke routine, destination steering, anti-repetition counter-prompt, memory formula, world-input interpretation or mental script may be introduced.

## Estate boundary

Estate-first scope remains active. South Lake Tahoe/public/backcountry/water expansion remains paused.

No traversable continuation exists from:
- Main Security Gate to public road;
- Concealed Forest Passage to Tahoe backcountry;
- Hidden Dock to water travel.

## Exact resume point

**W0 World Stimulus / Exposure Foundation v1 is deployed. Build W1 Environment / Weather Foundation next against both the W0 and Mind Engine contracts. Expand concrete world elements only when the active producer/consumer requires them. Do not activate a giant Mind/Planning system yet.**
