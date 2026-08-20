# Item Grading Coverage Foundation v1

Status: **APPROVED IMPLEMENTATION CONTRACT — FOUNDATION COMPLETION BEFORE FRESH MASS GENERATION**  
Date: 2026-08-20

## Decision

Do not mass-generate fresh Items until the grading evidence foundation is broad enough that common Item capabilities can be represented and graded without later schema churn.

This contract extends `UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

## Core problem

The grading socket can only grade represented facts. Current `item-v1` structured modules cover physical dimensions, stack/nutrition, container volume and resistance training. Common capability facts such as flashlight luminous output/runtime, battery energy capacity, device power, operating range, speed or digital throughput otherwise live only in prose descriptions and cannot participate in deterministic grading.

## Foundation rule

Add a generic **Item Metrics socket** rather than one schema module per Item family.

Canonical flow:

`Creator intent -> registered metric facts -> strict normalization -> registered grading dimensions/reference profiles -> deterministic grade results`

No `if backpack / flashlight / sword / battery` grading switchboard is permitted.

## Item Metrics module

`definition.modules.metrics` is a sparse mapping from registered metric id to one exact numeric measurement.

Each metric registration defines:
- stable metric id;
- human label;
- canonical unit;
- accepted input units and deterministic conversions;
- numeric constraints;
- whether the metric is safe for AI ordinary inference;
- optional grading dimension/reference binding.

Unknown metric ids fail closed. Adding a new registered metric must not require changing the Item validator core or provider schema structure.

Initial broad metric catalog should cover common universal quantitative capabilities:
- `luminous_flux` (lm);
- `runtime` (h);
- `power` (W);
- `energy_capacity` (Wh);
- `range` (m);
- `speed` (m/s);
- `data_rate` (Mbps);
- `digital_storage` (GB);
- `beam_distance` (m);
- `water_resistance_depth` (m);
- `charge_time` (h);
- `payload_capacity` (kg).

Container volume remains authoritative in the existing `container.capacity_volume` module and should be graded directly from that raw field rather than duplicated as a metric.

## Grading semantics

V1 coverage grades named **capability magnitude**, not vague overall quality.

Examples:
- Luminous Flux grade describes represented light-output magnitude.
- Runtime grade describes represented operating-duration magnitude.
- Storage Capacity grade describes represented physical container-volume magnitude.
- Energy Capacity grade describes represented stored-energy magnitude.
- Range grade describes represented operating/reach range magnitude.

A high grade does not imply the Item is generally better, safer, more efficient or more appropriate.

## Generic reference-band evaluator

Add one reusable deterministic evaluator family for monotonic numeric dimensions whose registered reference profile supplies explicit grade-band minima.

A reference profile contains:
- dimension binding;
- canonical unit;
- ascending grade minima;
- universe-policy compatibility;
- semantic note stating what the grade measures.

Reference bands are versioned registry data. AI does not invent or modify bands at Item-generation time.

## Initial realistic-universe coverage

The default realistic grading policy may allow registered magnitude dimensions for ordinary physical/technical capability values. Supernatural-specific dimensions remain excluded unless another universe policy explicitly admits them.

Initial dimensions should include:
- existing `resistance_load`;
- `storage_capacity` from `container.capacity_volume`;
- `luminous_flux`;
- `runtime`;
- `power`;
- `energy_capacity`;
- `range`;
- `speed`;
- `data_rate`;
- `digital_storage`;
- `beam_distance`;
- `water_resistance_depth`;
- `payload_capacity`.

`charge_time` is represented as a metric but should not receive a monotonic-high grade because lower charge time is normally preferable; leave it ungraded until a monotonic-low or context-aware evaluator is explicitly accepted.

## AI creation contract

The provider-facing Item form exposes nullable slots for every registered metric. Canonicalization removes null metric entries.

AI rules:
- populate a metric only when supported by Creator intent or conservative ordinary inference;
- do not invent unknown metric ids;
- do not author grade letters;
- do not author evaluator ids, thresholds or reference profiles;
- do not duplicate an authoritative existing module fact as a metric;
- leave unknown quantitative facts null.

Fresh flashlight example can therefore represent `luminous_flux=1000 lm`, `runtime=10 h`, `beam_distance=<known value or null>` and grading is derived after validation.

## Edit / persistence / display

- Metrics persist as raw normalized Item facts, not grade authority.
- Item Edit exposes metric values/units through the existing recursive Modules editor.
- Grades are rebuildable/read-time interpretations.
- Draft and approved Item detail show a human `PERFORMANCE METRICS` section plus `GRADING`.
- Raw `.txt` export retains canonical metrics but no GradePlan authority.

## Acceptance

Foundation completion must prove:
1. registered metric unit conversion is deterministic and idempotent;
2. unknown metric ids/units reject;
3. AI fill schema is generated from the metric registry and canonicalizer removes null metrics;
4. a fresh flashlight-like payload can represent luminous flux + runtime and derive grades automatically;
5. a container derives storage-capacity grade from the existing container module without duplicated metric data;
6. ordinary Items remain valid when no metrics apply;
7. new metric registrations can be added without Item-family branching;
8. realistic policy still rejects unauthorized supernatural dimensions;
9. Item Edit can revalidate normalized persisted metrics;
10. no DB migration, no canonical Real World mutation, no automatic overall Item grade.

Fresh broad Item regeneration should resume only after this foundation and its intended initial dimension catalog are repository-accepted and live-verified enough for Creator acceptance.
