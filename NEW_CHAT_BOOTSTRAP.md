# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-14

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical contracts/source files
5. current live production evidence before implementation decisions.

Current Creator instruction and newer repository/CI/deploy/live evidence override older chat memory.

## Development workflow

Default:
`test -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check -> sync test`

Keep persistent `main` + reusable `test`. Use disposable production-copy validation for state-sensitive work. Never accelerate/mutate production merely to manufacture acceptance evidence.

Any new architecture/control invariant updates its canonical contract + ROADMAP + bootstrap in the same development cycle.

## Current verified production checkpoint

Latest deployed production before current PR #76: **Deploy #179 `31812160413` SUCCESS**, PR #74 merge `edd345c317a52b702c00dd7889ad1eefffa51927`.

A fresh read-only runtime read before Eating Behavior implementation showed production naturally advanced to sim `2025-05-05T05:37:00+00:00`, Darian in the Kitchen, autonomy enabled/normal and a legacy in-flight `eat` action with `resources=[]`. This established the transition rule: already-persisted empty-resource meals may finish under legacy BC-1 semantics; newly planned meals must carry valid structured inventory resources.

Deployed baseline remains schema v5, world `thorne-estate-v3.3-physical-attribute-training`, wealthy inventory reserve migration applied once, Gemini `gemini-3.1-flash-lite` primary, Groq `qwen/qwen3.6-27b` fallback and Telegram connected.

## Universal character / object invariant

Darian and the Thorne Estate are production exemplars, never reusable-engine identity. Runtime, cognition, physiology, progression, inventory, eating and nutrition semantics remain actor/entity/definition-id driven.

Inventory/eating invariant:
`Universal food definition -> concrete stack -> reachable eating context -> structured quantity -> deterministic validation -> atomic stock transition + immutable evidence`

## Deployed inventory/nutrition checkpoint

- Inventory Foundation v1 — deployed PR #71 / Deploy #177.
- Inventory Operations v1 — deployed PR #73 / Deploy #178.
- Food Nutrition Semantics & Visibility v1 — deployed PR #74 / Deploy #179.

Universal food content is `config/items.v1.json`. Telegram item details already expose default-serving kcal/protein/carbs/fat. Ordinary init/deploy never refills depleted inventory.

## Eating Behavior v1 — CURRENT PR #76

Canonical: `docs/EATING_BEHAVIOR_V1.md`.

Minimum-runnable candidate:
- live cognition decision schema requires `resources`;
- `eat` selects one to six exact concrete food stack IDs + quantities from authoritative meal-resource choices;
- non-eat actions require `resources=[]`;
- deterministic v1 portion bounds are 0.5x–2x authored default, stock-capped, with whole-number piece quantities;
- direct local edible inventory wins; an eat-capable location lacking direct stock may use the nearest structural ancestor with edible inventory, never arbitrary global inventory;
- structured resources persist in existing `action_instances.resources_json`; no schema v6;
- action completion revalidates every resource and atomically decrements all selected stacks;
- combined definition-based kcal/protein/carbs/fat snapshots into existing BC-1 `payload_json.nutrition_intake`;
- any failed resource/stock validation rolls back the whole completion;
- pre-v1 in-flight empty-resource eat actions remain completion-compatible via legacy target nutrition and no stock decrement;
- Telegram completed structured meals show item quantities + combined kcal/P/C/F;
- no Darian-specific meal branch, model-owned macro arithmetic, recipe/cooking/economy or body mutation.

Candidate evidence before final doc-tail validation:
- CI #652 SUCCESS;
- Eating Behavior v1 Acceptance #3 SUCCESS on disposable production copy;
- Nutrition & Energy Evidence v1 Acceptance #6 SUCCESS;
- synthetic non-Estate inventory regression green;
- no model/Telegram API calls or live production mutation in acceptance.

Final-head gates must be rerun after docs synchronization before merge.

## Next gate after deployment

Perform **natural intake readiness observation** read-only before BC-2:
- structured meal resources actually appear in natural cognition/actions;
- meal cadence/portions/macros are plausible;
- inventory depletion matches completed evidence;
- expenditure evidence coverage remains sufficient;
- cognition does not enter repeated schema/payload/backoff failures.

Do not force production meals for acceptance and do not hide cadence defects by inflating meal calories.

## Later sequence

1. finish PR #76 -> merge/deploy/readback/sync;
2. natural intake/energy readiness gate;
3. BC-2 coupled Weight/BF/FM/FFM progression;
4. BC-3 measurements;
5. skills;
6. intellectual attributes;
7. mental/emotion dynamics;
8. later social/relationship/sexual physiology when prerequisites mature.

## Exact resume point

Finish PR #76 canonical synchronization, rerun **CI + Eating Behavior v1 Acceptance + Nutrition & Energy Evidence v1 Acceptance**, then merge/deploy/readback and sync `test`.

After that, natural intake readiness is next. Do not activate BC-2 before it passes. Do not add economy/currency, automatic restocking, deep recipes/crafting, Character Memory or a second production character merely for testing as side effects.
