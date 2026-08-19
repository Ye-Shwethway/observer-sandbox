# Creator Character Profile Editing & Grade Targeting v1 — Acceptance Notes

Status: **IMPLEMENTATION ACCEPTANCE NOTES**

Canonical contract: `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_V1.md`

## Implemented runtime

- `src/observer_sandbox/creator_profile_edit.py`
  - schema-aware profile/runtime field preview and apply;
  - represented skill-score editing;
  - monotonic inverse grade targeting;
  - preserve-shape and normalize modes;
  - stale-preview rejection;
  - targeted self-knowledge retirement;
  - progression/display/stat-notification baseline re-anchoring;
  - Creator audit event/provenance.
- `src/observer_sandbox/telegram_profile_edit.py`
  - compact preview/apply formatting and saved proposal token workflow.
- `src/observer_sandbox/telegram_runtime_bot.py`
  - Creator-only command adapter.

## Creator Telegram commands

- `/profileedit <character_id> <field_key> <value>` — build a no-mutation preview.
- `/profilegrade <character_id> <group> <grade> [preserve|normalize]` — build an inverse-grade preview for a supported monotonic group.
- `/profileapply <preview_token>` — atomically apply the exact still-fresh preview.

Example:

`/profilegrade char_darian physical B preserve`

The command does not immediately change the character. It returns the proposed raw-value diff and a bounded apply token. Apply is rejected if any affected value changed since preview.

## Grading behavior

Grades are still not persisted. The existing grading runtime evaluates the newly authoritative raw values on read.

V1 inverse targets:
- RAPS/Attributes 0..100 groups;
- Skills 0..100 groups.

Body remains automatically regraded after individual input edits but is not bulk inverse-targeted in v1 because Body uses ratio/reference/composite semantics rather than one monotonic raw scale.

## Reconciliation boundary

On apply:
- profile scalar history uses `character_profile_history` where applicable;
- skills preserve their existing store and receive Creator re-anchor provenance in metadata;
- profile/stat-notification baselines reset to the corrected current snapshot so the control edit is not later presented as organic progression;
- only active semantic memory explicitly tagged as deriving from affected profile field keys is retired;
- unrelated episodic/semantic memory is preserved;
- no historical Cognition Context is rewritten;
- no Mental Cycle/Episode/Artifact is created.

## Production acceptance boundary

Automated tests use disposable databases initialized from canonical repository seeds. Production acceptance must not alter Darian's live profile merely to prove the editor.

Production deployment acceptance is therefore:
- installation/service health;
- schema/readability health;
- Telegram command availability/owner authorization through tested adapter behavior;
- no forced live profile mutation.

A later Creator-initiated real profile edit is an explicit control action, not deployment validation.

## Initial CI correction

The first full CI run exposed one narrow implementation assumption: `character_skills` has no `updated_at` column. The implementation was corrected to preserve the existing schema and keep Creator re-anchor time in skill metadata rather than adding a migration solely for this feature.

## Next product checkpoint

After final CI, merge/deploy/health verification and continuity synchronization, resume **MIND-F2 Mental Episode Runtime**.
