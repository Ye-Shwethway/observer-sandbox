# Universal Creation Socket Foundation v1

Status: **APPROVED DESIGN CONTRACT — DOCS FIRST**
Date: 2026-08-19

## Purpose

Define one reusable creation substrate for all Creator-created universe content.

The project must not implement a separate bespoke CRUD pipeline for every type. Character, location, quest, job, skill, item, organization, service, world element and future creation types plug into one common creation contract through type-specific schemas and validators.

Canonical principle:

> **One proposal/apply pipeline, many registered creation sockets.**

---

## Creation envelope

Every creation proposal conceptually includes:

```text
proposal_version
creation_type
creation_schema_version
proposal_id
sandbox_id
source = manual | ai_generated | imported
creator_authority
identity
properties
capabilities
relationships
references
runtime_hooks
lifecycle
provenance
validation
```

Not every type uses every field. Type schemas declare required/optional structure.

The common envelope handles lifecycle, authority, provenance, validation, sandbox scope and transmigration. Type sockets handle domain-specific data.

---

## Socket registry

A creation socket definition should conceptually expose:

```text
creation_type
schema_version
label
field_schema
required_references
allowed_relationships
capability_schema
sandbox_instantiator
validators
dependency_resolver
transmigration_adapter
canonical_activation_hook
archive/delete policy
```

The registry is data/config driven where practical. Runtime code may provide validators/hooks, but routing must not switch on character names or hard-coded specific entities.

---

## Initial target sockets

Full roadmap target types include:

- character;
- location;
- item/resource/equipment;
- skill;
- job/role;
- quest;
- organization/faction;
- service/facility;
- event/action template;
- world element/environmental feature;
- system/rule-module descriptor;
- future registered extension types.

The first implementation proves only the minimum types needed to validate the architecture.

Recommended first vertical proof:

1. `character`
2. `location`

These exercise identity/profile data, containment, references, world membership, visibility and the existing second-character gate.

---

## Manual and AI generation share one backend

Manual Creator construction and AI-assisted generation must converge on the same proposal schema.

```text
Manual Telegram builder ─┐
                         ├→ structured creation proposal → validation → sandbox
AI prompt generator ─────┘
```

There is no AI-specific database path.

AI returns structured proposal data only. It may not directly instantiate canonical entities.

---

## Proposal validation layers

Validation is layered:

### Layer 1 — structural/schema

Checks:
- required fields;
- field types;
- units/ranges;
- identifiers;
- malformed references;
- schema version.

### Layer 2 — semantic/type

Checks type-specific coherence.

Examples:
- character age/date consistency;
- location parent/containment consistency;
- quest objective graph validity;
- job requirements/compensation shape;
- skill capability structure.

### Layer 3 — dependency/reference

Checks referenced objects exist in the allowed scope and dependency graph has no forbidden unresolved edges.

### Layer 4 — sandbox runtime compatibility

Checks whether the object can be instantiated/tested using currently available shared systems.

### Layer 5 — target-universe compatibility

Used only when preparing transmigration. Defined in `CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`.

---

## Stable IDs and provenance

Sandbox IDs and canonical IDs are distinct.

Do not make sandbox identity equal canonical identity merely because a sandbox object may later be promoted.

Transmigration records mapping:

```text
sandbox_object_id → canonical_object_id
```

Creator-approved provenance must survive promotion.

AI generation provenance may be retained, but Creator approval is the canonical authority boundary.

---

## Batch creation

The creation substrate is batch-native.

A batch may contain objects plus internal references/relationships:

```text
CreationBatch
- object A
- object B
- relationship A → B
- object C
- dependency B → C
```

Validation occurs over the dependency closure.

Sandbox activation should be atomic for a batch when required for coherence.

Transmigration should also operate on a selected dependency closure rather than blindly promoting one row at a time.

Example:

A clinic proposal may include:
- clinic location;
- staff characters;
- jobs;
- services;
- employment relationships;
- schedules.

The batch can remain sandbox-only until all dependencies pass target-universe compatibility.

---

## Lifecycle authority

Creation socket lifecycle is independent from in-world character action semantics.

Minimum creation lifecycle:

```text
draft
sandbox_ready
sandbox_active
sandbox_archived
transmigration_ready
canonical_active
canonical_archived
```

A Creator edit to a sandbox definition is not an in-world event unless explicitly modeled as one.

Likewise, transmigration is Creator/system provenance, not a character memory of having been created in a sandbox.

---

## Creator seed/import precedence

All socket types inherit the project-wide Creator authority invariant.

Ordinary baseline/seed import may:
- create missing baseline objects;
- update unclaimed baseline metadata when explicitly permitted.

It may not:
- overwrite Creator-owned canonical fields;
- replace a Creator-created canonical object with an older seed version;
- revert Creator-approved references/relationships;
- resurrect deleted/retired Creator objects silently.

If a seed and Creator-approved canonical object conflict, the conflict must be explicit and non-destructive.

---

## Runtime hooks

Sockets may declare optional runtime hooks, but the creation system does not prebuild every subsystem.

Examples:
- character → profile initialization / future autonomy registration;
- location → spatial graph registration;
- quest → quest engine registration;
- job → commitment/economy integration;
- skill → progression registry integration.

Hooks execute only in the appropriate scope.

Sandbox hooks write sandbox state only.

Canonical activation hooks execute only after successful transmigration approval.

---

## System creation safety

`system` or `rule-module` creations are descriptors/config proposals, not arbitrary executable code generated by AI.

The first architecture must reject direct AI-authored code execution or unregistered runtime modules.

A system proposal may describe:
- identity;
- capability domain;
- configuration;
- compatibility requirements;
- allowed registered engine adapters.

Actual executable runtime behavior must remain implemented/registered through trusted project code and validation.

This is especially important for supernatural or alternate-physics experiments in sandboxes.

---

## Query and observability

Creator must be able to inspect:
- all sandbox creations;
- type;
- sandbox/batch membership;
- lifecycle;
- validation status;
- dependencies;
- provenance;
- target-universe compatibility status;
- transmigration mapping if promoted.

Canonical observer views must not accidentally include sandbox objects unless explicitly entering Creator Sandbox views.

---

## Minimum implementation acceptance

The foundation is proven when:

1. socket registry can register at least Character and Location;
2. one generic proposal envelope serves manual and AI proposals;
3. proposals validate without DB mutation;
4. valid proposals instantiate into isolated sandbox state;
5. batch references resolve within sandbox scope;
6. deletion/reset cannot touch canonical rows;
7. ordinary seed/import cannot overwrite Creator-approved canonical state;
8. the same proposal can generate a transmigration plan after compatibility validation;
9. no type-specific canonical write bypass exists outside the shared apply/promote contract.
