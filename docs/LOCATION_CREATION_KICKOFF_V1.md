# Sandbox Location Creation Kickoff v1

Status: **AUTHORIZED NEXT SLICE — I5.11**  
Date: 2026-08-21

## Why Location is next

Character and Item Creation are now mature enough to produce modern Sandbox content, but a viable world cannot be rebuilt from Characters and Items alone. A represented spatial graph is a prerequisite for placement, containment, access, action affordances and later Character runtime activation.

Therefore the immediate project priority is:

> **Complete Sandbox Location Creation before Real World reset/transmigration work begins.**

This slice uses the existing `docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`. Do not create a second Location schema.

All implementation must follow `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`.

---

## Required vertical

The Location Creation flow must implement the same shared Creation architecture already proven by Character and Item Creation:

```text
UNIVERSAL_LOCATION_SCHEMA_V1
→ registered Creation socket/adapter
→ Manual full-schema construction + AI full-schema structured fill
→ safe deterministic canonicalization
→ exact Location validation
→ dependency / parent / topology validation
→ write-free human preview + raw .txt export
→ explicit Creator approval
→ one atomic Sandbox-only materialization
→ approved Location detail/browse
→ Edit Preview -> Apply -> Done
→ cleanup/delete/archive
```

Manual and AI paths must converge on the same exact Location payload, validator and materializer.

---

## Structural requirements

I5.11 must preserve these existing contracts:

- Locations are stable technical identities, not display-name paths;
- structural hierarchy uses `contains`;
- dynamic physical presence uses `located_at` rather than structural containment;
- `connected_to` is topology and remains separate from containment;
- structural parent references must resolve to active same-Sandbox Locations;
- the structural parent graph must be acyclic;
- interface/topology destinations must resolve to active same-Sandbox Locations;
- access/authorization remains distinct from topology;
- unknown geometry remains unknown rather than fabricated;
- no arbitrary free-form `contents` bag is allowed.

---

## Embedded contents

A Location may be created with embedded Items/fixtures where the canonical Location schema permits it.

Embedded Items must reuse the exact current Item member schema and Item Batch semantics. There is no Location-specific weaker Item format.

Whole composition rule:

```text
Location payload
+ embedded Item members
+ local refs / parent refs / storage refs
→ validate entire dependency graph
→ one atomic Sandbox apply
```

If any required member or relationship fails, there are zero materialized writes from that proposal.

Movable Items normally use `located_at`, or `stored_in` when placed in a valid typed container. Structural fixtures may use the Location composition semantics defined by the canonical contracts; ordinary inventory storage must not be collapsed into structural `contains`.

---

## AI creation

The Creator must be able to use a short natural prompt. Technical schema burden belongs in the shared system-side authoring contract.

The provider-facing structured form must expose the complete supported Location creation-owned schema and reuse shared registered enum/unit/Item surfaces where possible.

AI remains a form filler only. It cannot:

- invent new schema fields;
- bypass Location validation;
- write Sandbox state directly;
- write canonical Real World state;
- activate runtime automatically.

Use Telegram `typing` feedback for noticeable generation latency, consistent with the Creation Implementation Standard.

---

## Review / approval UX

Normal review must be human-facing:

- readable names instead of technical IDs where practical;
- grouped stable Location sections;
- null/unused values hidden;
- embedded contents rendered as understandable members;
- parent/topology references resolved to names;
- human unit formatting;
- pagination where necessary;
- raw `.txt` technical export retained for audit/debugging.

Approval must remain explicit and materialize only into the Creation Sandbox.

Cancel before approval must produce zero materialized Location/Item state.

---

## Edit lifecycle

Location Edit should reuse the existing Creation Edit lifecycle rather than creating a separate CRUD path:

```text
preflight
→ pause only if a concrete runtime race requires it
→ edit
→ Preview
→ Apply
→ Done
→ restore exact pre-edit pause state
```

Use stale protection and audit evidence consistent with Character/Item Edit parity.

No runtime activation is implied by editing or approving a Location.

---

## Isolation acceptance

Acceptance must prove at minimum:

1. AI and Manual payloads converge on the same Location validator/materializer;
2. valid nested Location structure materializes correctly;
3. invalid/missing/cross-Sandbox parent references fail closed;
4. structural cycles fail before writes;
5. embedded Items use exact Item schema semantics;
6. invalid embedded dependency closure causes zero writes;
7. preview/export are write-free;
8. explicit approval is atomic and Sandbox-only;
9. approved detail/readback preserves expected Location and embedded Item facts;
10. Edit Preview/Apply/Done reuses the same schema validation and restores pause state where used;
11. `canonical_state_fingerprint()` proves Real World state is unchanged;
12. approved Location is not automatically runtime-active.

---

## What follows I5.11

After Location Creation acceptance, pause ordinary feature expansion and begin the approved Genesis transition:

```text
Real World prototype-content reset contract/audit
→ remove or disable legacy content reseeding
→ controlled content reset while preserving reusable systems
→ Transmigration foundation against the clean Real World
→ Genesis transmigration in dependency-safe order
→ runtime readiness/activation
→ future Reincarnation/Renewal for modern canonical content
```

Later I5.12–I5.15 work should be reconciled against this Genesis sequencing rather than automatically proceeding under the old roadmap order.
