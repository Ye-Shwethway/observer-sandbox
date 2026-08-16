# Cognition Context Efficiency v1

Status: **COMPLETE / DEPLOYED**

## Purpose

The Telegram Cognition Context Inspector v1 exposed a practical runtime issue: a real production cognition snapshot rendered to roughly 21 Telegram pages, and the underlying model prompt was dominated by runtime-context metadata.

This slice reduces repeated model-facing metadata while preserving the deterministic runtime and the executable semantics needed for cognition.

## Evidence baseline

A read-only production audit before compaction (Deploy #242) measured the current real persisted cognition snapshot at:

- full prompt: **66,952 serialized characters**;
- runtime context: **64,575 serialized characters**;
- `capability_awareness`: **24,404 characters** (**37.8%** of runtime context);
- `action_options`: **17,866 characters** (**27.7%**);
- `action_options[*].training_method`: **8,411 characters**.

`capability_awareness` and `action_options` together accounted for about **65.5%** of the audited runtime context. The audit did not fabricate a new production cognition call; it inspected persisted real cognition evidence.

## Implemented compaction

Compaction occurs only in the model-facing prompt projection in `src/observer_sandbox/ai_runtime.py`.

Training action options retain executable decision semantics such as:

- action and target identity;
- authoritative duration bounds and derived preferred duration/purpose;
- training method identity/family/workload semantics;
- exact movement IDs and names.

Repeated training metadata such as catalog/source/target/planning duplication and redundant movement-pattern metadata is omitted from the projected prompt.

Capability awareness retains decision-relevant semantics such as:

- skill identity/category;
- proficiency score/grade/behavioral anchor;
- application identity and machine-relevant requirements;
- risk class;
- supporting attributes and knowledge keys.

Repeated descriptive definition/scope prose, verbose application descriptions/context prose, helpful-resource prose, and failure-mode prose are omitted from the projected prompt.

The deterministic engine state, canonical skill/training definitions, action validation, and mutation paths are unchanged.

## Inspector alignment

The Cognition Context Inspector remains an observation of the actual projected cognition context rather than a Telegram-side reconstruction. Both snapshot capture and provider prompt construction continue to use `_compact_prompt_state()`, so the inspector follows the same compact projection seen by the model.

## Verification

Runtime PR: **#191 — Compact cognition prompt metadata v1**

- final tested head: `b4febc29ad7ba37d67547346abd5bb9fff73b772`;
- final CI: **#954**, SUCCESS;
- full suite: **613 passed in 53.34s**;
- fresh DB init/status healthy; schema v5;
- task-relevant Eating Behavior and Solo Regulation acceptance workflows green;
- merge: `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6`;
- Deploy **#243** / run `31931381264`: **SUCCESS**.

Regression coverage proves that compaction:

- preserves executable training and capability semantics;
- preserves exact movement IDs;
- removes selected verbose duplicates;
- is idempotent;
- reduces serialized context on the deterministic fixture.

Deploy #243 also completed its production cognition-context audit step successfully. The current GitHub connector exposes the successful workflow/job state but did not return the raw redirected job-log body, so this checkpoint does **not** invent a post-deploy percentage or exact post-compaction production character count.

## Closure

Cognition Context Efficiency v1 is **CLOSED**.

The v1 goal was semantic-preserving prompt compaction driven by measured production bloat, not a predeclared numeric reduction target. That goal is satisfied by the targeted projection change, regression suite, full CI, successful deployment, and successful production audit execution.

Further compression should be evidence-driven from future observed cognition quality or prompt-size measurements rather than continued speculative trimming.