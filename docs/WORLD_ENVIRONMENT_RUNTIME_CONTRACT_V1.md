# World Environment Runtime Contract v1

Status: PLANNING AUTHORITY — IMPLEMENTATION NOT YET AUTHORIZED

## Purpose

This document refines WF-6. It defines the minimum environmental state needed for outdoor places to affect decisions and actions without building a meteorology simulator.

## Core rule

Environment is authoritative world state, not descriptive prompt prose.

The deterministic runtime owns environmental facts. Cognition receives only the locally relevant projection needed for decision-making.

## Environmental scope

V1 is location/region-scoped and may include:
- simulation date/time;
- daylight/daypart;
- ambient temperature;
- weather state;
- precipitation when applicable;
- visibility when applicable;
- exposure class of current/target place.

## Time authority

Simulation time remains the single temporal authority.

Daylight/daypart should be derived deterministically from simulation time and world/location metadata. It should not be independently mutable prose.

A later astronomical model may improve sunrise/sunset precision, but v1 only needs consistent time-aware daylight behavior.

## Weather state

Use a bounded enumerated representation rather than arbitrary text.

Candidate v1 states:
- `clear`
- `cloudy`
- `rain`
- `snow`
- `storm`

The first implementation may support fewer states if required for a minimum runnable exemplar.

Each state may expose compact derived properties such as precipitation and visibility. Avoid duplicating the same fact in several independently mutable fields.

## Temperature

Ambient temperature is numeric authoritative state, scoped to region/location as appropriate.

Indoor locations may inherit or override exterior temperature depending on later facility/HVAC depth, but v1 should avoid simulating room thermodynamics.

## Exposure

Place metadata should distinguish at minimum:
- `indoor`
- `covered_outdoor`
- `outdoor`

Environmental consequence logic reads this exposure rather than guessing from location names.

## Environmental consequence hooks

V1 should provide deterministic hooks, not a universal hazard engine.

Possible first effects:
- influence outdoor action desirability;
- modestly adjust expected travel duration under represented weather;
- expose local conditions to clothing/activity choice;
- gate obviously incompatible activities when a specific contract exists.

Do not infer injury, hypothermia, illness, or disaster mechanics until explicit systems represent them.

## Weather evolution

The first runtime may use a simple deterministic/scheduled producer or persisted authored state. A complex stochastic weather generator is not required for WF-6.

Required invariants:
- weather changes are persisted/auditable world changes;
- initialization does not randomly rewrite production weather without an explicit producer policy;
- cognition cannot mutate weather;
- a state has an effective time or clear current authority.

## Regional versus local state

South Lake Tahoe may provide regional baseline weather. Specific locations may later override local properties when justified.

Do not create a unique weather record for every room or node by default.

## Cognition projection

Only relevant environmental context should be injected:
- current local conditions;
- target conditions when materially different and relevant to an offered action/travel choice;
- compact time/daylight summary.

Do not send historical weather ledgers, all regional weather, or unrelated location conditions.

## First runnable proof

A suitable WF-6 proof is:
1. actor can reach an Estate outdoor node;
2. runtime exposes current time/daylight and one represented weather/temperature state;
3. outdoor cognition sees a compact environment summary;
4. at least one deterministic behavior/action-option or duration hook can consume the environment without direct LLM mutation;
5. returning indoors changes exposure context without rewriting global weather.

## Deferred depth

Not v1:
- forecast models;
- real-time external weather synchronization requirement;
- climate simulation;
- wind physics;
- snow accumulation physics;
- road closures unless separately authored;
- universal injury/hazard engine;
- building HVAC simulation;
- seasonal ecology.

## Dependency relationship

WF-6 depends on meaningful outdoor nodes from WF-4/WF-5. It then supplies environmental context to travel, venue, resource and later world-process systems.