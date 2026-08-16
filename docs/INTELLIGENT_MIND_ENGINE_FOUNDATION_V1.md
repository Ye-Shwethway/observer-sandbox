# Intelligent Mind Engine Foundation v1

Status: **CANONICAL FOUNDATION CONTRACT**

## Purpose

Establish the stable architectural and schema foundation for character mental processing without prematurely implementing a giant human-mind simulator.

The Mind Engine is broader than action selection or planning. It is the shared character-owned runtime through which future perception, attention, thought, affect, active concerns, intention, planning, social cognition, communication and relationship-appraisal systems must interoperate.

This foundation intentionally creates durable sockets and boundaries first. Future modules may be implemented incrementally, but they must align to this contract rather than inventing parallel cognition stores or bypass paths.

## Canonical alignment rule

**Every future system that can materially influence a character's internal cognition, interpretation, intention, social response or planning MUST read this Mind Engine contract before implementation and MUST integrate through the defined Mind Engine sockets or explicitly document why it is outside mental cognition.**

This rule applies especially to future:
- perception and sensory-context systems;
- weather/environment appraisal;
- economy/money concerns;
- media/information exposure;
- affect/emotion;
- spontaneous thought and reflection;
- goals and active concerns;
- intention and planning;
- social cognition;
- communication/dialogue;
- relationship appraisal/adaptation;
- commitments/schedules/obligations;
- future learning/reflection systems.

A subsystem must not create a competing hidden `mind`, `thought`, `planner`, `relationship reasoning`, or cognition-state store when the state belongs to this architecture.

## Core authority separation

Preserve these distinct layers:

1. **World / event truth** — objective represented simulation facts and events.
2. **Perceived information** — what information reached the actor through an implemented perception/exposure channel.
3. **Character memory** — actor-owned retained experience/knowledge and its current recallability.
4. **Mind state / mental processing** — what is currently mentally active, interpreted, evaluated or considered.
5. **Intention / planning** — future-directed mental artifacts that may influence later choice.
6. **Decision proposal** — the structured next-action proposal produced by cognition.
7. **Action authority** — deterministic legal action options and validation.
8. **Action / world mutation** — authoritative runtime effects and resulting events.

Canonical rule:

`world truth != perception != memory != thought != intention/plan != action proposal != action authority`

No mental artifact grants topology, possession, capability, resources or actions absent from deterministic state.

## Why the existing Cognition Context remains separate

The current Cognition Context inspector is valuable but raw. It records the compact context injected into a model decision. It is an observability surface, not the character's represented mind.

Do not reinterpret raw prompt context as mental state.

Future relationship:

`authoritative world/profile/state + perception + currently recallable memory + active mind artifacts -> cognition call -> structured mental cycle outputs + action proposal`

Cognition Context continues to answer:
> What did the model receive for this decision?

The Mind Engine answers:
> What represented internal mental activity/state belongs to this character?

## Foundation model

The minimum stable hierarchy is:

### 1. Mental Cycle

A bounded mental-processing boundary for one character at one represented simulation time.

A mental cycle may be triggered by:
- decision wake;
- action start/completion;
- communication received;
- salient world/perception event;
- future scheduled mental wake;
- explicit deterministic subsystem trigger.

A cycle is not automatically an LLM call. Future deterministic modules may also contribute through the same envelope.

### 2. Mental Episode

A bounded unit of represented thought or mental processing within a cycle.

Initial canonical modes:
- `task_focused` — attention on the current task/action;
- `spontaneous` — unconstrained or associative thought;
- `reflective` — consideration of past experience/self-state;
- `prospective` — future-oriented thought that is not yet a formal plan;
- `social` — thought about another actor or social situation;
- `evaluative` — appraisal/comparison/judgment.

These are extensible vocabulary, not six separate engines.

### 3. Mental Artifact

A persistent or semi-persistent actor-owned item that can survive beyond one mental cycle.

The foundation supports typed artifacts so future modules do not need new parallel stores.

Reserved canonical artifact types:
- `concern` — unresolved/currently significant issue;
- `goal` — desired future state;
- `intention` — near-term commitment/direction;
- `plan` — structured future-directed representation;
- `social_inference` — actor-relative interpretation about another entity;
- `appraisal` — interpreted significance of a perceived fact/event;
- `working_item` — temporary active working-memory content.

Foundation v1 does **not** implement the behavior/dynamics for all reserved types. It only defines their common storage/socket contract.

### 4. Typed Links

Mental cycles, episodes and artifacts may link to represented:
- memories;
- events;
- entities;
- locations;
- actions/action instances;
- other mental artifacts.

Links preserve provenance and allow future retrieval without copying world or memory truth into mental text blobs.

## Socket-style architecture

Future modules integrate through stable conceptual sockets.

### Input sockets

A mental-processing module may receive only represented data appropriate to its purpose, such as:
- `present_state`
- `profile_traits`
- `physiology`
- `current_action`
- `perception`
- `currently_recallable_memories`
- `active_mental_artifacts`
- `relationships`
- `goals`
- `world_context`
- `communication_context`

The exact payload should remain bounded and purpose-specific. Do not dump all world, memory or history state into every module.

### Output sockets

A module may emit typed results such as:
- `mental_episode`
- `artifact_create`
- `artifact_update`
- `artifact_resolve`
- `intention_candidate`
- `plan_candidate`
- `social_inference`
- `action_proposal`

Outputs are structured proposals/mental state. They do not mutate arbitrary world state.

## Canonical envelope

The runtime-facing contract should support a versioned envelope conceptually equivalent to:

```json
{
  "schema_version": 1,
  "character_id": "...",
  "sim_time": "...",
  "trigger": {
    "type": "decision_wake",
    "source_id": null
  },
  "inputs": {
    "present_state": {},
    "perception": [],
    "recall": [],
    "active_artifacts": []
  },
  "outputs": {
    "episodes": [],
    "artifact_mutations": [],
    "action_proposal": null
  }
}
```

The exact compact payload may evolve, but versioning and layer separation are mandatory.

## LLM-call policy

The Mind Engine must not require continuous LLM polling to represent continuous existence.

Preferred model:
- bounded mental cycles at meaningful runtime boundaries;
- one cognition call may generate an action proposal plus a small bundle of mental episodes likely to occur during the represented action interval;
- future deterministic/background settlement may maintain persistent artifacts without generating prose every simulated minute.

A 30-minute action does not require 30 thought calls.

Mental episodes are temporal compression of meaningful internal activity, not a transcript of every millisecond of consciousness.

## Thought versus memory

Thought and memory are separate.

- recalling an existing memory may generate a mental episode;
- a mental episode may reinforce an existing memory;
- a novel realization may later become semantic memory through a future reflection/learning module;
- most transient thoughts should not automatically become durable memories.

No module may treat every generated thought as a new permanent memory by default.

## Thought versus planning

Prospective thought is not automatically a plan.

Examples:
- `I wonder whether I should train later` -> prospective mental episode;
- `I intend to recover today` -> intention artifact;
- `Recover this morning, eat lunch, then perform light mobility` -> plan artifact.

Planning is a future module layered on top of the common mind substrate.

## External world factors

Weather, money, media, social information and other world systems must not directly apply arbitrary mental modifiers such as `rain -> mood -5` or `low cash -> anxiety +10`.

Preferred flow:

`external represented fact -> perception/exposure -> character-relative appraisal -> mental episode/artifact/affect -> possible intention/action`

This preserves individual differences and prevents world systems from becoming hidden behavior scripts.

## Social cognition / communication direction

Future communication must use the Mind Engine rather than direct chatbot ping-pong.

Target flow:

`utterance/event -> perception -> memory/person-context retrieval -> appraisal/social inference -> internal mental episode -> relationship-relevant interpretation -> response intention -> utterance proposal`

Relationship state changes should be driven by represented interpreted social evidence rather than arbitrary direct dialogue-to-trust increments.

The relationship engine remains a separate domain owner of relationship state; the Mind Engine owns the internal interpretation artifacts feeding it.

## Schema foundation

Foundation v1 introduces character-owned persistence for:

### `mental_cycles`
Tracks one bounded mental-processing cycle and its trigger/provider/runtime metadata.

Required conceptual fields:
- cycle id;
- character id;
- simulation time;
- trigger type/source;
- status;
- schema version;
- provider/model metadata when applicable;
- bounded input/output metadata;
- timestamps.

### `mental_episodes`
Tracks represented thought units within a cycle.

Required conceptual fields:
- episode id;
- cycle/character;
- mode;
- summary/content;
- importance;
- valence;
- activation/arousal;
- persistence;
- status;
- simulation-time interval;
- metadata.

### `mental_artifacts`
Shared extensible persistence for concerns/goals/intentions/plans/social inferences/appraisals/working items.

Required conceptual fields:
- artifact id;
- character;
- artifact type;
- title/summary/content;
- priority/activation;
- confidence;
- status;
- created/updated/resolved simulation times;
- metadata.

### `mental_links`
Typed provenance/association edges from cycles, episodes or artifacts to memories/events/entities/actions/other artifacts.

The database schema must remain generic. Character identity must never select a different mental schema or algorithm.

## Mental artifact lifecycle

Foundation states are intentionally generic:
- `active`
- `dormant`
- `resolved`
- `retired`

A future module owns transition semantics for its artifact type.

Do not invent generic timers such as "all concerns expire after 3 days".

## Working memory

Character Profile already contains `memory.working_memory`.

Foundation v1 reserves `working_item` mental artifacts for later active-context capacity logic, but does not yet impose a numerical slot limit or simulate every working-memory operation.

When implemented, working-memory dynamics should reference the existing Memory Ability profile rather than creating a second incompatible memory-capacity stat.

## Determinism and authority

The foundation schema does not make LLM prose authoritative.

- mental records are actor-owned simulation state;
- structured validators should validate enums, ownership and links;
- world mutation continues through deterministic action/runtime services;
- future plan/intention records may influence cognition but cannot bypass action validation;
- Telegram remains observer/control, never mind-state authority unless an explicit future Creator-control contract is approved.

## Observability direction

Future Telegram character surfaces should eventually distinguish:
- Profile — represented character facts;
- Memory — retained knowledge/experience;
- Mind — structured current/recent mental episodes and active artifacts;
- Cognition Context — raw actual model-injection snapshots.

Foundation v1 does not require a full Telegram Mind browser yet. It only requires schema/API readiness so one can be added without redesigning persistence.

## Implementation phases after foundation

Recommended sequence after Foundation v1:

1. **World Input Foundations** — minimum perception-ready weather/environment, economy/money, media/information and communication exposure channels as needed.
2. **Mental Episode Runtime** — generate/store bounded thought bundles during cognition cycles.
3. **Attention / Appraisal / Active Concerns** — small shared state above raw prompt context.
4. **Intention Foundation** — near-term future direction.
5. **Planning** — multi-step plans using currently recallable memory and authoritative present state.
6. **Social Cognition / Communication** — interpretation-before-response workflow.
7. **Relationship adaptation** — consume represented social evidence and appraisals.

This order is guidance, not a requirement to finish every world system before any mental runtime work. New world systems should expose clean perception/appraisal inputs rather than bypass the Mind Engine.

## Non-goals of Foundation v1

Do not implement in this slice:
- a full planner;
- continuous LLM thought streaming;
- artificial consciousness claims;
- complete emotion psychology;
- false memories;
- dreams;
- detailed theory-of-mind simulation;
- direct relationship adaptation;
- full weather/economy/media systems;
- hidden character-specific mental scripts;
- a giant monolithic `mind_engine.py` containing all future cognition logic.

## Acceptance

Foundation v1 is accepted when:
- this architecture is canonical;
- AGENTS/roadmap/bootstrap require future cognition-affect-planning-social systems to reference/align with it;
- schema provides generic mental cycles, episodes, artifacts and typed links;
- schema migration is idempotent and character-generic;
- a small runtime contract/API can create/read the foundation records without choosing behavior;
- memory/world/action authority boundaries remain intact;
- no character-specific behavior is introduced;
- existing cognition/action runtime behavior remains unchanged unless explicitly exercised through a future Mind runtime slice.
