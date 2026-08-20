# Universal Quantity & Measurement Contract v1

Status: **IMPLEMENTATION CANDIDATE — I5.3**  
Date: 2026-08-20

## Purpose

Provide one small presentation-independent physical quantity abstraction for Creator Item/Location creation while preserving existing Character/body and inventory storage contracts.

The first vertical needs four physical dimensions:
- mass/load;
- length;
- area;
- volume/capacity.

This slice does not redesign every existing measurement-bearing subsystem.

---

## Core invariant

`physical truth -> normalized quantity -> deterministic conversion -> Creator-facing display`

Presentation is not authority.

Examples:
- `55 lb` and `24.94758035 kg` normalize to the same mass truth;
- switching display from Imperial to Metric does not rewrite the object;
- grades, requirements and runtime calculations consume normalized quantities, not strings such as `"55 lbs"`.

---

## Runtime helper

Implementation:
`src/observer_sandbox/physical_quantity.py`

Authoritative object:
`PhysicalQuantity(kind, base_value)`

Normalized base units:
- mass -> `kg`;
- length -> `m`;
- area -> `m2`;
- volume -> `m3`.

The helper intentionally has no DB ownership. Item/Location schemas may serialize normalized values through their own strict contracts later.

---

## Creator-facing default

Imperial is the default presentation system.

Default v1 display units:
- mass/load -> `lb`;
- length/dimensions -> `in`;
- area -> `ft²`;
- volume/capacity -> US gallons.

Metric display remains available through the same physical truth:
- kg;
- m;
- m²;
- L.

A later UI may choose a more context-specific presentation unit (for example `ft` instead of `in`) without changing the normalized quantity.

---

## Supported v1 units

Mass:
- kg;
- g;
- lb;
- oz.

Length:
- m;
- cm;
- mm;
- in;
- ft;
- yd.

Area:
- m²;
- cm²;
- in²;
- ft²;
- yd².

Volume/capacity:
- m³;
- L;
- mL;
- in³;
- ft³;
- US fl oz;
- US cup;
- US pint;
- US quart;
- US gallon.

The internal schema tokens remain ASCII-safe (`m2`, `ft2`, `gal_us`, etc.); presentation may use friendly symbols/labels.

---

## Validation rules

The quantity layer fails closed when:
- quantity kind is unsupported;
- unit is unsupported;
- unit dimension does not match quantity kind;
- value is non-numeric/boolean;
- value is NaN/infinite;
- value is negative.

Zero is valid at this generic layer. Domain schemas may require strictly positive values where appropriate, for example an Item physical mass or non-empty capacity.

---

## Separation from domain semantics

This module represents physical dimensions only.

It does **not** decide:
- whether a mass represents an Item's total mass, resistance load, payload or capacity;
- whether an area is floor area, surface area or footprint;
- whether a volume is physical occupied volume, liquid capacity or storage capacity;
- whether a quantity is gradeable;
- whether a Character meets an interaction requirement.

Those meanings belong to strict Item/Location modules and later grade/requirement contracts.

Therefore:

`quantity kind != domain meaning`

and:

`Item Grade != raw quantity != interaction Requirement Grade`.

---

## Existing-system compatibility

### Character/body

Do not migrate existing Character body/profile measurement fields as part of I5.3. They remain authoritative under their current registry/storage contracts.

The new helper may later be used at adapters/boundaries when Item/Location calculations need to compare compatible quantities.

### Inventory

Existing `inventory_stacks.quantity + unit` remains authoritative for fungible stock. I5.3 does not rewrite stack persistence.

When future Item schemas need physical mass/dimensions/capacity, they use this normalized quantity contract separately from inventory stock count/mass/volume semantics.

Example:
- a bag of rice may have stack quantity semantics for stock;
- the bag object may also have physical dimensions and total mass;
- these are related but not the same field.

---

## Deterministic conversion policy

Conversions use fixed standard constants in code.

Round-trip acceptance is tested with explicit numeric tolerance; display rounding is downstream and cannot mutate `PhysicalQuantity.base_value`.

Explicit display-unit override is presentation-only.

---

## Non-goals

I5.3 does not implement:
- temperature;
- speed/velocity;
- force/torque/power/energy;
- currency;
- nutrition units;
- time/duration;
- arbitrary user-defined units;
- localization/pluralization engine;
- global Character measurement migration;
- DB schema migration;
- Telegram setting for Metric/Imperial switching.

Add another dimension only when a concrete later vertical needs it.

---

## Acceptance

`tests/test_physical_quantity_v1.py` proves:
- Imperial and Metric equivalents normalize to the same physical truth;
- mass, length, area and volume conversions work;
- Imperial is the default Creator-facing presentation;
- display switching does not mutate authoritative state;
- round-trip conversion stays within explicit tolerance;
- serialized authority is normalized rather than formatted text;
- invalid units/kinds/values fail closed.

Next dependency after green CI:

**I5.4 — Universal Cross-Domain Grade Contract.**
