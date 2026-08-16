# Character Memory Foundation v1

Status: ACTIVE FOUNDATION CONTRACT

## Purpose

Introduce a generic actor-owned memory layer that can persist represented experience and knowledge, retrieve bounded relevant context for cognition, and expose live memory state through the Telegram observer.

This foundation is intentionally smaller than a full human-mind simulator. It establishes the schema and runtime seams needed for later consolidation, forgetting, reflection and planning without replacing current world, event, profile, physiology, autonomy or action authority.

## Core separation

Preserve four distinct authorities:

1. **World / event truth** — objective represented facts and completed events.
2. **Character memory / knowledge** — what a character has encoded or is initialized to know.
3. **Cognition / planning context** — the bounded subset of memory retrieved for the present decision.
4. **Current action authority** — exact deterministic actions/targets available now.

Canonical rule:

> Events say what happened. Memory says what this actor retained or knows. Cognition retrieves only what is relevant. Action options remain the execution authority.

Memory must never grant teleportation, access, topology, inventory, capability or any other authority that is absent from deterministic runtime state.

## Universal autonomy invariant

Memory is character-owned state, not character-specific behavioral policy.

Allowed character-specific content includes factual experience, learned knowledge, relationships, places known, possessions remembered, observations and established history.

Forbidden:
- named-character behavior instructions;
- routines disguised as memories;
- `Darian should train/rest/go outside` style records;
- destination quotas or anti-repetition commands;
- memory rows that bypass generic cognition or deterministic validation.

A new character must use the same memory schema, encoding rules, retrieval APIs and cognition interfaces.

## V1 memory types

### Episodic

A represented experience associated with simulation time and usually traceable to an event.

Examples:
- a completed training session;
- a meal or shower;
- a visit/move;
- a rest, walk, observation or other completed represented action;
- later, meaningful interactions, injuries, discoveries or conversations.

V1 automatically encodes completed actor actions. This is deliberately broad but compact: one structured memory per completed action rather than a prose copy of the entire event payload.

### Semantic

Stable represented knowledge owned by the character rather than an objective world record.

Examples:
- known locations and spatial familiarity;
- learned facts about entities, resources or relationships;
- later, consolidated facts derived from repeated episodes.

V1 schema supports semantic records. Migration of the temporary Darian spatial-familiarity bootstrap is the next bounded migration consumer and must preserve the existing world-truth / actor-known-world / action-authority separation.

## Schema contract

`character_memories` stores one actor-owned memory record with:

- `memory_id` — stable technical identity;
- `character_id` — owning character;
- `memory_type` — `episodic` or `semantic` in v1;
- `summary` — concise human/model-readable memory summary;
- `content_json` — structured bounded payload;
- `source_type` — provenance category such as `event`, `seed`, `consolidation`;
- `source_event_id` — optional event provenance;
- `event_sim_time` — represented occurrence/knowledge time;
- `encoded_sim_time` — when memory entered actor state;
- `salience` — normalized 0..1 importance signal;
- `confidence` — normalized 0..1 actor knowledge confidence;
- `status` — lifecycle state, initially `active`;
- `last_recalled_sim_time` — most recent cognition retrieval time;
- `recall_count` — bounded observability counter;
- `metadata_json` — extensibility without schema churn.

`character_memory_entities` associates memories with represented entities/locations/targets for deterministic relevance filtering.

## Encoding v1

Completed actor actions are encoded after the authoritative event has been inserted.

Encoding rules:
- event truth remains the provenance source;
- one event must not create duplicate actor memories;
- summary/content are derived from structured event fields, not invented narrative;
- location and target references are associated when represented;
- salience is generic and action-category based in v1, not identity based;
- encoding failure must fail the transaction rather than silently desynchronize event and memory state.

V1 salience is intentionally simple. Later versions may incorporate novelty, emotional/physiological impact, relationship relevance, goal relevance and reinforcement.

## Retrieval v1

Cognition receives a bounded `relevant_memories` projection, never the full memory store.

Initial deterministic ranking combines:
- recency in simulation time;
- stored salience;
- current-location association;
- current reachable/target entity associations where available;
- action-category relevance to current options where represented.

V1 keeps retrieval cheap and explainable and does not require a vector database. Semantic/vector retrieval may be added later only when current scale demonstrates a concrete need.

Retrieval updates `last_recalled_sim_time` and `recall_count` only for memories actually injected into cognition.

## Dynamic lifecycle

Memory is dynamic state, not a static profile section.

V1 implements:
`experience -> encode -> retrieve -> recall metadata`

Schema reserves clean extension points for:
`reinforcement -> consolidation -> reconsolidation -> fading/retirement`

Forgetting/consolidation are intentionally deferred until there is evidence for the correct policy. V1 does not fake them with arbitrary timers.

## Cognition integration

Memory enters model cognition as a compact actor-relative section:

`relevant_memories: [{memory_id, type, sim_time, summary, salience, confidence, related_entities}]`

The model may use those memories to reason about recent experience and known facts, including multi-day history. It may not treat memory as action authority.

The existing recent-event window remains useful as immediate objective context during migration. Memory is the durable actor-owned layer and future planning should increasingly consume memory rather than accumulating bespoke history proxies.

## Telegram observer UX

Memory is a character-level dynamic surface, parallel to Profile and Cognition Context.

Character menu:
- `📖 Profile`
- `🧠 Memory`
- owner-only `🧠 Cognition Context`

Memory view is a live database query, not a snapshot:
- active total;
- episodic count;
- semantic count;
- latest encoded simulation time;
- paginated recent memories.

Each memory row exposes concise type/time/summary/salience/recall metadata. The Telegram surface is read-only and never mutates memory.

Observability distinction:
- **Memory** answers: `What does this character currently remember/know?`
- **Cognition Context** answers: `What context was actually injected for this model decision?`

This separation allows debugging whether a memory exists, whether retrieval selected it, and whether cognition used it.

## Spatial-familiarity migration

`config/characters/darian.spatial_familiarity.v1.json` remains temporary only until the generic semantic-memory bootstrap migration is completed.

Migration requirements:
1. preserve all valid initial represented spatial knowledge;
2. preserve `unknown -> aware -> familiar -> intimate` vocabulary;
3. preserve concealed/secret knowledge independently from familiarity;
4. keep world truth and current move authority separate;
5. remove the Darian-specific file and loader/path dependency after equivalence is verified;
6. do not replace it with another named-character cognition/behavior file.

## Planning boundary

V1 does not implement a daily planner, weekly schedule or full Mind System.

It creates the durable substrate needed for the next bounded planning foundation:

`profile/state + physiology + environment + affordances + goals + relevant memories -> intention/plan -> local action execution`

First intended planning consumers are:
- multi-day training/recovery balance without fixed rest-day schedules;
- purposeful destination + activity selection across represented Estate space without outdoor quotas.

## Acceptance

V1 is accepted when:
- schema migration is idempotent;
- completed actions create actor-owned episodic memories exactly once;
- retrieval is bounded and character-scoped;
- cognition receives relevant memory context without changing action authority;
- recall metadata updates only for retrieved records;
- Telegram Character exposes a live read-only Memory view;
- no character-specific behavior rule is introduced;
- existing autonomy/action/event behavior remains compatible.
