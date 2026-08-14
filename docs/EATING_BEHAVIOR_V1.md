# Eating Behavior v1

Status: **IMPLEMENTATION CANDIDATE**
Synchronized: 2026-08-14

## Purpose

Make autonomous eating causally consume concrete inventory while preserving universal food semantics and the existing BC-1 nutrition/energy evidence contract.

Core invariant:

`local eat capability + reachable inventory food stacks + structured quantities -> deterministic validation -> atomic stock decrement + immutable combined nutrition evidence`

The model chooses intent. The deterministic engine owns availability, portion bounds, nutrition arithmetic, stock mutation and event evidence.

## Universal boundaries

- Darian and the Thorne Estate are first production exemplars only.
- Food identity/nutrition remains definition-scoped in `config/items.v1.json`.
- A meal references concrete inventory stack IDs and quantities; it does not redefine food nutrition.
- Character policy/preferences may influence food choice, but no character-specific branch exists in the meal engine.
- Non-eat actions cannot attach food resources in v1.

## Cognition resource contract

Live cognition decisions include a required `resources` array.

For `eat`, each entry is exactly:

```json
{"stack_id": "<concrete inventory stack>", "quantity": 200}
```

For every non-eat action, `resources` must be `[]`.

Cognition receives only authoritative meal choices derived from currently reachable edible stacks. It may select one to six foods and quantities within deterministic bounds. It never invents stack IDs or calculates kcal/macros.

## Portion policy

Eating Behavior v1 uses the authored `default_portion_quantity` on each universal food definition as a behavioral anchor:

- ordinary minimum: 0.5 x default portion;
- ordinary maximum: 2.0 x default portion;
- maximum is also capped by current stock;
- piece-based foods require whole-number quantities and a minimum of one piece;
- at most six meal resources may be selected.

These are bounded v1 behavior guardrails, not nutrition identity and not a permanent human physiology law. Future behavior calibration may revise them without changing historical event evidence.

## Inventory reachability

Meal resources are resolved generically by structural scope:

1. direct inventory in the current location wins;
2. if that location has a local `eat` capability but no direct edible stack, the nearest structural ancestor containing edible inventory may provide the stock;
3. arbitrary global/remote inventory is never exposed merely because it exists elsewhere.

This supports rooms such as a food-storage/preparation area that share site-level provisions while preventing bedroom-to-warehouse remote consumption. No Estate-specific location name is encoded in the engine.

## Atomic completion

Structured meal resources are persisted in the existing `action_instances.resources_json` field when an action is planned.

At `action_completed`:

1. the engine revalidates each persisted stack/quantity against current reachable inventory and bounds;
2. definition-based nutrition is computed for every item;
3. all selected stacks are decremented inside one SQLite transaction/savepoint;
4. combined kcal/protein/carbohydrate/fat is written into the existing `payload_json.nutrition_intake` evidence field;
5. if any item fails validation or stock changed underneath the action, the whole completion is rolled back rather than partially consuming a meal.

Historical evidence is a snapshot. Later catalog changes do not rewrite completed meals.

## Transition compatibility

A pre-v1 `eat` action may already be in flight with `resources_json=[]` when this version is deployed. Such an action is allowed to finish using the legacy target-based BC-1 nutrition profile and does **not** decrement inventory.

This compatibility applies only to already-persisted empty-resource actions. Newly model-planned `eat` decisions fail closed unless at least one valid inventory resource is supplied.

## Telegram observation

For a completed structured meal, the existing `CHARACTER UPDATE` notification adds a compact meal block showing:

- each consumed food and quantity;
- combined kcal;
- combined protein, carbohydrates and fat.

Legacy target-based meals are not mislabeled as structured inventory meals.

## Validation

Current pre-document candidate evidence:

- CI #652 SUCCESS;
- Eating Behavior v1 Acceptance #3 SUCCESS on a disposable production copy;
- Nutrition & Energy Evidence v1 Acceptance #6 SUCCESS;
- synthetic non-Estate inventory regression proves generic meal-resource discovery;
- structured two-item settlement is proven rollback-safe on a production copy;
- no model or Telegram API call is required for acceptance;
- live production is never mutated by acceptance validation.

Final-head validation must be rerun after canonical-document synchronization before merge.

## Explicit non-goals

Eating Behavior v1 does not add:

- recipes, cooking steps or prepared-meal graphs;
- shops, currency, economy or automatic restocking;
- spoilage;
- micronutrient/endocrine simulation;
- body-weight/body-fat mutation;
- model-authored macro arithmetic;
- a second production character solely for testing.

## Next gate

After deployment, observe **natural production intake and expenditure read-only**. Confirm plausible meal cadence, quantities/macros, inventory depletion and evidence coverage before authorizing BC-2 body-composition mutation. Do not force production meals solely to manufacture acceptance evidence.
