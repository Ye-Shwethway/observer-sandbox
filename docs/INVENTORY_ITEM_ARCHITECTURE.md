# Universal Item, Container, and Inventory Architecture

Status: ACTIVE / SCHEMA V5 FOUNDATION DEPLOYED

## Purpose

Observer Sandbox treats reusable world concepts separately from concrete universe possession. An apple is one universal definition everywhere; a household, shop, backpack, character or other entity may own or contain concrete quantities/instances of that definition.

This contract is broader than food. Consumables are the first runnable exemplar because body-composition progression needs causal nutrition evidence, but the same architecture later covers training equipment, tools, clothing, weapons, books, medical supplies, electronics, materials and economy-linked physical objects.

Operational inventory detail: `docs/INVENTORY_OPERATIONS_V1.md`.

## Core invariant

`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

Definitions never encode a specific character or location. Ownership/location never change item semantic identity.

Example:
- `item.food.apple` = universal definition;
- an Estate refrigerator may contain one apple stack;
- a future market may contain another stack of the same definition;
- a future backpack may contain apples moved from either source;
- every stack retains the same universal apple semantics and nutrition definition.

## Definition versus instance

`entity_definitions` is the canonical reusable-definition registry. Concrete physical entities reference a definition through `entities.definition_id`.

Definition data may include category, semantic tags, capabilities, mass/volume/unit semantics, stackability, nutrition, later durability/equipment semantics and future economic classification metadata.

Character, household, shop or region names do not belong in universal definition ids.

## Containers

A container is any universe entity capable of physically containing movable items.

### Fixed / immovable

Examples:
- house/estate or room storage;
- refrigerator;
- pantry;
- storage shelf;
- locker;
- armory rack.

Container mobility is `fixed`.

### Movable

Examples:
- backpack;
- bag/suitcase;
- crate;
- toolbox;
- medical kit.

Container mobility is `movable`. When a movable container changes location/carrier, its contents move logically with it; contained stacks do not require independent world-location rewrites merely because the backpack moved.

Container nesting must remain bounded/validated. Cycles are invalid.

## Spatial, containment and ownership semantics

Do not overload relations.

- `located_at`: dynamic physical presence.
- structural `contains`: authored world/layout topology; not mutable inventory state.
- `stored_in`: mutable inventory containment.
- `owned_by`: legal/economic ownership independent of current location.
- `carried_by`: direct carriage.
- `equipped_by`: equipped state when activated.

A character may carry something they do not own; an owned item may remain stored elsewhere.

## Stackable versus unique items

Stackable items share definition and compatible stack state and use numeric quantity in a canonical unit: apples by piece, rice by mass, liquids by volume, etc.

Unique/non-stackable physical items use quantity 1 and keep instance-specific state: a treadmill, backpack, laptop, tool/weapon, document/artifact.

Do not create `Darian's apple` or `Darian's treadmill` definitions. Create universal definitions plus concrete owned/stored instances.

## Schema v5 foundation

Schema v4 already provided reusable definitions, concrete entities, generic relations, actions/events and dynamic location semantics. Durable stack quantity/depletion was the concrete missing persistence invariant.

Schema v5 therefore adds normalized `inventory_stacks` and reuses the existing graph/entity model. It does not create a parallel mini-world.

Inventory Foundation v1 is deployed. It provides:
- universal food definitions in `config/items.v1.json`;
- concrete Estate stock stacks in `config/worlds/home.inventory.v1.json`;
- quantity/unit persistence;
- fixed-container metadata;
- `stored_in` and `owned_by` semantics;
- deterministic availability/decrement;
- definition-based quantity-scaled nutrition;
- first-seed/no-refill safety: ordinary re-init/deploy does not restore depleted stock.

## Universe-wide observation invariant

Inventory observer/query surfaces are **not** tied to Darian or the Thorne Estate.

Canonical scopes:
- arbitrary location;
- arbitrary character;
- arbitrary fixed/movable container;
- all universe stocks.

Darian's Estate is only the first production content exemplar. Query/control code takes stable entity/stack ids. Synthetic non-Estate location and non-Darian character/backpack regression tests guard this invariant.

Telegram must therefore browse:

`Inventory -> Locations | Characters | Containers | All Stocks -> selected scope -> stack`

Adding a future character, shop, warehouse or backpack must not require a new inventory backend/handler family.

## Wealthy-residence baseline versus replenishment

A one-time explicit Creator-approved Estate reserve migration may establish realistic starting stock while outside-world economy/purchasing is unavailable. That is a migration, not an automatic refill loop.

After its durable migration marker is recorded, ordinary initialize/deploy preserves depletion. Later additions occur through explicit inventory/economy operations.

Inventory Operations v1 introduces owner-only typed replenishment of an existing stack. It adds positive bounded quantity, preserves ownership/container/simulation time and emits an audit event. Telegram only adapts this reusable backend control.

## Eating behavior boundary

Food-choice behavior belongs above inventory semantics.

Cognition may consider hunger/daypart, recent intake, training/recovery, body-composition goals, preferences/aversions/dietary constraints, convenience/cooking context, available stock and later budget/cost context.

The model proposes a structured food/portion intent. Deterministic inventory/nutrition engines validate quantity, decrement stock, calculate nutrients and emit evidence. The model never owns quantity mutation or macro arithmetic.

Darian may prioritize protein/recovery because of character goals/habits. That is character policy, not a different chicken/apple definition.

## Future universal object migration

Migrate by structural family rather than one-off object rewrites:
1. consumable food/drink definitions and stacks — exemplar foundation complete;
2. movable containers and carried inventory;
3. fixed storage capacity semantics where needed;
4. training equipment definitions + concrete Estate instances;
5. general tools/electronics/books/medical supplies;
6. clothing/equipment/equipped-state;
7. materials/crafting when justified;
8. economic ownership transfer, vendors, pricing, currency/accounts, transactions, scarcity/replenishment.

Current Estate-specific training-equipment object ids are valid legacy concrete content, but later become instances of reusable equipment definitions. Training-method semantics attach to reusable equipment/method definitions, never a named-character identity.

## Economic-system extension

Inventory is the substrate for economy, not the economy itself. Future additions may include wallets/accounts, market listings, purchases/sales/transfers, vendors, ownership-transfer events, replenishment/supply and production/logistics.

Economic value is context/state, not item identity. The same apple definition can have different owners, locations, prices and availability over time.

## Current non-goals

Do not add as side effects:
- full RPG inventory UI;
- encumbrance/capacity simulation;
- arbitrary-depth nested containers;
- durability for every item;
- spoilage/expiration;
- deep recipe/cooking graph;
- currency/shops/economy simulation;
- migration of every existing world object at once;
- generalized crafting;
- item image/icon pipeline.
