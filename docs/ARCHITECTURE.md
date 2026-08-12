# Observer Sandbox Architecture

## Foundation contract

Observer Sandbox starts deliberately small while preserving stable extension points.

### Logical world model

Every meaningful thing in the sandbox is an entity node. Relationships form edges between entities. Examples include characters, rooms, objects, equipment, food, and later external locations.

### Physical persistence

SQLite stores the graph using relational tables:

- `entities` — node identity, state and capabilities.
- `relations` — typed edges between entities.
- `fields` — rich profile values with mode and update authority.
- `events` — append-oriented simulation history.
- `runtime_state` — pause/speed/world runtime controls.

The first implementation uses SQLite, but domain code must treat persistence through runtime/storage boundaries so a future database change does not alter the world ontology.

## Field modes

A rich profile may contain values before every simulation system exists.

- `canonical` — authoritative facts defined by the profile.
- `static` — represented but not actively simulated.
- `derived` — calculated from other authoritative values.
- `simulated` — actively changed by an enabled domain engine.

Each field records an `authority`. Domain engines must not mutate fields they do not own.

## Runtime rule

The LLM never receives arbitrary database-write authority. An agent proposes a structured action; the runtime validates prerequisites and capabilities, applies state transitions, advances simulation time, records events, and emits observer notifications.

## Module boundary

Future modules such as needs, sleep, physiology, training adaptation, emotion, memory and relationships attach to the core runtime through explicit capabilities, event consumption and field authorities. Core entity identity and relations remain stable.

## Remote operation

GitHub is canonical for code/configuration. GitHub Actions deploys to the VPS over SSH and can read runtime status through `sandboxctl`. The live database remains on the VPS and is not publicly exposed.
