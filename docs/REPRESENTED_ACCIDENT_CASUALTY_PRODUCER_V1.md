# Represented Accident Casualty Producer v1

Status: implemented exemplar

## Purpose

Provide the first legitimate producer of the casualty lifecycle state without introducing a general Injury Engine or inferring medical state from narrative prose.

Canonical path:

`typed represented accident -> explicit casualty-role source event -> casualty lifecycle initialization -> simulated medical.deterioration_risk`

## V1 scope

Implementation: `src/observer_sandbox/represented_accident_casualty.py`.

V1 proves exactly one accident kind:

- `represented_fall`

Finite abstract risk classes map deterministically to deterioration risk:

- `low` -> `25`
- `moderate` -> `50`
- `high` -> `75`

These values are simulation pressure classes only. They do not encode a wound diagnosis, injury taxonomy, treatment recommendation, incapacity, or death state.

## Required contract

`record_represented_accident_casualty(...)` requires:

- caller-provided stable `incident_id` for retry identity;
- an existing represented character casualty;
- an existing spatial location;
- the casualty's current dynamic location exactly matches the declared accident location;
- explicit simulation time;
- one finite accident kind;
- one finite risk class.

No free-form accident narrative is accepted by the producer API.

## Event and state semantics

The producer first emits `represented_accident_occurred` with the character explicitly bound as event participant role `casualty`.

That source event contains structured accident identity/classification only and records:

- `injury_created: false`
- `diagnosis_created: false`
- `incapacity_created: false`
- `learning_evidence: false`

The source event itself performs no state mutation.

The producer then calls the canonical `initialize_casualty_state(...)` lifecycle API with origin kind `represented_accident`. The lifecycle API remains the only owner of creating `medical.deterioration_risk` and emits the causal `casualty_state_initialized` event.

## Atomicity and retries

The source event and lifecycle initialization share one SQLite savepoint. If lifecycle initialization fails, the accident source event is rolled back as well.

`incident_id` is retry identity. Repeating the same incident with identical semantics returns the existing source/lifecycle evidence without creating a second state transition. Reusing the same incident id with conflicting casualty/location/accident/risk semantics fails closed.

## Boundaries

This exemplar does not add:

- autonomous random accidents;
- probability tables;
- generic hazard simulation;
- wounds or bleeding;
- diagnosis;
- definitive treatment;
- death/incapacity;
- automatic deterioration or recovery;
- controlled-H2H injury generation;
- Weapons consequences;
- Field Medicine XP;
- production casualty fixtures or forced live accidents.

Follow-on accident/environmental producers should reuse this proven typed-source-event -> lifecycle pattern rather than growing this module into a universal hazard engine.
