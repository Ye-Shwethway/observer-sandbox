# Universal Item, Container, and Inventory Architecture

Status: CANONICAL DESIGN / MINIMUM FOUNDATION ACTIVE

## Purpose

Observer Sandbox treats reusable world concepts separately from concrete universe possession. An apple is one universal item definition everywhere in the universe; a particular household, shop, backpack, or character owns or contains concrete quantities/instances of that definition.

This contract is intentionally broader than food. Consumables are the first runnable exemplar because body-composition progression now requires causal nutrition evidence, but the same architecture must later cover training equipment, tools, clothing, weapons, books, medical supplies, electronics, materials, currency instruments, and other physical objects.

## Core invariant

`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

Definitions never encode a specific character or location. Ownership and location never change the semantic identity of an item.

Example:
- `item.food.apple` = universal definition;
- an Estate refrigerator may contain a stack of 8 apples;
- a future market may contain another stack of the same definition;
- a future backpack may contain 2 apples moved from a household stack;
- all stacks retain the same reusable apple semantics and nutrition data.

## Definition versus instance

Use existing `entity_definitions` as the canonical reusable definition registry. Concrete physical entities reference a definition through `entities.definition_id`.

Definition data may include:
- category/subcategory;
- display name and semantic tags;
- capabilities;
- mass/volume/unit semantics;
- stackability;
- nutrition for foods;
- durability/condition model when later activated;
- equipment/training/tool semantics;
- future economic metadata such as tradability or reference pricing class.

Character, household, shop, or region names do not belong in universal definition ids.

## Containers

A container is any universe entity capable of physically containing movable items.

### Immovable containers / spaces

Locations and fixtures may act as fixed containers:
- house/estate;
- room;
- refrigerator;
- pantry;
- storage shelf;
- locker;
- armory rack.

Their container mobility is `fixed`. Moving their contents does not move the container.

### Movable containers

Objects may act as movable containers:
- backpack;
- bag;
- suitcase;
- crate;
- toolbox;
- medical kit.

Their container mobility is `movable`. When the container changes physical location or carrier, its contained inventory moves with it logically; individual contained stacks do not need independent world-location rewrites merely because the backpack moved.

Container nesting must remain bounded/validated. Cycles are invalid.

## Spatial, containment, and ownership semantics

Do not overload relations.

- `located_at`: dynamic physical presence of actors/ordinary movable entities.
- structural `contains`: authored world/layout containment already used by the world model; do not repurpose it as mutable inventory state.
- inventory containment: mutable stack/item -> container relationship owned by the inventory layer.
- `owned_by`: legal/economic ownership, independent of current location.
- `carried_by`: direct carriage when needed.
- `equipped_by`: equipped state when equipment work is activated.

A character may carry an item they do not own; an owned item may remain stored at home.

## Stackable versus unique items

Stackable items share definition and compatible stack-state and use a numeric quantity in a canonical unit.

Examples:
- apples by piece;
- rice by gram or kilogram-equivalent quantity;
- water by volume;
- ammunition/materials by count or mass where later allowed.

Unique/non-stackable physical items use quantity 1 and keep instance-specific state.

Examples:
- a specific treadmill;
- a specific backpack;
- a specific laptop;
- a specific weapon/tool;
- unique documents/artifacts.

Do not create `Darian's apple` or `Darian's treadmill` definitions. Create universal definitions and concrete Estate instances/ownership state.

## Minimum body-composition foundation

The first runnable slice is intentionally limited to what causal nutrition/body progression needs:

1. reusable food definitions;
2. concrete Estate food stacks in fixed food-storage containers;
3. quantity and canonical units;
4. deterministic inventory containment and quantity decrement;
5. nutrition evidence derived from definition semantics and consumed quantity;
6. action validation must reject unavailable/insufficient quantities;
7. immutable consumption evidence must record definition id, stack id, quantity, unit, and nutrient totals;
8. no currency, shopping, pricing, spoilage, recipe graph, or generalized equipment migration in this slice.

BC-1 object-id nutrition profiles are transitional compatibility data and must be retired as food consumption migrates to definition-based evidence.

## Eating behavior boundary

Food-choice behavior belongs above inventory semantics.

Cognition may consider:
- hunger and time of day;
- recent intake and meal cadence;
- training/recovery state;
- body-composition goals;
- preferences/aversions/dietary constraints;
- cooking skill/time/convenience;
- available inventory;
- future budget/cost context.

The model chooses a structured food/portion intent from available options. Deterministic inventory and nutrition engines validate quantity, decrement stock, calculate nutrients, and emit evidence. The model never owns quantity mutation or macro arithmetic.

Darian may strongly prioritize protein/recovery because of character goals and habits. That is character policy, not a different chicken/apple definition.

## Future universal object migration

After body-composition prerequisites are stable, migrate world objects by structural family rather than one-off object rewrites.

Planned order:
1. consumable food/drink definitions and stacks (current exemplar);
2. movable containers and carried inventory;
3. fixed storage fixtures/container capacities;
4. training equipment definitions + concrete Estate instances;
5. general tools/electronics/books/medical supplies;
6. clothing/equipment/equipped-state surfaces;
7. broader materials/crafting inputs where needed;
8. economic ownership, vendors, pricing, currency, transactions, scarcity/supply.

Training equipment currently authored as Estate-specific object ids is valid legacy content but should eventually become reusable definitions (`equipment.treadmill.high_speed`, `equipment.free_weights`, etc.) with Estate instances referencing those definitions. Training-method semantics should attach to reusable equipment/method definitions rather than a character-owned identity.

## Economic-system extension

The inventory contract is the substrate for later economy, not the economy itself.

Future additions may include:
- account/wallet/currency balances;
- item price observations and market listings;
- purchases/sales/transfers;
- vendors and inventories;
- ownership transfer events;
- scarcity/replenishment;
- production/crafting/logistics.

Economic value must not be encoded into item identity. The same apple definition can have different owners, locations, prices, and availability at different times.

## Schema direction

Schema v4 already provides reusable definitions, concrete entities, generic relations, events, actions, and dynamic location semantics. Quantity/depletion and mutable inventory containment are genuinely missing persistence invariants.

A schema v5 is therefore justified when the minimum inventory foundation is implemented. It should add only the smallest normalized persistence needed for stacks/quantity/container state and retain existing generic definition/entity/relation architecture.

Do not create a parallel mini-world model.

## Explicit non-goals for the first slice

- full RPG inventory UI;
- encumbrance;
- arbitrary nested-container depth;
- durability for every item;
- spoilage/expiration;
- recipes/cooking graph;
- currency or shops;
- economy simulation;
- migration of every existing Estate object;
- generalized crafting;
- item image/icon pipeline.

Those remain documented extension points, not prerequisites for BC-2.
