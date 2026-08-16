# World Spatial Familiarity Contract v1

Status: ACTIVE FOUNDATION

## Purpose

Represent what a character knows about authored geography without conflating world truth, current perception, physical reachability, or a future episodic memory system.

## Core separation

The runtime must preserve three distinct layers:

1. **World truth** — represented locations and topology that objectively exist.
2. **Character-known world** — the subset of represented geography the character is authored to know, with a familiarity level.
3. **Current actionable space** — exact movement/action targets the deterministic runtime currently allows from the actor's present location.

Knowing a place never grants teleportation, access permission, or immediate action authority. A location can exist in world truth without being known to a character.

## Familiarity levels

The v1 ordinal vocabulary is:

- `unknown` — the actor is not entitled to reason from the location's existence or route.
- `aware` — the actor knows the place exists but has weak spatial knowledge.
- `familiar` — the actor knows the place and useful route/context well enough for ordinary planning.
- `intimate` — the actor has strong home-like or repeatedly established spatial knowledge.

These levels describe authored spatial knowledge, not emotional attachment or legal access.

## Hidden / secret is orthogonal

`hidden` or `secret` is a discovery/visibility property, not a familiarity level.

A concealed place can be:
- unknown to one actor;
- known/familiar to another actor;
- intimate after long-term use.

Therefore hiddenness must never be encoded by inventing a special familiarity grade.

## Cognition contract

Model cognition may receive a compact `spatial_knowledge` projection containing:
- known locations grouped by familiarity;
- represented known connections among those places;
- explicitly known concealed/secret places;
- guidance that this is planning knowledge only.

The model must still choose exact executable movement from `action_options`. The known map may justify a multi-step destination intention, but it cannot supply a non-local target ID or bypass deterministic routing.

Locations absent from the authored character-known projection must not be inferred as known merely because they exist in the world database.

## Generic preview versus actor-specific knowledge

Generic one-hop location previews have no actor-specific discovery authority and must omit globally concealed destinations.

Actor-specific cognition may still expose an exact move to a concealed adjacent destination when that character is explicitly authored to know it and the deterministic topology makes the move legal.

This prevents secret-space leakage while preserving realistic knowledge for residents who legitimately know a concealed facility.

## Darian Estate v1 seed

Darian's ordinary represented home/interior and normal private Estate campus are authored as `intimate` knowledge. The represented Rear Forested Estate is `familiar`. The Hidden Dock and Concealed Forest Passage are represented as known concealed facilities and `familiar`, matching current established Estate/story continuity.

No South Lake Tahoe public location or outside road/backcountry/water continuation is made known or unlocked by this foundation.

Future secret Estate locations that Darian has not discovered must be authored `unknown` or omitted from his known-location seed until a later discovery/memory mechanism explicitly changes that state.

## Memory-system boundary

v1 is **not** a general character memory engine.

It does not infer familiarity from event history, time lived at a location, intelligence, ownership, or world existence. Initial knowledge is explicit authored character-world state.

A later memory/discovery system may update spatial familiarity from validated observations, exploration, teaching, maps, forgetting, or revelation events. That future system must consume this contract rather than replace the world-truth/action-authority separation.

## Authority boundary

Spatial familiarity shapes autonomous character cognition. It does not rewrite world topology or Creator/manual inspection authority.

Canonical rule:

> World truth says what exists. Spatial familiarity says what this character knows. Current action options say what this character can execute now.

## Non-goals v1

Do not add:
- episodic memory;
- automatic discovery progression;
- forgetting curves;
- GIS geometry;
- route-confidence scoring;
- map-item mechanics;
- public Tahoe knowledge merely because the Estate is located near Tahoe;
- topology changes or outside-world unlocks.
