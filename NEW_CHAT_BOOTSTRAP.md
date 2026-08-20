# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-20**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. task-relevant canonical docs/source
6. verified production/runtime evidence before live claims.

Authority order:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches: `main`, `test` only.

Workflow:
`develop on test -> focused tests -> PR/final CI -> merge to main -> runtime deploy if applicable -> production verification -> continuity sync -> main/test synchronization`.

Do not claim production deployment from a merge alone.

---

## Current implementation checkpoint

Latest merged implementation checkpoint before this docs update:

### PR #322 — Auto-sync scoped Telegram command menus

Merge commit:
`366f07b4a9e1cfd0670d768132e9500f10c51b44`

Evidence:
- CI #1154 targeted mode — **96 passed**;
- main/test synchronized at merge;
- startup publishes role-scoped Telegram command menus from the final `/help` contract and removes stale chat scopes;
- ambiguous legacy `/pause`, `/resume`, `/speed`, `/time` remain non-mutating redirects and are not advertised.

Production deployment/live command-menu behavior for #322 is not independently verified from repository evidence. Do not infer live state from merge alone.

### PR #321 — Manual Character field-editing UX closure

Merge commit:
`6c568711e67b63f0412daf84189187834e9e71dd`

Evidence:
- CI #1153 targeted mode — **135 passed**;
- successful manual field saves remain in the same section/page;
- consumed input prompt cards are deleted; invalid input edits the existing prompt into retry state;
- Creator live Telegram verification — **PASS**.

### PR #319 — Manual Character Creation Exact Parity

Merge commit:
`6838c9503fee9d9bd2bd8b4786e10cc907ba5c2`

Manual and AI Character creation now converge on the exact creation-owned Character profile contract, with typed structured fields/collections, deterministic validation, revisioned drafts and isolated Sandbox approval/materialization.

Character creation is sufficiently closed for the next dependency family.

---

## Creator Creation architecture now locked

Creator explicitly selected the next direction:

**Item Creation first, then complete Location Creation, then bind Character + Location + Items into runtime readiness/affordances.**

Reason:
- a Character alone is not meaningfully runnable;
- a usable Location is required;
- a Location is a **spatial container** and can contain Items/fixtures/resources/child locations/occupants;
- Creator must be able to create a Location with initial Items or add/remove/move Items afterward;
- therefore Item creation/instance semantics must be robust before Location contents become a strict creation contract.

Do not build a parallel Sandbox inventory/world ontology. Reuse existing universal world foundations through Sandbox-owned adapters/state.

---

## Strict schema / AI rule

Every Creation type must have a complete explicit versioned schema.

Canonical pipeline:

`Creator intent -> exact registered JSON-like schema -> AI fills permitted fields only -> deterministic validation -> draft/preview -> explicit approval -> Sandbox apply`.

AI must not guess or deviate:
- no unknown/extra keys;
- no missing required core fields;
- no arbitrary conditional-module structures;
- no runtime/derived fields supplied as source truth;
- no direct DB/runtime write;
- no bypass of units/enums/value policies/references.

Preferred architecture:

`strict core + strict conditional modules`.

Manual and AI input modes must converge on the same validator/apply boundary.

---

## Measurement direction

Imperial is the default Creator-facing system.

Use pounds (`lb`) for Item weight/load presentation. Use appropriate Imperial length/area/volume units by domain.

Future display switching to Metric must not rewrite physical truth.

Invariant:

`normalized physical quantity -> presentation conversion -> Imperial(default) | Metric`.

Grades, requirements and simulation consume normalized quantities, not formatted strings.

---

## Universal grading direction

The existing shared vocabulary remains:

`E < D < C < B < A < S < SS < SSS < X < XX`.

The proven profile grading architecture is the base:

`authoritative raw state + explicit named grading scheme -> derived grade`.

Extend it cross-domain; do not replace it.

Important rules:
- shared vocabulary, domain-specific evaluators;
- Character Strength S, Item Durability S and Location Prestige S do not share one raw scale;
- grades are normally derived from raw facts/state rather than AI-authored truth;
- optional overall grades require an explicit composite scheme;
- current RAPS/Skill 0..100 grading remains unchanged and legitimately uses E..S only;
- realistic universe profiles may restrict grade/capability ceilings; future Sandbox/supernatural universes may represent higher/impossible ranges.

Core interaction distinction:

> **Item Grade describes the item. Requirement Grade describes the interaction.**

A 55 lb dumbbell may have S load grade, but required Character Strength depends on the actual action/exercise/workload. Do not blindly map Item grade to Character requirement.

---

## Universal requirements and Location access

Use one typed/composable requirement contract across future Items, Locations, Quests and Actions where possible.

Potential predicates include grade thresholds, raw capability, required skill/equipment, authorization/ownership/residency, quest/state and operating/time state.

**Grade is not authorization.**

Location access policy is separate and may be:
- public/access-to-all;
- private;
- owner/resident;
- authorized-only;
- grade-gated;
- quest/state-gated;
- composite.

A high-grade public place can still admit a low-grade Character. A high-grade private estate can reject a high-grade stranger.

Operating/open state is separate again from access policy.

---

## Item architecture direction

Reuse `docs/INVENTORY_ITEM_ARCHITECTURE.md`:

`universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`.

Universal Item Schema v1 must support strict core facts such as:
- identity/family/spec variant/classification;
- stackable/unique;
- consumable/non-consumable;
- movable/carriable/fixed;
- physical mass, dimensions, occupied space/volume where meaningful;
- materials/composition;
- durability/condition where meaningful;
- capabilities/affordances;
- container/storage compatibility;
- economic-value policy and price/value inputs;
- registered modifier/effect references where applicable;
- derived grade profile;
- strict conditional-module selection/version.

Candidate strict conditional modules include container, consumable, food/nutrition, wearable/equipment, tool, powered device, resistance-training equipment and later justified families.

Items should expose intrinsic facts/capabilities rather than unconditional Character stat bonuses.

Dumbbell exemplar:
- 2 lb and 55 lb versions share a definition family/spec logic;
- exact load differs;
- runtime training effect derives from Item spec × actor × exercise/action × workload × state/context;
- 2 lb can be trivial for elite strength work but useful for rehab/warm-up/endurance.

Item Creation must support both **single Item** and **strict batch Item** creation.

---

## Economic-value integration

Reuse existing valuation/economy contracts.

Core distinction remains:

`has economic value != contributes independent net worth`.

New Items/Locations must carry an explicit applicable economic-value policy rather than accidental defaults. Replacement value, market value, purchase price and independent net-worth contribution remain distinct.

Sandbox valuation data must not alter canonical Real World net worth/economy before a future authorized transmigration/apply boundary.

---

## Location architecture direction

Authoritative semantic definition:

> **Location = an identifiable spatial container with extent, contents, boundary/interface semantics, local state and explicit relationships to surrounding space.**

Location schema must eventually support identity/kind, parent containment, known extent/exposure, interfaces/topology, access, operating state, ownership/control, environment, facilities/affordances, child Locations, structural fixtures, mutable Items/resources, occupancy, value/asset policy, grading and provenance.

Do not overload relations:
- `contains` = authored structural containment;
- `stored_in` = mutable inventory containment;
- `located_at` = dynamic presence;
- `owned_by` = ownership;
- `carried_by` / `equipped_by` separate.

Containment does not imply traversal. Connection does not imply current permission. Unknown geometry remains unknown rather than fabricated.

Location creation can include a new validated Item batch atomically, or reference already active Sandbox Items. Embedded contents are never free-form unvalidated prose.

---

## Active implementation sequence

Detailed plan: `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`.

1. **I5.2 — Creation Contract Audit & Reuse Map**
2. **I5.3 — Universal Quantity & Measurement Contract**
3. **I5.4 — Universal Cross-Domain Grade Contract**
4. **I5.5 — Universal Requirement & Access Contract**
5. **I5.6 — Universal Item Schema v1**
6. **I5.7 — Item Creation v1: Single**
7. **I5.8 — Item Batch Creation v1**
8. **I5.9 — Sandbox Item / Container Operations**
9. **I5.10 — Universal Location Schema v1**
10. **I5.11 — Location Creation + Embedded Contents**
11. **I5.12 — Location Contents Editing / Operations**
12. **I5.13 — Character ↔ Location Binding & Runtime Readiness**
13. **I5.14 — Item / Location Runtime Affordance Bridge**
14. **I5.15 — Sandbox Vertical Acceptance**

Active next slice is **I5.2**.

Do not skip directly to broad Location AI generation before Item/quantity/grade/requirement contracts are settled.

---

## Runtime and isolation locks

- Full Sandbox autonomous ticking is still **not implemented**.
- `runtime_ready != running` remains hard-locked.
- Adrian Vale remains Creation Sandbox-only and is not canonical.
- Do not mutate canonical Thorne Estate/world topology while building Sandbox creation foundations.
- Do not activate/transmigrate a second Real World Character.
- Creation Sandbox reset/delete must clean Sandbox dependencies without touching canonical entities/world/economy.

Target pre-autonomy chain:

`strict Character + strict Location + strict Items -> active Sandbox objects -> contents/binding -> runtime readiness -> deterministic represented options`.

After I5.15, stop for Creator review before defining any autonomous Sandbox execution slice.

---

## Transmigration boundary

I6 remains deferred and planning/validation-only unless Creator explicitly changes scope.

Future requirements:
- freeze source revision;
- compute dependency closure;
- select target-universe profile;
- validate grade/capability/system compatibility;
- produce structured result + deterministic proposed mutations;
- failure/incompatibility = zero target-universe writes;
- no automatic canonical apply.

Sandbox-valid supernatural/impossible content may be rejected by the current realistic Real World and remain valid for another future universe profile.

---

## Production evidence boundary

Repository implementation evidence is current through PR #322. PR #321 manual Character editing is Creator live-verified. PR #322 production deployment/live menu state is not independently verified here.

This continuity/roadmap update is documentation-only and does not imply a runtime deployment.

---

## Exact resume point

**Start from I5.2 — Creation Contract Audit & Reuse Map. Reconcile existing Item/inventory, valuation/economy, grading, Location/spatial-container and Creation Sandbox models before adding runtime schema. Then implement I5.3 Quantity/Measurement with Imperial default, I5.4 cross-domain derived grading, I5.5 universal requirements/access, and only then the strict Universal Item Schema. AI is exact-schema-only; no guessing/deviation. Item Grade is separate from interaction Requirement Grade; Grade is separate from Location authorization/access. Build single Item creation before batch creation, Item/container operations before full Location contents, then strict Location creation, contents operations, Character↔Location binding, property-driven runtime affordances and vertical acceptance. Preserve Real/Sandbox isolation and do not start full Sandbox autonomy or transmigration.**
