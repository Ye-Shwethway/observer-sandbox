# Minimum Nutrition & Energy Balance Evidence v1

Status: **DEPLOYED + UNIVERSAL ITEM BRIDGE ACTIVE**
Synchronized: 2026-08-14

## Purpose

Provide causal, actor-scoped nutrition and energy-expenditure evidence before any body-composition engine is allowed to change body weight or body-fat percentage.

This is BC-1 under `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`.

## Core invariant

`completed actor action + actor profile + authored food/activity policy -> immutable intake/expenditure evidence`

Later body-composition settlements may aggregate that evidence over bounded simulated-time windows. They must not infer calories or protein from abstract hunger/energy need scores.

BC-1 itself **does not mutate body composition**.

## Nutrition authority layers

There are now two intentionally distinct nutrition surfaces during the transition from legacy generic meal targets to real inventory foods.

### 1. Legacy generic action-target nutrition profiles

Canonical transitional content: `config/nutrition_profiles.v1.json`.

These profiles support the pre-inventory `eat` action targets such as generic Estate meal resources. Each authored portion profile contains:
- energy kcal;
- protein grams;
- carbohydrate grams;
- fat grams;
- human-readable portion label;
- evidence-source revision.

The values are simulation meal-content policy for those older generic targets. They remain separate from hunger/energy effects. Hunger reduction does not mathematically imply calorie content, and calorie content does not directly write the hunger score.

Completed legacy `eat` events snapshot the selected target's nutrition profile into `payload_json.nutrition_intake`. Historical events are not retroactively re-derived when the catalog changes.

If a legacy edible target has no nutrition profile, the action remains valid for ordinary needs behavior but the corresponding energy-balance window is incomplete for body-composition purposes.

### 2. Universal inventory-food nutrition definitions

Canonical universal food content: `config/items.v1.json`.

For real inventory foods, nutrition belongs to the **universal item definition**, never to Darian, the Estate, a specific refrigerator, or a specific stack. Concrete inventory stacks reference those reusable definitions.

Each current food definition provides:
- authored nutrition basis quantity + canonical unit;
- energy kcal;
- protein grams;
- carbohydrate grams;
- fat grams;
- default portion quantity.

Deterministic code scales those definition values for requested quantities. The model must never invent or perform authoritative macro arithmetic.

`nutrition_facts.py` provides a definition-scoped projection suitable for observer surfaces and future eating decisions. It is independent of current stock quantity: a depleted stack still has the same food definition and nutrient facts. Actual eating will separately validate that requested stock is available before mutation.

Telegram Inventory item details expose **Nutrient Facts · Default Portion** from the same universal definition semantics. This observer presentation is not a second nutrition database.

Current examples:
- cooked chicken breast: 100 g basis, default 200 g -> 330 kcal / 62 g protein / 0 g carbohydrate / 7.2 g fat;
- apple: 1 piece basis/default -> 95 kcal / 0.5 g protein / 25 g carbohydrate / 0.3 g fat.

Until Eating Behavior v1 replaces the old generic meal-target path, both layers may coexist. New natural inventory eating must use universal item definitions; it must **not** bind new food behavior back to the transitional generic meal-target profiles.

## Resting energy reference

Canonical policy: `config/energy_expenditure.v1.json`.

v1 uses the **Mifflin-St Jeor 1990** healthy-adult resting-energy equation because the current profile already supplies its required causal inputs:
- body weight;
- height;
- age derived from date of birth + simulation time;
- sex.

Reference: Mifflin MD et al. *A new predictive equation for resting energy expenditure in healthy individuals.* Am J Clin Nutr. 1990;51:241-247. PMID 2305711.

The result is an estimate, not measured calorimetry. If a future actor lacks required profile inputs or has a sex value not supported by this published equation, BC-1 fails the energy-reference evidence explicitly rather than inventing a coefficient or copying Darian.

This choice does not make Mifflin-St Jeor the permanent whole-universe metabolic model. Once live FM/FFM exists, later versions may compare or replace it with body-composition-informed REE models under a separately validated policy.

Relevant body-composition evidence includes:
- Nelson KM et al. *Prediction of resting energy expenditure from fat-free mass and fat mass.* Am J Clin Nutr. 1992. PMID 1415003.
- Wang Z et al. *Resting energy expenditure-fat-free mass relationship: new insights provided by body composition modeling.* Am J Physiol Endocrinol Metab. 2000. PMID 10950820.
- Bosy-Westphal/related human studies showing FFM, FM and age contribute materially to REE and that body-composition structure explains substantial sex-related differences.

## Action energy expenditure

Every supported completed action receives `payload_json.energy_expenditure` containing:
- estimated kcal for that action duration;
- actor-specific resting kcal component;
- authored activity multiplier;
- duration;
- resting-reference inputs/formula/source;
- energy-policy revision.

Activity multipliers are **Compendium-informed intensity anchors**, not claims of direct calorimetry for each fictional action.

Reference: Herrmann SD et al. *2024 Adult Compendium of Physical Activities: A third update of the energy costs of human activities.* J Sport Health Sci. 2024. PMID 38242596; official Compendium tables.

Examples informing current policy include:
- sleeping about 1.0 MET;
- eating sitting 1.5;
- showering 2.0;
- moderate walking around 3.5;
- vigorous resistance training around 6.0;
- punching bag 5.8;
- sparring 7.8;
- obstacle/boot-camp exercise 5.0;
- general yoga/mobility around 2.3.

The Adult Compendium itself warns that a standard MET is not a precise individual energy-cost measurement and discusses correction for age, height, body mass and sex. v1 therefore scales the authored activity ratio against the actor's own estimated resting expenditure rather than assigning one kcal/min value to all actors.

Future older-adult support may use the 60+ Compendium or a dedicated age policy instead of silently applying young/middle-adult intensity assumptions unchanged.

## Energy-balance window

`energy_balance_window()` aggregates persisted BC-1 evidence between two simulated-time boundaries.

It reports:
- total intake kcal;
- protein/carbohydrate/fat grams;
- intake-event count;
- estimated expenditure kcal;
- net energy kcal;
- covered action minutes;
- evidence coverage ratio;
- missing energy event IDs;
- missing nutrition event IDs;
- `complete` evidence status.

Current completeness threshold is 95% action-time coverage, with no overlapping action events lacking expenditure evidence and no completed eat event lacking nutrition evidence.

The 95% threshold is an **evidence-quality policy**, not physiology. It prevents a partially observed day from becoming an artificial calorie deficit.

Historical pre-BC-1 events are intentionally not recomputed from current catalogs. Their missing evidence makes a window incomplete. This guarantees catalog revisions cannot silently rewrite prior energy balance.

## Universal character behavior

No Darian-specific metabolic branch exists.

The evidence engine reads the selected actor's persisted profile fields and event history. Darian supplies the first production-complete fixture because his DOB, sex, height and weight are already known.

For another actor:
- their own age/sex/height/weight drive resting reference;
- their own action duration/target drives expenditure evidence;
- the consumed universal food definition + quantity will drive new inventory-based intake;
- missing prerequisites fail evidence coverage rather than falling back to Darian.

## Relationship to needs

`needs.hunger` and `needs.energy` remain short-timescale behavioral/physiological control signals.

BC-1 deliberately does not pretend they are kcal stores. A future calibration may connect energy-balance history back into hunger/energy behavior, but that requires its own causal contract and must not be smuggled into body composition.

## Eating Behavior v1 bridge

Eating Behavior v1 should retire dependence on one generic meal target for new natural intake.

Minimum direction:
- model proposes structured multi-food resources + quantities;
- engine validates universal definitions, portion policy and current stock;
- all required inventory quantities are validated before mutation;
- consumption is atomic across the meal resource list;
- combined nutrient evidence is deterministic from universal definitions;
- historical intake evidence snapshots exact foods/quantities/macros;
- bounded satiety/needs effects are a separate deterministic policy, not a direct kcal-to-hunger identity.

## BC-2 activation gate

Before `body.weight_lb` or `body.body_fat_pct` are made simulated, observe or dry-run enough BC-1 + natural inventory-food evidence to answer:
- does natural action history provide near-complete daily expenditure coverage?
- are all commonly consumed universal food definitions nutritionally complete?
- is natural meal cadence/intake plausible for the exemplar rather than an artifact of the older abstract hunger loop?
- are estimated REE and action-energy magnitudes plausible for the actor?

If meal cadence is structurally too low/high, calibrate the behavioral/needs-to-meal bridge before enabling body-composition mutation. Do not hide a cadence problem by assigning implausibly huge or tiny calories to one generic meal.

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
