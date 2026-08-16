# Autonomy Intent Continuity v1

Status: COMPLETE v1

## Problem

Observer Sandbox already had strong single-action autonomy: cognition sees current state and legal options, proposes one action, deterministic runtime validates and schedules it, completion commits state and wakes cognition again.

The missing minimum foundation was cross-action purpose continuity. `action_instances.intent` was only the reason for one action, while `actor_runtime` persisted scheduler state but no authoritative ongoing purpose. Recent event reasons supplied history, not an active cross-action continuation signal.

## Contract

Autonomy Intent Continuity v1 adds one bounded actor-scoped intent overlay without changing action legality or simulation authority.

Authority:

`committed purposeful movement -> bounded persisted intent -> next cognition context -> ordinary legal follow-up -> intent settlement`

Key invariants:

- deterministic runtime owns intent persistence;
- the LLM still proposes only ordinary actions/reasons through the existing decision contract;
- no new action vocabulary is added;
- no action/target/resource becomes legal because of an intent;
- physiological needs, safety and authoritative `action_options` override intent guidance;
- intent state is distinct from the authored profile and from the current pending action;
- initialization/deployment preserves active runtime intent rather than reseeding it;
- v1 uses existing `runtime_state`; schema remains v5.

## Exemplar lifecycle

### Start

When no intent is active, a committed `move` proposal with a concrete destination and meaningful reason may establish an active intent. Ordinary non-movement actions do not spontaneously create sticky goals.

### Continue

Additional movement may continue the same intent, but movement continuation is capped at four planned movement steps. Crossing the bound abandons the intent rather than creating a navigation/planner loop.

### Self-care interruption

Basic self-care actions (`sleep`, `eat`, `drink`, `shower`, `rest`) may interrupt the purpose without automatically deleting it. Intent therefore never outranks physiological needs.

### Finish

The first ordinary local non-movement follow-up is the bounded fulfillment/exit boundary. Intent stays visible while that action is in progress and clears only after represented completion.

V1 deliberately does not claim arbitrary semantic goal-completion understanding; it proves only the minimum purpose bridge needed for purposeful movement and an immediate follow-up.

### Staleness

An active intent older than 12 simulated hours is removed at the next free decision boundary so deploy-surviving stale intent cannot become permanent scripting.

## Cognition surface

The next decision receives compact `autonomy_intent` context: active/inactive state, intent id, summary, origin/destination, movement-step count, interruption count, and explicit guidance that intent is not an order and cannot override needs, safety or legal action options.

Internal transition metadata is stored on the planned action in `conditions.autonomy_intent_transition`; completion can therefore settle the same intent deterministically without re-parsing model prose.

## Runtime integration

Production service routing uses a thin intent-aware wrapper around the unchanged core `autonomy.autonomy_tick`.

The wrapper:
1. expires stale intent only at a free decision boundary;
2. injects compact intent context before cognition;
3. decorates the already-proposed `Action` with deterministic transition metadata;
4. calls the unchanged core scheduler/validator;
5. commits start/continuation/interruption only after successful planning;
6. clears a finish transition only after the represented follow-up completes.

Scheduling, leases, retries, validation, action instances and consequences remain under the existing tested authority.

## Validation and production checkpoint

Runtime PR: **#178 — Autonomy Intent Continuity v1**

- final tested head: `563e102c6a9d73ea2f39e828da6329840632ef79`;
- **CI #940 / run `31920821319`: SUCCESS**;
- **583 passed in 58.57s**;
- fresh DB init/status healthy; schema v5;
- all automatic production-copy acceptance gates were green without retry;
- merge: `0cf9a38e7fadafa178f1f69f9f5b7013cbd1961f`;
- **Deploy #236 / run `31920905305`: SUCCESS**.

Verified deploy readback:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed 1x;
- Darian was naturally sleeping in Darian's Master Suite;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

The deploy log masked the hour component of sim time, so the checkpoint records only the authoritative visible form `2025-05-07T***:27:00+00:00`; no hour is inferred.

No `autonomy_intent_v1:` runtime-state row appeared in deploy readback. Deploy/init therefore did not fabricate a live intent and no production intent is claimed. Natural production proof remains evidence-driven: a qualifying purposeful `move` must occur before the overlay exists.

## Non-goals

V1 does not add arbitrary LLM goal-state writes, multi-goal prioritization, plan trees/task graphs, quests/jobs/projects, long-term commitments, semantic success scoring, deterministic action selection, relationship goals, broad episodic memory, or a generic planner framework.

## Closure

**Autonomy Intent Continuity v1 is COMPLETE at minimum-foundation depth.** Return to the Overall Workflow/Foundation Review and select the next actual cross-system gap from current evidence rather than automatically deepening planning/autonomy.
