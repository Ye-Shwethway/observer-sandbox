# Telegram Profile Schema-Driven UX

Status: IMPLEMENTED / VALIDATION PENDING

## Goal

Character Profile presentation is schema/config-driven so future ordinary profile fields and sections can appear in Telegram without repeated adapter edits.

Telegram remains a presentation adapter. The profile query layer owns represented data, section metadata and sensitivity filtering; Telegram renders the descriptors/content it receives.

## Section metadata contract

Canonical section presentation metadata lives in:

`config/profile_sections.v1.json`

Each section can declare:
- section id;
- label and icon;
- display order;
- renderer kind;
- represented domains and/or collection;
- optional runtime fields;
- visibility policy;
- allowed sensitivity classes.

The generic profile query enumerates represented sections from this metadata and current represented values. Ordinary field membership is still driven by profile field definitions/domain values rather than Telegram source code.

## Special renderers

Special renderers remain bounded to genuinely different shapes:
- grouped graded attributes;
- skills collections;
- preferences/habits collections;
- runtime/derived recovery views.

A special renderer formats content; it does not own whether an ordinary section exists.

## Sexual Anatomy & Physiology

The profile config now includes an owner-only `Sexual Anatomy & Physiology` section.

It can combine:
- represented `sexual_anatomy` profile values;
- represented `raps_sa` private/intimate profile values;
- represented `sexual_state` values;
- materialized runtime erectile/arousal state when such state actually exists.

The query layer does not invent a momentary sexual state merely to fill the UI.

Security rules:
- section visibility is `owner`;
- only configured `private`/`intimate` fields are eligible for that owner view;
- allowed non-owner users do not receive the menu entry;
- a direct non-owner section request fails closed at the query/presentation boundary;
- Telegram button hiding is not the sole security mechanism.

## Attribute grading presentation

The existing read-only `raps-100-proof-v1` evaluator remains presentation-independent and preserves raw profile values.

Telegram now formats a graded row as:

`Strength   90 (S) · Expert`

The proven 0..100 thresholds remain unchanged. Their labels are aligned with the shared canonical vocabulary for the tiers that this scheme can actually reach:
- E — Beginner
- D — Novice
- C — Capable
- B — Skilled
- A — Advanced
- S — Expert

The shared vocabulary also retains the future higher tiers `SS — Elite`, `SSS — Master`, `X — Mythic`, and `XX — Transcendent`. They are not artificially squeezed into the current 0..100 RAPS proof scale.

### Dynamic aggregate grades

The Attributes query also derives:
- one overall Attributes grade from all current compatible graded attribute values;
- one group grade per represented compatible domain, such as Physical or Mental.

Aggregation is the arithmetic mean of the current values participating in the same named grading scheme, followed by evaluation through that same scheme.

Non-compatible values, notably IQ on its different scale, remain visible but are excluded from the aggregate.

No aggregate grade is persisted. If an authoritative underlying value changes, the row, group and overall grades change on the next read.

## Acceptance

This slice must prove:
- adding a normal field to an existing represented domain requires no Telegram code change;
- adding a new ordinary section requires config metadata only, not a new Telegram handler branch;
- ordering, label, icon, visibility and sensitivity are authoritative outside Telegram;
- the owner can inspect represented Sexual Anatomy & Physiology values;
- allowed non-owner users cannot discover or direct-open the intimate section;
- individual grading renders as `value (grade) · label`;
- group and overall grades are deterministically recomputed from current values;
- IQ remains excluded from the 0..100 grading aggregate;
- profile browsing and grade calculation do not mutate universe state.

## Sequencing

After validation/deploy, this required Telegram profile debt is complete. The next profile-system family can proceed without carrying a fixed section registry forward.
