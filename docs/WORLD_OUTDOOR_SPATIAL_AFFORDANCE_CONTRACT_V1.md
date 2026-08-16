# World Outdoor Spatial Affordance Contract v1

Status: ACTIVE RUNTIME CONTRACT

## Purpose

A represented outdoor location must be able to function as lived space, not merely as a traversable node between indoor rooms and boundaries.

This contract adds a small generic bridge between spatial-container semantics and ordinary autonomous activity. It does not add weather simulation, a character-memory engine, public South Lake Tahoe, or a rule that characters must go outdoors.

## Core distinction

Three authorities remain separate:

1. **World truth** — the location and its authored spatial affordances exist.
2. **Character-known world** — spatial familiarity determines whether the character knows that place well enough to plan around it.
3. **Current executable activity** — exact `action_options` determine what the character can do now at the current location.

Knowledge of a distant outdoor destination never authorizes teleportation or non-local action.

## Location-authored affordances

`world.spatial_container.affordances` is the machine-readable source for ordinary activities supported directly by a spatial container.

V1 introduces three generic location-level activities:

- `walk` — low-intensity movement within the current represented container; it does not change `located_at`.
- `relax` — quiet discretionary recovery/decompression supported by the current place; weaker than dedicated `rest` recovery.
- `observe` — deliberately spend time taking in the represented surroundings without inventing new world facts.

The action runtime exposes these actions only when the current location explicitly authors the matching affordance, and validation rejects them elsewhere.

## Lifestyle destinations

`world.spatial_container.lifestyle_destination=true` marks a place that should be considered ordinary lived space rather than only transit, training, security, service, or egress infrastructure.

Known lifestyle destinations may be projected to cognition with:

- friendly location name;
- supported outdoor activities;
- compact atmosphere tags;
- familiarity level;
- `planning_only=true`.

This projection supplies positive reasons to consider the wider represented property while preserving current action options as the only executable authority.

## Thorne Estate v1 authoring

Current ordinary lifestyle destinations are:

- Mansion Exterior — `observe`, `relax`;
- Core Estate Grounds — `walk`, `relax`, `observe`;
- Private Lake Access — `relax`, `observe`;
- Rear Forested Estate — `walk`, `relax`, `observe`.

The Tactical Obstacle Course remains training-oriented. The Main Estate Approach is primarily transit. The Main Security Gate, Concealed Forest Passage, and Hidden Dock remain security/egress or utility spaces and are deliberately not promoted as ordinary recreation destinations.

## Cognition policy

Outdoor choices are **soft positive alternatives**, never quotas. When no stronger physiological or safety need dominates, familiar outdoor walking, quiet relaxation, and observation may compete with indoor rest, reading, productivity, or repeated training.

Training repetition pressure may make these non-training alternatives more attractive, but it does not force an outing and does not change training legality.

## Runtime boundaries

- `walk`, `relax`, and `observe` do not bypass movement topology.
- `walk` is not inter-location travel.
- No public-road, Tahoe-backcountry, or water continuation is created.
- No weather/daylight claim may be invented from an outdoor affordance.
- Secret or boundary locations do not become lifestyle destinations merely because they are outdoors.
- Indoor rest/sleep remain legal and competitive choices.

## Future extensions

Later environment runtime may condition outdoor suitability using authored weather, daylight, temperature, visibility, or hazards. Later character memory/preferences may modify attraction to particular places. Those systems should consume this affordance layer rather than replace its deterministic world authority.
