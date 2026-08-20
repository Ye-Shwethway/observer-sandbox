# Item AI Schema / Canonicalizer / Validator Compatibility Audit v1

Status: IMPLEMENTATION AUDIT — 2026-08-20

## Boundary

AI Item creation has three distinct contracts:

1. provider structured-output schema (`item_ai_fill_schema` / batch wrapper),
2. deterministic AI canonicalization (`canonicalize_ai_item_fill` / batch canonicalization),
3. strict authoritative Item validation (`validate_item_payload`).

The provider schema is intentionally a transport/fill shape. The authoritative acceptance invariant is:

`schema-shaped AI output -> deterministic canonicalization -> strict item-v1 validator`

The validator is not relaxed to accommodate AI formatting mistakes.

## Compatibility rules audited

### Registry surfaces

Provider enums/slots must track validator registries for:
- Item kinds;
- mobility;
- capabilities;
- module names;
- registered Item metric ids and metric units.

### Stable-token fields

AI may emit human-readable labels. Canonicalization converts mechanically safe identifier fields before strict validation:
- `definition.key`;
- `definition.tags[]`;
- `economic_policy.valuation_method`;
- stack/instance/nutrition unit labels where the Item contract defines them as symbolic units;
- consumable `economic_policy.unit_label`;
- batch `ref` values.

Human-readable batch references use one alias map for batch-local `stored_in` and `included_in_parent_ref` references.

### Nullable module slots

Provider schemas expose nullable module slots. Canonicalization removes null slots before strict validation. An all-null physical module is removed rather than passed as an invalid represented physical module. Null metric entries are removed and an empty metrics module is omitted.

### Stack contract

`modules.stack` is authoritative when represented. Canonicalization aligns:
- `definition.stackable`;
- `instance.mode`;
- initial quantity;
- symbolic stack unit.

If the AI supplies an explicit stack instance with quantity/unit but omits the stack module, the same represented facts may reconstruct the stack module. No quantity is invented.

When nutrition is represented on a stack, the canonical stack unit is used for the nutrition unit because the strict Item v1 contract requires the same symbolic unit.

Consumable-stock economics likewise uses the canonical stack unit for `unit_label`.

### Module / capability invariants

Canonicalization reconciles these deterministic pairs bidirectionally:
- nutrition <-> `eat`;
- container <-> `store`;
- resistance_training <-> `train`.

A represented module gains its required capability. A stray dependent capability with no corresponding module is removed. The validator remains strict.

### Economic formatting

Currency strings are trimmed/uppercased. Valuation-method labels are normalized to stable tokens. Existing immaterial-value behavior remains deterministic. Semantic economic contradictions that require changing factual meaning are not silently invented away; they remain validator/self-correction failures.

## Fail-closed boundary

Canonicalization only repairs deterministic representation mismatches. It does not invent missing raw facts.

Examples that remain invalid until AI self-correction supplies evidence:
- nutrition with no stack quantity/unit evidence;
- consumable stock lacking required unit economics;
- invalid monetary classification/treatment combinations whose repair would require choosing new economic meaning;
- unsupported capabilities/modules/metrics/units;
- empty required names/descriptions;
- contradictory physical-placement relations.

## Acceptance

`tests/test_item_ai_schema_validator_compatibility.py` covers registry alignment, human-readable token fields, null-module cleanup, stack reconstruction/alignment, nutrition/stack/economic unit consistency, module/capability reconciliation, batch aliasing and fail-closed non-mechanical gaps.
