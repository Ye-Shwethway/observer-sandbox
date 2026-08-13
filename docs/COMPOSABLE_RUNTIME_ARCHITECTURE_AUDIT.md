# Composable Runtime Architecture Audit

Status: PROPOSED ARCHITECTURE / PRE-EXPANSION AUDIT

## Goal

Observer Sandbox should grow as a composable universe rather than as a collection of character-specific scripts.

The target runtime expression is:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> validated transition -> State Changes + Events`

This is the project's LEGO-like building rule. New characters, locations, items, relationships, environmental conditions and future simulation modules should plug into this expression without redesigning the core runtime.

## What is already structurally sound

### Entity / relation graph

The generic `entities`, `relations`, and `fields` foundation is a good base. Spatial identity is now globally scoped and recursively composable. `contains` and `connected_to` are already separate.

### Field authority

Canonical/static/derived/simulated modes plus explicit authority are a strong long-term contract. Domain engines can progressively activate fields without giving the LLM arbitrary mutation access.

### Proposal / validation / application boundary

The LLM currently proposes a structured action, while deterministic runtime validates and applies the transition. Preserve this separation permanently.

### Global simulation clock

A single canonical simulation clock is appropriate for one shared universe. Individual actors should schedule work against that clock rather than own separate universe clocks.

## Structural gaps that should be fixed before broad world expansion

### A1 — Actor-scoped runtime scheduling (MUST FIX NOW)

Current scheduler state is stored in singleton runtime keys such as `autonomy_pending_action`, `autonomy_lease`, `autonomy_retry`, cognition wake state and cognition statistics. This works for Darian only but cannot safely represent Darian and Quasi acting concurrently.

Required direction:

- runtime action/pending state must be scoped by actor or runtime-agent id;
- lease/retry/wake telemetry must also be actor-scoped;
- global pause/speed/world-id may remain global;
- multiple actors must be able to have independent pending actions at the same simulation time.

A dedicated runtime table is preferable to dynamically-named global keys once multiple actors exist.

Suggested logical record:

`actor_runtime(actor_id, autonomy_enabled, current_action_id, pending_action_json/ref, retry_state, cognition_state, updated_at)`

The exact physical schema can remain minimal, but do not add the second autonomous character while singleton pending/lease state remains.

### A2 — First-class action instance contract (MUST FIX NOW)

The present action shape is approximately:

`name + duration_minutes + target + reason`

Future composition needs a richer but still compact envelope. An action instance should be able to represent:

- unique `action_id`;
- action type/key;
- primary actor;
- zero or more participants;
- target entity/location;
- optional tool/resource entity ids;
- origin location and intended destination where relevant;
- planned start simulation time;
- duration / planned end simulation time;
- structured conditions/prerequisites snapshot;
- structured modifiers snapshot;
- intent/reason metadata;
- status (`planned|active|completed|cancelled|failed`).

Not every action needs every slot. The envelope exists so future actions compose without changing the scheduler schema.

### A3 — Data-driven action definitions (MUST FIX BEFORE ACTION VOCABULARY GROWS)

Action semantics are currently spread across Python dictionaries and validation branches. Before introducing many more verbs, add a definition layer.

An action definition should describe, where applicable:

- action key and display label;
- duration bounds;
- actor capability requirements;
- target type/capability requirements;
- location/co-location requirements;
- resource/tool requirements;
- base deterministic effects/costs;
- interruptibility;
- concurrency/exclusivity rules;
- tags/categories.

Python engine code should execute generic validation/application primitives. Domain-specific complexity can still live in modules, but the core action vocabulary should not become a large hard-coded switch statement.

### A4 — Conditions and modifiers as first-class inputs (MUST DEFINE NOW, IMPLEMENT IN SLICES)

The target LEGO rule explicitly includes conditional modifiers. Today physiological thresholds are mostly decision guidance and effects are direct numerical deltas.

Define a generic modifier/effect contract capable of representing:

- additive change (`+/- value`);
- multiplicative factor;
- set/clamp;
- temporary modifier with start/end sim time;
- conditional application;
- source entity/action/event;
- stack policy (`stack`, `replace`, `max`, etc.).

Examples:

- Energy Drink: immediate Energy +10, Sleepiness -8, temporary stimulant modifier for 120 simulated minutes;
- injury: training energy cost ×1.25 while injury condition is active;
- night time: sleep effectiveness ×1.10;
- wet clothing/weather later: cleanliness/temperature modifiers.

Do not require every module to use modifiers immediately. Freeze the contract so future effects do not need another schema redesign.

### A5 — Event envelope / causality (MUST FIX BEFORE MULTI-ACTOR STORYLINE EXPANSION)

The current append-oriented event history is useful, but a future universe needs events to be queryable by more than actor and JSON payload.

Future event envelope should support:

- stable event id;
- event type;
- simulation timestamp;
- primary actor;
- participants;
- location;
- action id / causal parent event id;
- target/resource references;
- structured state-change summary;
- visibility/audience metadata later;
- arbitrary payload for domain-specific detail.

This supports scoped history such as "what happened in the gym", "events involving Darian and Quasi", and causal chains without parsing every JSON blob.

### A6 — Definition / instance separation (MUST DEFINE NOW)

The long-term universe needs repeatable types and concrete instances.

Examples:

- definition: `item_def_energy_drink`
- instance/stack: `item_thorne_estate_energy_drink_stack_01`
- definition: `location_template_bedroom` may be optional; concrete rooms remain scoped location instances.

At minimum establish the distinction:

1. **Definitions/Templates** — reusable semantics and defaults.
2. **Instances** — actual entities in the universe.
3. **Runtime State** — mutable state attached to instances.

Do not duplicate the same food/item/equipment effect schema on every physical instance once inventory begins to grow.

### A7 — Ownership / containment / possession semantics (DEFINE BEFORE ITEM BROWSER BECOMES INVENTORY)

`contains` currently works for fixed spatial containment. Future movable items need explicit semantics for:

- located in room/container;
- carried by character;
- equipped by character;
- owned by character/faction/location;
- stored inside another item/container.

Keep ownership separate from current physical location. A Darian-owned object can be temporarily located elsewhere.

Do not overload one relation to mean all of these.

### A8 — Generic location for entities (DEFINE BEFORE MOVABLE OBJECTS/NPCs GROW)

Darian currently uses a `runtime.location` field, while fixture objects use static `contains` relations. This is sufficient for the current mansion but future movable items, vehicles and NPCs need a consistent answer to "where is this entity now?"

Recommended semantic rule:

- static structural containment remains `contains`;
- dynamic presence/location is represented through one generic runtime-location mechanism or explicit `located_at` relation contract;
- choose one authoritative dynamic-location pattern before movable inventory/entities proliferate.

The implementation may retain a field for performance, but the domain contract must be entity-generic rather than character-only.

## Important gaps that can wait until their feature slice

### B1 — Inventory quantities / stacks / durability

Do not build full inventory now. Define it when P2 item browsing begins evolving into actual possession/consumption. Definition/instance and ownership contracts should exist first.

### B2 — Relationship simulation

The normalized relationship table is already a useful placeholder. Rich relationship events, memories and modifiers can wait until a second character is near.

### B3 — Memory

Do not add a large memory subsystem now. Events plus future causal/context metadata should be the durable raw substrate; memory can later derive/select from it.

### B4 — Environment/weather

Do not implement before estate exterior/Tahoe exists. Future environment state should enter actions through the same conditions/modifiers contract.

### B5 — Complex simultaneous/group actions

The action envelope should allow participants now, but synchronization/reservation rules for combat, conversations, shared meals, etc. can be implemented later.

## Recommended canonical runtime pipeline

1. **Observe** — collect actor state, place, global sim time, nearby entities/resources, relevant conditions/modifiers and recent events.
2. **Propose** — AI or deterministic policy proposes one structured action instance.
3. **Resolve Options** — runtime derives legal action options from definitions, capabilities, topology and state.
4. **Validate** — check actor/target/location/resource/time/condition prerequisites.
5. **Reserve/Schedule** — assign action id, start/end sim time and actor-scoped pending state.
6. **Complete/Interrupt** — deterministic engine applies effects using the conditions/modifiers snapshot and current interruption rules.
7. **Commit State** — update authoritative fields/relations atomically.
8. **Emit Event** — append the action/event envelope plus state-change summary and causal references.
9. **Notify/Observe** — Telegram/query surfaces consume committed state/events downstream; they never become simulation authority.
10. **Wake Next Mind** — only actors reaching a real decision boundary wake cognition.

## LEGO composition examples

### Drinking water

`Darian + Drink + Kitchen + 1:30 PM + local Drinking Water available -> thirst reduction + time advance + event`

### Energy drink later

`Darian + Drink + Kitchen + 3:00 PM + Energy Drink instance + not depleted -> immediate stats + temporary stimulant modifier + inventory decrement + event`

### Two-character conversation later

`Darian + Talk + Quasi + Living Room + 8:10 PM + both present/available -> relationship/emotion/memory candidate effects + shared event references`

### Training with injury later

`Darian + Train + Heavy Bag + Home Gym + 10:00 AM + shoulder injury modifier -> higher cost / restricted options / injury-sensitive effects`

The same runtime pipeline handles each case; only definitions, conditions and effect handlers differ.

## Recommended pre-expansion hardening sequence

Before broad South Lake Tahoe or second autonomous-character expansion:

1. **C1 Actor-scoped runtime state** — remove singleton-character scheduler assumption.
2. **C2 Action envelope + action-definition registry** — establish generic action identity and validation metadata.
3. **C3 Conditions/modifiers/effect contract** — support source, duration and stack semantics without necessarily implementing every modifier type yet.
4. **C4 Event envelope + causal/location references** — make history universe-queryable.
5. **C5 Definition/instance + possession/location semantics** — enough foundation for future item browsing/inventory.
6. Run fresh-DB and legacy-development migration tests plus accelerated autonomy acceptance.
7. Resume P2.2 Telegram Estate Browser on the hardened query contracts.

This is intentionally a bounded foundation pass, not a Simiverse/EIDOLON-scale engine rewrite.

## Schema guidance

The current physical SQLite v3 graph tables remain useful, but the audit finds that future multi-actor scheduling and queryable events likely justify a small schema revision rather than continuing to pack all runtime structures into singleton `runtime_state` JSON keys.

Prefer a small number of generic tables/contracts over one table per feature. Candidate additions are actor runtime/action records and normalized event references/modifiers only where JSON would prevent reliable validation/querying.

Do not add tables merely to mirror every domain concept. Keep the logical LEGO model richer than the physical schema where JSON/typed relations remain sufficient.

## Decision boundary

This audit does **not** authorize broad feature implementation by itself. It identifies the contracts that should be locked before universe expansion. Once approved, perform the hardening as one bounded pre-expansion architecture slice, then return to P2.2.