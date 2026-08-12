# Observer Sandbox

Observer Sandbox is a tiny, persistent AI-life simulation designed to start with one character (Darian) in one home environment and grow through optional domain modules without requiring architectural rewrites.

## Core principles

- Tiny-first, expandable-by-module.
- Rich character profiles from day one; simulation activates progressively.
- World model is a graph logically and relational storage physically.
- Entities own data; domain modules gain explicit update authority over selected fields.
- LLM agents choose intentions/actions; the runtime validates and mutates state.
- Telegram is the initial observer/control interface.
- GitHub Actions is the deployment and runtime-control spine.
- VPS is the live runtime; the database is never exposed directly to the public internet.

## Continuity / new-chat recovery

`NEW_CHAT_BOOTSTRAP.md` is the durable cross-chat source of current project state. Any new development session should read it first, together with `AGENTS.md`.

After every material repository or verified runtime change, `NEW_CHAT_BOOTSTRAP.md` must be synchronized in the same work session/change set. Repository-only, CI-validated, deployed, schema-applied, and live-verified states must never be conflated.

## Initial milestones

- **P0 — Foundation & Remote Control:** COMPLETE / LIVE VERIFIED. Repository, SQLite runtime, CLI, systemd service, GitHub Actions rsync deployment and independent runtime readback are operational.
- **P0.5 — AI Provider Layer:** FOUNDATION COMPLETE. Dynamic provider catalogs/bindings exist for Gemini, NanoGPT, OpenAI and OpenRouter; NanoGPT is subscription-first.
- **P1 — Living Darian Minimum:** NEXT. One home, one rich character, basic needs, actions, autonomous loop.
- **P2 — Telegram Observer:** status, watch feed, pause/resume, speed and notifications.
- **P3 — Rich State & Memory:** routines, short-term goals, recent episodic memory and mood.
- **P4 — First Simulation Module:** physiology/training adaptation as the first optional module.
- **P5 — Second Character:** multi-character interaction after the single-agent loop is stable.

## Status

P0 remote deployment/control is live verified. Darian's deep canonical profile/schema foundation is prepared. Resume at P1 unless the Creator changes direction.
