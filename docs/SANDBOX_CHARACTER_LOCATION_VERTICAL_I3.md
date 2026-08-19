# Sandbox Character + Location Vertical Proof I3

Status: IMPLEMENTATION CONTRACT
Date: 2026-08-19

## Purpose

Prove that a Creator-staged Character and Location can become richly represented and reach `runtime_ready` without creating canonical universe rows or starting full sandbox autonomy.

## Shared vocabulary, isolated state

Sandbox Character profile values use the canonical `profile_field_definitions` registry for field keys, domains, units, default modes and sensitivity metadata.

Sandbox values are stored only in `creation_sandbox_profile_values`.
Sandbox skills use the same record shape as canonical Character skills but are stored only in `creation_sandbox_character_skills`.

No sandbox Character receives a `character_profiles`, `character_profile_values`, `character_skills`, `entities`, `fields`, canonical `actor_runtime`, canonical `events`, or canonical `ai_bindings` row.

## Character minimum representation

I3 supports:
- identity/profile fields already present in canonical profile vocabulary;
- Body measurements and other represented profile domains through the shared registry;
- represented initial skills through isolated sandbox skill rows;
- Character capability declarations that can expose supported action affordances.

Unknown profile fields fail closed. New concepts such as supernatural powers must use a future dedicated socket/system vocabulary rather than smuggling arbitrary fields into Character profile data.

## Location minimum representation

I3 supports:
- Location identity/properties from the universal creation envelope;
- Location capabilities;
- sandbox-only parent/containment through `contains` relations;
- one parent per child Location in the minimum proof;
- cycle rejection.

No sandbox Location is inserted into the canonical world graph.

## Affordance projection

Runtime options are no longer required to be manually invented for the vertical proof.

`refresh_sandbox_runtime_options()` deterministically projects currently represented Character + current Location capabilities into action options, limited to the canonical `ACTION_NAMES` vocabulary.

Current sources:
1. Character capabilities;
2. current sandbox Location capabilities.

Future Item/Element/System sockets extend the derivation sources rather than bypassing this projection boundary.

Unsupported capability names are not silently converted into executable actions.

## Runtime readiness

I3 does not start sandbox autonomy.

A Character may reach `runtime_ready` when I2.5 readiness gates pass:
- Character active;
- sandbox Location assigned;
- represented runtime options available;
- sandbox-owned cognition AI binding assigned;
- sandbox clock configured.

`runtime_ready` is not `running`.

## Schema

Schema v18 adds:
- `creation_sandbox_profile_values`;
- `creation_sandbox_character_skills`.

All mutable data remains under the Creation Sandbox namespace.

## Acceptance

Required proof:
- shared profile field metadata is reused;
- sandbox profile/skill writes create no canonical Character rows;
- unknown profile fields fail closed;
- nested sandbox Locations work and cycles fail;
- represented capabilities derive deterministic action options;
- AI + clock + Location + derived options can reach `runtime_ready`;
- canonical-state fingerprint remains unchanged throughout sandbox-only operations.

## Non-goals

Not included:
- full sandbox action execution/autonomy tick;
- Item/Element/System/Quest/Job creation sockets;
- Creator Studio wizard;
- canonical transmigration;
- second real Character activation;
- arbitrary custom executable actions.
