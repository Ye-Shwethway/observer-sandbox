# Telegram Creator Item UX v1

Status: IMPLEMENTED ON TEST — ACCEPTANCE PENDING

## Purpose

Expose the already-established I5.6-I5.9 Item creation foundation as a usable Creator-facing Telegram vertical before continuing deeper Location composition work.

## Creator flow

`Observer Home -> Sandbox World -> Creator Studio -> Create -> Item`

Creation methods:

- `Single Item · AI` — natural-language Item intent fills the complete provider-facing `item-v1` schema/form.
- `Item Batch · AI` — one natural-language request becomes a heterogeneous batch graph; every `items[].payload` uses that same complete `item-v1` schema/form.
- `Single Item · Exact JSON` — advanced/manual path for one complete `item-v1` object.
- `Batch · Exact JSON` — advanced/manual path using `{"items":[{"ref":"...","payload":{...item-v1...}}]}`.

All methods converge on deterministic preview and approval boundaries.

## Creator AI schema-fill invariant

Item AI follows `docs/CREATOR_AI_SCHEMA_FILL_CONTRACT_V1.md` and the strict Character creation exemplar.

The structured-output API receives the actual full Item schema. The prompt does not substitute prose instructions for missing schema structure.

Provider-facing full form rules:
- every stable Item field/slot is represented in the schema;
- unused arrays are `[]`;
- unknown/unused nullable values are `null`;
- all registered conditional module slots are present in the AI form and unused modules are `null`;
- AI cannot invent, rename or omit canonical fields;
- a small adapter strips only schema-defined nullable module placeholders before the authoritative sparse `item-v1` validator runs;
- Manual and AI still converge on the same deterministic I5.6 validation/materialization contracts.

Batch is orchestration only; it must never replace member Item payloads with a generic object schema.

## Single Item approval authority

Single Item approval MUST NOT use generic creation activation.

The approved draft is revalidated and materialized through the existing I5.7 Item service (`create_sandbox_item`, batch-size-one path), preserving Item definition/instance/economic/relation separation and Sandbox-only persistence.

## Batch approval authority

Batch creation reuses the existing I5.8 services directly:

- `preview_sandbox_item_batch` validates the complete graph without Item writes;
- batch-local forward refs may be used for `stored_in` container relationships;
- duplicate/self/cyclic/invalid refs fail closed;
- `create_sandbox_item_batch` applies the whole batch atomically;
- one invalid member means zero new batch Items;
- canonical Real World state remains unchanged.

The Telegram batch preview shows member count, compact member summaries and represented batch-local storage relationships before one approval action.

## Observer surfaces

After approval the Creator can:

- open a single Item immediately;
- browse `Sandbox Items` after single or batch creation;
- inspect Item definition/instance/economic/relation summaries;
- return to Creator Studio or Sandbox World.

Sandbox World and Sandbox Universe summaries include Item counts/presence.

## Scope boundary

This slice exposes existing Item creation capability. It does not add new Item runtime behavior, autonomous execution, transmigration, or Location embedded-content orchestration.

I5.11 Sandbox Location Creation + Embedded Contents remains the next backend composition slice after this UX vertical is accepted.
