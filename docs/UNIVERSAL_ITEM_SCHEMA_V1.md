# Universal Item Schema v1

Status: **IMPLEMENTATION CANDIDATE — I5.6**  
Date: 2026-08-20

## Purpose

Define one exact deterministic Item creation contract shared by later Manual creation, AI generation, single creation, batch creation and Location embedded-content creation.

This schema does not persist an Item. It validates and normalizes one creation payload before any Sandbox apply boundary exists.

Core model:

`universal Item definition -> concrete unique instance OR stack -> current placement/storage -> ownership/carriage/equipment -> runtime state/history`

These concepts remain distinct even when Creator Studio later presents them as one creation flow.

---

## Strictness rule

I5.6 uses:

`strict core + strict conditional modules`.

Unknown top-level fields, definition fields, modules and executable capabilities reject.

AI cannot make a new field valid by inventing a plausible name.

Manual and AI payloads pass through the same `validate_item_payload()` function and normalize to the same contract.

---

## Implementation

`src/observer_sandbox/item_creation_schema.py`

Schema version:
`item-v1`.

The validator is pure. It accepts no database connection and performs no persistence.

---

## Exact top-level contract

Every Item payload contains exactly:
- `schema_version`;
- `definition`;
- `instance`;
- `economic_policy`;
- `requirements`;
- `relationships`.

Derived output such as Item grades is computed by the validator and is not accepted as source input.

---

## Definition core

Every definition contains exactly:
- `key` — stable lowercase semantic token;
- `name`;
- `kind`;
- `description`;
- `stackable`;
- `mobility`;
- `capabilities`;
- `tags`;
- `modules`.

V1 Item kinds:
- `object`;
- `fixture`;
- `equipment`;
- `consumable`;
- `container`.

V1 mobility:
- `movable`;
- `fixed`.

A fixture must be fixed.

Definition identity never includes current owner or current location.

---

## Registered capabilities

V1 executable/semantic capability tokens:
- `inspect`;
- `eat`;
- `store`;
- `train`;
- `use`;
- `equip`;
- `wear`.

This is deliberately bounded. Later slices may register another capability when an implemented runtime consumer exists.

Do not accept arbitrary AI-authored capabilities merely because they sound plausible.

---

## Conditional modules

V1 registers only modules needed by the current Item/Location route.

### `physical`

Exact fields:
- `mass`;
- `length`;
- `width`;
- `height`.

Each field is either an I5.3 physical quantity input `{value, unit}` or `null` when unknown.

At least one physical quantity must be known when the module is present.

Normalized output uses I5.3 SI-base physical truth.

### `stack`

Exact fields:
- `canonical_unit`;
- `initial_quantity`.

A stackable definition must declare this module.
A non-stackable definition must not declare it.

The concrete initial stack instance must use the same unit and quantity.

This preserves the existing inventory distinction between reusable definition semantics and durable stack quantity.

### `nutrition`

Exact fields align with the current item catalog:
- `basis_quantity`;
- `unit`;
- `energy_kcal`;
- `protein_g`;
- `carbohydrate_g`;
- `fat_g`.

Rules:
- requires a stackable Item;
- requires the `eat` capability;
- nutrition unit must match the stack canonical unit;
- `eat` requires nutrition in v1 so the capability cannot exist without deterministic nutrient semantics.

### `container`

Exact field:
- `capacity_volume`.

It uses I5.3 normalized volume/capacity truth.

Rules:
- requires `store` capability;
- `store` capability requires this module.

This module describes a container Item. Current mutable contents later use `stored_in`; they are not embedded in the reusable definition.

### `resistance_training`

Exact field:
- `resistance_load`.

It uses I5.3 normalized mass truth.

Rules:
- requires `train` capability;
- `train` requires the module;
- Item resistance-load grade is derived through the registered I5.4 `item-resistance-load-v1` scheme.

The grade is output metadata, never an input field.

---

## Concrete instance intent

### Unique/non-stackable

Exact instance:

```json
{"mode":"unique"}
```

No fake quantity `1` is needed as competing stock semantics.

### Stackable

Exact instance:

```json
{"mode":"stack","quantity":12,"unit":"piece"}
```

Initial quantity/unit must match the definition's `stack` module.

Later I5.9 quantity mutations operate on the concrete stack state, not the definition.

---

## Relationships

The creation payload declares exactly the current relation slots:
- `located_at`;
- `stored_in`;
- `owned_by`;
- `carried_by`;
- `equipped_by`.

Each target is a reference string or `null`.

Rules:
- definition identity never absorbs these relation facts;
- only one current physical placement mode may be active among `located_at`, `stored_in`, `carried_by`, `equipped_by`;
- ownership may coexist with any legal placement mode;
- fixed Items cannot be carried or equipped.

I5.6 validates relation intent only. It does not resolve whether referenced Sandbox objects exist; I5.7/I5.8 apply boundaries own reference resolution.

Structural Location `contains` is intentionally not an Item mutable-placement slot here. Structural fixture composition is resolved by the later Location composition contract rather than turning ordinary inventory storage into `contains`.

---

## Economic policy

Every Item must explicitly declare one value policy.

The schema reuses existing classifications:
- `standalone_asset`;
- `component`;
- `consumable_stock`;
- `resource_proxy`;
- `economically_immaterial`.

And existing net-worth treatments:
- `independent`;
- `included_in_parent`;
- `derived_stock`;
- `excluded`.

Exact staged policy fields:
- `classification`;
- `currency_code`;
- `market_value_minor`;
- `replacement_value_minor`;
- `unit_value_minor`;
- `unit_quantity`;
- `unit_label`;
- `net_worth_treatment`;
- `included_in_parent_ref`;
- `valuation_method`.

Important coherence:
- represented monetary values require a 3-letter currency code;
- `included_in_parent` requires an explicit staged parent reference;
- `derived_stock` is reserved for `consumable_stock`;
- `consumable_stock` requires stackability plus unit value/quantity/label matching stack unit;
- `resource_proxy` and `economically_immaterial` are excluded and carry no monetary value in Item schema v1.

These are staged Sandbox policy semantics only. The validator does not write canonical `economic_value_profiles`, assets, accounts or net-worth state.

---

## Requirements

Exact top-level requirement slot:
- `use`.

It is either `null` or an I5.5 typed requirement contract.

The requirement is validated but not evaluated as permission during Item creation because no actor context is implied by creating an Item.

Important:

`derived Item grade != Item use requirement`.

A 55 lb dumbbell can derive S Item resistance-load grade while its explicit use requirement is B, A, S or absent according to the represented interaction contract. The grade is never copied automatically into the requirement.

I5.6 also closes one fail-closed edge in I5.5: invalid minimum-grade tokens are rejected even when evaluation context lacks the requested grade dimension.

---

## Pure validation / isolation

`validate_item_payload()` has no persistence argument.

Acceptance additionally fingerprints a migrated database before and after validating multiple Item payloads and proves canonical state is unchanged.

No I5.6 path writes:
- canonical `entity_definitions`;
- canonical `entities`;
- `inventory_stacks`;
- canonical relations;
- canonical economic value/asset/account state;
- Creation Sandbox tables.

Sandbox materialization begins only in I5.7.

---

## Representative v1 coverage

Acceptance validates at least:
- unique movable resistance-training equipment;
- stackable consumable/nutrition stock;
- movable container Item.

This is enough to prove the conditional-module architecture without prebuilding every future tool/electronic/medical/durability subtype.

---

## Explicit non-goals

I5.6 does not:
- create or persist Items;
- add Telegram Item creation UI;
- create batch orchestration;
- resolve Sandbox relation references;
- implement move/store/equip operations;
- implement arbitrary capacity kinds beyond represented volume;
- add durability/condition simulation;
- add crafting;
- add arbitrary executable capability names;
- migrate existing Real World catalog rows into the new schema;
- change existing inventory persistence.

---

## Acceptance

`tests/test_universal_item_schema_v1.py` proves:
- exact top-level/core/module/capability rejection;
- required core fields cannot be omitted;
- conditional module requirements are enforced;
- unique versus stackable instance semantics cannot conflict;
- Imperial/Metric inputs normalize to equivalent physical truth;
- deterministic Item grade derives from normalized resistance load;
- stack/nutrition semantics align with current catalog rules;
- container capacity is normalized without collapsing storage relation;
- economic policy is mandatory and coherent;
- Item grade and actor use requirement remain separate;
- definition identity does not absorb current owner/location;
- current physical placement modes are mutually exclusive;
- Manual/AI-shaped payloads converge on one normalized contract;
- validation produces zero canonical DB mutation.

Next slice after green CI:

**I5.7 — Sandbox Item Creation v1: Single.**
