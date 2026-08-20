# Sandbox Item Batch Creation v1

Status: ACTIVE IMPLEMENTATION CONTRACT  
Slice: I5.8

## Purpose

Create heterogeneous I5.6 Items in one validated Creation Sandbox transaction. Batch creation is orchestration over the same Item schema and materialization semantics as I5.7; it does not define a second Item model.

Core rule:

`validate whole batch -> resolve dependencies -> preview -> one transaction -> all Items or none`

## Entry shape

Each member is exactly:

```json
{"ref":"stable_local_ref","payload":{...I5.6 Item payload...}}
```

`ref` is batch-local only. It is not a canonical ID and is not persisted as object identity.

## Batch-local references

A relationship target beginning with `$` refers to another batch member, for example:

`stored_in: "$refrigerator"`

V1 Item-only batches permit batch-local references only for `stored_in`, because the batch creates Items rather than Characters or Locations. Other relations must target already-active same-Sandbox objects of the correct type.

Forward references are legal: an Item may reference a container declared later in the batch.

Batch-local storage targets must declare the I5.6 `container` module. Self-storage and cyclic `stored_in` graphs fail closed.

## Preview

`preview_sandbox_item_batch()` performs the complete semantic validation pass without writing Item state. It validates:

- every member through I5.6 exact Item validation;
- unique local refs;
- same-key definition semantic consistency inside the batch;
- compatibility with any existing same-key Sandbox definition;
- existing relation targets;
- batch-local reference existence/type;
- storage acyclicity;
- generic creation-envelope compatibility.

The preview exposes normalized members and resolved relation intent. It does not reserve object IDs.

## Atomic materialization

After a valid preview, all object IDs are allocated and one transaction writes:

1. needed Item definitions;
2. all generic Sandbox Item objects;
3. all unique/stack instances;
4. all staged economic policies;
5. all resolved relations;
6. per-Item materialization events;
7. one batch materialization event.

Relations are inserted after all batch Item objects exist, so forward references do not require partial commits.

Any transaction failure rolls back the complete Item batch.

The Sandbox namespace itself may pre-exist or be initialized independently; the all-or-nothing guarantee applies to Item materialization state.

## Definition semantics

Multiple members may use the same definition key only when all definition-owned semantics match exactly. One shared Sandbox definition may then back multiple concrete instances/stacks.

A semantic conflict under one stable key invalidates the whole batch before Item writes.

## Single-item equivalence

`create_sandbox_item()` is implemented as a one-member call to `create_sandbox_item_batch()`.

Therefore single and batch creation share:

- exact I5.6 validation;
- target validation;
- definition reuse policy;
- transaction behavior;
- economic staging;
- relation materialization;
- audit semantics.

This prevents semantic drift between two creation paths.

## Isolation

Successful or failed Item batches must not mutate canonical Real World state. In particular they do not write canonical:

- entities or entity definitions;
- inventory stacks;
- economic profiles/assets;
- relations;
- runtime state.

A successful batch must preserve `canonical_state_fingerprint()`.

## Acceptance

I5.8 is complete when tests prove:

- preview is Item-write-free;
- heterogeneous batches materialize atomically;
- forward `$ref` storage works;
- batch-local storage requires a container Item;
- unknown/duplicate/self references fail closed;
- storage cycles fail closed;
- same-key semantic conflicts reject the whole batch;
- one invalid member means zero Item materialization;
- successful batch preserves canonical fingerprint;
- single creation demonstrably runs through the batch path.

## Deferred

Not part of I5.8:

- Telegram batch authoring UI;
- edit/move/quantity management after creation;
- Location embedded-content orchestration;
- cross-type creation batches;
- runtime affordances;
- transmigration.
