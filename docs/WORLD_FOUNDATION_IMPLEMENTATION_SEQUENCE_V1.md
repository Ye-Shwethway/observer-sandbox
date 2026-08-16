# World Foundation Implementation Sequence v1

Status: PLANNING AUTHORITY — CODING NOT YET AUTHORIZED

## Purpose

This document turns the World Foundation Expansion program into a low-drift implementation sequence. It does not authorize coding by itself. It defines what each future slice must prove before the next dependent slice begins.

## Governing rule

Prefer consecutive vertical slices, but never batch across an unproven dependency boundary.

Use exemplar-first for a genuinely new invariant; once proven, batch structurally equivalent follow-ons.

## Phase A — Representation foundation

### Slice A1 — WF-1 Spatial Metadata & Outdoor Node Support

Implement only the metadata/query support needed for outdoor/property/road/boundary nodes and optional edge cost metadata while preserving the existing recursive graph.

Proof:
- old Estate interior behavior unchanged;
- outdoor/property kinds are representable;
- containment remains separate from traversal;
- no new exterior edge yet.

### Slice A2 — WF-2 Access Foundation

Add deterministic access classification/evaluation reused by option shaping and validation.

Proof:
- public/private/restricted/closed distinctions work;
- Thorne Estate private access is represented;
- access cannot be granted by LLM prose;
- no law/crime system.

### Slice A3 — WF-3 Route/Travel Runtime

Generalize movement to legal multi-edge walking routes and represented duration.

Proof:
- route derived from graph + access;
- travel advances simulation time;
- location settles through generic location runtime;
- invalid/unrepresented destinations fail closed.

Do not open the Estate boundary until A1-A3 are green.

## Phase B — Usable Estate world

### Slice B1 — WF-4 Estate Campus Seed

Author the approved campus nodes/edges in one coherent batch after graph/access/travel invariants are proven.

Minimum useful set:
- mansion exterior/entrance;
- front/rear grounds or equivalent approved zones;
- garden;
- pool area;
- tennis court;
- driveway;
- security gate;
- only other path/perimeter nodes needed for meaningful connectivity.

Proof:
- actor can leave mansion and traverse multiple outdoor Estate destinations;
- existing indoor actions remain valid;
- gate outward edge still absent;
- Telegram/generic location query can observe the campus without special-case code.

### B1 acceptance milestone — Estate Campus Unlock

At this milestone, the simulation is no longer mansion-interior-only. The entire represented private Estate campus is usable, but the public world remains intentionally locked.

## Phase C — Regional opening

### Slice C1 — WF-5 South Lake Tahoe Regional Anchor

Insert regional parent and immediate public connector graph without renaming Estate identities.

Proof:
- existing IDs remain stable;
- Estate belongs structurally to Tahoe;
- gate can connect to one bounded public connector;
- only authored public nodes are reachable.

### Slice C2 — First Public Destination

Author one simulation-useful regional destination, preferably a venue candidate that later supports a resource loop.

Proof:
- Estate -> public connector -> destination -> return route works;
- travel duration represented;
- no exhaustive city map.

### C acceptance milestone — Outside World Unlock

Darian may legally leave the Estate and enter the bounded represented South Lake Tahoe world. This does not imply arbitrary travel to unrepresented real places.

## Phase D — Environment and useful places

### Slice D1 — WF-6 Environment v1

Add local daylight/temperature/weather/exposure authority and one deterministic consumer hook.

Proof:
- outdoor context differs from indoor exposure;
- cognition sees compact local environment only;
- world state is deterministic/persisted;
- no hazard engine.

### Slice D2 — WF-7 Venue/Service v1

Turn the first public destination into an operational venue with access/opening schedule and one stable capability.

Proof:
- open/closed derives from simulation time/state;
- service capability is machine-readable;
- cognition sees relevant capability without full regional catalog.

## Phase E — Resource and world-process loop

### Slice E1 — WF-8 Resource Distribution v1

Represent finite/available stock at Estate and/or first venue using existing inventory/resource semantics.

Proof:
- resource has location/ownership/quantity authority;
- ordinary use can deplete it;
- shortage can become cognition-relevant;
- no supply-chain simulator.

### Slice E2 — WF-9 Ambient Presence v1

Add lightweight venue staff/patron presence sufficient for generic service availability.

Proof:
- ambient presence changes through deterministic schedule/state;
- no full LLM agent per person;
- no fake persistent identities.

### Slice E3 — WF-10 Basic Economy v1

Add bounded balance/price/purchase transaction support.

Proof:
- price and balance are authoritative;
- transaction changes money and resource consistently;
- event/state audit exists;
- no jobs/macroeconomics required.

## Final program acceptance — First Living Outside-World Loop

The program is considered minimum complete when an ordinary autonomous character can naturally execute a loop equivalent to:

`Estate resource shortage -> decide to obtain resource -> leave mansion -> cross Estate campus -> pass legal gate -> travel through bounded Tahoe graph -> reach open staffed venue -> purchase/obtain finite resource -> return -> resource becomes available at actor/Estate -> persistent events/state reflect the journey`

The exact live action does not need to be artificially manufactured in production for proof. Tests/disposable copies may prove the loop; production should be observed naturally unless the Creator explicitly chooses an intervention.

## Cross-slice invariants

Every implementation slice must preserve:
- stable globally scoped entity IDs;
- deterministic world authority;
- LLM proposal-only boundary;
- legal options and validation consuming the same underlying rules;
- simulation-time continuity;
- generic event/state auditability;
- relevance-bounded cognition projection;
- no mansion/Darian-specific runtime branches unless they are authored data exemplars rather than engine logic.

## Context budget discipline

Before each world slice merges, inspect whether its cognition projection adds global catalog data. Reject designs that scale prompt size with total world size.

Preferred query pattern:
`current context -> legal/relevant nearby facts -> compact projection`

Avoid:
`serialize entire world -> let model discover relevance`.

## Schema discipline

Reuse existing generic entities/relations/fields/runtime state first. A schema migration is justified only if the new invariant cannot be represented cleanly and generically with current contracts.

Do not pre-create tables for later weather, vehicles, economy, population, or routes merely because they appear in the roadmap.

## Documentation discipline during coding

For each completed slice:
- mark actual implemented scope separately from planned scope;
- update the relevant contract only when implementation proves the design needs refinement;
- update ROADMAP/NEW_CHAT_BOOTSTRAP at material checkpoints;
- do not silently reinterpret later milestones during implementation.

## Coding start gate

Sustained coding should begin only after Creator approval that this contract set is sufficiently complete for implementation. Until then, discussion may continue to refine:
- exact Estate campus geography;
- first public Tahoe destination(s);
- initial environment-state model;
- first venue/resource/economy loop;
- any source/reality policy needed for real-world Tahoe content.