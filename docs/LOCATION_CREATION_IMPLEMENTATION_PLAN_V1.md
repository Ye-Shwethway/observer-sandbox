# Sandbox Location Creation — Implementation Plan v1

Status: **APPROVED PLANNING BASELINE — IMPLEMENTATION SLICES DEFINED**  
Date: 2026-08-21

## Objective

Complete Location Creation as the next full Creator Studio domain before Real World reset/transmigration work begins.

A viable rebuilt universe requires represented space before Characters and Items can be placed, activated, traversed, owned, stored, used or simulated. Therefore Location Creation is the immediate prerequisite for the approved Genesis transition.

Canonical sequencing:

`Location schema refinement + grading -> Location Creation vertical -> Location acceptance -> prototype Real World content reset -> legacy reseeding removal -> Transmigration -> fresh Genesis rebuild -> future Reincarnation`

This plan does **not** authorize the destructive Real World reset yet.

---

# 1. Mandatory implementation rules

All work follows:

- `docs/CREATION_SECTION_IMPLEMENTATION_STANDARD_V1.md`;
- `docs/CREATION_CONTRACT_REUSE_MAP_V1.md`;
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`;
- `docs/CREATION_SANDBOX_ISOLATION_V1.md`;
- `docs/CREATOR_AI_SCHEMA_FILL_CONTRACT_V1.md`;
- `docs/WORLD_LOCATION_NODE_MODEL.md`;
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`;
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`;
- `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

Core Creation pipeline:

`versioned Location schema -> registered socket -> Manual/AI exact payload parity -> safe canonicalization -> exact validator -> graph/dependency validation -> write-free review/export -> explicit Sandbox approval -> atomic materialization -> detail/browse -> Edit Preview/Apply/Done -> cleanup`

Locks:

- one shared Creation pipeline, not bespoke Location CRUD;
- Manual and AI converge on one exact schema/validator/materializer;
- structural/schema/isolation failures may block;
- fine realism remains non-blocking by default;
- AI authors facts, never authoritative grades or canonical writes;
- approval creates Sandbox state only;
- `Created != running`;
- no automatic transmigration.

---

# 2. Schema refinement decision

The current `location-v1` is a strong foundation but is intentionally incomplete for long-term universe building. It already represents identity, structural parentage, physical extent, access, topology/interfaces, facilities/resources/capabilities, small environment state, economic policy, provenance and derived L0-L4 completeness.

The refinement must preserve its stable semantics while adding the minimum high-value dimensions identified by repository review and external spatial-model research.

Because the refined payload changes exact top-level/nested structure, it should be treated as a **versioned schema evolution**, not a silent incompatible mutation. The implementation slice must make the final version decision explicitly (`location-v2` preferred if exact payload compatibility breaks).

No second competing Location ontology is permitted.

## 2.1 Refined Location conceptual shape

The target schema should support:

### Identity

- stable key;
- display name;
- spatial kind;
- description;
- registry-backed `functional_classes[]` rather than one free-form functional class;
- optional tags where they improve query/authoring without becoming authority.

### Structure

- canonical `parent_ref` where applicable;
- exposure classification;
- one structural parent in the first implementation;
- acyclic hierarchy.

### Geography — new

Optional real-world/geographic anchoring:

- address text;
- locality;
- administrative region;
- country code;
- optional latitude/longitude;
- optional coarse bounds only if supported cleanly.

Unknown geography remains null. AI must not invent coordinates or addresses merely for completeness.

### Spatial

Retain normalized:

- area;
- length;
- width;
- height;
- elevation;
- terrain;
- orientation notes.

Add a bounded surface/ground classification only if it has a concrete downstream use or grading/query value.

### Boundary — new

Minimum conceptual evidence:

- boundary type: physical / virtual / mixed / open / unknown;
- enclosure: enclosed / partially_enclosed / unenclosed / unknown;
- optional notes.

Boundary is not access authority and is not topology.

### Access and operations split

Stable policy and changing operating state must not be conflated.

- `access.policy` = who may enter/use;
- operational/initial state = initial open/closed/locked/blocked seed where represented;
- live changing operating state becomes runtime authority after activation.

Future schedules/opening hours may extend operations only when a concrete consumer needs them.

### Topology / interfaces

Retain:

- stable local interface key;
- friendly name;
- destination reference;
- directionality;
- enabled state;
- supported traversal modes;
- bounded base duration.

Add registry-backed interface kind, initially sufficient for common semantics such as:

- door/opening;
- gate;
- stairs;
- elevator;
- path/road connection;
- tunnel;
- dock;
- portal/other where universe policy allows.

Optional distance may be supported when represented. Containment never creates topology automatically.

### Facilities / resources / capabilities

Replace arbitrary free-text lists with registry-backed semantic tokens where practical:

- location capabilities;
- facility types;
- resource types;
- utilities.

A Location label such as `Gym` or `Hospital` does not itself grant executable actions. Affordance/runtime authority must resolve from represented machine-readable evidence.

### Environment

Creation owns stable environment profile/evidence and optional initial seed state, not future live weather/temperature authority.

Keep the first refinement deliberately bounded:

- lighting profile/state evidence where useful;
- weather exposure;
- represented utilities;
- no full thermal/HVAC/hazard/sensor model.

### Control / ownership — new

Minimal stable control semantics:

- ownership class: private / public / institutional / communal / unowned / unknown;
- optional owner reference;
- optional operator/manager reference.

Residency and current occupancy remain relationship/runtime state rather than embedded ownership shortcuts.

### Economic policy

Retain existing value-policy separation from access and completeness.

### Provenance

Retain explicit content provenance separately from Creation-envelope provenance.

---

# 3. Location grading architecture

Project grading rule:

> Every major represented element must participate in the universal grading architecture where meaningful, while raw facts remain authoritative and grades remain derived.

Reuse the existing invariant:

`authoritative Location facts + registered grading sockets + universe policy/reference profiles -> derived Location GradeProfile`

AI and Creator forms do **not** author grade letters, thresholds, evaluator ids or reference profiles.

## 3.1 Mandatory dimension — completeness

Retain current `location-completeness-v1`:

- L0 -> E;
- L1 -> D;
- L2 -> C;
- L3 -> B;
- L4 -> A.

Meaning: **representation completeness only**.

It is not prestige, access authorization, market value, security or physical size.

Every valid Location can therefore participate in grading even when no other grading evidence exists.

## 3.2 Spatial scale — evidence-gated

Candidate dimension:

`location / spatial_scale`

Evidence:

- represented area and/or compatible dimensions;
- Location kind/reference profile.

Rules:

- larger does not mean better;
- grade describes magnitude/scale only;
- references should be kind-aware rather than applying one global room/building/property/region threshold;
- missing size/reference => ungraded dimension, not guessed precision.

## 3.3 Infrastructure / facility capability — evidence-gated

Candidate dimension:

`location / infrastructure_capability`

Evidence derives from registered facility/resource/utility/capability semantics rather than string count.

The evaluator must measure represented support breadth/depth under a declared reference policy, not reward arbitrary metadata quantity.

Examples of possible evidence classes include potable water, electric power, sanitation, food preparation, medical support, communications, security, training, storage and transport support when represented by authoritative registry entries.

## 3.4 Connectivity / mobility — evidence-gated

Candidate dimension:

`location / connectivity`

Evidence may include:

- valid enabled interfaces;
- supported traversal modes;
- reachable represented destinations;
- directionality / route evidence.

This is descriptive graph connectivity, **not access permission** and not design quality. A deliberately isolated bunker may have low connectivity without being a poor Location.

Graph-dependent grading may be finalized only after materialization/dependency resolution rather than from an isolated draft.

## 3.5 Economic / asset value — context/reference-gated

Candidate dimension:

`location / asset_value`

Use only when:

- authoritative economic evidence exists;
- a compatible currency/universe/reference profile exists;
- Location kind/context makes the interpretation meaningful.

Do not encode a timeless global rule such as a fixed dollar value automatically equalling one grade.

## 3.6 Security / protection — reserved future dimension

Security is useful but should **not** be graded until a bounded authoritative raw security-evidence contract exists.

Do not create an S-grade security field in the schema merely to satisfy coverage.

Future extension should be additive through `EvaluatorSpec + DimensionSpec + ReferenceProfile + UniverseGradingPolicy`.

## 3.7 Overall Location grade

No automatic overall grade in the first Location implementation.

A profile such as:

- Completeness: A
- Spatial Scale: B
- Infrastructure: S
- Connectivity: C
- Asset Value: A

is more meaningful than averaging unrelated semantics into one letter.

`GradeProfile.overall = null` until an explicit context-specific composite evaluator is approved.

Possible future composites may be residential capability, commercial venue capability, military-facility capability or wilderness accessibility, each with explicit semantics.

---

# 4. Location Grading Evidence Matrix requirement

During schema refinement, every meaningful field/module must be classified as one of:

- authoritative stable definition fact;
- initial-state seed;
- runtime-owned changing state;
- relationship/graph proposal;
- grading evidence;
- policy/configuration;
- presentation/provenance metadata;
- explicitly ungraded.

A separate Location Grading Evidence Matrix may be created if the implementation table becomes too large for this plan.

Minimum mappings expected:

| Evidence family | Candidate grading dimension | Notes |
| --- | --- | --- |
| L0-L4 represented structure | completeness | mandatory derived dimension |
| area/dimensions + kind reference | spatial_scale | magnitude, not quality |
| registered facility/resource/utility evidence | infrastructure_capability | no string-count grading |
| resolved interfaces/topology | connectivity | separate from access |
| economic policy/value + reference | asset_value | universe/context gated |
| future security evidence | security | deferred until raw contract exists |

---

# 5. Embedded content boundary

Location Creation must ultimately support atomic composition with child Locations and Items, but it must not invent a generic `contents` bag.

Rules:

- child Locations use exact current Location member schema;
- embedded Items reuse exact current Item member schema / Batch semantics;
- local references are deterministic and resolvable before writes;
- structural child Location uses `contains`;
- movable Item normally uses `located_at`;
- Item inside a typed container uses `stored_in`;
- ownership remains independent;
- interface destinations must resolve to active same-Sandbox Locations or same-batch local refs;
- whole proposal graph validates before one atomic apply;
- any failed member/dependency => zero materialized writes.

The first implementation may stage composition breadth across slices, but no weaker duplicate Item/Location schema is permitted.

---

# 6. Implementation slices

## L11.0 — Schema Refinement + Grading Contract

**Goal:** lock the exact refined Location schema before UI/AI/materialization.

Deliverables:

- final schema version decision;
- refined exact payload;
- registries/enums for functional classes, interface kinds, facilities/resources/capabilities where justified;
- definition vs initial/runtime ownership map;
- Geography, Boundary and Control modules;
- access vs operations separation;
- grading evidence matrix;
- Location GradeProfile contract;
- compatibility/update of `UNIVERSAL_LOCATION_SCHEMA_V1.md` or successor versioned contract;
- focused schema examples for at least:
  - property/building-style Location;
  - room/outdoor-zone-style Location.

Acceptance:

- no UI/AI code before schema is locked;
- unknown precision remains null;
- no authored grades;
- no meaningless automatic overall grade;
- current stable world relation semantics remain unchanged.

## L11.1 — Exact Validator + Registry/Grading Foundation

**Goal:** make the refined schema executable and self-consistent.

Deliverables:

- exact schema validator/canonicalizer;
- provider-safe normalization boundary;
- registry-backed tokens/enums;
- validator read-back/revalidation tests;
- completeness grade retained;
- initial deterministic grading sockets for justified dimensions;
- universe-policy gating;
- ungraded behavior when evidence/reference is absent.

Recommended first real grading set:

1. completeness;
2. spatial scale when reference/evidence exists;
3. infrastructure capability when registry evidence exists;
4. connectivity once graph context is available.

Asset value may be enabled only if the existing economy/reference contract is sufficient without arbitrary thresholds.

## L11.2 — Sandbox Location Persistence + Graph Materializer

**Goal:** materialize validated Locations into isolated Creation Sandbox state.

Deliverables:

- registered Location Creation socket/adapter;
- Sandbox-owned normalized Location persistence;
- stable Sandbox IDs;
- same-Sandbox parent validation;
- structural acyclicity;
- local-ref/dependency resolution;
- explicit topology/interface materialization;
- zero canonical writes;
- atomic single/batch graph transaction;
- readback query/detail representation.

Approval does not make the Location runtime-active.

## L11.3 — Manual Full-Schema Location Creation

**Goal:** provide the complete diagnostic/reference authoring path before relying on AI.

Deliverables:

- Creator Studio Location entry;
- friendly section-based Manual editor exposing the complete supported creation-owned schema;
- optional Exact JSON advanced path if still useful;
- write-free Preview;
- raw `.txt` export;
- Cancel/no-write;
- explicit Approve into Sandbox;
- human-readable validation diagnostics.

Manual output must pass the same exact validator/materializer used everywhere else.

## L11.4 — AI Full-Schema Location Creation

**Goal:** natural-language Location authoring through the same exact schema.

Deliverables:

- complete provider-facing structured fill schema generated/aligned from authoritative registries/schema;
- strong system-side Location authoring contract;
- short natural Creator prompt support;
- safe deterministic canonicalization;
- at most one bounded repair attempt for deterministic representation errors;
- Telegram `typing` feedback;
- same Preview/export/Approve path as Manual;
- same strict validator/materializer;
- no AI-authored grades or runtime activation.

## L11.5 — Nested Composition + Embedded Items

**Goal:** create useful world sections rather than isolated empty nodes.

Deliverables:

- nested child Location composition;
- exact Item schema embedding/reuse;
- batch-local references;
- parent/storage/location relation resolution;
- whole dependency graph validation;
- one atomic apply/rollback;
- human review of nested contents;
- grading/readback after graph materialization.

No arbitrary `contents` JSON bag.

## L11.6 — Approved Detail / Browse + Edit Parity

**Goal:** bring Location to Character/Item lifecycle parity.

Deliverables:

- approved Location browse/detail;
- Location GradeProfile presentation;
- readable hierarchy/topology/facility/environment/economic sections;
- Edit using the same exact schema/validator;
- preflight;
- stale guard;
- Preview -> Apply -> Done;
- pause only where an actual Sandbox runtime race exists;
- exact prior pause-state restoration;
- audit evidence;
- delete/archive/cleanup.

## L11.7 — Location Vertical Acceptance

**Goal:** prove the complete Location Creation domain before Genesis reset/transmigration work begins.

Acceptance scenarios should include at least:

1. one property/building hierarchy;
2. one room/outdoor-zone hierarchy;
3. explicit interfaces/topology;
4. access policy distinct from operating state;
5. geography left partially unknown without fabrication;
6. boundary semantics represented;
7. facility/resource registry evidence;
8. derived completeness + applicable Location GradeProfile dimensions;
9. nested child Locations;
10. embedded multi-class Items;
11. Manual and AI parity;
12. Preview/export write-free;
13. atomic approval;
14. invalid parent/cycle/cross-Sandbox/local-ref failure -> zero writes;
15. Edit Preview/Apply/Done parity;
16. `canonical_state_fingerprint()` unchanged;
17. approved Locations remain not runtime-active.

Only after this acceptance closes should the project begin the approved Real World prototype-content reset/Genesis transition.

---

# 7. Explicit non-goals for this Location pass

Do not block Location Creation on:

- full GIS/GPS fidelity;
- polygon/mesh geometry;
- BIM wall/window graph;
- navigation meshes;
- traffic/congestion;
- public transit;
- exact crowd/capacity simulation;
- HVAC/thermal simulation;
- acoustic propagation;
- universal hazard taxonomy;
- sensor/digital-twin telemetry;
- arbitrary jurisdiction trees;
- security grading before raw security evidence exists;
- automatic overall Location grade;
- Real World reset;
- canonical transmigration;
- autonomous runtime activation.

These may arrive later through bounded consumers and registered extensions.

---

# 8. Completion boundary

Location Creation is complete for the Genesis prerequisite when:

`refined versioned schema + grading evidence/profile + strict validator + Sandbox graph materialization + Manual/AI parity + nested Location/Item composition + preview/export/approval + browse/detail + Edit lifecycle + isolation acceptance`

are all proven without canonical Real World mutation.

Then pause ordinary feature expansion and execute the separately approved Genesis transition plan.
