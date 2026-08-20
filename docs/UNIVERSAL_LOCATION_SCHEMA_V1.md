# Universal Location Schema v1

Status: ACTIVE IMPLEMENTATION CONTRACT  
Slice: I5.10

## Purpose

Turn the existing Creation Sandbox Location prototype from a name-only arbitrary properties bag into a strict typed spatial-container contract, while preserving the existing generic creation envelope and Real/Sandbox isolation.

This contract implements the stable semantics of `WORLD_LOCATION_NODE_MODEL.md`, `WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`, `WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`, I5.3 quantity normalization, I5.4 Location completeness grading and I5.5 access policy.

I5.10 is schema/validation only. Location materialization and embedded Item composition are later slices.

## Exact payload

A `location-v1` payload contains exactly:

- `schema_version`;
- `identity`;
- `structure`;
- `spatial`;
- `access`;
- `topology`;
- `facilities`;
- `environment`;
- `economic_policy`;
- `provenance`.

Unknown top-level or nested fields fail closed.

## Identity

Identity contains:

- stable `key`;
- display `name`;
- spatial `kind`;
- description;
- optional functional classification.

Supported initial kinds reuse the world contract: region, property, building, floor, room, outdoor zone, boundary, road, path, venue, wilderness and service area.

Kind/classification does not grant traversal or access.

## Structure

`parent_ref` is the intended one-parent structural containment relation when known. It may be null for a root/placeholder or before composition resolves the parent.

`exposure` is one of indoor, covered-outdoor, outdoor, mixed or unknown.

Containment never implies `connected_to`.

## Spatial extent

Optional represented measurements:

- area;
- length;
- width;
- height;
- elevation.

They use I5.3 normalized physical quantities. Terrain and orientation notes are optional descriptive facts.

All precision is optional. Unknown measurements remain null. The validator does not invent dimensions, coordinates, area, elevation or geometry to improve completeness.

## Access and operating state

Access contains two separate authorities:

- I5.5 access `policy`;
- current `operating_state` (`open`, `closed`, `locked`, `blocked`).

A public Location may be closed. A private/restricted Location may be physically open. These states never collapse into one field.

## Topology / interfaces

A Location may declare zero or more explicit spatial interfaces. Each interface contains:

- stable local key;
- friendly name;
- optional destination reference;
- directionality (`two_way`, `outbound`, `inbound`);
- enabled state;
- supported traversal modes;
- optional positive base duration.

V1 supports `walk` only. Unsupported modes fail closed rather than being inferred.

A structural parent does not create an interface automatically. A Location without interfaces is not treated as traversable merely because it exists inside another Location.

## Facilities and affordance evidence

The Location may declare machine-readable:

- capabilities;
- facilities;
- resources.

These are affordance evidence for later runtime adapters. Labels such as "Gym" do not by themselves create executable actions.

I5.10 does not execute these capabilities.

## Environment

V1 keeps environment intentionally small:

- optional lighting state;
- optional weather-exposure state;
- represented utility labels.

Later deterministic environment systems may extend/adapt this boundary. I5.10 does not fabricate ambient temperature, weather, hazards, capacity or detailed utilities.

## Economic policy

Optional Location economic policy reuses the existing semantic vocabulary rather than inventing a Location-only price model.

Supported initial classifications:

- standalone asset;
- component;
- resource proxy;
- economically immaterial.

Supported treatments:

- independent;
- included in parent;
- excluded.

`included_in_parent` requires an explicit parent asset reference. Economic value remains independent from access authority and Location completeness.

## Provenance

Creator-facing source status is explicit:

- canonical;
- creator-authored;
- provisional;
- imported.

An optional source note can explain evidence/uncertainty. This content provenance is separate from the generic creation-envelope provenance describing whether the proposal was manual/AI/imported.

## Completeness derivation

Completeness is read-time derived, not an authored source-of-truth field.

The validator derives the existing conceptual levels:

- L0 — identity placeholder;
- L1 — structural container;
- L2 — traversable place with explicit interface/access semantics;
- L3 — usable place with machine-readable facility/resource/capability evidence;
- L4 — living place with represented changing environment/economic state.

The level is then mapped through the I5.4 `location-completeness-v1` grading scheme.

A grade is therefore descriptive completeness evidence. It is not access permission, property value or runtime authority.

## No automatic contents

I5.10 does not embed or create Items. Contents are intentionally deferred to I5.12 after typed Location materialization exists.

Structural child Locations, contained fixtures and movable Items must preserve their distinct relations rather than being flattened into one `contents` blob.

## Acceptance

I5.10 is complete when tests prove:

- exact schema rejects unknown fields;
- unknown spatial precision remains null;
- area/length normalize through I5.3;
- access policy and operating state remain separate;
- topology is explicit and not inferred from structural parentage;
- unsupported traversal modes/duplicate interfaces/invalid durations fail closed;
- economic semantics remain separate from access;
- invalid requirement-grade access policy fails closed;
- L0-L4 completeness/grade derives from represented facts only.

## Deferred

Not part of I5.10:

- Location Sandbox materialization/storage adapter;
- parent-cycle enforcement against live Sandbox graph;
- embedded Item/child Location composition;
- topology relation materialization/routing;
- runtime-ready gating;
- Telegram Location authoring UX;
- canonical transmigration.
