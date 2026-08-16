# World Spatial, Access & Travel Contract v1

Status: PLANNING AUTHORITY — IMPLEMENTATION NOT YET AUTHORIZED

## Purpose

This document refines WF-1 through WF-3 of `WORLD_FOUNDATION_EXPANSION_PLAN_V1.md` into one coherent world-mobility contract. It extends, but does not replace, `WORLD_LOCATION_NODE_MODEL.md`.

The objective is to let an actor move through a represented world without teleportation, prompt-only geography, or mansion-specific routing logic.

## Core invariants

1. `contains` answers **where a place belongs structurally**.
2. `connected_to` answers **where physical traversal is possible**.
3. `located_at` answers **where a movable entity currently is**.
4. ownership/residency answers **who controls or belongs to a place**.
5. access state answers **whether this actor may traverse/enter now**.
6. route runtime answers **how a legal multi-edge journey proceeds over simulation time**.

No one relation may silently substitute for another.

## Spatial node classes

The recursive `location` entity remains the universal place primitive. `kind` should describe spatial role without creating one table/class per place type.

Minimum planned kinds:
- `region`
- `property`
- `building`
- `floor`
- `room`
- `outdoor_zone`
- `boundary`
- `road`
- `path`
- `venue`
- `wilderness`
- `service_area`

Kinds are descriptive and queryable; they do not by themselves grant movement or access.

## Containment model

Containment may be arbitrarily recursive but must remain acyclic for locations.

Examples:

`South Lake Tahoe -> Thorne Estate -> Main Mansion -> Ground Floor -> Living Room`

`South Lake Tahoe -> Thorne Estate -> Estate Grounds -> Garden`

A location may have one canonical structural parent in v1. Cross-cutting geographic/grouping concepts should not be emulated by giving a node multiple structural parents.

## Traversal edges

A traversable connection is explicit and authored.

Minimum edge semantics:
- source location
- destination location
- directionality: two-way by default only when authored as such
- enabled/disabled state
- optional traversal class: `walk`, later additional modes
- optional bounded distance or base-duration metadata
- optional boundary/access reference

Containment never creates a traversal edge automatically.

If a physical doorway/path/road is not represented by a legal edge, the engine must fail closed rather than infer it from prose.

## Distance and geometry

V1 does not require GIS coordinates.

Travel cost may be represented using one of:
- authored base minutes for an edge;
- authored coarse distance plus a deterministic mode-speed policy;
- a future compatible geometric representation.

The implementation should prefer the smallest model sufficient for deterministic route duration. Exact latitude/longitude remains optional metadata until a feature requires geospatial precision.

## Place classification

A place may carry orthogonal classification metadata such as:
- ownership class: private / public / institutional / unowned
- functional class: residence / road / business / park / medical / food / recreation / wilderness / service
- exposure: indoor / covered-outdoor / outdoor
- occupancy class: private-use / public-use / staff-only / restricted

Classification informs queries and policy; it is not itself permission.

## Access authority

Movement into a connected place is legal only if both topology and access permit it.

Minimum access modes:
- `public`
- `owner_or_resident`
- `authorized`
- `restricted`
- `closed`
- `locked`

Actor-specific authorization may be derived from represented relationships such as ownership, residency, invitation/authorization, or later credentials. V1 must avoid a universal scripting language.

Access checks are deterministic and occur both when shaping legal movement options and when validating the committed move/travel action.

## Opening state versus access state

A venue may normally be public but currently closed. A private property may be physically open but still not publicly enterable.

Therefore:
- access policy = who may enter;
- operating/open state = whether entry/service is available now.

These remain separate fields/queries and compose at validation.

## Boundaries

Boundary nodes or boundary-linked edges exist to make transitions explicit:
- mansion interior -> estate grounds
- estate grounds -> security gate
- estate gate -> public road

A locked/unimplemented boundary has no legal outward route.

The current `loc_thorne_estate_exterior_boundary` remains locked until the planned Estate-campus graph exists. Documentation does not unlock it.

## Route model

A route is a deterministic sequence of legal graph edges from origin to destination.

V1 route selection:
- starts from authoritative actor `located_at`;
- considers only enabled connections legal for the selected travel mode;
- filters inaccessible/closed transitions;
- may use shortest path by bounded cost;
- returns no route when any required world segment is unrepresented.

Cognition may choose among reachable destinations, but it does not author the route graph.

## Travel lifecycle

Planned lifecycle:

`proposal -> route validation -> travel action starts -> simulation time passes -> route completion -> actor location updates -> event/state consequences`

For very short local movement, runtime may settle the route as one bounded move action while still deriving it from the same route contract.

For longer travel, the action should persist destination, route identity/edge sequence or reproducible route snapshot, travel mode, start time, expected duration, and completion state.

## Revalidation policy

Before action start, route legality is authoritative.

Once an in-progress travel action begins, v1 should avoid silently recomputing a materially different route unless a later dynamic-routing feature explicitly supports interruptions. If an edge/state changes before departure, validation fails. Mid-route disruption is later depth unless required by a concrete feature.

## Travel modes

First supported mode: `walk`.

Later modes may include personal vehicle, bicycle, public transport, or service transport, but they must plug into the same route contract by declaring compatible edges, duration policy, resource/vehicle requirements, and any operating constraints.

Do not encode car behavior into generic `move` before the vehicle foundation exists.

## Cognition projection

The model should receive only decision-relevant mobility information:
- current friendly location;
- legal adjacent options;
- a bounded set of useful reachable destinations where route lookup is justified;
- travel duration estimate;
- relevant access/open-state reason when a destination is unavailable or excluded from options;
- active journey summary if already travelling.

Do not inject the entire location graph or all access records.

## First runnable proof

The first implementation proof should use the Thorne Estate only:
1. represented mansion exit;
2. one or more Estate outdoor nodes;
3. security-gate boundary;
4. deterministic walking route across multiple nodes;
5. access remains private to represented owner/resident authorization;
6. South Lake Tahoe beyond the gate remains locked.

Success means Darian can autonomously leave the mansion, traverse the Estate grounds, reach the gate, and return through the ordinary action/location runtime without special-case mansion code.

## Failure behavior

Fail closed when:
- destination does not exist;
- no legal route exists;
- an edge is disabled;
- access cannot be established;
- destination is outside the represented/unlocked graph;
- unsupported travel mode is requested.

The LLM must not be invited to improvise around these failures.

## Deferred depth

Not part of this contract v1:
- GPS/GIS fidelity;
- traffic;
- congestion;
- vehicle physics;
- route hazards;
- mid-route rerouting;
- public transit timetables;
- crime/trespass consequences;
- keys/cards/locks inventory taxonomy;
- universal policy language.

## Dependency unlock

This contract is sufficient planning authority for future WF-1, WF-2 and WF-3 implementation slices. WF-4 Estate Campus must author actual campus nodes/edges before the current exterior boundary can be opened.