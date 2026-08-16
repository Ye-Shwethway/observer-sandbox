# Estate Campus Reachability v1

Status: COMPLETE / DEPLOYED

## Purpose

This milestone closes the first Estate-first world expansion sequence after the location spatial-container ontology was established.

The goal was deliberately bounded: refactor the already represented Thorne Estate into richer spatial-container semantics, prove existing gameplay/runtime still works, then let Darian leave the mansion and use the private Estate campus without opening South Lake Tahoe.

## Completed sequence

### A0 — Location Spatial Container Contract v1

PR #196 established the canonical semantic rule:

`location = identifiable nested spatial container with extent, contents, boundaries/interfaces, local state, control and explicit relationships to surrounding space`

The graph node remains the stable identity/hierarchy/topology representation; it is not conceptually a dimensionless point.

Merge: `d1167771ddb9c358a464c6efb863d9edf6800e18`.

### A1 — Existing Estate Location Refactor

PR #197 added authored spatial-container metadata for every already represented Estate location without changing stable IDs, current topology, schema, or adding campus/Tahoe nodes.

Key results:
- `config/worlds/home.spatial.v1.json` added;
- `world.spatial_container` seeded through the existing generic field store;
- `world_spatial_revision = thorne-estate-spatial-v1`;
- Thorne Estate represented as an approximately 50-acre mixed-exposure private-property container;
- source confidence and provisional layout confidence separated;
- existing exterior boundary remains an outdoor locked/non-traversable property-perimeter container.

CI #955 SUCCESS. Strength Live Cycle Validation #86 SUCCESS.

Merge: `886001a1d5d1cc62e5e9aab26a64fc08dedf08f1`.
Deploy #244: SUCCESS.

### A2 — Gameplay Runtime Reconnection / Regression

PR #198 added focused end-to-end regression coverage against the refactored Estate model.

Verified:
- actor snapshot/current location;
- legal local action/movement options;
- deterministic move settlement;
- completed-event and history location linkage;
- follow-up action options after movement;
- generic object/location queries;
- Home Gym training-location consumers;
- locked Estate exterior does not leak into movement options.

The first CI attempt exposed a test misconception: completed move events canonically link to the destination/completion location, not the source location. Runtime behavior was correct; the regression was corrected to the existing event contract.

Final CI #957: SUCCESS.

Merge: `3425315d2a3f564f0f3f5beb15084fda214c3036`.

### B — Estate Campus Reachability

PR #199 added the first bounded private Estate campus as an additive world seed.

Added locations:
- Mansion Exterior;
- Core Estate Grounds;
- Tactical Obstacle Course;
- Private Lake Access;
- Hidden Dock;
- Rear Forested Estate;
- Concealed Forest Passage;
- Main Estate Approach;
- Main Security Gate.

Existing interior connections were preserved. New topology begins at the existing Foyer and Garage and branches through the private campus.

Primary ordinary path:

`Darian's Master Suite -> Grand Foyer -> Mansion Exterior -> Core Estate Grounds`

From Core Estate Grounds:
- Tactical Obstacle Course;
- Private Lake Access -> Hidden Dock;
- Rear Forested Estate -> Concealed Forest Passage;
- Main Estate Approach -> Main Security Gate;
- Garage & Workshop remains connected back into the Estate interior.

Machine-readable campus fixtures/capabilities provide executable local options through the existing generic action-option engine, including outdoor training at the Tactical Obstacle Course.

No Darian-specific movement engine or campus-specific action dispatcher was introduced.

## Acceptance evidence

Campus acceptance tests prove:
1. Darian begins in the existing Master Suite;
2. normal `move` options allow a sequence through Foyer -> Mansion Exterior -> Core Estate Grounds -> Tactical Obstacle Course;
3. the outdoor obstacle-course location exposes an executable `train` option via a represented training fixture;
4. Darian can traverse to Rear Forested Estate and return to the mansion through ordinary action/runtime paths;
5. Hidden Dock, Concealed Forest Passage and Main Security Gate are reachable Estate-side places;
6. each of those egress endpoints has only its Estate-side return edge;
7. no South Lake Tahoe location is seeded or reachable;
8. repeated initialization is idempotent and preserves existing interior topology.

The first PR #199 CI attempt failed only because an A1-era historical regression still asserted that no campus locations could ever exist. The test was correctly evolved to preserve the actual invariant: all base Estate locations remain present and no South Lake Tahoe location appears.

Final evidence:
- CI #959: SUCCESS;
- Strength Live Cycle Validation #88: SUCCESS;
- Inventory Foundation Acceptance #51: SUCCESS;
- Skill Evidence Semantics Acceptance #42: SUCCESS;
- Skill Progression Acceptance #59: SUCCESS;
- Technology Diagnostic Acceptance #33: SUCCESS.

Merge: `f0955a582e11394ec64387f2a3fc0bfb468350b4`.
Deploy #245 / run `31936858504`: SUCCESS, including sync, install/configure, restart and verification.

No synthetic production movement was performed solely for proof.

## Outside-world boundary

South Lake Tahoe remains deliberately paused.

There is still no represented outward edge from:
- Main Security Gate to a public road;
- Concealed Forest Passage to Tahoe backcountry;
- Hidden Dock to a water-travel network;
- legacy `loc_thorne_estate_exterior_boundary` to any outside location.

The Estate is now the active complete simulation boundary for the next observation/refinement work.

## Current interpretation

The project has moved from “mansion interior only” to a bounded **private Estate world**.

Darian can now, through the same generic gameplay/runtime mechanisms used indoors:
- leave the mansion;
- enter the Estate grounds;
- choose among represented campus destinations;
- use machine-readable campus facilities/actions;
- return inside;
- remain blocked from all unrepresented outside-world continuation.

Further South Lake Tahoe work requires a separate Creator priority decision and should not be inferred from this completion.