# Creation Sandbox Isolation v1

Status: **IMPLEMENTATION CONTRACT**
Date: 2026-08-19

## Purpose

Provide the first persistent Creator Creation staging substrate without allowing sandbox-only work to mutate the canonical universe.

This slice implements Phase I2 of `CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`.

## World-layer UX

`/start` uses a world-layer top level:

```text
Observer Home
├─ Real World
│  ├─ Universe
│  ├─ Characters
│  ├─ Runtime
│  ├─ History
│  └─ Inventory
├─ Sandbox World
│  ├─ Universe
│  ├─ Characters
│  ├─ Locations
│  └─ History
└─ Creator Settings
```

Creator Settings remains world-independent.

The Sandbox World is Creator-only. It is not presented as a second canonical universe; it is an isolated Creation Sandbox namespace.

## Persistence boundary

Schema v16 adds only dedicated Creation Sandbox tables:

- `creation_sandboxes`
- `creation_sandbox_objects`
- `creation_sandbox_relations`
- `creation_sandbox_events`

Sandbox operations do not insert into or update canonical `entities`, `relations`, runtime state, profile state, world graph, or autonomy membership.

Sandbox object IDs use an `sbx_` prefix and are collision-checked against both canonical and sandbox IDs before activation.

## Shared engine, isolated state

The sandbox reuses:

- universal creation proposal/socket validation;
- existing process/runtime DB connection and migration infrastructure;
- presentation adapters where safe.

It does not clone the canonical engine and does not route sandbox characters into the canonical autonomy scheduler.

## Minimum lifecycle

Supported in I2:

- ensure/default sandbox namespace;
- activate a validated Character or Location proposal;
- inspect/list sandbox objects;
- bind a sandbox Character to a sandbox Location through an isolated relation;
- archive a sandbox object;
- delete a sandbox object;
- reset the sandbox and increment its revision;
- inspect isolated sandbox history.

No canonical transmigration/apply path exists in this slice.

## Isolation invariant

For any sequence consisting only of Creation Sandbox operations:

```text
canonical_state_before == canonical_state_after
```

The implementation exposes a deterministic canonical-state fingerprint used by acceptance tests. Sandbox tables and schema metadata are excluded from that fingerprint; canonical/runtime data tables are included.

## Telegram semantics

Every Sandbox World view clearly labels staging isolation and states that the canonical universe is unchanged.

The Real World retains the pre-existing live observer feature callbacks, now grouped one level below Observer Home.

The Sandbox World currently exposes only concepts actually represented by I2. Additional parallel surfaces such as sandbox Inventory or Runtime should appear only when their creation/runtime sockets exist rather than as dead placeholder controls.

## Non-goals

I2 does not include:

- Creator Studio creation wizard;
- manual field editor;
- AI draft generation UI;
- sandbox runtime simulation;
- sandbox inventory creation;
- canonical promotion/transmigration;
- second real production character;
- multi-universe runtime.

## Acceptance

Required proof:

1. schema v16 migrates cleanly;
2. Character + Location activate inside sandbox;
3. sandbox Character binds to sandbox Location;
4. sandbox IDs are absent from canonical entities/relations;
5. delete/reset operate only in sandbox state;
6. canonical state fingerprint is unchanged;
7. `/start` groups canonical observer features under Real World;
8. Sandbox World is Creator-only and lists only sandbox objects.

## Next slice

Phase I3: Character + Location vertical proof using existing profile/location ontology while keeping every object sandbox-only.
