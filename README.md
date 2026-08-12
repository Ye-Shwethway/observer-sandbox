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

## Initial milestones

- **P0 — Foundation & Remote Control:** repository, runtime skeleton, SQLite schema, CLI, tests, deploy/read workflows.
- **P1 — Living Darian Minimum:** one home, one rich character, basic needs, actions, autonomous loop.
- **P2 — Telegram Observer:** status, watch feed, pause/resume, speed and notifications.
- **P3 — Rich State & Memory:** routines, short-term goals, recent episodic memory and mood.
- **P4 — First Simulation Module:** physiology/training adaptation as the first optional module.
- **P5 — Second Character:** multi-character interaction after the single-agent loop is stable.

## Status

P0 foundation bootstrap in progress.
