# W3.1 — Universe Object Valuation & Creation Rules v1

Status: IMPLEMENTATION CONTRACT

## Purpose

W3.1 gives every currently represented world object and inventory item definition an explicit economic-value policy, while preventing those values from being incorrectly added to Darian's net worth when they are already contained in the USD 16.5M Thorne Estate valuation.

It also creates a fail-closed creation-rule socket: adding a new represented world object or item definition through canonical seed paths requires an explicit economic-value policy in the same slice.

## Core distinction

`has economic value != contributes independent net worth`

A bed, power rack, surveillance console or medical diagnostic station can have a real replacement value while still being a component already included in the parent real-estate asset.

## Value classifications

- `standalone_asset` — independently represented economic asset;
- `component` — value-bearing component of a larger represented asset;
- `consumable_stock` — quantity-bearing stock valued from a unit price;
- `resource_proxy` — legacy/interaction proxy whose economic truth lives elsewhere;
- `economically_immaterial` — explicitly covered but intentionally not valued.

## Net-worth treatments

- `independent` — may contribute separately through the authoritative asset/valuation model;
- `included_in_parent` — already captured by a parent asset valuation and must not be double counted;
- `derived_stock` — current value derives from live inventory quantity and definition unit value;
- `excluded` — does not contribute separately.

## Thorne Estate policy

The canonical Estate remains USD 16.5M as one represented real-estate asset. Current installed fixtures/facilities receive replacement-value estimates for future repair, replacement, insurance, purchasing and depreciation systems, but use:

`net_worth_treatment = included_in_parent`

with:

`included_in_asset_id = asset_thorne_estate`

Therefore W3.1 must not change Darian's seeded USD 25.0M net worth.

## Resource proxies

The old convenience objects `Stored Food Provisions`, `Drinking Water` and `Meal Ingredients` are not treated as separate stock assets. They are interaction/resource proxies. Actual represented food stock lives in inventory stacks, so their economic policy is `resource_proxy / excluded` to prevent duplicate value.

## Inventory stock

Every current food item definition has a canonical unit price in the same canonical unit used by inventory. Current stack value is deterministic:

`stack quantity / policy unit quantity * unit value`

Changing live stack quantity therefore changes derived stock value without rewriting the item-definition price.

W3.1 does not automatically add household consumable stock to Darian's personal net worth. It establishes the value truth needed for later replenishment, purchase, loss and household accounting.

## Creation rule

Canonical initialization performs coverage validation after world, campus and inventory seeding. Every represented `object` entity and every `item` entity definition must have a value profile.

A new canonical object that lacks policy causes initialization/CI to fail with a missing-value-policy error. The developer must choose an explicit classification, valuation method and net-worth treatment rather than allowing an accidental default.

Runtime object-creation APIs added in the future must call the same `require_entity_value_policy(...)` boundary before committing a new represented object, or provide an atomic creation path that writes the object and its approved policy together.

This is intentionally not a blanket assumption that all objects are worth zero or are included in real estate. New objects outside the Estate may instead be standalone assets, stock, or economically immaterial.

## Current valuation method

Current fixture amounts are `canonical_replacement_estimate` values. They are simulation-authoritative seed estimates, not claims of live real-world market quotes. Later dynamic economy/market systems may append or derive time-varying market values while preserving the original provenance.

## Future sockets

This policy layer is designed to support later:
- repairs and replacement;
- purchase and sale;
- depreciation/appreciation;
- insurance;
- household/business accounting;
- job/career equipment;
- corporate asset registers;
- regional/global wealth aggregation;
- dynamic price and market systems.

Those systems must continue to distinguish replacement value, market value, purchase price and independent net-worth contribution.
