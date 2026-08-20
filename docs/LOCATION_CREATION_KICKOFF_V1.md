# Sandbox Location Creation Kickoff v1

Status: **AUTHORIZED NEXT FEATURE FAMILY — SCHEMA REFINEMENT FIRST**  
Date: 2026-08-21

## Why Location is next

Character and Item Creation can already produce modern Sandbox content, but a viable rebuilt universe cannot activate Characters or place Items without represented spatial structure.

Therefore:

> **Complete modern Sandbox Location Creation before Real World reset/transmigration work begins.**

Canonical implementation plan:

`docs/LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`

Mandatory meta-contract:

`docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`

---

## Schema-first clarification

`docs/UNIVERSAL_LOCATION_SCHEMA_V1.md` and `src/observer_sandbox/location_creation_schema.py` are the existing authoritative Location foundation. They must be **refined**, not discarded and not bypassed with a parallel Location ontology.

Creator-approved refinement areas are:

- optional Geography;
- explicit Boundary semantics;
- richer registry-backed interface kinds;
- registry-backed functional/facility/resource/capability classification;
- stable definition/configuration vs initial/runtime-state separation;
- minimal control/ownership semantics;
- Location-specific universal grading evidence/profile.

Because exact-schema fields may change, the first slice must explicitly decide whether compatibility allows the current `location-v1` identifier to remain or whether the refined exact payload becomes a successor version such as `location-v2`.

Rule:

> **No UI/AI/materialization implementation begins until the refined exact versioned Location schema and validator contract are locked.**

This is schema evolution of the existing Location model, not a second competing model.

---

## Location grading lock

Location participates in the existing universal grading architecture:

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived GradeProfile`

Retain current `location-completeness-v1` as the mandatory representation-completeness dimension.

Initial/refinement candidates:

- completeness — mandatory;
- spatial scale — evidence/reference gated, magnitude not quality;
- infrastructure/facility capability — registry evidence gated;
- connectivity/mobility — graph evidence gated and separate from access;
- asset value — economy/reference gated;
- security/protection — deferred until an authoritative raw security-evidence contract exists.

AI/Creator forms never author final grades, thresholds, evaluator ids or reference profiles.

Do not create an automatic overall Location grade without an explicit approved composite semantic.

---

## Required Creation vertical after schema lock

```text
refined versioned Location schema
→ registered Creation socket/adapter
→ Manual full-schema construction + AI full-schema structured fill
→ safe deterministic canonicalization
→ exact Location validation
→ dependency / parent / topology validation
→ write-free human preview + raw .txt export
→ explicit Creator approval
→ one atomic Sandbox-only materialization
→ approved Location detail/browse + GradeProfile
→ Edit Preview -> Apply -> Done
→ cleanup/delete/archive
```

Manual and AI paths converge on the same exact Location payload, validator and materializer.

---

## Structural requirements

Preserve:

- stable technical Location identity independent of display path/name;
- structural hierarchy through `contains`;
- dynamic physical presence through `located_at`;
- topology/traversability separate from containment;
- access authorization separate from topology and current operating state;
- active same-Sandbox parent validation;
- acyclic structural Location graph;
- explicit interface destinations/local refs;
- unknown geometry/geography remains unknown rather than fabricated;
- no arbitrary free-form `contents` bag.

---

## Embedded composition

Nested child Locations and embedded Items must reuse their exact authoritative member schemas.

Whole composition:

`Location members + Item members + local refs + structural/storage/placement relations -> validate complete dependency graph -> one atomic Sandbox apply`

Any failed member/dependency results in zero materialized writes.

Ordinary movable Items use `located_at`, or `stored_in` when a valid typed container exists. Structural containment must not replace inventory storage or ownership.

---

## AI / review / edit UX

- Creator prompts remain short and natural;
- provider receives the complete supported structured fill schema;
- AI remains form filler only;
- Telegram `typing` is used for noticeable generation latency;
- review is human-facing with names/units resolved where practical;
- raw `.txt` technical export remains available;
- Cancel before approval causes zero writes;
- approval is explicit and Sandbox-only;
- approved Location is not runtime-active automatically;
- Edit reuses the exact current schema/validator, stale guard, Preview/Apply/Done and exact pause restoration where pausing is actually required.

---

## Implementation slices

The canonical detailed breakdown is in `LOCATION_CREATION_IMPLEMENTATION_PLAN_V1.md`:

- **L11.0** Schema Refinement + Grading Contract
- **L11.1** Exact Validator + Registry/Grading Foundation
- **L11.2** Sandbox Persistence + Graph Materializer
- **L11.3** Manual Full-Schema Creation
- **L11.4** AI Full-Schema Creation
- **L11.5** Nested Composition + Embedded Items
- **L11.6** Detail/Browse + Edit Parity
- **L11.7** Full Location Vertical Acceptance

Only after L11.7 closes should the approved Genesis reset/transmigration transition begin.

---

## Isolation acceptance

Acceptance must prove:

1. exact schema/validator authority;
2. Manual/AI convergence;
3. valid nested Location graph materialization;
4. invalid/missing/cross-Sandbox parents fail closed;
5. structural cycles fail before writes;
6. embedded Items use exact Item semantics;
7. dependency failure causes zero writes;
8. preview/export are write-free;
9. explicit approval is atomic and Sandbox-only;
10. derived Location grades come only from represented evidence/registered policy;
11. approved detail/readback preserves expected facts and grades;
12. Edit reuses the same exact schema/validator;
13. `canonical_state_fingerprint()` proves Real World state unchanged;
14. approved Location is not automatically runtime-active.

---

## What follows

After Location Creation acceptance:

`prototype-content reset audit -> remove/disable legacy reseeding -> controlled Real World content reset while preserving reusable systems -> Transmigration foundation -> Genesis Locations -> Items/fixtures -> Characters -> readiness/activation -> future modern Reincarnation/Renewal`

The destructive reset is not authorized before Location acceptance.
