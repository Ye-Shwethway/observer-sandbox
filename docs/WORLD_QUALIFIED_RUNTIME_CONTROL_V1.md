# World-Qualified Runtime Control v1

## Purpose

Real World and Creation Sandbox clocks are separate runtime authorities. Telegram controls must name the target world explicitly so a command can never mutate the canonical universe by implication.

## Canonical commands

Real World:
- `/realstatus`
- `/realpause`
- `/realresume`
- `/realspeed <value>`
- `/realtime <ISO-8601>`

Sandbox World:
- `/sandboxstatus`
- `/sandboxpause`
- `/sandboxresume`
- `/sandboxspeed <value>`
- `/sandboxtime <ISO-8601>`

The old ambiguous `/pause`, `/resume`, `/speed`, and `/time` command names do not mutate runtime. They return a world-selection redirect.

## Authority and isolation

- Real World runtime state remains in canonical runtime/autonomy storage.
- Sandbox runtime state remains in `creation_sandbox_runtime`.
- Sandbox controls must not change canonical runtime state.
- Real World controls must not change Sandbox runtime state.
- Runtime mutations are Creator/Owner controls.
- Authorized non-owner users may read Real World runtime status.
- Creation Sandbox remains Creator-only.

## Manual time edits

Manual time editing is a discontinuous administrative operation, not simulated elapsed time.

`/realtime <ISO-8601>`:
1. automatically pauses Real World runtime;
2. cancels pending autonomous actions planned against the old clock;
3. clears stale scheduling lease/retry state and returns affected actors to idle;
4. writes the new canonical simulation time;
5. records a Creator audit event;
6. leaves Real World paused until explicit `/realresume`.

`/sandboxtime <ISO-8601>`:
1. automatically pauses the Sandbox runtime;
2. writes only the isolated Sandbox clock;
3. leaves Sandbox paused until explicit `/sandboxresume`.

Sandbox does not yet have a full autonomous action scheduler, so no canonical pending-action semantics are imported into it.

## Telegram UX

Both runtime pages use parallel controls:
- Pause/Resume
- 1x
- 60x
- 3600x
- world-specific Back navigation

Callback namespaces remain isolated:
- Real World: `rw:rt:*`
- Sandbox World: `sw:rt:*`

No callback or command is allowed to infer a target world from context.
