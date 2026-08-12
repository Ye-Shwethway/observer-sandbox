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

## AI provider layer

AI model IDs are never hard-coded into character or engine logic. The runtime stores provider catalogs and resolves bindings by scope and role.

Built-in provider adapters currently include Google Gemini, NanoGPT, OpenAI and OpenRouter. Provider credentials are referenced by environment-variable name and are never stored as plaintext API keys in the database.

Model binding precedence is:

1. task + role
2. character + role
3. engine + role
4. character default
5. global + role
6. global default

This lets future characters and simulation engines use different models without changing their implementation.

### NanoGPT subscription-first behavior

NanoGPT is a first-class adapter rather than a generic placeholder. Its default base URL is `https://nano-gpt.com/api`.

Observer Sandbox intentionally refreshes the NanoGPT text catalog from the subscription-only endpoint (`/subscription/v1/models?detailed=true`). This prevents a normal catalog refresh from presenting pay-as-you-go-only models as if they were covered by the subscription. The raw detailed model metadata and capabilities are retained in the catalog cache.

Subscription status and remaining usage can be read from `/subscription/v1/usage` through `sandboxctl ai nanogpt-usage` once `OBSERVER_NANOGPT_API_KEY` is provisioned on the VPS.

NanoGPT also exposes canonical, paid-only and personalized model catalogs. These may be surfaced later as explicit Telegram catalog filters, but the default Observer Sandbox path remains subscription-safe unless the Creator deliberately opts into paid routing.

Do not set NanoGPT's explicit upstream-provider selection header for ordinary subscription traffic: NanoGPT documents that explicit provider selection switches that request to pay-as-you-go billing. The generation adapter must preserve subscription routing by default.

## Remote operation

GitHub is canonical for code/configuration. GitHub Actions deploys to the VPS over SSH and can read runtime status through `sandboxctl`. The live database remains on the VPS and is not publicly exposed.
