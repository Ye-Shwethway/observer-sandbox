# Telegram Creator Studio UX Polish — I4.3

Status: IMPLEMENTATION CONTRACT
Date: 2026-08-19

## Scope

This slice improves Creator Studio presentation without changing sandbox schema, Character creation semantics, or canonical state.

### Input-card lifecycle

Creator Studio guided input cards are tracked by their Telegram message ID. When the next ordinary message is consumed by the active Creator Studio input session, the old input card is deleted exactly once before the result is presented. Navigating away from the input screen clears the tracked card instead of leaving stale deletion state.

### Native typing status

AI-assisted Creator Studio generation emits Telegram `sendChatAction` with action `typing` immediately and refreshes it approximately every four seconds while generation is in progress. The refresh thread stops when generation returns or fails. Manual creation does not use this indicator.

### Reboot checkpoint

The Observer reboot message performs a best-effort read-only lookup of the repository `main` commit and appends:
- the short commit SHA;
- a meaningful commit summary, preferring the merged PR title when the top commit is a merge commit.

Repository lookup failure never blocks runtime startup or the normal boot notification.

## Non-goals

- no schema migration;
- no runtime simulation behavior change;
- no autonomous decision timeout change;
- no persistent Telegram UI-message table;
- no write access to GitHub from runtime.
