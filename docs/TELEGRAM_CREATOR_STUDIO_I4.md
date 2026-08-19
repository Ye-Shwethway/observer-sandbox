# Telegram Creator Studio I4

Status: IMPLEMENTATION CONTRACT
Date: 2026-08-19

## Purpose

Expose the existing Creator Creation proposal/sandbox foundation through a minimum usable Telegram Creator Studio without granting AI or Telegram direct canonical-write authority.

## Core boundary

`Creator intent -> Manual Draft or AI Draft -> Sandbox Draft -> Preview -> Explicit Approve -> Creation Sandbox object`

A draft is not an object. A sandbox object is not canonical. Canonical transmigration remains a separate future validation and approval boundary.

## Telegram surface

Sandbox World adds `🛠 Creator Studio`.

Minimum commands:
- `/studio`
- `/create character <name>`
- `/create location <name>`
- `/createai character <description>`
- `/createai location <description>`

The Studio preview provides:
- `♻️ Reroll` for AI-generated drafts;
- `✅ Approve into Sandbox`;
- `✕ Cancel Draft`.

Manual and AI paths converge on the same validated creation proposal and approval path.

## AI authority

AI Draft uses the independently configured Creator Creation AI binding.

AI may only return schema-compatible proposals. It cannot:
- activate sandbox objects without Creator approval;
- write canonical universe state;
- transmigrate creations;
- bypass target-universe compatibility validation.

## Persistence

Schema v19 adds `creation_sandbox_drafts`.

Drafts are:
- sandbox-scoped;
- Creator/user-scoped;
- revisioned;
- replaceable by reroll/new draft;
- deleted after approve or cancel.

Drafts never use canonical `runtime_state` as temporary UI storage.

## Scope

I4 supports Character and Location because those are the currently proven creation sockets.

It does not yet provide a full field-by-field Telegram editor for every Character profile/Body/Skill field or Location affordance. Rich editing/configuration can extend this Studio incrementally while preserving the same proposal boundary.

## Acceptance

Required proof:
- schema v19 creates sandbox draft storage;
- manual draft creates no sandbox object before approval;
- AI draft uses Creator Creation AI and creates no object before approval;
- approval uses the normal sandbox activation path;
- canonical-state fingerprint remains unchanged;
- non-owner Telegram users cannot use Creator Studio;
- Sandbox World exposes Creator Studio navigation.

## Non-goals

Not included:
- full sandbox autonomous execution;
- Item/System/Quest/Job sockets;
- canonical transmigration;
- second canonical Character activation;
- direct AI database writes.
