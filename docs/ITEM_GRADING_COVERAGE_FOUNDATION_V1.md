# Item Grading Coverage Foundation v1

Status: **REPOSITORY-ACCEPTED — LIVE REPRESENTATIVE ACCEPTANCE PENDING**  
Date: 2026-08-20

## Decision

Do **not** mass-generate fresh Items yet. The broad grading/evidence foundation is repository-accepted, but production deployment and one representative fresh multi-class generation pass should be verified before large-scale Item creation resumes.

This contract extends `UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

Repository acceptance:
- PR **#362 — Complete broad Item grading coverage foundation**
- merged at `b2b2d0b058bd9835cd311b78586b4ee3b09534ef`
- CI **#1198** ✅ after 112 selected test files + CLI smoke
- first CI #1196 found only two stale exact-schema expectations; after updating those contracts, #1198 passed
- no DB migration
- no canonical Real World mutation

---

## Core architecture

The grading socket can only grade represented facts. Broad Item creation therefore now has a generic **Item Metrics socket** rather than one schema module per Item family.

Canonical flow:

`Creator intent -> registered raw metric facts -> strict normalization -> registered grading dimensions/reference profiles -> deterministic grade results`

No `if backpack / flashlight / sword / battery` grading switchboard is permitted.

### `definition.modules.metrics`

A sparse mapping from registered metric id to one exact numeric measurement.

Each metric registration supplies:
- stable metric id;
- human label;
- canonical unit;
- accepted input units + deterministic conversion;
- numeric constraints;
- provider-form slot generation.

Unknown metric ids and unsupported units fail closed. Null AI slots are removed during canonicalization. Normalized persisted metrics revalidate idempotently for Item Edit/re-entry.

Initial registered metric catalog:
- `luminous_flux` — lm
- `runtime` — h
- `power` — W
- `energy_capacity` — Wh
- `range` — m
- `speed` — m/s
- `data_rate` — Mbps
- `digital_storage` — GB
- `beam_distance` — m
- `water_resistance_depth` — m
- `charge_time` — h
- `payload_capacity` — kg

Container volume remains authoritative in existing `container.capacity_volume`; resistance load remains authoritative in existing `resistance_training.resistance_load`. They are not duplicated into metrics.

---

## Initial realistic Item grading coverage

Grades in this foundation describe named **capability magnitude**, not vague overall Item quality.

Current registered dimensions:
- `resistance_load`
- `storage_capacity`
- `luminous_flux`
- `runtime`
- `power`
- `energy_capacity`
- `range`
- `speed`
- `data_rate`
- `digital_storage`
- `beam_distance`
- `water_resistance_depth`
- `payload_capacity`

The expanded Item registry uses reusable versioned reference-band evaluators/profiles and the realistic Item coverage universe policy. Current magnitude dimensions use E–S within that policy.

`charge_time` is represented as raw evidence but intentionally ungraded in v1 because lower is normally preferable; it must not be forced into a monotonic-high evaluator.

A high capability-magnitude grade does **not** imply the Item is generally better, safer, more efficient, more durable or more appropriate.

Overall Item Grade remains absent unless a later explicit defensible composite contract is accepted.

---

## AI generation contract

Single and Batch Creator AI provider forms now derive nullable metric slots from the registry.

AI may:
- map represented measurable specifications to matching registered metric slots;
- use conservative ordinary inference where already permitted by Creator creation policy;
- leave unknown/inapplicable values null.

AI must not:
- invent unknown metric ids;
- author grade letters;
- author evaluator ids, thresholds or reference profiles;
- duplicate container capacity/resistance load into generic metrics;
- fabricate unknown quantitative precision.

Final grades remain deterministic derived interpretation.

---

## Persistence / Edit / UI

- metrics persist as normalized **raw Item facts**, not grade authority;
- GradePlan/GradeProfile remain rebuildable/read-time interpretation;
- Item Edit's recursive Modules traversal automatically exposes metric `value` and `unit` fields without Item-family editor code;
- any edited metric is previewed and revalidated through strict current `item-v1` before Apply;
- draft detail shows `PERFORMANCE METRICS` + `GRADING`;
- approved Item detail shows `⚙️ PERFORMANCE METRICS` + `🏅 GRADING`;
- technical `.txt` export retains raw metric facts but no GradePlan authority.

Representative accepted test semantics include:
- flashlight `1 klm` -> normalized `1000 lm` -> Luminous Flux A;
- runtime `600 min` -> normalized `10 h` -> Runtime B;
- beam distance `300 m` -> Beam Distance B;
- 30 L container -> Storage Capacity B from the existing container module;
- charge time can persist without a fabricated grade;
- unknown metric/unit rejects;
- normalized metric payload revalidates across persistence/Edit boundary.

---

## Remaining gate before broad fresh generation

Repository foundation is accepted, but deployment/live behavior must be verified separately.

Before mass Item generation:
1. verify production runtime includes PR #362 or later;
2. generate **one small representative fresh batch**, not a large catalog, covering several different classes such as container + flashlight/device + battery/power item + training/load item;
3. verify AI captures supported raw metrics rather than leaving known specs only in prose;
4. verify Preview shows normalized human metrics and deterministic dimension grades;
5. approve and verify approved Item detail shows the same semantics;
6. enter Item Edit on a metric-bearing Item, edit one metric, Preview/Apply/Done, and verify revalidation/pause restoration;
7. verify Real World/canonical state remains unchanged.

Only after that representative live pass should broad fresh Item generation resume.

Future metric/dimension additions remain socket registrations rather than Item-family rewrites. Items with genuinely unrepresented/uncovered dimensions remain valid and explicitly ungraded rather than receiving fake precision.
