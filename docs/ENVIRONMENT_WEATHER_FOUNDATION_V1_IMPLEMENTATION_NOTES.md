# Environment / Weather Foundation v1 — Implementation Notes

Status: implementation companion to `ENVIRONMENT_WEATHER_FOUNDATION_V1.md`.

This note records the concrete W1 runtime shape so future producers and Mind consumers can extend it without reversing the authority boundaries.

## Current files

- `src/observer_sandbox/environment_schema.py` — environment persistence schema v1.
- `src/observer_sandbox/environment_weather.py` — generic environment state, applicability, W0 publication and direct-outdoor exposure APIs.
- `tests/test_environment_weather_foundation_v1.py` — focused contract coverage.

## Current runtime boundary

W1 is deliberately source-neutral. No production weather API, stochastic generator or default weather seed is installed.

A producer supplies an authoritative `environment_state`; W1 can then:
1. resolve it by represented location containment;
2. publish its direct ambient surface as W0 `environmental` stimuli scoped only to explicit outdoor locations;
3. record direct character exposure only when the actor is represented at one of those outdoor locations.

Indoor locations may resolve geographic environment truth for future mediated consumers, but they are not direct ambient exposure locations.

## Extension sockets

Future modules should extend the existing path rather than create a second weather feed:

- authoritative live/seed/generator producer -> `record_environment_state`
- direct ambient publication -> `publish_environment_stimulus`
- direct outdoor exposure -> `record_outdoor_environment_exposure`
- future perception/Mind handoff -> consume W0 exposures, not `environment_states` globally

Future phone/TV/internet forecast or alert systems are information/media producers. They should retain source provenance to weather data where appropriate but use represented devices/network access and W0 delivery/exposure.

## Compatibility rule

Do not change `world.spatial_container.exposure` semantics merely for weather. W1 consumes that existing spatial contract. New semi-outdoor categories, windows, sheltered structures, vehicles or HVAC should receive explicit world representation and an intentional exposure model when those features are implemented.
