# Creator Staging & Transmigration Architecture v1

Status: **APPROVED DESIGN CONTRACT — DOCS FIRST**
Date: 2026-08-19

## Purpose

Observer Sandbox must let Creator design, inspect, revise, reroll, test, delete and later promote new universe content without allowing unfinished or incompatible creations to mutate the canonical universe.

This applies to **all Creator-created content**, not only characters:

- characters;
- locations and location graphs;
- items/resources/equipment;
- jobs, roles and occupations;
- skills and skill definitions;
- quests and objective graphs;
- organizations/factions;
- services/facilities;
- world elements and environmental rules;
- event/action templates;
- systems and rule modules;
- future extensible creation types registered through the universal creation socket contract.

Canonical principle:

> **Create anywhere safely; canon nowhere automatically.**

Every new Creator creation begins outside the canonical universe. It may become canonical only through an explicit, validated transmigration transaction approved by Creator.

---

## Core architecture

The system has three distinct authority/state layers:

```text
Creator intent
    ↓
Draft proposal
    ↓
Creation Sandbox / Staging Universe
    ↓ explicit validated transmigration
Canonical Universe
```

These are not merely UI states. They have different mutation authority.

### 1. Draft proposal

A draft is non-runtime structured data. It may be created manually or by AI.

Drafts may be edited, rerolled, duplicated or discarded freely.

Drafts have **zero canonical runtime authority**.

### 2. Creation Sandbox

A sandbox creation may become runnable/testable, but remains isolated from canonical state.

The sandbox uses the same approved schemas, validators, deterministic engines and project rules wherever those rules are applicable. It must not fork a separate toy implementation.

Canonical model:

> **shared engine, isolated state**

Sandbox execution may use canonical definitions as read-only references when explicitly allowed, but must not mutate canonical entities, histories, runtime state, relationships, event logs, schedules or world graphs.

### 3. Canonical Universe

Only explicit Creator-approved transmigration can create or activate canonical state from sandbox state.

Transmigration is a new canonical mutation. It is never an implicit merge, seed refresh or side effect of sandbox execution.

---

## Creator authority invariant

The project generalizes the Creator Profile Edit lesson into a universe-wide authority rule.

Authority precedence:

```text
explicit Creator-approved canonical state
    > live simulation-owned state within its declared authority
    > canonical seed/default/import baseline
```

Ordinary seed import, initialization, deployment, schema refresh or baseline synchronization must never silently overwrite an explicit Creator-approved correction or creation.

A seed is an initializer, not a superior authority.

This invariant applies to profile values and all future Creator-created objects.

---

## Sandbox isolation contract

A Creation Sandbox must have a stable `sandbox_id` and isolated object/state namespace.

Sandbox-created objects must not:

- appear in canonical character/location lists unless explicitly viewed through Creator sandbox UI;
- enter the canonical autonomy scheduler;
- affect canonical needs, physiology, inventory or relationships;
- publish canonical world events;
- satisfy or fail canonical quests;
- alter canonical economy/resources;
- become canonical exposure/perception inputs;
- create canonical memories, commitments, intentions or plans;
- write into canonical Telegram observer streams.

Sandbox notifications use a clearly separate Creator-only surface.

Sandbox-created objects may interact with other objects in the same sandbox when dependencies are valid.

---

## Sandbox modes

### Isolated Sandbox — default

Uses shared schemas/rules/engines but no canonical runtime state.

Best for:
- first creation tests;
- supernatural/alternate-rule experiments;
- destructive rerolls;
- schema and compatibility testing;
- character creation before multi-character production gates are open.

### Reference Sandbox — optional later

May read a bounded canonical snapshot for compatibility testing.

Examples:
- test whether a new NPC fits an existing canonical location ontology;
- validate a proposed job against a canonical workplace definition;
- check whether a quest references available canonical resources.

Reference mode is still read-only toward canonical state.

---

## Lifecycle

Minimum lifecycle:

```text
draft
→ sandbox_ready
→ sandbox_active
→ sandbox_archived | deleted
→ transmigration_ready
→ canonical_approved
→ canonical_active
```

A creation may move backward among draft/sandbox states when Creator revises it.

`canonical_active` is not reversible by deleting the old sandbox object. Canonical retirement/archive/removal uses canonical lifecycle semantics.

A transmigrated sandbox record remains auditable so the project can answer which tested design became canonical.

---

## Deletion, reset, clone and reroll

Before transmigration, Creator must be able to:

- delete a sandbox creation;
- reset its runtime test state;
- clone it;
- create variants;
- reroll AI-generated fields;
- edit individual fields;
- replace dependencies;
- archive it without affecting canon.

Deletion must cascade only inside the sandbox according to explicit dependency rules.

No sandbox delete operation may delete or rewrite a canonical object.

---

## Transmigration

Transmigration is a **validated atomic promotion**, not table copy/paste.

Canonical pipeline:

```text
freeze selected sandbox revision
→ validate object schemas
→ validate dependency closure
→ resolve target universe
→ validate target-universe compatibility
→ resolve canonical IDs/references
→ validate canonical conflicts
→ build canonical mutation plan
→ Creator preview
→ explicit Creator approval
→ atomic canonical transaction
→ canonical activation event
→ sandbox provenance link
```

If any required validation fails, there are **zero canonical writes**.

---

## Target-universe compatibility

Every universe has an explicit compatibility/policy profile.

Transmigration must validate the creation against the **target universe**, not only against generic data schemas.

Examples of compatibility dimensions:

- ontology/type support;
- realism/fantasy/supernatural policy;
- technology level;
- geography/time-period constraints;
- physics and physiology rules;
- allowed power systems;
- economy/resource model;
- skill/action capability compatibility;
- narrative/canon constraints;
- relationship/social-system prerequisites;
- required subsystem availability;
- location/reference existence;
- uniqueness and naming conflicts;
- second-character/live-population gates.

A structurally valid creation can still be **incompatible with the target universe**.

Example:

A sandbox may contain:
- supernatural powers;
- magic systems;
- non-human physiology;
- impossible travel rules.

Those may be valid sandbox creations while the current realistic Observer Sandbox universe rejects their transmigration.

A future separate universe may explicitly allow those same systems.

Therefore:

> **schema-valid does not imply universe-compatible.**

---

## Universe profiles

The architecture must support future multiple universes without rewriting creation types.

Conceptually each target universe exposes a compatibility profile such as:

```text
universe_id
rule_profile_id
allowed_creation_types
capability_policies
physics_profile
physiology_profile
technology_profile
supernatural_policy
required_systems
world_constraints
custom validators
```

The current production universe should initially use a conservative realistic policy matching existing canonical Observer Sandbox rules.

Future universes may opt into different systems.

---

## Compatibility outcomes

Validation should produce structured outcomes, not a single boolean.

Suggested categories:

- `compatible` — safe to prepare for canonical promotion;
- `compatible_with_transform` — deterministic adaptation is possible and shown in preview;
- `missing_dependencies` — required objects/systems absent;
- `policy_conflict` — violates target-universe policy;
- `schema_conflict` — invalid structure/data;
- `canonical_conflict` — collides with existing canonical state;
- `gate_blocked` — project policy intentionally prevents activation yet.

Creator may revise the sandbox creation after a rejection. Rejection does not destroy it.

---

## Character gate preservation

The existing rule remains:

> Do not add another real production character until the required Mind/Relationship foundations and Foundation Completion Review are satisfied.

Creator Creation work does **not** remove that gate.

A new character may be fully created and tested in Creation Sandbox before the gate opens.

Transmigration into the current canonical production universe remains blocked until the gate requirements are satisfied.

This allows creation infrastructure to mature without contaminating the live single-character universe.

---

## AI generation boundary

AI may draft creation proposals but has no canonical write authority.

Canonical AI flow:

```text
Creator prompt
→ bounded AI structured draft
→ schema validation
→ sandbox preview
→ edit/reroll/approve into sandbox
```

AI may never bypass:
- proposal validation;
- sandbox isolation;
- transmigration compatibility;
- explicit Creator approval.

Manual creation and AI creation converge on the same structured proposal schema and the same apply path.

---

## Telegram separation

Creation Sandbox Telegram UX must be visually and semantically distinct from canonical Observer output.

Suggested banner:

```text
🧪 CREATION SANDBOX
━━━━━━━━━━━━━━━━━━
Sandbox: CS-xxxx
Status: Sandbox Active
Canonical universe: unchanged
```

Typical controls:

- View/Edit;
- Validate;
- Run sandbox test;
- Reroll AI draft;
- Clone;
- Reset sandbox state;
- Delete sandbox creation;
- Prepare Transmigration.

Transmigration requires a separate high-signal preview showing:

- target universe;
- creation/dependency counts;
- canonical IDs/references to be created;
- compatibility result;
- transformations if any;
- conflicts/blockers;
- canonical mutation count.

Only then may Creator choose `Approve Transmigration`.

---

## Events and provenance

Minimum provenance should distinguish:

- manual Creator draft;
- AI-assisted draft;
- sandbox activation;
- sandbox revision;
- sandbox validation;
- transmigration proposal;
- compatibility rejection;
- canonical approval;
- canonical activation.

Canonical event/log names are implementation-detail decisions, but provenance must remain queryable and auditable.

---

## Non-goals for the first implementation

The first implementation does not require:

- every creation type;
- multiple fully runnable production universes;
- supernatural production support;
- advanced graphical builders;
- autonomous AI canonical creation;
- sandbox/canonical live synchronization;
- arbitrary code/module execution from AI-generated systems.

Start with minimum universal substrate and prove it vertically.

---

## Acceptance principles

The architecture is acceptable only when tests can demonstrate that:

1. a sandbox object can be created without modifying canonical state;
2. sandbox runtime actions cannot leak canonical mutations;
3. Creator can delete/reset/reroll sandbox objects safely;
4. shared validators/engines are reused rather than forked;
5. a valid-but-incompatible object is rejected for a target universe;
6. a compatible dependency closure can produce a deterministic transmigration plan;
7. failed transmigration creates zero canonical writes;
8. successful transmigration requires explicit Creator approval;
9. canonical Creator-owned state survives ordinary seed/import/reinitialization;
10. character transmigration remains blocked while the second-character gate is closed.
