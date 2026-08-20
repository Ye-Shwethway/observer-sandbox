# Location-First Genesis Decision Record v1

Status: **APPROVED ARCHITECTURE DECISION**  
Date: 2026-08-21

## Decision

Observer Sandbox will not attempt to preserve, upgrade in place, or individually reincarnate the current prototype-era Real World Character/Location/Item content.

Instead, the project will:

1. complete the modern Sandbox Location Creation vertical first;
2. then perform a controlled reset of prototype Real World content while preserving reusable universe infrastructure;
3. implement Transmigration against the clean Real World target;
4. rebuild canonical content from modern Sandbox creations;
5. reserve Reincarnation/Renewal for later modern-to-modern canonical evolution.

## Why this decision exists

The current Real World exemplars predate the present Creation architecture. Darian, the Thorne Estate, Estate objects and legacy inventory content were useful development fixtures while the project was discovering how a simulation world should be represented.

Trying to preserve those prototype contracts would require disproportionate bridge logic, seed precedence handling, special-case adapters and compatibility work for content that is intentionally disposable.

The newer Creation Sandbox is now the better source of future content authority because it has:

- versioned schemas;
- exact validators;
- Manual/AI parity;
- isolated approval/materialization;
- editing lifecycle;
- dependency-aware batch semantics;
- shared quantity/grading/requirements/value foundations;
- explicit future Transmigration boundaries.

A clean Genesis therefore reduces complexity rather than discarding valuable architecture.

## Why Location must come first

A rebuilt world cannot activate Characters meaningfully without represented spatial structure.

Locations establish:

- canonical containment hierarchy;
- topology and movement destinations;
- placement/storage context for Items;
- interfaces/access boundaries;
- starting positions for Characters;
- later runtime affordance discovery.

Therefore Character/Item Creation completion alone is insufficient for a clean Genesis.

The immediate prerequisite is I5.11 Sandbox Location Creation + Embedded Contents.

## Alternatives rejected

### Preserve and migrate every legacy object

Rejected because the current exemplars are intentionally disposable and preserving them would create migration debt with little long-term value.

### Build Reincarnation first and use it as a legacy upgrade bridge

Rejected for now. Reincarnation is more valuable and simpler when both the source and replacement already use modern Creation contracts.

### Wipe the Real World immediately

Rejected because Location Creation is not yet complete. A premature wipe would remove the only current spatial world before the replacement creation path is ready.

### Duplicate Creation Studio directly inside the Real World

Rejected as an authority model. Canonical creation should still pass through staged validation/approval rather than granting direct AI/UI canonical write authority. Real World UI may later expose Creator tools, but the underlying write path remains Sandbox/staging + explicit promotion.

## Consequences

Positive:
- fewer legacy adapters and special cases;
- cleaner canonical authority;
- one modern content-origin path;
- simpler Transmigration target;
- easier future multi-universe support;
- Reincarnation can focus on modern content rather than prototype rescue.

Costs:
- current exemplar content will be destructively retired from the active Real World;
- a controlled reset audit and backup are required;
- legacy reseeding paths must be neutralized before reset;
- retained platform systems must be checked for assumptions about Darian/Thorne Estate/default object IDs;
- Genesis content must be recreated through the modern Creation workflow.

## Locked boundary

This decision authorizes documentation and planning of the Genesis transition, and authorizes Location Creation as the next feature slice.

It does **not** authorize destructive Real World reset execution yet.

Destructive reset begins only after Location Creation acceptance and a dedicated keep/wipe dependency audit.
