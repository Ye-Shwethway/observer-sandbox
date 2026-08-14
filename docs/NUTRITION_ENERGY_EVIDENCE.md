# Minimum Nutrition & Energy Balance Evidence v1

Status: **DEPLOYED + STRUCTURED EATING BRIDGE CANDIDATE**
Synchronized: 2026-08-14

## Purpose

Provide causal, actor-scoped nutrition and energy-expenditure evidence before any body-composition engine is allowed to change body weight or body-fat percentage.

This is BC-1 under `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`.

## Core invariant

`completed actor action + actor profile + authored food/activity policy -> immutable intake/expenditure evidence`

Later body-composition settlements may aggregate that evidence over bounded simulated-time windows. They must not infer calories or protein from abstract hunger/energy need scores.

BC-1 itself **does not mutate body composition**.

## Nutrition authority layers

There are two intentionally distinct nutrition surfaces during the transition from legacy generic meal targets to real inventory foods.

### 1. Legacy generic action-target nutrition profiles

Canonical transitional content: `config/nutrition_profiles.v1.json`.

These profiles support pre-inventory `eat` targets such as generic Estate meal resources. Completed legacy events snapshot the target profile into `payload_json.nutrition_intake`; historical events are never retroactively rewritten.

Legacy profiles remain only for historical/pre-v1 compatibility. They are not the source of truth for newly structured inventory meals.

### 2. Universal inventory-food nutrition definitions

Canonical universal food content: `config/items.v1.json`.

For real inventory foods, nutrition belongs to the **universal item definition**, never to a character, location, container or concrete stack. Definitions provide nutrition basis, canonical unit, kcal/protein/carbohydrate/fat and default portion quantity.

Deterministic code scales those values for requested quantities. The model must never invent or perform authoritative macro arithmetic.

`nutrition_facts.py` provides definition-scoped observer projections. Telegram Inventory item details expose the same universal facts; this is not a second nutrition database.

Examples:
- cooked chicken breast: 100 g basis, default 200 g -> 330 kcal / 62 g protein / 0 g carbohydrate / 7.2 g fat;
- apple: 1 piece basis/default -> 95 kcal / 0.5 g protein / 25 g carbohydrate / 0.3 g fat.

## Eating Behavior v1 integration

Canonical: `docs/EATING_BEHAVIOR_V1.md`.

PR #76 makes new natural eating inventory-backed while preserving the existing BC-1 event field:

- cognition proposes one to six exact food stack IDs + quantities;
- the deterministic engine validates reachability, stock and bounded portion policy;
- all selected stacks are consumed atomically at action completion;
- definition-based nutrition for every consumed quantity is aggregated;
- the combined snapshot is persisted in the existing `payload_json.nutrition_intake` field with `source=eating-behavior-v1`;
- each structured item snapshot preserves stack/definition/quantity/unit/macros and remaining quantity;
- an already-persisted pre-v1 empty-resource eat action may finish through the legacy target profile without decrementing inventory;
- newly model-planned eat actions fail closed without valid resources.

This means `energy_balance_window()` does not need a second aggregation model for structured meals: it continues reading the same immutable top-level kcal/protein/carbohydrate/fat fields.

Hunger/satiety effects remain separate short-timescale behavior signals. Eating Behavior v1 does not treat kcal as a direct numerical hunger-score store.

## Resting energy reference

Canonical policy: `config/energy_expenditure.v1.json`.

v1 uses the **Mifflin-St Jeor 1990** healthy-adult resting-energy equation because the current profile supplies body weight, height, age derived from DOB + simulation time, and sex.

Reference: Mifflin MD et al. *A new predictive equation for resting energy expenditure in healthy individuals.* Am J Clin Nutr. 1990;51:241-247. PMID 2305711.

The result is an estimate, not measured calorimetry. Missing required actor profile inputs fail explicitly rather than copying Darian or inventing coefficients.

This does not make Mifflin-St Jeor the permanent whole-universe model. Once live FM/FFM exists, later versions may compare or replace it with body-composition-informed REE models under separately validated policy.

Relevant evidence includes:
- Nelson KM et al. *Prediction of resting energy expenditure from fat-free mass and fat mass.* Am J Clin Nutr. 1992. PMID 1415003.
- Wang Z et al. *Resting energy expenditure-fat-free mass relationship: new insights provided by body composition modeling.* Am J Physiol Endocrinol Metab. 2000. PMID 10950820.

## Action energy expenditure

Every supported completed action receives `payload_json.energy_expenditure` with estimated kcal, actor-specific resting component, authored activity multiplier, duration, resting-reference inputs/formula/source and policy revision.

Activity multipliers are **Compendium-informed intensity anchors**, not direct calorimetry.

Reference: Herrmann SD et al. *2024 Adult Compendium of Physical Activities: A third update of the energy costs of human activities.* J Sport Health Sci. 2024. PMID 38242596.

Examples informing current policy include sleeping about 1.0 MET, eating sitting 1.5, showering 2.0, moderate walking around 3.5, vigorous resistance training around 6.0, punching bag 5.8, sparring 7.8, obstacle/boot-camp exercise 5.0 and general yoga/mobility around 2.3.

v1 scales authored activity ratio against the actor's own estimated resting expenditure rather than assigning one kcal/min value to all actors.

## Energy-balance window

`energy_balance_window()` aggregates persisted BC-1 evidence between simulated-time boundaries and reports intake kcal/macros, intake count, estimated expenditure, net energy, covered action minutes, evidence coverage, missing event IDs and completeness.

Current completeness threshold is 95% action-time coverage, with no overlapping action events lacking expenditure evidence and no completed eat event lacking nutrition evidence. This is an evidence-quality policy, not physiology.

Historical pre-BC-1 events are intentionally not recomputed from current catalogs.

## Universal character behavior

No Darian-specific metabolic or meal branch exists.

For another actor:
- their own age/sex/height/weight drive resting reference;
- their own action duration/target drives expenditure evidence;
- consumed universal food definitions + quantities drive structured intake;
- missing prerequisites fail evidence coverage rather than falling back to Darian.

## Relationship to needs

`needs.hunger` and `needs.energy` remain short-timescale behavioral/physiological control signals. BC-1 deliberately does not pretend they are kcal stores.

## BC-2 activation gate

Before `body.weight_lb` or `body.body_fat_pct` become simulated, observe natural post-Eating-Behavior production evidence read-only and answer:
- are newly completed meals actually structured inventory meals?
- is natural meal cadence/intake plausible?
- are commonly consumed universal food definitions nutritionally complete?
- does inventory depletion match immutable meal evidence?
- is near-complete daily expenditure coverage maintained?
- are REE/action-energy magnitudes plausible?

If meal cadence is structurally wrong, calibrate the smallest behavior/needs-to-meal bridge before enabling body-composition mutation. Do not hide a cadence defect with implausibly large or small meals.

## Explicit non-goals

This layer does not add:
- body-weight or body-fat mutation;
- FM/FFM partitioning;
- genetic muscle-potential settlement;
- protein-driven hypertrophy settlement;
- fluid/glycogen dynamics;
- detailed micronutrient tracking;
- endocrine simulation;
- recipes/cooking;
- economy/currency/vendors;
- additional model calls merely to calculate nutrition.
