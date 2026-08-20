# Creator AI Full-Schema Fill Contract v1

Status: **LOCKED CREATION INVARIANT**  
Date: 2026-08-20

## Rule

Every Creator AI creation path must follow the same pattern established by strict Character creation:

`Creator intent -> complete canonical type schema/form -> AI fills that form -> deterministic type validator -> preview -> explicit approval -> Sandbox-only materialization`

The AI is a form filler and proposal generator. It is not a schema designer.

## Provider-facing contract

For every creation type with a deterministic schema:
- pass the complete supported schema to structured generation;
- expose every canonical creation-owned field/slot that the type contract supports;
- require the stable structural fields rather than describing them only in prose;
- use `[]` for unused arrays;
- use `null` for unknown or unused nullable scalar/object slots;
- use a complete registered-module slot map when provider strict-schema rules require it, with unused modules represented as `null`;
- never ask the model to invent, rename, omit, or free-form reconstruct canonical schema fields;
- derived/runtime-owned fields remain outside Creator seed authority.

A long prompt describing a schema is not a substitute for passing the actual schema to the structured-output API.

## Canonicalization boundary

Provider-facing full forms may contain explicit nullable placeholders needed for strict structured-output compatibility. Before deterministic validation/materialization, an adapter may canonicalize those placeholders into the canonical sparse source representation when the authoritative type validator expects sparse conditional modules.

This adapter may only remove schema-defined empty/null placeholders. It may not infer new facts, repair invalid facts, or relax the deterministic contract.

## Manual / AI parity

Manual and AI creation converge on the same deterministic type validator and materialization service. AI output receives no privileged validation bypass.

## Batch rule

Batch creation is orchestration only. Each member uses the exact same full type schema as single creation. A batch envelope may add batch-local references, but must not replace member payloads with generic `object` schemas.

The whole graph is validated before any write and applies atomically.

## Failure rule

Structured-generation errors and deterministic validation errors must remain distinguishable and visible to the Creator. A failed AI fill must not silently fall back to another creation mode or a looser schema.

## Current applications

- Character: existing strict full Character seed schema remains the exemplar.
- Item Single: must use the complete item-v1 AI fill schema.
- Item Batch: every `items[].payload` must use that same complete item-v1 AI fill schema.
- Location and all future Creator-created domains must adopt this contract when their deterministic schema exists.

This rule is architecture-level and is not optional UX guidance.
