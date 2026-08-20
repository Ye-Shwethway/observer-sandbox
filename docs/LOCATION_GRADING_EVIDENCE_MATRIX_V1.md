# Location Grading Evidence Matrix v1

Status: **L11.0 AUTHORITATIVE EVIDENCE CLASSIFICATION**  
Date: 2026-08-21

## Purpose

Define exactly which `location-v2` facts may feed grading, which facts remain policy/runtime/relationship data, and which values are explicitly ungraded.

Core invariant:

> **Raw represented Location facts are authority. Grades are deterministic derived interpretations only.**

AI, Manual Creator forms and persisted Location source payloads do not author final grade letters, evaluator ids, thresholds or reference profiles.

---

## Evidence classification legend

Each field/family is classified primarily as one or more of:

- **Definition** — stable authored Location fact.
- **Initial state** — Creation seed only; live value becomes runtime authority after activation.
- **Runtime** — downstream changing state, not Location Creation source truth.
- **Relationship/graph** — reference or graph proposal resolved during materialization.
- **Policy/config** — deterministic policy/configuration input.
- **Grading evidence** — may feed a registered grade dimension when evidence/reference/policy is sufficient.
- **Presentation/provenance** — descriptive/audit context.
- **Ungraded** — must not be automatically treated as quality/capability evidence.

---

# Matrix

| Schema path / family | Primary authority class | Grade dimension(s) | Rules |
| --- | --- | --- | --- |
| `identity.key` | Definition | completeness only | Stable identity evidence; never quality/prestige. |
| `identity.name` | Definition | completeness only | Display name existence may support representation completeness only. |
| `identity.kind` | Definition | completeness; reference selector | May select kind-aware spatial-scale/reference profiles; kind itself is not a grade. |
| `identity.description` | Presentation/definition | completeness only | Text length/detail is never graded. |
| `identity.functional_classes[]` | Definition | infrastructure applicability only | Classification may select applicable evaluators; count is not a score. |
| `identity.tags[]` | Presentation/query | none | Explicitly ungraded. |
| `structure.parent_ref` | Relationship/graph | completeness | Structural resolution supports L1+ completeness; parent prestige never transfers. |
| `structure.exposure` | Definition | completeness/context | May shape environment/reference applicability; not a quality score. |
| `geography.*` | Definition | completeness/context only | Geographic precision must not improve a quality grade merely because coordinates exist. |
| `spatial.area` | Definition + grading evidence | spatial_scale | Requires compatible kind/reference policy. Larger means greater scale, not better. |
| `spatial.length/width/height` | Definition + grading evidence | spatial_scale when evaluator supports | May derive size evidence when area absent/appropriate; no generic larger=better. |
| `spatial.elevation` | Definition | none by default | Ungraded until a concrete elevation-relative dimension exists. |
| `spatial.terrain` | Definition/presentation | none by default | No subjective terrain quality grade. |
| `spatial.surface` | Definition/context | infrastructure/connectivity applicability only | May affect later traversal/facility evaluators; surface token alone is not a grade. |
| `spatial.orientation_notes` | Presentation | none | Explicitly ungraded. |
| `boundary.type` | Definition | completeness/context | Supports represented boundary completeness; no physical=better assumption. |
| `boundary.enclosure` | Definition | completeness/context | Supports container completeness; no enclosed=better assumption. |
| `boundary.notes` | Presentation | none | Explicitly ungraded. |
| `access.policy` | Policy/config | completeness only | Access semantics help L2 representation; never converted into connectivity/security/quality grade automatically. |
| `operations.initial_state` | Initial state | completeness only | Initial operational configuration may support L4 completeness; open is not better than closed/locked. |
| `topology.interfaces[].key/name/kind` | Graph definition | completeness/connectivity | Kind may shape evaluator semantics; names never score. |
| `topology.interfaces[].destination_ref` | Relationship/graph | completeness/connectivity | Connectivity only after successful graph resolution. |
| `topology.interfaces[].directionality` | Graph definition | connectivity | Deterministic graph evidence; no simplistic two_way=better rule outside evaluator semantics. |
| `topology.interfaces[].enabled` | Initial state/config | connectivity after resolution | Draft/initial state may affect available edge evidence. Runtime changes supersede after activation. |
| `topology.interfaces[].traversal_modes` | Graph definition | connectivity | Mode breadth may be evaluator evidence only under a reference policy; raw count is not sufficient. |
| `topology.interfaces[].base_duration_minutes` | Definition/evidence | connectivity | May support cost-aware graph interpretation; faster is not automatically higher grade unless an approved evaluator says so. |
| `topology.interfaces[].distance` | Definition/evidence | connectivity | May support route/cost context; distance alone is ungraded. |
| `facilities.capabilities[]` | Definition + grading evidence | infrastructure_capability | Evaluator uses registered semantic capability coverage, never raw string count. |
| `facilities.facility_types[]` | Definition + grading evidence | infrastructure_capability | Registry semantics/reference profile required. |
| `facilities.resource_types[]` | Definition + grading evidence | infrastructure_capability | Registry semantics/reference profile required. |
| `facilities.utilities[]` | Definition + grading evidence | infrastructure_capability | Registry semantics/reference profile required. |
| `environment.lighting_profile` | Definition/context | completeness/infrastructure applicability only | No brighter=better assumption. |
| `environment.weather_exposure` | Definition/context | completeness/infrastructure applicability only | Protected/exposed are contextual, not universal quality. |
| `control.ownership_class` | Definition/policy | completeness/context | Private/public/etc. are not prestige grades. |
| `control.owner_ref` | Relationship | completeness/context only | Owner identity/value does not transfer into Location grade. |
| `control.operator_ref` | Relationship | completeness/context only | Operator identity does not transfer into Location grade. |
| `economic_policy.classification` | Policy/evidence | asset_value applicability | Selects whether asset-value interpretation is meaningful. |
| `economic_policy.market_value_minor` | Definition/evidence | asset_value | Requires currency, universe/time/context reference profile. |
| `economic_policy.replacement_value_minor` | Definition/evidence | asset_value where applicable | Must not be mixed blindly with market value. |
| `economic_policy.currency_code` | Definition/context | asset_value reference selector | Currency itself ungraded. |
| `economic_policy.net_worth_treatment` | Policy | none | Accounting treatment is not a grade. |
| `economic_policy.included_in_parent_ref` | Relationship/policy | none | Explicitly ungraded. |
| `economic_policy.valuation_method` | Provenance/context | asset_value validation context | Method text/token does not score. |
| `provenance.*` | Presentation/provenance | none | Source status/confidence must never inflate grade. |

---

# Initial Location GradeProfile contract

Domain: `location`

Initial dimensions:

## 1. `completeness`

Status: **mandatory / active**

Evaluator: existing `location-completeness-v1` semantics, evolved only as needed to recognize v2 fields without changing meaning.

Evidence:

- valid identity;
- structural container evidence;
- explicit access/topology;
- machine-readable affordance evidence;
- operational/environment/economic/control configuration.

Output remains representation completeness, not quality.

## 2. `spatial_scale`

Status: **planned for L11.1; evidence/reference gated**

Evidence:

- `identity.kind`;
- `spatial.area` and compatible dimensions.

Required contract:

- kind-aware `ReferenceProfile`;
- deterministic evaluator;
- universe-policy allowance.

The grade describes scale magnitude only.

## 3. `infrastructure_capability`

Status: **planned for L11.1; evidence/reference gated**

Evidence:

- registered `capabilities`;
- registered `facility_types`;
- registered `resource_types`;
- registered `utilities`.

Evaluator rules:

- no raw count grading;
- semantically equivalent evidence must not double-count automatically;
- reference profile defines expected capability groups for the relevant Location kind/function;
- absent evidence remains ungraded/low evidence according to explicit evaluator semantics, never guessed.

## 4. `connectivity`

Status: **graph-context gated; finalize in/after L11.2**

Evidence:

- resolved interface destinations;
- directionality;
- enabled state;
- supported traversal modes;
- route/topology context where required.

Rules:

- connectivity != access authorization;
- connectivity != design quality;
- isolated Locations can legitimately grade low in this descriptive dimension;
- isolated drafts without resolved graph context remain ungraded.

## 5. `asset_value`

Status: **reference gated / optional**

Evidence:

- economic classification;
- represented market/replacement value;
- currency;
- compatible universe/time/kind reference profile.

Rules:

- no timeless fixed USD thresholds;
- no currency conversion guesswork in grading;
- no market-value grade without a compatible reference profile.

## 6. `security`

Status: **reserved / inactive**

No grade is produced until a bounded authoritative security evidence contract exists.

Do not infer security from `private`, `locked`, `gate`, `security` functional class, or sparse surveillance labels alone.

---

# Overall grade policy

`GradeProfile.overall = null` for Location v2 initial implementation.

No average of completeness, size, infrastructure, connectivity or asset value is semantically valid by default.

Future overall/composite grades require explicit named context-specific semantics, for example:

- `residential_capability`
- `commercial_venue_capability`
- `military_facility_capability`
- `wilderness_accessibility`

Each future composite must register its own evaluator/reference/policy rather than averaging unrelated grade ranks.

---

# Universe policy

The default realistic universe policy may allow only grading dimensions whose evidence/evaluator/reference semantics are represented and realistic.

Registering a future fantasy/supernatural facility, portal or dimension does not make that grading legitimate in the realistic Real World automatically.

`schema-valid != universe-compatible` remains authoritative.

---

# Creation and UI implications

- Provider-facing AI schema contains raw Location facts only.
- Manual Location forms contain raw facts only.
- Preview/detail may show derived GradeProfile.
- Raw `.txt` authoring export must not gain grade authority fields.
- Edit changes raw evidence; grades are recomputed afterward.
- Missing grading evidence is displayed as ungraded/not available, not fabricated.
