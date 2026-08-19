# Telegram Creator Profile Edit UX v1

## Purpose

Expose the existing Creator Character Profile Editing & Grade Targeting v1 runtime through the normal Telegram character-profile browser. The preferred UX must not require the Creator to know field keys or copy profile-edit commands.

Canonical entry path:

`Characters -> Character -> Profile -> Edit Profile`

The advanced `/profileedit`, `/profilegrade`, and `/profileapply` commands remain available for diagnostics/manual operation, but they are not the primary Creator workflow.

## Authority

The edit surface is Creator/owner only.

Authorized non-owner observers retain the existing read-only Profile browser and must not receive edit buttons or edit callbacks.

Telegram remains a control adapter. All mutations continue through `creator_profile_edit.py`; the Telegram UX must not implement competing profile/grading semantics.

## Universe pause boundary

Entering `Edit Profile` creates a bounded Creator edit session and freezes the universe before editing controls are shown.

Required behavior:
- record whether the universe was already paused before entry;
- if it was running, pause through the canonical autonomy pause control;
- show a prominent `UNIVERSE PAUSED — CREATOR EDIT MODE` warning throughout the edit workflow;
- keep the universe paused across field selection, typed value input, grade-target preview, Apply, Cancel Preview, and Continue Editing;
- `Done Editing` closes the edit session and restores the pause state that existed before the session;
- if the universe was already paused before entry, `Done Editing` must leave it paused;
- applying one edit must not auto-resume the universe.

The pause exists to prevent autonomous simulation from changing actor state while the Creator is reviewing and correcting profile state.

## Field-edit workflow

1. Creator opens `Profile -> Edit Profile`.
2. Universe pauses and the warning banner is shown.
3. Creator chooses a profile section.
4. Telegram lists only represented fields writable by the current Creator profile editor contract.
5. Creator selects one field.
6. Telegram asks for the new value as the next private message.
7. The value is parsed/validated by `preview_profile_edit(...)`.
8. Telegram shows a before/after preview.
9. Creator presses `Apply Change` or `Cancel Preview`.
10. Apply uses the existing saved-proposal path and stale-proposal checks.
11. The edit session remains open/paused until `Done Editing`.

Derived-only fields are not offered as writable inputs. Collections not owned by the current editor contract (for example preferences/habits) remain read-only in v1.

## Grade-target workflow

The native Telegram edit UX exposes compatible monotonic grade-target groups:
- Physical Attributes
- Mental Attributes
- Intellectual Attributes
- Verbal Charisma
- All Attributes
- All Skills

For each group, the Creator may choose E/D/C/B/A/S and either:
- Preserve Shape — preserve relative strengths/weaknesses while shifting the aggregate into the requested grade interval;
- Normalize — move compatible values to the target midpoint.

The resulting raw values are previewed before Apply. Grade labels remain derived read-time output and are never persisted as independent authority.

Body bulk inverse-grade targeting remains outside v1 because Body grading uses target-range/composite semantics rather than the monotonic RAPS/skill scale. Individual writable Body facts may still be edited and automatically regraded.

## Warning / notification semantics

Every edit-mode screen must make the pause explicit. The warning is part of the edited Telegram message so it remains visible throughout navigation rather than relying on a short-lived toast.

Minimum warning text must communicate:
- the universe is paused;
- character simulation is frozen for Creator editing;
- `Done Editing` restores the previous pause state.

After Apply, Telegram must explicitly state that the universe remains paused because Creator Edit Mode is still open.

## Reconciliation semantics

The Telegram UX does not change the existing profile-edit reconciliation contract:
- raw profile/runtime/skill values remain authoritative;
- grades recompute from raw values;
- Creator corrections are audited;
- progression/stat-notification baselines are re-anchored so corrections are not reported as earned progression;
- only directly profile-derived stale semantic self-knowledge may be retired;
- unrelated Character Memory remains untouched;
- no Mental Cycle/Episode/Artifact is created by profile editing;
- no broad memory wipe is allowed.

## Acceptance

Minimum automated proof must show:
- owner Profile menu contains `Edit Profile`;
- authorized non-owner Profile menu does not;
- entering edit mode pauses a running universe;
- warning text is visible;
- Done Editing resumes only when the pre-edit state was running;
- pre-existing pause remains paused after Done Editing;
- field selection -> typed value -> preview -> Apply works without profile commands;
- raw value remains unchanged before Apply;
- Apply changes the authoritative value while universe remains paused;
- native Physical Attributes -> Grade B Preserve preview resolves to B under the existing grading engine;
- no production character value is changed merely for deployment acceptance.
