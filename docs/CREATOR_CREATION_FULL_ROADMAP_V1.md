# Creator Creation Systems — Full Roadmap v1

Status: **APPROVED ROADMAP — DOCS FIRST**
Date: 2026-08-19

## Goal

Build Observer Sandbox toward the long-term Creator goal: a universe platform where Creator can create, test, revise and eventually activate characters, locations, jobs, quests, skills, items, organizations, systems and other world elements through Telegram, either manually or with AI-assisted proposal generation.

Creation capability is separated from canonical activation.

All new content begins as draft/sandbox state. Nothing becomes canonical automatically.

---

## Track C0 — Creator Authority & Canonical Protection

Purpose: generalize the Creator Profile Edit persistence lesson into a project-wide invariant.

Deliverables:
- formal Creator authority precedence;
- seed/import/reinitialize protection for Creator-owned state;
- explicit conflict handling instead of silent overwrite;
- provenance retention;
- canonical delete/archive semantics separated from sandbox deletion;
- regression acceptance covering profile and generic Creator-owned objects.

Exit condition:
- ordinary initialization cannot snap Creator-approved state back to older seed/default values.

---

## Track C1 — Universal Creation Socket Foundation

Purpose: one reusable creation substrate for every creation type.

Deliverables:
- creation type registry;
- common proposal envelope;
- schema versions;
- validation pipeline;
- stable sandbox object IDs;
- dependency/reference graph;
- batch-native creation;
- lifecycle/provenance;
- registered runtime hooks;
- generic apply interfaces.

Initial proof sockets:
- Character;
- Location.

Exit condition:
- Character and Location proposals can be validated generically without canonical mutation.

---

## Track C2 — Creation Sandbox / Staging Universe

Purpose: allow real testing without contaminating the canonical universe.

Deliverables:
- sandbox IDs/scopes;
- isolated object/state namespace;
- shared-engine/isolated-state enforcement;
- sandbox activation lifecycle;
- sandbox reset/delete/clone/reroll;
- sandbox-only event/provenance logging;
- isolated sandbox observability;
- canonical leakage guards;
- optional bounded read-only canonical references later.

Exit condition:
- sandbox Character + Location can be instantiated and exercised while canonical DB/runtime truth is unchanged.

---

## Track C3 — Character + Location Vertical Proof

Purpose: validate the architecture with high-value ontology types while preserving the second-character production gate.

Character scope:
- identity/basic profile;
- represented profile fields through existing ontology;
- initial skills/reference support when available;
- sandbox-only location membership;
- no canonical autonomy registration;
- no canonical relationship creation.

Location scope:
- identity/name/type;
- parent/containment;
- represented properties;
- sandbox spatial references;
- no canonical world graph mutation.

Acceptance:
- create manually;
- create as AI proposal;
- validate;
- activate in sandbox;
- edit/reroll/reset/delete;
- confirm no canonical mutation.

Exit condition:
- first end-to-end Creator-created content works entirely inside sandbox.

---

## Track C4 — Telegram Creator Studio v1

Purpose: give Creator a native creation surface.

Entry point concept:

`Observer Home -> 🛠 Creator Studio`

Minimum UX:
- Create;
- Sandbox Creations;
- Validation;
- Archive/Delete;
- Prepare Transmigration.

Per-type creation:

```text
Create Character
→ Build Manually | Generate with AI
→ Draft Preview
→ Edit / Reroll
→ Validate
→ Approve into Sandbox
```

AI mode:
- Creator supplies natural-language intent;
- bounded AI call returns structured proposal;
- no direct DB write;
- schema failures are surfaced;
- reroll can replace whole draft or selected fields later.

Telegram sandbox notifications must be visually separate from canonical Observer messages.

Exit condition:
- Creator can create and manage Character + Location sandbox objects without repository intervention.

---

## Track C5 — Transmigration Foundation

Purpose: safely promote sandbox creations into a target universe.

Deliverables:
- frozen sandbox revision selection;
- dependency closure selection;
- target universe selector/profile;
- target compatibility validation;
- conflict detection;
- deterministic canonical ID/reference plan;
- canonical mutation preview;
- explicit Creator approval;
- atomic transaction;
- rollback on failure;
- sandbox→canonical provenance mapping;
- canonical activation events.

Exit condition:
- a compatible non-character exemplar can be promoted safely on disposable acceptance state;
- character promotion remains policy-gated until the second-character gate opens.

---

## Track C6 — Universe Compatibility Profiles

Purpose: make transmigration target-aware and prepare future multiple universes.

Deliverables:
- universe registry/profile;
- realism/supernatural policy;
- technology/time/geography profiles;
- supported creation types;
- required systems;
- physics/physiology/capability policies;
- custom validators;
- compatibility result taxonomy.

Current production universe policy:
- conservative realism consistent with existing Observer Sandbox canon;
- supernatural/magic/impossible-physics systems are rejected for canonical promotion unless explicitly authorized by a future universe policy.

Future universes may adopt different policies without changing the generic creation socket types.

Exit condition:
- the same sandbox object can produce different compatibility outcomes for different target-universe profiles.

---

## Track C7 — Creation Type Expansion

After foundation stabilizes, add sockets incrementally.

Recommended order:

1. Skill
2. Item / Resource / Equipment
3. Job / Role
4. Organization / Faction
5. Service / Facility
6. Quest
7. Event / Action Template
8. World Element / Environment Feature
9. System / Rule-Module Descriptor

Each new type must reuse:
- common proposal envelope;
- sandbox lifecycle;
- validation layers;
- Telegram Creator Studio patterns;
- transmigration pipeline.

Do not implement a second bespoke creation framework per type.

---

## Track C8 — Rich Batch Worldbuilding

Purpose: create coherent groups of interconnected content.

Examples:
- clinic + staff + jobs + services;
- school + courses + teachers + schedules;
- faction + members + headquarters + resources;
- quest line + locations + items + rewards;
- neighborhood + businesses + residents.

Deliverables:
- dependency-aware batch graph;
- batch AI generation;
- partial edit/reroll;
- batch validation;
- sandbox activation as coherent unit;
- selected dependency closure transmigration.

Exit condition:
- Creator can create a meaningful small world package and validate it before canonical activation.

---

## Track C9 — Multiple Universe Creation

Long-term, not minimum implementation.

Purpose:
- create separate universes with different rule profiles;
- isolate all runtime state by universe;
- allow alternate realism/fantasy/science-fiction policies;
- target transmigration/import intentionally between universes where compatible.

Requirements before activation:
- universe registry stable;
- scope isolation proven;
- compatibility profiles mature;
- cross-universe references forbidden unless explicitly supported;
- lifecycle and persistence contracts validated.

---

## Relationship to Mind/Relationship Systems

Creator Creation Foundation comes **before** deeper Mind Engine continuation only to establish stable dynamic-world sockets and safe staging.

Do not delay Mind until all Creator Creation roadmap tracks are complete.

Minimum threshold before returning to MIND-F2:

- C0 Creator authority invariant documented/implemented;
- C1 common socket/proposal foundation implemented;
- C2 isolated Creation Sandbox implemented;
- C3 Character + Location sandbox proof implemented;
- C4 minimum Telegram Creator Studio works;
- basic transmigration contract exists or is documented strongly enough that current sandbox object model will not need redesign.

Then resume Mind foundation while later creation sockets expand incrementally.

---

## Second-character canonical gate

Creation Sandbox does not count as adding another real production character.

The current production-universe Character transmigration gate remains closed until:

- external-input/perception foundations remain healthy;
- Creator profile/body controls are production-stable;
- MIND-F2..F7 minimum foundations are complete;
- relationship adaptation foundation is complete;
- A3.3 interim planning scaffolding is reconciled;
- Foundation Completion Review v2 passes;
- Creator explicitly approves a character transmigration.

Until then, new characters are sandbox-only.

---

## Implementation philosophy

- docs first;
- minimum runnable vertical slices;
- no overbuilt generic framework before Character/Location proof;
- no duplicate engines for sandbox;
- no AI canonical write authority;
- no silent seed overwrite of Creator state;
- no blind transmigration;
- no assumption that structurally valid equals target-universe compatible;
- keep Telegram observability/control vertically complete;
- preserve current canonical world while experimentation grows around it.
