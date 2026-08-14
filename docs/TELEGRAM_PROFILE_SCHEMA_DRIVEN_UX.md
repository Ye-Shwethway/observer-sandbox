# Telegram Profile Schema-Driven UX

Status: DESIGN DEBT / REQUIRED FOLLOW-UP

## Goal

Character Profile presentation should be schema/config-driven so future profile fields and sections appear in Telegram without repeated adapter edits.

Telegram remains a presentation adapter. The profile schema/query layer owns represented data and section metadata; Telegram renders what that backend exposes.

## Current strength

Existing profile sections already query represented fields by domain instead of hard-coding every field row. This is why a newly represented normal-sensitivity `body.hips_in` field appears automatically in the Body section without a Telegram-specific hips patch.

Preserve this behavior for every ordinary profile field.

## Remaining debt

The section registry is still declared in `profile_observer.py` as a fixed `PROFILE_SECTIONS` tuple. Adding a completely new profile domain/section can therefore require backend presentation-registry code changes even when the field schema itself is valid.

This is acceptable as current technical debt, but it is not the desired final UX contract.

## Target contract

Move ordinary section presentation metadata to schema/config-driven data, for example:

`domain/collection -> section id + label + icon + order + visibility + renderer kind`

Then the generic profile query should enumerate represented sections from that metadata and represented values. Telegram should receive section descriptors and content and render them without knowing the canonical section list.

Special renderers remain allowed for genuinely different data shapes, such as:
- grouped graded attributes;
- skills collections;
- preferences/habits collections;
- runtime/derived recovery views.

Special formatting must not become a reason to hard-code ordinary field membership.

## Acceptance direction

A future profile UX slice should prove:

- adding a normal field to an existing represented domain requires no Telegram code change;
- adding a new ordinary schema-driven section requires metadata/config only, not a new Telegram handler branch;
- ordering, label, icon, visibility, and sensitivity remain authoritative outside Telegram;
- private/intimate fields do not become visible merely because they exist in schema;
- synthetic future character fields render through the same path;
- read-only profile browsing never mutates universe state.

## Sequencing

Complete this debt before profile/domain expansion makes the fixed registry expensive to unwind. It is especially relevant before large Skill, Intellectual, Mental/Emotion, Social, Relationship, or additional physiology profile expansions.
