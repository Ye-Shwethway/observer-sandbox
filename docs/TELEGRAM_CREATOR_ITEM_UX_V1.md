# Telegram Creator Item UX v1

Status: IMPLEMENTED ON TEST — ACCEPTANCE PENDING

## Purpose

Expose the already-established I5.6-I5.9 Item creation foundation as a usable Creator-facing Telegram vertical before continuing deeper Location composition work.

## Creator flow

`Observer Home -> Sandbox World -> Creator Studio -> Create -> Item`

Creation methods:

- `Single Item · AI` — natural-language Item intent is converted into one exact `item-v1` contract.
- `Item Batch · AI` — one natural-language request becomes a heterogeneous batch graph.
- `Single Item · Exact JSON` — advanced/manual path for one complete `item-v1` object.
- `Batch · Exact JSON` — advanced/manual path using `{"items":[{"ref":"...","payload":{...item-v1...}}]}`.

All methods converge on deterministic preview and approval boundaries.

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
