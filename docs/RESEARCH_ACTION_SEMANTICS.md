# Minimum Research Action Semantics

Status: IMPLEMENTED CANDIDATE / NOT YET DEPLOYED

## Purpose

Add the first selective semantic activity beyond the original generic `inspect/use/read/train` vocabulary without creating a large action taxonomy.

The first verb is `research` and the first authored target is the existing Library & Study `Research Desk`.

## Contract

- `research` is a first-class action definition.
- broad legal duration: 10–180 simulated minutes;
- preferred planning duration at the Research Desk: 30–90 simulated minutes;
- target mode: local object;
- required capability: `research`;
- the Research Desk exposes `research` in addition to its existing inspect/use/read capabilities;
- other library objects such as the Bookshelf do not automatically become research targets;
- normal passive physiology/time advancement still applies;
- no skill XP, knowledge inventory, memory object, grading, or progression is created by this slice.

## Model vocabulary

The model-backed decision provider now unions the legacy known action vocabulary with action names that are actually present in the current authoritative `action_options`. This lets later selective semantic verbs become choosable when and only when current world affordances expose them, instead of requiring every new verb to be added to a second model-only hard-coded vocabulary list.

Runtime validation remains authoritative.

## Timing hardening

The same slice adds a regression invariant for the existing one-simulated-minute minimum at the maximum allowed 3600x universe speed. A 1 sim minute action schedules a positive wall delay of 1/60 real second, remains in progress immediately before its due time, and completes immediately after it. No new minimum wall-delay clamp is required.

## Non-goals

This slice does not add:
- web/internet research;
- durable knowledge acquisition;
- research topics/projects;
- skill progression;
- memory consolidation;
- monitor/repair/maintain actions;
- schema v5.
