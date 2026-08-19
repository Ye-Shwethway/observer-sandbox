# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — MINIMUM FIRST**
Date: 2026-08-19

## Objective

Implement the smallest vertical foundation that proves Creator can create new content safely without touching the canonical universe, while preserving a clean path to later AI-assisted creation and validated transmigration.

This plan intentionally does **not** implement the full Creator Creation roadmap at once.

---

## Phase I0 — Creator authority hardening

Implement/centralize a reusable authority rule so Creator-approved canonical state cannot be silently replaced by ordinary seed/import/reinitialize flows.

Minimum work:
- define Creator-owned provenance marker/contract reusable beyond profile fields;
- add generic conflict-preserving import semantics where applicable;
- add regression acceptance proving Creator-approved state survives ordinary initialization;
- keep existing PR #278 profile protections intact.

No new UI required.

---

## Phase I1 — Universal creation proposal/socket core

Implement:
- creation type registry;
- proposal envelope;
- proposal validation API;
- stable proposal IDs;
- sandbox IDs;
- lifecycle state;
- provenance/source;
- dependency/reference representation;
- batch proposal container;
- no canonical writes.

Initial registered types:
- `character`;
- `location`.

Keep schemas minimal and reuse existing profile/location ontology instead of inventing parallel fields.

Acceptance:
- valid manual Character/Location proposals pass;
- invalid proposals fail with structured errors;
- validation does not mutate canonical DB state.

---

## Phase I2 — isolated Creation Sandbox state

Implement one sandbox namespace/state substrate.

Minimum rules:
- sandbox objects are separate from canonical entity/world queries;
- sandbox object IDs cannot collide with canonical IDs;
- sandbox events/state are isolated;
- sandbox Character is not added to canonical autonomy scheduler;
- sandbox Location is not inserted into canonical world graph;
- sandbox reset/delete works;
- canonical state hash/snapshot remains unchanged across sandbox-only operations.

Prefer shared runtime helpers/validators where safe; do not clone engines.

Acceptance:
- create Character + Location in sandbox;
- bind sandbox Character to sandbox Location;
- inspect them;
- delete/reset them;
- canonical universe remains unchanged.

---

## Phase I3 — Character + Location vertical proof

Character minimum:
- name/identity;
- sex/reference facts;
- date of birth or age-compatible representation;
- basic represented body/profile fields using existing definitions;
- optional initial skills only through existing skill schema when available;
- sandbox lifecycle/provenance.

Location minimum:
- name;
- type/category;
- parent/containment when represented;
- basic location properties using existing spatial schema;
- sandbox lifecycle/provenance.

Do not build full profession/quest/inventory creation here.

Do not connect sandbox Character to canonical Darian or canonical relationships.

---

## Phase I4 — Telegram Creator Studio minimum

Add owner-only entry point:

`🛠 Creator Studio`

Minimum screens:
- Create;
- Sandbox Creations;
- View creation;
- Delete/Reset;
- Validate.

For Character and Location:

```text
Create
→ Build Manually | Generate with AI
```

### Manual mode

Use simple guided fields with preview.

### AI mode

Use one bounded provider call to convert Creator intent into the same structured proposal schema.

AI output must be schema-validated before showing as valid.

Minimum controls:
- Edit;
- Reroll whole proposal;
- Validate;
- Approve into Sandbox;
- Cancel.

No AI direct DB/canonical write.

---

## Phase I5 — sandbox Telegram notifications

Add separate Creator-only sandbox messaging.

Every sandbox message must make isolation obvious, for example:

```text
🧪 CREATION SANDBOX
━━━━━━━━━━━━━━━━━━
Canonical universe: unchanged
```

Do not send ordinary CHARACTER UPDATE / canonical progression notifications for sandbox objects through production observer streams.

Minimum notifications:
- sandbox creation activated;
- validation failed/passed;
- sandbox reset/deleted;
- AI reroll ready.

---

## Phase I6 — transmigration plan contract only

Before returning to Mind work, implement at least the internal planning/validation boundary even if current production Character promotion remains gate-blocked.

Minimum:
- select frozen sandbox revision;
- choose target universe profile;
- compute dependency closure;
- compatibility validator interface;
- structured result taxonomy;
- deterministic proposed canonical mutations;
- no actual canonical apply required for Character while gate is closed.

Recommended disposable proof:
- allow a harmless compatible Location exemplar to produce a promotion plan in test/disposable state;
- reject an intentionally incompatible supernatural/system exemplar for the current realistic universe profile;
- prove failure creates zero canonical writes.

---

## Stop point before Mind resumes

Return to MIND-F2 when all are true:

1. Creator authority no-snap-back invariant is regression-tested;
2. Character/Location creation sockets exist;
3. Creation Sandbox isolation is proven;
4. Creator can create/manage those types from Telegram;
5. AI and manual modes share one proposal path;
6. compatibility/transmigration planning boundary exists;
7. production second-character transmigration remains blocked.

Then continue:

`MIND-F2 → F3 → F4 → F5 → F6 → F7`

while later Creator creation sockets are expanded in separate minimum slices.

---

## Explicit non-goals

Do not include in this minimum implementation:
- full multi-universe runtime;
- all creation types;
- rich graphical editors;
- automatic canonical promotion;
- supernatural production systems;
- arbitrary AI-generated executable code;
- full quest/job/faction builders;
- second real production character activation;
- redesign of current Body/Profile controls.

---

## Test policy

Use focused tests during implementation.

Required high-value acceptance:
- authority precedence/no snap-back;
- proposal validation;
- sandbox/canonical isolation;
- reset/delete safety;
- batch internal reference resolution;
- manual/AI proposal equivalence at the apply boundary;
- target-universe incompatibility rejection;
- explicit second-character gate rejection;
- final CI at PR checkpoint.

No production Darian mutation is required for acceptance.
