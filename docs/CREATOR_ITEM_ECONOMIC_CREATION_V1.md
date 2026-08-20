# Creator Item Economic Creation v1

Status: **LOCKED CREATION / PRESENTATION CONTRACT**

## Purpose

Creation Sandbox Items participate in the same economic semantics already used by the Real World inventory system. Sandbox isolation changes authority and lifecycle, not whether ordinary goods have economic meaning.

## Future AI-created Items

Single Item and Item Batch AI creation MUST use one shared economic instruction.

For the default Creation Sandbox:

- ordinary purchasable, sellable, or replaceable goods are economically represented even when the Creator does not state a price;
- USD is the default currency for conservative ordinary-market estimates;
- individual durable goods normally use `standalone_asset` + `independent` with plausible market/replacement values;
- stackable consumable goods normally use `consumable_stock` + `derived_stock` with a per-unit value whose unit matches the stack unit;
- total stock value is derived from approved unit value and quantity rather than stored as a competing total;
- physical containment does not imply `component` or `included_in_parent` economics;
- `component` + `included_in_parent` requires explicit economic parent semantics;
- `resource_proxy` and `economically_immaterial` are reserved for genuinely non-independent value semantics or explicit Creator exclusion;
- unknown exact price does not erase ordinary economic existence: use a conservative rounded estimate and identify the valuation method as an estimate.

All generated economic fields remain proposals until Creator approval. Existing exact Item schema validation remains authoritative.

## Existing approved Items

Previously approved Sandbox Items are NOT silently revalued when this policy changes. Their approved economic policy remains persisted truth until an explicit Creator edit/revalue operation changes it.

The generic Sandbox Item operation service already permits audited `economic_policy` edits. Telegram revalue/edit UX may expose that service separately; presentation changes alone MUST NOT mutate approved data.

## Approved Item detail presentation

Approved Sandbox Item details SHOULD follow the same information architecture as Real World inventory where equivalent data exists:

1. quantity / definition / placement / ownership / mobility;
2. economic value;
3. nutrient facts when `modules.nutrition` exists;
4. physical facts when `modules.physical` exists;
5. container capacity or training facts when those modules exist;
6. Sandbox/canonical boundary statement.

Creator-facing UI resolves Sandbox relation IDs to human names when possible and does not expose raw object IDs merely because the storage layer uses them.

If an existing approved Item has no represented monetary value, normal UI says **Value not assigned** rather than presenting raw `economically_immaterial / excluded` implementation terminology.

## Boundary

This contract does not transmigrate Sandbox value into the canonical universe and does not auto-edit existing approved Items. Economic proposals remain subject to Creator review, deterministic schema validation, Sandbox isolation, and explicit approval.
