# Environment / Weather Foundation v1

Status: **CANONICAL W1 WORLD-INPUT CONTRACT**

## Purpose

Establish a small authoritative environment/weather domain that can produce real world stimuli through the W0 World Stimulus / Exposure contract without directly scripting character mood, thought, memory, planning, or behavior.

This is the first concrete W0 producer exemplar.

Read together with:
- `docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md`
- `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
- `docs/WORLD_OUTDOOR_SPATIAL_AFFORDANCE_CONTRACT_V1.md`
- `docs/WORLD_LOCATION_NODE_MODEL.md`

Canonical chain:

`environment truth -> location applicability -> W0 environment stimulus -> actual outdoor exposure -> future perception/appraisal -> possible thought/memory/intention -> validated action`

Preserve:

`weather fact != weather stimulus != exposure != perception != mood/appraisal != thought != memory != action authority`

## Scope

W1 represents only the minimum environment facts required by future cognition and outdoor-world systems:
- general weather condition;
- air temperature;
- precipitation kind/intensity;
- wind speed;
- visibility;
- cloud cover;
- daylight state/light level;
- simulation-time validity;
- geographic/location scope and provenance.

W1 does not attempt a complete meteorological simulation.

## Authoritative environment state

Environment truth is stored separately from W0 stimuli.

An environment state describes objective represented conditions over a location scope during a simulation-time interval.

Initial weather-condition vocabulary:
- `clear`
- `partly_cloudy`
- `cloudy`
- `fog`
- `rain`
- `snow`
- `storm`
- `mixed`
- `other`

Initial precipitation vocabulary:
- `none`
- `rain`
- `snow`
- `sleet`
- `mixed`
- `other`

Initial daylight vocabulary:
- `day`
- `dawn`
- `dusk`
- `night`

These labels are world facts, not emotional meanings.

## Data model

### `environment_states`

One row is one bounded authoritative environment snapshot.

Conceptual fields:
- stable state id;
- location scope id;
- condition;
- temperature C;
- precipitation kind/intensity 0..1;
- wind speed m/s;
- visibility km;
- cloud cover 0..1;
- daylight state;
- light level 0..1;
- valid-from / valid-until simulation time;
- status (`active`, `superseded`, `expired`, `retired`);
- source type/id;
- metadata/provenance;
- timestamps.

A later state may supersede an older state. History is retained.

## Location applicability

Environment scope follows represented containment, not string-name rules.

A state scoped to an ancestor location may apply to represented descendant locations unless a more specific active state overrides it.

Example:

`Thorne Estate environment state -> Core Estate Grounds / Rear Forested Estate / Private Lake Access`

Most-specific represented scope wins.

W1 does not open new topology or extend the current Estate boundary.

## Indoor / outdoor boundary

Direct ambient weather exposure is allowed only when the actor's current represented location explicitly declares:

`world.spatial_container.exposure = "outdoor"`

Current Estate outdoor authoring already uses this field.

Indoor or unclassified locations do **not** receive direct ambient weather exposure merely because an outdoor state exists for the Estate.

Future windows, balconies, HVAC, open doors, phone weather apps, televisions, smart-home displays, or other mediated channels may expose selected environment information through their own represented producer rules. They must not weaken this direct-exposure boundary.

## W0 stimulus production

Publishing an environment state may create one W0 stimulus:
- `stimulus_type = environment`
- `channel = environmental`
- source references the environment-state id;
- payload contains a bounded factual environment snapshot;
- location scopes include currently represented outdoor descendant locations to which the state applies.

Publishing a stimulus does not expose any character.

Environment signal salience is external prominence only. It may consider represented precipitation/wind/visibility severity, but it is not personal importance, emotion, or mental priority.

## Actual character exposure

W1 may record direct environment exposure only when all are true:
1. character exists;
2. character has a represented current location;
3. that location is explicitly outdoor;
4. an active applicable environment state exists at the exposure simulation time;
5. a matching active W0 environment stimulus exists for that location/time.

The exposure record links back to the environment-state stimulus and source location.

Exposure still does not mean attention, understanding, emotion, belief, durable memory, or behavior change.

## Daylight

Daylight is represented as objective environment context, not inferred mental state.

W1 may store a source-provided daylight state/light level. A later astronomical/timezone module may derive daylight deterministically from represented date/location, but W1 does not require that depth.

Do not infer `daylight -> happiness` or `night -> sleep`.

## Deterministic world effects

W1 v1 does not globally alter action legality merely because weather exists.

Future action/environment contracts may use authoritative fields such as severe visibility, precipitation, wind, temperature, or hazards to modify deterministic affordances/conditions. Those effects must be explicit and data-driven.

Example future flow:

`heavy snow truth -> outdoor surface/visibility condition -> deterministic action condition or modifier`

not:

`heavy snow -> character decides to stay inside`.

The latter belongs to future perception/appraisal/Mind processing.

## Cognition / Mind boundary

W1 does not inject global weather tables into cognition.

Target future path:

`environment state -> W0 stimulus -> character exposure -> perception-ready handoff -> character-relative appraisal -> mental episode/artifact`

A character indoors does not automatically possess current outdoor weather knowledge unless a represented exposure channel makes it available.

## Devices / internet / weather information

W1 direct ambient exposure requires no device.

A future weather forecast, alert, phone widget, TV report, website, or internet weather service is **information/media**, not direct ambient weather truth. When implemented it should use represented devices/network/media plus W0 exposure and retain provenance to the underlying source where appropriate.

This preserves:

`weather exists != forecast exists != character received forecast != character believes forecast`.

## Update / expiry lifecycle

When a new environment state supersedes an overlapping previous state for the same scope:
- the old state becomes `superseded`;
- its active W0 stimulus is retired/expired as appropriate;
- the new state becomes current truth;
- a new or replacement stimulus is published with its own provenance.

Do not mutate old environment history into the new condition.

## Genericity

The environment runtime must be character-generic and location-generic.

Forbidden:
- Darian-specific weather reactions;
- named-character temperature preferences inside W1;
- hard-coded lists of Estate outdoor location IDs in the environment algorithm;
- direct weather-to-mood values;
- direct weather-to-action steering.

Outdoor applicability derives from represented world fields and containment.

## Initial implementation boundary

W1 v1 implements:
- environment schema and migration;
- create/read/current-state APIs;
- ancestor-scope resolution;
- W0 stimulus publication;
- direct outdoor exposure proof/recording;
- bounded factual payloads;
- character/location generic tests.

W1 v1 does **not** require:
- live internet weather API integration;
- stochastic weather generation;
- forecast simulation;
- climate/season model;
- indoor HVAC/temperature simulation;
- clothing thermal comfort;
- weather-driven mood;
- automatic Mind or Memory records;
- Telegram weather UI.

## Initial production state policy

The runtime must not silently invent a live weather condition merely to populate the table.

If no authoritative environment state has been authored or produced, the correct state is `no represented current environment state`.

Tests may author fixture conditions to prove the contract. A later weather producer/generator or Creator-approved seed can supply actual simulation conditions.

## Acceptance

W1 is accepted when:
- this contract is canonical;
- schema migration is idempotent;
- authoritative environment state is separate from W0 stimuli/exposures;
- most-specific containment-based state resolution works;
- direct exposure occurs only at explicitly outdoor locations;
- environment stimulus publication uses W0 rather than bypassing it;
- exposure does not create Memory, Mind records, relationship changes, or action execution;
- a second character/location can use the same APIs without identity-keyed logic;
- current action/autonomy behavior remains unchanged;
- no live weather is fabricated when no producer/source exists.
