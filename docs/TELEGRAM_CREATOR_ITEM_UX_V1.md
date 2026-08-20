# Telegram Creator Item UX v1

Status: IMPLEMENTED ON TEST — ACCEPTANCE PENDING

## Purpose

Expose the already-established I5.6-I5.9 Item creation foundation as a usable Creator-facing Telegram vertical before continuing deeper Location composition work.

## Creator flow

`Observer Home -> Sandbox World -> Creator Studio -> Create -> Item`

Creation methods:

- `Generate with AI` — natural-language Item intent is converted into the exact `item-v1` contract, then deterministic validation runs before a draft is saved.
- `Exact Item JSON` — advanced/manual path accepts one complete `item-v1` object and validates it identically.

Both methods converge on the same draft preview and approval boundary.

## Approval authority

Item approval MUST NOT use generic creation activation.

The approved Item draft is revalidated and materialized through the existing I5.7 Item service (`create_sandbox_item`, batch-size-one path), preserving:

- Item definition vs concrete instance/stack separation;
- economic policy separation;
- explicit Item relation semantics;
- Sandbox-only persistence;
- canonical Real World zero-mutation behavior.

## Observer surfaces

After approval the Creator can:

- open the Item immediately;
- browse `Sandbox Items`;
- inspect Item definition/instance/economic/relation summary;
- return to Creator Studio or Sandbox World.

Sandbox World and Sandbox Universe summaries include Item counts/presence.

## Scope boundary

This slice exposes existing Item creation capability. It does not add new Item runtime behavior, autonomous execution, transmigration, or Location embedded-content orchestration.

I5.11 Sandbox Location Creation + Embedded Contents remains the next backend composition slice after this UX vertical is accepted.
