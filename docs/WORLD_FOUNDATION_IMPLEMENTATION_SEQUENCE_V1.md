# World Foundation Implementation Sequence v1

Status: PLANNING AUTHORITY — CODING NOT YET AUTHORIZED

## Purpose

This document defines the low-drift implementation sequence for World Foundation Expansion. It now reflects the Creator's current priority: **make the location model semantically complete enough, refactor the already represented Estate first, reconnect gameplay/runtime, then unlock the private Estate campus before any South Lake Tahoe expansion.**

## Governing rule

Prefer consecutive vertical slices, but never batch across an unproven dependency boundary.

Use exemplar-first for a genuinely new invariant; once proven, batch structurally equivalent follow-ons.

The immediate target is the Estate as a complete simulation boundary. Public Tahoe expansion is paused.

## Phase A — Location semantic foundation

### Slice A0 — Location Spatial Container Contract v1

Planning-only ontology closure.

Authoritative semantic rule:

`location = nested spatial container; graph node = identity/topology representation, not a point`

Required concepts:
- extent/area where known;
- parent/child containment;
- boundaries;
- entrances/exits/spatial interfaces;
- explicit traversable connections;
- ownership/control/access;
- local environment/state;
- facilities/affordances;
- occupants/resources/contained elements;
- adjacency reserved separately from traversability.

Proof:
- existing node/topology contract remains compatible;
- no requirement for GIS/polygon precision;
- no doorway micro-node explosion;
- Estate-first sequence is explicit.

### Slice A1 — Existing Estate Location Refactor

Before adding new campus reachability, audit and refactor the current represented Estate locations against `WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`.

Scope:
- preserve stable IDs wherever possible;
- confirm structural parentage and container kinds;
- classify exposure/indoor-outdoor role where relevant;
- preserve/repair child locations and contained fixtures/resources;
- make entrances/exits/interfaces derivable from actual topology;
- confirm ownership/access semantics where relevant;
- attach only source-supported/provisional extent/layout metadata;
- make facilities/affordances reflect actual machine-readable contents/capabilities;
- avoid converting uncertain layout into canon.

Proof:
- current Estate interior remains representable without identity churn;
- existing room/floor/object semantics fit the richer ontology;
- current exterior boundary remains locked;
- no campus or Tahoe traversal is added yet.

### Slice A2 — Gameplay Runtime Reconnection / Regression

Run the current gameplay/runtime against the refactored Estate model and fix compatibility errors before any campus expansion.

Required consumer checks:
- actor `located_at` resolution and mirrored compatibility location;
- current movement options/routing;
- action-target compatibility;
- place-dependent validation;
- object/resource/inventory location queries;
- training/physiology/action consumers that depend on place context;
- cognition compact projection;
- scheduler/pending-action location references;
- history/event location linkage;
- Telegram/generic location browsing.

Proof:
- existing gameplay behavior remains green or intentionally improved;
- no stale location IDs/references;
- option shaping and committed validation agree;
- no new campus destination leaks into cognition yet.

This is the hard gate before Estate-campus reachability work.

## Phase B — Estate Campus Reachability

### Slice B1 — Campus Spatial Seed

Author only the approved/source-backed/story-established Estate-side containers plus the minimum provisional connector spaces required for coherent traversal.

Preferred first set based on the Estate source/canon map:
- Mansion Exterior / Primary Entrance;
- Core Estate Grounds or equivalent minimal connector zone;
- Garage & Workshop access where spatially meaningful;
- Tactical Obstacle Course;
- Private Lake Access;
- Hidden Dock;
- Rear Forested Estate;
- Main Approach;
- Main Security Gate;
- Concealed Forest Passage;
- only other internal paths/interfaces required to make these relationships coherent.

Garden, swimming pool and tennis court are not minimum canon and remain excluded unless explicitly approved later.

All outward public/backcountry/water continuations remain locked/unrepresented.

### Slice B2 — Estate Access & Walking Topology

Ensure Estate-private access, interfaces and deterministic walking routes compose correctly across the new campus containers.

Proof:
- mansion -> campus destinations use generic topology/access rules;
- route duration/simulation time is represented as required by the travel contract;
- Main Security Gate is reachable from the Estate side but cannot lead to Tahoe;
- Concealed Forest Passage is reachable on the Estate side but has no external backcountry continuation;
- Hidden Dock is usable as a place/facility but has no water-travel capability yet.

### Slice B3 — Campus Action/Choice Expansion

Expand machine-readable facilities/affordances and model-facing choosable options so Darian can meaningfully decide to use represented campus locations.

Examples of valid option sources:
- obstacle/agility training at Tactical Obstacle Course;
- walking/exploration/recovery where existing action definitions support them;
- moving to Garage & Workshop when an existing relevant action/resource applies;
- moving to lake/dock/forested zones for supported generic activities.

Do not invent actions solely because a place label sounds plausible. Choosable options must compose existing/generic action definitions, target/resource/facility requirements and deterministic validation.

### B acceptance milestone — Estate Campus Runtime Acceptance

Minimum proof:
1. Darian begins in an existing mansion location;
2. cognition receives legal Estate-side destinations/options only;
3. he can choose or be directed through ordinary action/runtime paths to leave the mansion;
4. multi-node Estate walking/travel resolves deterministically;
5. current location updates correctly;
6. at least multiple meaningful campus destinations/actions are usable;
7. he can return to the mansion;
8. time/events/history/location queries remain coherent;
9. Main Gate, forest passage and Hidden Dock expose no illegal outside-world continuation;
10. existing indoor gameplay remains green.

Production need not be manipulated solely to manufacture this proof; focused tests/disposable copies plus ordinary read-only production observation are preferred unless the Creator explicitly requests an intervention.

## Phase C — PAUSED: South Lake Tahoe Regional Opening

WF-5 and all public-world work remain planned but **not the current target**.

Do not begin Phase C until:
- Location Spatial Container Contract is canonical;
- current Estate refactor is complete;
- gameplay/runtime regressions are resolved;
- Estate Campus Runtime Acceptance is green;
- Creator separately prioritizes outside-world expansion.

When later resumed, Phase C may cover regional parent insertion, public connectors, first useful destination and bounded return route. Existing Estate IDs must remain stable.

## Later phases — also paused

Environment, public venues/services, world resource distribution, ambient public population and basic economy remain roadmap work after the Estate-first milestone unless a narrowly needed Estate-local feature justifies an earlier reusable hook.

Do not implement them merely because they are documented.

## Cross-slice invariants

Every implementation slice must preserve:
- stable globally scoped entity IDs;
- nested spatial-container semantics;
- deterministic world authority;
- LLM proposal-only boundary;
- containment != adjacency != traversability != access;
- legal options and validation consuming the same underlying rules;
- simulation-time continuity;
- generic event/state auditability;
- relevance-bounded cognition projection;
- authored data rather than mansion/Darian-specific engine branches.

## Context budget discipline

Before each location/world slice merges, inspect whether its cognition projection adds global catalog data.

Preferred:
`current container -> relevant contained facilities/interfaces -> legal/relevant nearby destinations -> compact options`

Avoid:
`serialize entire Estate/world -> ask model to discover relevance`.

## Schema discipline

Reuse existing generic entities/relations/fields/runtime state first. Add a schema migration only where the spatial-container invariant cannot be represented cleanly and generically with current storage.

Do not pre-create tables for Tahoe, weather, vehicles, economy, population or unrelated later depth.

## Documentation discipline during coding

For each completed slice:
- record implemented scope separately from planned scope;
- refine contracts only when implementation evidence requires it;
- update ROADMAP/NEW_CHAT_BOOTSTRAP at material checkpoints;
- preserve source-confirmed/story-established/provisional distinctions;
- do not silently move the South Lake Tahoe gate forward.

## Current coding-start interpretation

The Creator has authorized the **sequence and priority**, but requested that the Location Spatial Container Contract be completed carefully first.

Therefore the current documentation task ends at A0. The next implementation work, after this contract checkpoint is canonical, is A1 Existing Estate Location Refactor, followed by A2 runtime reconnection/regression, then Phase B Estate Campus Reachability.
