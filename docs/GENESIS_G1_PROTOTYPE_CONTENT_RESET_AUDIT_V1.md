# Genesis G1 — Prototype Content Reset Audit & Contract v1

Status: **G1 AUDIT CONTRACT — NON-DESTRUCTIVE**  
Date: 2026-09-04

## Purpose

This document is the evidence-backed contract for the future controlled Real World prototype-content reset.

G1 does **not** authorize deletion, mutation, reseeding changes, runtime activation, or transmigration. Its job is to define what later G2/G3 work must preserve, remove, generalize, delete, verify, and recover.

Authoritative direction remains:

> **Preserve reusable universe infrastructure; retire prototype content; rebuild canonical content from modern Sandbox creations through explicit transmigration.**

This is a **content reset, not an engine reset**.

---

## Safety boundary

Until a later explicitly authorized destructive slice:

- do not delete Real World rows;
- do not alter the production SQLite database;
- do not remove current seeders from production runtime;
- do not transmigrate Sandbox creations;
- do not activate any new canonical Character;
- do not modify Creation Sandbox records as part of reset preparation;
- do not treat historical/archive material as runtime authority.

The future reset must be preceded by a verified database backup/snapshot and must be bounded by deterministic preflight/postflight checks.

---

## Confirmed current production bootstrap chain

`pyproject.toml` exposes `sandboxctl = observer_sandbox.cli:main`.

`sandboxctl init` calls `runtime.initialize()`.

More importantly, `runtime.status()` also calls `_initialize_conn()` before reporting health. Therefore status/health execution currently has **write-capable bootstrap semantics**, not read-only inspection semantics.

Current `_initialize_conn()` order includes:

1. schema migration;
2. reusable provider/profile/schema seeds;
3. `seed_home_and_darian()`;
4. `ensure_information_media_seed()`;
5. `seed_initial_economy()`;
6. memory/profile values;
7. `seed_estate_campus()`;
8. spatial familiarity;
9. skill hierarchy reconciliation;
10. simulation clock;
11. `seed_home_inventory()`;
12. generic and represented action/task runtime seeds;
13. economic value profiles/coverage;
14. runtime defaults;
15. default-actor resolution/location recovery/progression settlement;
16. legacy actor-runtime migration.

### Consequence

Deleting prototype rows from the database without first changing bootstrap authority is unsafe: a later init/status/service-health cycle can silently recreate or re-bind retired content.

**G2 must remove/generalize content-specific bootstrap authority before G3 destructive reset.**

---

## Confirmed prototype source files

### Character

Production `config/characters/` currently contains only:

- `darian.canonical.json`;
- `darian.runtime-defaults.json`;
- `registry.json`.

No Quasi or Elias canonical Character seed file exists in the current production character seed directory. They must therefore **not** be assumed to be active seeded Character rows without separate database evidence.

Confirmed prototype Character ID:

- `char_darian`

### Base world / Estate

`config/worlds/home.v1.json` seeds:

- root universe `world_observer_universe`;
- Thorne Estate and its interior Location graph;
- Estate fixtures/objects;
- Estate topology/connections;
- Darian start Location `loc_thorne_estate_master_suite`.

Confirmed Estate root:

- `loc_thorne_estate`

The file includes the Estate floors, rooms, boundary and numerous hard-coded object IDs under `obj_thorne_estate_*`.

### Estate campus

`config/worlds/estate_campus.v1.json` is loaded by `seed_estate_campus()` and adds further Estate-campus Locations, objects and connections. This is content-bound to the retired exemplar Estate and is part of the prototype reseed surface.

### Estate inventory

`config/worlds/home.inventory.v1.json` has:

- `owner_id = loc_thorne_estate`;
- Estate fixture containers;
- `stack_estate_*` inventory stack entities;
- a prototype stock migration marker/revision.

`seed_home_inventory()` also calls `seed_item_definitions()`. This means G2 must **split generic reusable Item definitions from Estate-specific inventory materialization** rather than blindly removing the whole inventory module.

### Darian economy

`config/economy/darian.v1.json` binds economy state to:

- represented Character `char_darian`;
- economic entity `econ_char_darian`;
- Darian account(s);
- Darian assets/liability;
- `asset_thorne_estate` represented by `loc_thorne_estate`.

This is prototype content, while the economy schema/engine itself is reusable infrastructure.

### Information/media exemplar

`ensure_information_media_seed()` is hard-bound to:

- `obj_thorne_estate_living_media_console`.

It may only remain after G2 if generalized to operate on represented media devices without privileging that retired Estate object. The generic information/media subsystem remains KEEP.

### Represented task fixtures

Current production initialization includes several content-bound represented task/simulator seeders.

Confirmed hard-bound examples include:

- technology diagnostic simulator in `loc_thorne_estate_intelligence_hub`;
- tactical assessment simulator in `loc_thorne_estate_intelligence_hub`;
- represented skill runtime batch simulators under Thorne Estate Intelligence Hub / Training Hall.

These fixture entities are prototype content even when the underlying action/task/skill contracts are reusable.

By contrast, current controlled-H2H and field-medicine stabilization seeders explicitly register generic action vocabulary without fabricating live fixtures. Their generic definitions are infrastructure and should not be removed merely because Darian/Thorne Estate are retired.

---

## G1 classification matrix

### KEEP — reusable infrastructure

Keep schema/code/contracts and non-content-specific rows needed for the platform, including:

- database/schema infrastructure and migrations;
- `schema_meta` schema versioning machinery;
- Creation Sandbox schema/tables/data;
- universal Creation schemas, registries, validators and materializers;
- simulation clock/time architecture;
- generic environment/weather foundations;
- generic economy/money schema and services;
- AI providers/models/bindings infrastructure;
- generic action definitions and action engine;
- generic physiology/effect engines;
- Character Mind/Memory schema/contracts;
- shared grading, quantity, requirement and value-policy contracts;
- generic information/media schema/services;
- audit/provenance/event infrastructure;
- generic world/location/runtime engines;
- generic controlled-H2H action vocabulary;
- generic field-medicine stabilization action vocabulary;
- generic Item definitions that are valid independently of the Thorne Estate exemplar;
- target-universe policy / future compatibility infrastructure.

KEEP does not mean every current row survives unchanged. A reusable table may contain prototype rows that belong in WIPE.

### WIPE — confirmed prototype content

Future G3 reset must remove, through a bounded deterministic migration, the active prototype content set including at minimum:

- `char_darian` and Character-owned canonical/profile/runtime state;
- Thorne Estate Location graph rooted at `loc_thorne_estate`;
- Estate campus Locations added by `estate_campus.v1.json`;
- Estate fixtures/objects from the base world and campus seeds;
- `stack_estate_*` inventory entities/stacks and Estate placement/ownership relations;
- prototype inventory migration/runtime markers that exist only for the Estate stock seed;
- Darian-specific economy rows (`econ_char_darian`, accounts, assets, liabilities, valuations and seed-specific transactions where identified by the bounded preflight);
- `asset_thorne_estate` and its valuation rows;
- Estate-bound media-device projection for `obj_thorne_estate_living_media_console`;
- Estate-bound represented simulator/task fixture entities;
- content-specific relations, placements, ownership, actor runtime rows, actions/modifiers/participants and other rows whose authority exists only through the retired prototype entities.

Do **not** infer Quasi/Elias Character deletion by name alone. They are deletion candidates only if pre-reset production DB audit proves corresponding active prototype entities/rows exist.

### RESEED-AUTHORITY REMOVE / GENERALIZE — G2

G2 must make normal initialize/status/deploy health unable to recreate or privilege retired prototype content.

Confirmed G2 targets:

1. `seed_home_and_darian()` — remove from ordinary production initialization or convert to an explicitly opt-in historical/dev fixture path.
2. `seed_estate_campus()` — remove from ordinary production initialization or make it fixture-only.
3. `seed_home_inventory()` — split generic Item-definition registration from Estate stack/container materialization; Estate materialization becomes fixture-only/retired.
4. `seed_initial_economy()` — remove Darian-specific canonical seeding from ordinary startup; retain generic economy engine.
5. `ensure_information_media_seed()` — remove hard-coded Thorne Estate TV bootstrap; generalize or fixture-gate it.
6. `seed_technology_diagnostic_runtime()` — separate reusable action/task contract from Estate simulator fixture materialization.
7. `seed_tactical_assessment_runtime()` — same separation.
8. `seed_represented_skill_runtime_batch()` — separate reusable represented-task definitions from Thorne Estate simulator fixture materialization.
9. any additional content-bound memory/familiarity/value/bootstrap rows discovered by the final DB preflight must be generalized or fixture-gated before G3.

Generic action vocabulary seeders that create no live exemplar fixture remain KEEP unless a later audit proves content coupling.

---

## Critical empty-world runtime requirement

The future post-reset canonical Real World may legitimately contain **zero active Characters** until Genesis transmigration reaches the Character phase.

Current runtime does not fully support that state:

- `_initialize_conn()` calls `ensure_default_actor_id()` and then may continue actor-specific migration logic;
- `status()` calls `resolve_actor_id()` unconditionally;
- `resolve_actor_id()` raises `KeyError("No character is available")` when no Character exists.

Therefore G2/G3 must introduce explicit healthy **empty-canonical-world semantics**.

Required behavior after the change:

- init/migration succeeds with zero canonical Characters;
- status/health succeeds with zero canonical Characters;
- no synthetic/default Character is created merely to satisfy health;
- actor runtime recovery/progression runs only when represented actors exist;
- `default_actor_id` is absent/null when no valid actor exists;
- runtime remains not-running until explicit readiness/activation gates are later satisfied.

This is a reset blocker, not optional polish.

---

## Dependency and deletion rules

### Core entity cascades already confirmed

The base schema uses `entities(id)` as the represented-entity root.

Confirmed FK behavior includes:

- `relations.source_id/target_id -> entities(id) ON DELETE CASCADE`;
- `fields.entity_id -> entities(id) ON DELETE CASCADE`;
- `character_profiles.entity_id -> entities(id) ON DELETE CASCADE`;
- Character profile child rows cascade through `character_profiles`;
- `action_instances.actor_id -> entities(id) ON DELETE CASCADE`;
- `action_instances.place_id/target_id -> entities(id) ON DELETE SET NULL`;
- `action_participants.entity_id -> entities(id) ON DELETE CASCADE`;
- `actor_runtime.actor_id -> entities(id) ON DELETE CASCADE`;
- `active_modifiers.subject_id -> entities(id) ON DELETE CASCADE`;
- `active_modifiers.source_entity_id -> entities(id) ON DELETE SET NULL`;
- `event_participants.entity_id -> entities(id) ON DELETE CASCADE`;
- `inventory_stacks.entity_id -> entities(id) ON DELETE CASCADE`.

FK cascades are useful but **not sufficient reset authority**. Several economy/media/runtime/provenance tables use their own identifiers or nullable represented references and must be audited explicitly rather than assumed to disappear when an entity root is deleted.

### Required future G3 ordering

The final executable migration must use a transaction and perform logical cleanup in this order, even where SQLite cascades can remove some child rows automatically:

1. acquire exclusive/bounded maintenance authority and prevent concurrent canonical writers;
2. verify G2 reseed authority is absent and empty-world health support is deployed;
3. create/verify backup snapshot and record reset revision;
4. freeze/pause canonical runtime activity without touching Creation Sandbox;
5. identify the exact prototype entity set from stable IDs/source revisions plus dependency queries;
6. detach/delete non-entity-root content dependencies that would survive or block entity deletion, especially economy/media/value/runtime marker rows;
7. clear prototype pending actor/action/runtime references as required;
8. delete prototype Character roots and Estate inventory/fixture/Location roots in dependency-safe order;
9. clear only content-bound runtime markers/default actor/world-start assumptions that point at retired content;
10. preserve generic definitions/infrastructure and the Creation Sandbox;
11. run foreign-key/orphan checks inside the same bounded migration;
12. commit atomically only if all invariants pass; otherwise rollback;
13. restart/health-check under empty-world semantics and prove no retired content reseeds.

The implementation may collapse steps through verified CASCADE behavior, but the contract must not depend on accidental deletion order.

---

## Root universe decision

`world_observer_universe` is currently both:

- the root entity seeded by `home.v1.json`; and
- the runtime default `world_id` in `_initialize_conn()`.

G1 does **not** classify this root as disposable Estate content by assumption.

For Genesis, retain the target universe/root identity if it is still the approved Real World universe, but remove its dependence on the Thorne Estate as required start content. If later target-universe policy chooses a new canonical universe identity, that must be an explicit separate migration decision rather than an incidental Estate cascade.

Default rule for G2/G3 planning: **KEEP the universe root; REMOVE hard-coded Estate/Character bootstrap assumptions from it.**

---

## Item-definition boundary

Do not wipe `entity_definitions` wholesale.

The Estate inventory seeder uses reusable definitions such as food definitions from the universal Item catalog, while `stack_estate_*` are exemplar-world instances.

Contract:

- generic reusable definition: KEEP;
- Estate stack/item instance: WIPE;
- Estate-only represented simulator/fixture definition or projection: WIPE or retire from active seed authority if it has no reusable contract role;
- ambiguous definition: require provenance/reference audit before deletion.

---

## Runtime-state boundary

`runtime_state` is mixed infrastructure + content binding and must never be wholesale-cleared.

Expected KEEP examples:

- simulation clock/time state that is not content-specific;
- generic system configuration where valid after reset.

Expected REMOVE/RESET examples when present:

- `default_actor_id` if it points to retired Character;
- Estate world identity/spatial revision markers if they only describe retired seed content;
- `estate_campus_revision`;
- Estate inventory seed/migration revision markers;
- content-bound information/media scheduler state if its only device is retired;
- pending/retry/lease state that references retired actor/action content.

Every runtime-state key must be classified by preflight rather than cleared by prefix guess alone.

---

## NO-TOUCH set

G2/G3 must not mutate or purge the following merely because they coexist in the same database:

- Creation Sandbox objects, revisions, sessions and audits;
- universal Creation schema registries/contracts;
- unrelated Real World content not proven to be part of the prototype reset set;
- AI provider/model configuration unless a row is explicitly Character-scoped to retired content;
- generic action/item/profile definitions that remain valid platform contracts;
- schema migrations/version history;
- audit/provenance evidence required to explain the reset;
- target-universe policy infrastructure;
- generic clock/environment/economy/information engines.

A later migration must use exact IDs, provenance/source revisions and FK/reference discovery. Broad `DELETE FROM <table>` operations against mixed-purpose tables are forbidden unless that table is proven to contain only disposable prototype content.

---

## Rollback / archive contract

Before G3 destructive execution:

1. stop or bound concurrent canonical writers;
2. create a byte-for-byte SQLite backup/snapshot using the deployment-approved mechanism;
3. record backup path/id, file size and checksum in operator evidence;
4. record the pre-reset canonical fingerprint and reset revision;
5. preserve a compact retired-ID manifest/audit record;
6. verify the backup can be opened and passes SQLite integrity check before mutation;
7. keep the backup outside the active runtime DB path so service restart cannot overwrite it.

Rollback trigger includes any failed invariant, orphaned reference, unexpected Creation Sandbox change, failed empty-world health check, or retired-content reseed after restart.

Historical backup/archive has **zero runtime authority**.

---

## Mandatory pre-reset DB audit

Immediately before future G3 execution, query the actual production DB rather than relying only on repository seeds.

The bounded audit must enumerate:

- all active Character entities and their profile/runtime descendants;
- all descendants/fixtures under `loc_thorne_estate` plus campus seed IDs;
- all `stack_estate_*` rows and inventory relations;
- all relations where either endpoint is in the retirement set;
- action instances/participants/modifiers/events referencing retirement-set entities;
- economy entities/accounts/assets/liabilities/valuations/transactions tied to Darian/Estate;
- media-device/information rows tied to retired devices;
- value/economic profile rows tied to retired entities;
- memory/mind/familiarity rows tied to retired Character/Locations;
- AI bindings whose scope is the retired Character;
- runtime-state keys whose values identify retired content;
- any active Quasi/Elias or other prototype-era Character rows not represented by current seed files;
- every FK reference into the retirement set using SQLite FK/schema introspection where practical.

Any unexpected dependent row must fail closed and extend the reviewed deletion manifest before mutation.

---

## Post-reset acceptance invariants

G3 is not complete until all are proven after commit **and after a normal service restart/status health cycle**:

1. `char_darian` is absent from active canonical entities/profile/runtime state.
2. `loc_thorne_estate` and its retired Estate/campus descendants are absent.
3. Estate fixtures and `stack_estate_*` instances are absent.
4. Darian/Estate-specific economy rows are absent.
5. Estate-bound media/simulator projections are absent.
6. no active relation/reference points at a retired entity.
7. no retired content reappears after init/status/restart.
8. zero canonical Characters is a healthy supported state.
9. no Character is auto-created or auto-activated.
10. generic reusable schema/engines/definitions remain available.
11. Creation Sandbox fingerprint/state is unchanged by the reset.
12. SQLite foreign-key and integrity checks pass.
13. runtime health passes without requiring Darian or Thorne Estate.
14. canonical runtime remains not-running until explicit future Genesis readiness/activation.
15. new canonical content can only enter through the future explicit validated Transmigration path.

---

## Slice handoff

### G1 closes when

- this KEEP/WIPE/reseed/dependency/no-touch/rollback/post-reset contract is reviewed;
- all content-bound startup seeders are classified;
- empty-world health is recognized as a hard prerequisite;
- the exact destructive set remains deferred to production DB preflight rather than guessed from source alone;
- no destructive canonical mutation has occurred.

### G2 — next after G1 approval

Implement **legacy reseed authority removal/generalization + healthy empty-canonical-world runtime**.

G2 must prove through tests and deployed runtime health that ordinary init/status/restart cannot create Darian/Thorne Estate/Estate inventory/economy/simulator fixtures and can remain healthy with no canonical Character.

### G3 — only after G2 is production-green and explicitly authorized

Execute the controlled content reset using a reviewed preflight manifest, verified backup, bounded transaction, rollback checks and post-restart no-reseed verification.

---

## Evidence sources audited for v1

- `docs/CREATOR_REAL_WORLD_RESET_AND_GENESIS_PLAN_V1.md`
- `NEW_CHAT_BOOTSTRAP.md`
- `ROADMAP.md`
- `pyproject.toml`
- `src/observer_sandbox/cli.py`
- `src/observer_sandbox/runtime.py`
- `src/observer_sandbox/world.py`
- `src/observer_sandbox/db.py`
- `src/observer_sandbox/composition_schema.py`
- `src/observer_sandbox/actor_selection.py`
- `src/observer_sandbox/actor_runtime.py`
- `src/observer_sandbox/inventory.py`
- `src/observer_sandbox/estate_campus.py`
- `src/observer_sandbox/information_media.py`
- `src/observer_sandbox/technology_diagnostic_runtime.py`
- `src/observer_sandbox/tactical_assessment_runtime.py`
- `src/observer_sandbox/represented_skill_runtime_batch.py`
- `src/observer_sandbox/controlled_h2h_runtime.py`
- `src/observer_sandbox/field_medicine_stabilization.py`
- `config/characters/`
- `config/worlds/home.v1.json`
- `config/worlds/home.inventory.v1.json`
- `config/worlds/estate_campus.v1.json`
- `config/economy/darian.v1.json`

This v1 contract intentionally distinguishes repository-confirmed seed authority from future production-DB evidence. Source code defines what can be recreated; the live DB preflight defines the exact rows that exist and therefore the exact G3 deletion manifest.
