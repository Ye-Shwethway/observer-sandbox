# Sandbox Runtime Readiness Foundation v1

Status: **IMPLEMENTATION CONTRACT**
Date: 2026-08-19

## Purpose

A Creator-created Character must not become autonomous merely because its profile object exists.

Creation, configuration, runtime readiness and execution are separate lifecycle boundaries.

Canonical rule:

`created -> configured -> runtime_ready -> running -> stopped`

The Creation Sandbox remains isolated from the canonical Real World at every stage.

## Core principle

> **Created is not alive. Runtime readiness must be earned by complete local dependencies.**

A sandbox Character may be inspected, edited, reset or deleted while incomplete.

It may enter `runtime_ready` only when all minimum runtime dependencies are represented and valid.

## Minimum readiness gates

A sandbox Character requires:

1. an active sandbox Character object;
2. an active sandbox Location assignment inside the same sandbox;
3. at least one represented runtime/action option produced by sandbox elements, capabilities or approved shared systems;
4. an explicit sandbox cognition AI binding;
5. a configured sandbox clock/runtime namespace.

If any gate is missing, start/run must fail closed with structured unmet requirements.

## AI model architecture

The canonical AI provider/model catalog is shared infrastructure.

Assignments are scope-owned.

Real World already supports character-scoped bindings in the canonical `ai_bindings` resolution chain.

Creation Sandbox must not store sandbox Character assignments as ordinary canonical character bindings.

Use sandbox-owned binding state:

`shared provider/model catalog -> sandbox character binding -> sandbox cognition runtime`

This preserves:
- provider/model catalog reuse;
- independent model selection per sandbox Character;
- no canonical character-binding contamination;
- clean delete/reset semantics with sandbox lifecycle.

Minimum sandbox role is `cognition`.

Future roles may include dialogue, planning, memory summarization or specialist engines without changing the ownership boundary.

## Time/runtime isolation

Canonical Real World clock, pause and speed currently live in canonical runtime state and must not control the Creation Sandbox.

Each sandbox namespace owns its own:
- simulation time;
- speed multiplier;
- paused state;
- pause start wall time;
- runtime status.

Therefore:

`Real World /speed` must never change Sandbox World speed.

`Sandbox World speed/pause/resume` must never change canonical Real World runtime state.

The initial Creation Sandbox uses one clock per sandbox namespace, not one clock per Character. Characters sharing a sandbox therefore share temporal reality.

Future separate universes may each own a distinct runtime clock through the same pattern.

## Runtime options / affordances

A Character needs something valid to do before autonomy can be enabled.

The readiness layer stores/reads represented sandbox runtime options separately from canonical action options.

Options are not invented merely to satisfy readiness.

They must come from represented sandbox content or approved shared system adapters, for example:
- location affordances;
- usable elements/items;
- character capabilities;
- approved universal actions such as idle/rest when the target runtime explicitly exposes them.

The readiness gate checks for available options; later vertical slices expand how those options are derived.

## Runtime controls

Sandbox controls are namespace-specific.

Minimum service operations:
- configure initial sandbox time;
- set sandbox speed;
- pause sandbox;
- resume sandbox;
- inspect sandbox runtime status.

Do not route these operations through canonical `runtime_state`.

Telegram should surface Sandbox Runtime separately under Sandbox World.

Command semantics must remain unambiguous. Until a persistent Telegram world-context selector exists, canonical `/speed`, `/pause`, `/resume` retain Real World semantics; sandbox controls should use explicit sandbox-scoped callbacks/commands rather than silently reinterpreting canonical commands.

## Activation

`start sandbox Character` performs readiness evaluation first.

It must not:
- insert the Character into canonical `entities`;
- register it in canonical `actor_runtime`;
- create canonical events;
- consume canonical runtime time;
- use canonical location graph membership.

This foundation may establish `runtime_ready` state before full sandbox autonomy execution exists.

Full autonomous sandbox ticking must reuse shared engine semantics only after adapters can read sandbox-owned character/location/state safely.

## Real World follow-up

The underlying canonical AI resolver already supports character-specific overrides.

A later Telegram UX refinement should expose explicit Real World per-character AI assignment instead of presenting Character AI as if only one global selection exists.

This is a UI/configuration exposure gap, not a need to rebuild the canonical resolver.

## Acceptance

Minimum acceptance must prove:
- sandbox and canonical clocks can hold different times;
- sandbox speed/pause changes do not mutate canonical `runtime_state`;
- sandbox Character AI binding is independent from canonical character/global bindings;
- incomplete Character readiness reports exact missing gates;
- Character cannot become `runtime_ready` without Location + options + cognition model + clock;
- once all gates exist, readiness becomes true without canonical mutation;
- sandbox reset/delete removes its runtime/binding state cleanly.

## Non-goals

This slice does not yet implement:
- full sandbox autonomous action execution;
- full item/element creation sockets;
- quests/jobs runtime;
- canonical transmigration;
- a second production Character;
- multi-universe runtime scheduling.
