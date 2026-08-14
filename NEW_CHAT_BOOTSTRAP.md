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

Keep persistent `main` + reusable `test`. Use disposable production-copy validation for state-sensitive migrations. Never accelerate/mutate production merely to manufacture acceptance evidence.

## Current verified production checkpoint

Latest live runtime deployment: **Deploy #179 `31812160413` SUCCESS**, PR #74 merge `edd345c317a52b702c00dd7889ad1eefffa51927`.

Readback:
- healthy/service active;
- schema v5;
- world `thorne-estate-v3.3-physical-attribute-training`;
- `inventory_seed_revision=thorne-estate-inventory-v1`;
- wealthy reserve migration remains applied once;
- default actor `char_darian`;
- autonomy enabled/normal, paused false, retry null, speed 1.0;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram API connected;
- decision calls 356;
- Darian remains asleep in Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

Post-merge CI #647 succeeded. No production acceleration, forced action or model probe was used for Deploy #179 acceptance.

## Universal character / object invariant

Darian and the Thorne Estate are production exemplars, never reusable-engine identity. Runtime, cognition, physiology, progression, inventory and nutrition semantics remain actor/entity/definition-id driven.

Inventory invariant:
`Universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

Telegram Inventory is universe-wide:
`Inventory -> Locations | Characters | Containers | All Stocks -> Scope -> Stack`

## Deployed inventory/nutrition checkpoint

### Inventory Foundation v1
**COMPLETE / DEPLOYED** via PR #71 / Deploy #177.

Schema v5 `inventory_stacks`, universal food definitions, concrete stacks, fixed-container metadata, deterministic decrement and definition-based nutrition are live.

### Inventory Operations v1
**COMPLETE / DEPLOYED** via PR #73 / Deploy #178.

Universe-wide inventory browsing, one-time wealthy Estate reserve, owner-only confirmed replenishment and audited typed stock control are live. Ordinary init/deploy never refills depleted stock.

### Food Nutrition Semantics & Visibility v1
**COMPLETE / DEPLOYED** via PR #74 / Deploy #179.

Canonical universal food content remains `config/items.v1.json`.

Deployed behavior:
- `nutrition_facts.py` projects deterministic nutrient facts from universal item definitions;
- nutrition arithmetic is independent of character, location and current stock quantity;
- authored default serving is used, falling back to nutrition basis;
- Telegram item details show `NUTRIENT FACTS · DEFAULT PORTION` with serving, kcal, protein, carbs, fat and basis;
- no new nutrition numbers, schema change, stock mutation, body mutation or model call were introduced.

Regression examples:
- cooked chicken breast 200 g -> 330 kcal / 62 g protein / 0 g carbs / 7.2 g fat;
- apple 1 piece -> 95 kcal / 0.5 g protein / 25 g carbs / 0.3 g fat.

Evidence:
- final-head CI #646 SUCCESS;
- Inventory Operations Acceptance #19 SUCCESS;
- merge `edd345c317a52b702c00dd7889ad1eefffa51927`;
- post-merge CI #647 SUCCESS;
- Deploy #179 SUCCESS with runtime/autonomy/cognition/inventory/body state preserved and Telegram connected.

`docs/NUTRITION_ENERGY_EVIDENCE.md` distinguishes transitional legacy generic meal-target profiles from universal inventory-food nutrition. New natural eating must use universal item definitions.

## Next slice — Eating Behavior v1

Do not make a Darian-specific meal script.

Minimum-runnable direction:
- cognition receives universal food availability plus hunger/daypart, recent intake, energy/protein context, training/recovery, body-composition goal, preferences/diet constraints and convenience;
- model proposes structured **multi-food resources + quantities**;
- deterministic engine validates portion policy + current stock before mutation;
- all meal resources are consumed atomically;
- combined kcal/protein/carbs/fat evidence is calculated from universal definitions;
- bounded satiety/needs effects remain separate from kcal arithmetic;
- no recipes/cooking/economy as side effects.

After deployment, observe natural intake/expenditure read-only before BC-2. Do not hide cadence defects by inflating generic meal calories.

## Later sequence

1. Eating Behavior v1;
2. natural intake/energy readiness gate;
3. BC-2 coupled Weight/BF/FM/FFM progression;
4. BC-3 measurements;
5. skills;
6. intellectual attributes;
7. mental/emotion dynamics;
8. later social/relationship/sexual physiology as prerequisites mature.

## Exact resume point

Start from **PR #74 / Deploy #179**. The next minimum-runnable slice is **Eating Behavior v1**.

Do not activate BC-2 before natural Eating Behavior evidence passes readiness. Do not add economy/currency, automatic restocking, full RPG encumbrance, arbitrary deep container nesting, all-object migration, Character Memory or a second production character merely for testing as side effects.
