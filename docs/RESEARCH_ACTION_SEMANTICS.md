# Minimum Research Action Semantics

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED

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

The model-backed decision provider unions the legacy known action vocabulary with action names actually present in current authoritative `action_options`. Later selective semantic verbs therefore become choosable only when current world affordances expose them, without requiring a second model-only hard-coded vocabulary edit.

Runtime validation remains authoritative.

## Timing hardening

The same slice locks the existing one-simulated-minute minimum at the maximum allowed 3600x universe speed. A 1 sim minute action schedules a positive wall delay of 1/60 real second, remains in progress immediately before its due time, and completes immediately after it. No minimum wall-delay clamp is required.

## Evidence

- PR #10 merged at `c50f4cf9a87b15589be3b3ea4878990da7e69d02`.
- PR CI #365 / run `31681648655` SUCCESS after one stale duration-profile-count assertion was updated; the first failed PR run changed no production state.
- main CI #366 / run `31681716298` SUCCESS.
- Research Action Semantics Acceptance #1 / run `31681716339` SUCCESS on candidate source/config against a disposable copy of the live production DB with zero model calls.
- acceptance proved Research Desk is the only research target, Bookshelf is rejected, planning clamps 5→30 and 200→90 minutes, and research completes as a first-class action/event.
- release commit `8f3487feccc84ef10b045dff960097bc0c44ceb6`.
- Deploy #136 / run `31681760620` SUCCESS.
- deploy readback: service healthy, schema v4, autonomy enabled/normal/unpaused, Gemini binding preserved, Telegram connected. Production speed was 5x at that readback snapshot and must always be re-read live rather than treated as a fixed baseline.

## Non-goals

This slice does not add:
- web/internet research;
- durable knowledge acquisition;
- research topics/projects;
- skill progression;
- memory consolidation;
- monitor/repair/maintain actions;
- schema v5.
