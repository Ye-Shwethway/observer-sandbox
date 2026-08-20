# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-21**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. task-relevant canonical contracts/source
6. current branch/PR/CI/runtime evidence before completion or live claims.

For any Creator Creation work, `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md` is mandatory before material planning/coding/review/debugging.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.
Do not infer production deployment from merge alone.

---

## Current strategic checkpoint

The representative post-rollback Item Batch has been explicitly **approved by Creator**. Treat that acceptance gate as closed for sequencing.

The immediate authorized feature is now:

> **I5.11 — Sandbox Location Creation + Embedded Contents**

This is not merely the next ordinary Creator feature. It is the missing prerequisite for the approved Real World Genesis transition.

Characters and Items cannot form a runnable rebuilt world without represented Locations, containment/topology and valid placement. Therefore Location Creation must reach modern Creation-standard parity before any destructive Real World content reset.

Canonical kickoff docs:
- `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`
- `docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`
- `docs/LOCATION_CREATION_KICKOFF_V1.md`
- `docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`
- `docs/LOCATION_FIRST_GENESIS_DECISION_RECORD_V1.md`

---

## Approved Real World direction — prototype era will be retired

Creator has explicitly classified the current Real World content as prototype-era exemplars created before the present universal Creation architecture was mature.

This includes the current:
- Darian exemplar Character;
- Thorne Estate / hard-coded Location graph;
- Estate objects, fixtures and training equipment;
- legacy Item/inventory content associated with the exemplar world.

Do **not** spend development effort building a complex legacy-preservation or legacy-reincarnation bridge around that content.

Approved principle:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

The reset is **not authorized to execute yet**. Location Creation comes first.

---

## What will be preserved through the future reset

The future Genesis reset is a content reset, not an engine reset.

Retain and align reusable infrastructure such as:
- DB/schema foundation;
- simulation time/clock;
- weather/environment foundations;
- economy/money foundations;
- AI provider/model/binding infrastructure;
- generic events/actions/runtime;
- physiology/effects foundations;
- Mind/Memory foundations;
- grading, quantity, requirements and economic-value contracts;
- Creation Sandbox / schema / validator / materializer foundations;
- generic world/location runtime engines not intrinsically tied to prototype IDs;
- audit/provenance infrastructure.

Content-bound seeders/defaults must later be removed, disabled, generalized or converted to optional fixtures so restart/deploy cannot recreate retired prototype content.

---

## Approved sequence from here

```text
NOW: I5.11 Sandbox Location Creation + Embedded Contents
→ accept Location + embedded Item vertical
→ audit exact Real World keep/wipe dependency set
→ remove/disable legacy Darian/Estate/Item reseeding authority
→ controlled Real World prototype-content reset
→ preserve shared time/weather/economy/runtime infrastructure
→ implement Transmigration foundation against clean Real World
→ Genesis transmigration: Locations -> Items/fixtures -> Characters
→ validate runtime readiness / affordances
→ explicit activation
→ later Reincarnation/Renewal for modern canonical content
```

Do not automatically continue into the old I5.12–I5.15 order after I5.11 without reconciling those slices against this Genesis transition.

---

## I5.11 implementation lock

Do **not** invent another Location schema. `docs/UNIVERSAL_LOCATION_SCHEMA_V1.md` already exists and is authoritative.

Required Location vertical:

`Location schema -> registered Creation socket -> Manual full-schema + AI full-schema -> canonicalize -> validate -> dependency/graph validation -> write-free review + .txt -> explicit approval -> atomic Sandbox-only materialization -> approved detail -> Edit Preview/Apply/Done -> cleanup`.

Required semantics:
- stable Location identity independent of display path/name;
- same-Sandbox active parent validation;
- acyclic structural parent graph;
- structural hierarchy through `contains`;
- topology through `connected_to`;
- dynamic presence through `located_at`;
- access distinct from topology;
- interface destinations must resolve to active same-Sandbox Locations;
- no arbitrary `contents` bag;
- embedded Items reuse exact current Item schema/Batch semantics;
- whole Location + embedded Item graph validates before one atomic write;
- movable Items normally use `located_at` or valid `stored_in` containers;
- human-readable review + raw `.txt` technical export;
- Telegram `typing` during noticeable AI generation;
- Cancel before approval = zero writes;
- approved Location does not become runtime-active automatically;
- `canonical_state_fingerprint()` proves Real World isolation;
- Location Edit reuses shared schema/validator and Preview/Apply/Done with exact pause restoration where pausing is actually required.

---

## Item baseline / acceptance lock

Creator deliberately selected commit `b59e632aa8e31647b85eeb244a4436c31e9e1e9d` as the acceptable Item Creation behavior after later realism tightening caused repeated rejection loops.

Rollback PR #372 restored that behavior as merge `6fe07ec4fde0375b29477c026e4ace991f8834ce` while preserving history.

Do not re-add/tighten fine-grained Item realism validation without explicit Creator authorization.

The approved representative camping-style multi-class Item Batch is sufficient to close the current representative acceptance gate. Do not regenerate it merely to delay Location work.

Retained Item ontology:
`Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations remain distinct:
`contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by`.

---

## Transmigration after Genesis reset

The approved `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md` remains authoritative.

Transmigration remains an explicit validated atomic promotion, not table copy/paste:

`freeze Sandbox revision -> schema/dependency validation -> target-universe compatibility -> canonical IDs/refs -> conflict check -> mutation plan -> Creator preview -> explicit approval -> atomic canonical materialization -> provenance`.

The clean Real World target should simplify this path by removing prototype-era schema/content coexistence.

Genesis dependency order starts with spatial structure:
1. Locations/root topology;
2. Items/fixtures/containers and placement;
3. Characters with valid starting Location bindings;
4. runtime readiness/affordance validation;
5. explicit runtime activation.

A Character must not be activated without a valid represented Location.

---

## Reincarnation / Renewal — later

Reincarnation remains planned, but it is **not** a mechanism for preserving or upgrading the current prototype Darian/Estate/legacy Item content.

Its future purpose is modern-to-modern renewal:

`modern canonical v1 -> Renew in Sandbox -> edit/regenerate/test -> compatibility + diff -> explicit Creator approval -> canonical v2`.

Because both source and replacement originate from modern Creation/Transmigration contracts, future renewal should avoid most prototype-to-modern inconsistencies.

---

## Retained universal locks

- Create anywhere safely; canon nowhere automatically.
- Sandbox-created content never transmigrates automatically.
- Target-universe compatibility validation precedes transmigration.
- `runtime_ready != running`; Created is not alive.
- `canonical_state_fingerprint()` remains a high-value isolation invariant.
- Full autonomous Sandbox ticking remains unauthorized unless Creator explicitly expands scope.
- Until the reset is actually implemented and verified, the current Real World prototype content still exists; do not claim otherwise.
- Do not make production/deploy/live claims without current evidence.

---

## Exact resume sentence

**The Item representative acceptance gate is approved and closed. The immediate authorized slice is I5.11 Sandbox Location Creation + Embedded Contents. Read the mandatory Creation Standard, existing Universal Location Schema, Location kickoff contract and Location-first Genesis decision record, then implement the shared schema-driven Manual/AI -> canonicalize -> validate graph -> preview/export -> explicit atomic Sandbox approval -> approved detail -> Edit lifecycle with zero Real World mutation. Do not wipe the Real World yet. After Location acceptance, execute the approved Genesis transition: audit/reset the prototype Darian/Thorne Estate/legacy Item content, remove legacy reseeding authority while preserving reusable time/weather/economy/runtime foundations, then implement Transmigration against the clean target and rebuild canonical content in dependency-safe order: Locations first, Items/fixtures second, Characters third, then readiness/activation. Reincarnation is deferred for later modern canonical renewals.**
