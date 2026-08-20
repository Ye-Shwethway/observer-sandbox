# Real World Reset & Genesis Plan v1

Status: **APPROVED DIRECTION — DOCS FIRST**  
Date: 2026-08-21

## Purpose

Observer Sandbox is transitioning from its prototype-era hard-coded Real World content to a schema-driven universe-building workflow.

The current Real World Characters, Locations, Items and Estate/world fixtures were created as early exemplars before the current Creation Sandbox, universal schemas, Creation sockets and transmigration architecture existed. They are not required to be preserved as canonical production content.

The approved direction is therefore:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

This is a content reset, not an engine reset.

---

## Sequencing lock

The Real World reset does **not** happen immediately.

The current next feature remains:

> **I5.11 — Sandbox Location Creation + Embedded Contents**

Reason: Characters and Items cannot form a runnable canonical world without represented Locations. Location Creation must reach the same modern Creation-standard maturity as Character and Item Creation before the prototype Real World is wiped.

Approved order:

```text
complete Sandbox Location Creation
→ verify Location + embedded Item Creation acceptance
→ define and execute controlled Real World prototype-content reset
→ implement/activate transmigration foundation against the clean target
→ transmigrate fresh Locations / Items / Characters in dependency-safe order
→ rebuild runtime readiness and canonical world activity
→ later add Reincarnation/Renewal for modern canonical content
```

Do not wipe the current Real World content before the Location Creation vertical is ready enough to rebuild a viable spatial world.

---

## What the future reset retires

The controlled reset will retire prototype-era canonical content such as:

- current exemplar Characters, including Darian as an early implementation exemplar;
- current Thorne Estate Location graph and other hard-coded exemplar Locations;
- current Estate objects, fixtures and training equipment;
- current legacy Item definitions/stacks and prototype inventory content where they belong to the exemplar world;
- prototype relations, placement and ownership records that exist only because of the retired content;
- content-specific bootstrap assumptions and hard-coded exemplar IDs that would otherwise recreate or privilege the retired world.

The exact deletion set must be derived from a pre-reset dependency audit and executed atomically or through a bounded deterministic migration.

The reset must not leave orphaned active references.

---

## What the reset preserves

Reusable platform/system infrastructure is retained and aligned rather than discarded, including where applicable:

- database/schema infrastructure;
- simulation time and clock architecture;
- environment/weather foundations;
- economy/money foundations;
- AI provider/model/binding infrastructure;
- generic event/action infrastructure;
- generic physiology/effect engines;
- Character Mind/Memory foundations;
- shared grading, quantity, requirements and value-policy contracts;
- Creation Sandbox infrastructure;
- universal Creation schemas/validators/materializers;
- generic world/location/runtime engines that are not intrinsically tied to prototype content;
- audit/provenance infrastructure;
- future target-universe policy and compatibility infrastructure.

Preservation does not mean every current seed row survives unchanged. Content-bound seeders or exemplar defaults must be removed, disabled, generalized or converted into optional fixtures so a restart cannot silently recreate retired content.

---

## Prototype archive policy

The active Real World does not need duplicate legacy content after reset.

Before destructive cleanup, preserve enough evidence for debugging and historical recovery through one of the following bounded mechanisms:

- a pre-reset database backup/snapshot; and/or
- compact migration/audit records identifying the reset revision and retired content set.

Prototype content must not remain active merely to preserve history.

Historical/archive material has zero runtime authority.

---

## Post-reset canonical content authority

After the Genesis reset, new canonical world content should originate through the modern Creation path:

```text
Creator intent
→ Draft
→ Creation Sandbox
→ schema/domain validation
→ Sandbox approval/test
→ target-universe compatibility
→ Transmigration preview
→ explicit Creator approval
→ atomic canonical materialization
```

Ordinary seed/import/deploy initialization must not recreate the old exemplar content or overwrite explicitly approved canonical creations.

Canonical principle remains:

> **Create anywhere safely; canon nowhere automatically.**

---

## Genesis dependency order

A fresh canonical universe must be materialized in dependency-safe order.

Initial expected order:

1. universe/root policy and retained infrastructure;
2. Locations and structural topology;
3. embedded/freestanding Items, fixtures and containers;
4. Characters and their valid starting Location bindings;
5. runtime readiness / action affordance validation;
6. runtime activation only after explicit readiness gates pass.

A Character must not be activated into a world without a valid represented Location.

`Created != running` and `runtime_ready != running` remain authoritative.

---

## Location Creation is therefore the immediate prerequisite

Before reset work begins, I5.11 must prove the modern Location vertical using the existing `UNIVERSAL_LOCATION_SCHEMA_V1.md` and the locked Creation Implementation Standard.

Required minimum:

- complete Manual/full-schema Location construction;
- complete AI structured fill aligned to the canonical Location schema;
- deterministic canonicalization and validation;
- structural parent/dependency checks;
- embedded Items using exact current Item schemas/contracts;
- whole-graph validation before writes;
- one atomic Sandbox apply;
- human preview and raw `.txt` export;
- approved Location detail/browse;
- Edit `Preview -> Apply -> Done` parity where applicable;
- Sandbox isolation and zero canonical mutation;
- no automatic runtime activation.

Only after this vertical is accepted should the project begin destructive Real World content reset work.

---

## Transmigration after reset

The existing approved Transmigration architecture remains the target promotion model.

Transmigration is not raw table copy. It remains:

```text
freeze approved Sandbox revision
→ validate schema/dependencies
→ resolve target universe
→ validate universe compatibility/policy
→ resolve canonical IDs/references
→ detect conflicts
→ build mutation plan
→ Creator preview
→ explicit approval
→ atomic canonical transaction
→ provenance link
```

The clean post-reset Real World should make this path substantially simpler because it no longer needs to coexist with incompatible prototype-era content contracts.

---

## Reincarnation / Renewal — later modern-content feature

Reincarnation is retained as a future feature, but it is **not** the mechanism used to preserve or upgrade the current prototype content.

Its intended future role is:

> renew an already-modern canonical creation by staging a new schema-compatible incarnation in the Sandbox, validating and testing it, showing a high-signal diff, then explicitly replacing the canonical incarnation while preserving the intended stable identity and runtime continuity.

Typical future flow:

```text
modern canonical object v1
→ Renew in Sandbox
→ edit/regenerate/test
→ compatibility + diff
→ Creator approval
→ canonical v2
```

Because both source and replacement originate from the modern Creation contracts, future Reincarnation should avoid most prototype-to-modern incompatibility problems.

---

## Non-goals of the current Location slice

I5.11 does not itself:

- wipe Real World content;
- transmigrate Sandbox content;
- activate new canonical Characters;
- implement Reincarnation;
- rebuild every retained platform subsystem;
- start autonomous Sandbox ticking.

Its job is to finish the missing spatial Creation prerequisite cleanly.

---

## Acceptance of this plan

This direction is satisfied when the repository and later implementation demonstrate that:

1. Location Creation is completed before destructive Real World reset;
2. prototype Characters/Locations/Items are explicitly classified as disposable exemplars rather than preservation constraints;
3. reusable system infrastructure is retained;
4. reset removes or disables legacy reseeding paths that would recreate retired content;
5. post-reset canonical content enters through explicit validated transmigration;
6. Genesis ordering requires Locations before Character activation;
7. future Reincarnation targets modern canonical content rather than serving as a legacy-upgrade bridge.
