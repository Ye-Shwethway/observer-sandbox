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
- `ai_providers` — provider registry and adapter configuration.
- `ai_models` — fetched/cached model catalog.
- `ai_bindings` — model assignment by global, character, engine or task scope.
- `ai_catalog_sync` — provider catalog refresh status.

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

## AI provider layer

Model identifiers are never hard-coded into character or engine code. Runtime AI selection is resolved through four boundaries:

1. **Provider registry** — provider identity, adapter type, endpoint and credential reference.
2. **Model catalog** — models are fetched from provider APIs and normalized into a local cache.
3. **Model bindings** — a selected model is attached to a runtime scope and role.
4. **Provider adapters** — provider-specific transport stays behind a common runtime interface.

Built-in provider definitions initially include Gemini, OpenAI, OpenRouter and NanoGPT. NanoGPT intentionally has no assumed base URL until its deployment/API contract is configured. Additional OpenAI-compatible providers can use the same adapter contract.

Credentials are not stored in SQLite. `credential_ref` names an environment variable on the VPS, such as `OBSERVER_GEMINI_API_KEY`. Telegram and runtime controls may select providers/models but should never display or persist plaintext API keys in normal state.

### Binding precedence

The current resolver chooses the most specific enabled binding in this order:

1. task + role
2. character + role
3. engine + role
4. character default
5. global + role
6. global default

This permits one model for Darian cognition, a different model for a future memory engine, and task-specific overrides without changing character profiles or engine implementations.

P0.5 implements provider/catalog/binding infrastructure only. Automatic provider fallback and arbitrary hot failover are intentionally deferred until runtime behavior is observable and failure semantics are defined.

## Module boundary

Future modules such as needs, sleep, physiology, training adaptation, emotion, memory and relationships attach to the core runtime through explicit capabilities, event consumption and field authorities. Core entity identity and relations remain stable.

## Telegram control boundary

Telegram is an observer/admin interface, not the source of truth. Future Telegram controls call the same provider/catalog/binding services used by `sandboxctl`. Expected controls include provider enable/disable, catalog refresh, model browsing and binding selection per character/engine/role.

## Remote operation

GitHub is canonical for code/configuration. GitHub Actions deploys to the VPS over SSH and can read runtime status through `sandboxctl`. The live database remains on the VPS and is not publicly exposed.
