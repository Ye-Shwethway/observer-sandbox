# Sandbox Character Configuration UX I4.1

Status: ACTIVE
Date: 2026-08-19

## Purpose

Provide an owner-only inline Telegram configuration surface for an approved Creation Sandbox Character without creating a second runtime backend or implying that creation/readiness means autonomous execution.

## Navigation

`Sandbox World -> Characters -> Character -> Configure`

The configuration dashboard exposes:

- represented Sandbox Location assignment;
- sandbox-owned per-Character cognition AI assignment from the shared enabled provider/model catalog;
- deterministic runtime-option refresh from represented Character/current-Location affordances;
- Sandbox clock state and one-time initialization from the current Real World time snapshot when not configured;
- consolidated readiness state and link to detailed readiness diagnostics.

## Ownership boundaries

- Location relations remain in Creation Sandbox relation state.
- Sandbox Character AI assignment remains in `creation_sandbox_ai_bindings` and never writes `sbx_*` identities into canonical Character `ai_bindings`.
- Provider/model catalog metadata is shared; assignment state is isolated.
- Runtime options remain sandbox-owned and are derived through the existing deterministic affordance adapter.
- Sandbox clock remains independent after initialization. Real World time is read only as a snapshot source.
- Canonical universe entities, relations, runtime state, autonomy membership and history remain unchanged by configuration operations.

## Readiness contract

The dashboard presents these gates:

1. active sandbox Character;
2. represented Location assigned;
3. represented runtime options available;
4. cognition AI bound;
5. Sandbox clock configured.

When all gates pass, the Character may be labeled `runtime_ready`.

`runtime_ready != running`.

I4.1 does not enable autonomy, start an action loop, schedule cognition, or create canonical participation.

## UX behavior

Location selection uses active Locations in the same Creation Sandbox. Assigning a Location immediately refreshes represented runtime options so the readiness view cannot retain an obviously stale Location/options pairing.

Character AI selection uses enabled providers and active models from the existing AI catalog. Re-selecting a model replaces only the sandbox Character's cognition binding.

If required supporting state is absent, the UX should guide recovery rather than present dead controls:

- no Location -> link to Creator Studio;
- no enabled AI provider/model -> link to AI Settings;
- no Sandbox clock -> initialize from Real World time snapshot;
- represented options -> explicit deterministic refresh.

## Explicit non-goals

I4.1 does not add:

- full sandbox autonomous execution;
- automatic Run when readiness turns green;
- canonical Character activation or transmigration;
- new AI resolver semantics;
- new profile/body/skill schemas;
- Item/System/Quest/Job creation sockets;
- cross-sandbox relations.

The next execution-capable slice must introduce a sandbox-safe execution adapter separately and preserve the same isolation invariants.
