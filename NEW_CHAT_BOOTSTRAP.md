# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-17

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches are only `main` and `test`.

Default workflow:
`develop on test -> focused tests + final PR CI -> merge test into main -> automatic deploy when runtime-affecting -> production verification -> sync test to final main checkpoint`.

After material repository or verified-runtime checkpoints, continuity must be reconciled here and in `ROADMAP.md` where roadmap state changed. Never leave already-deployed work represented as future work.

## Current canonical checkpoint

**W5 Communication Exposure Foundation v1 is COMPLETE / DEPLOYED on top of the already-deployed W0-W4.1 world-input stack, A3.3 bounded route awareness, and Diagnostics v2.**

Latest runtime evidence:
- PR #267 — `Add W5 communication exposure foundation`
  - final tested head `03519395b89b9ba7fae3d0db8c9d1b4ad0fe102b`
  - CI #1053 / run `32044642343`: SUCCESS
  - merge `520ebd9d10077bf1880acf75414e29ca258dbac9`
  - **Deploy #288 / run `32044773094`: SUCCESS**
- production health after Deploy #288:
  - canonical `observer_sandbox.service` entrypoint active;
  - runtime log ready;
  - SQLite readable and `PRAGMA quick_check=ok`;
  - schema remains **v15**; W5 required no migration;
  - Gemini cognition binding preserved at `gemini-3.1-flash-lite`;
  - cognition recovery probe `ok=true`, `mutated=false`, `validated=true`;
  - Telegram API/owner/allowed-user configuration healthy.

## W5 — Communication Exposure Foundation v1 — DEPLOYED / MINIMUM COMPLETE

Canonical docs:
- `docs/COMMUNICATION_EXPOSURE_FOUNDATION_V1.md`
- `docs/W5_IMPLEMENTATION_PLAN_V1.md`
- `docs/W5_ACCEPTANCE_NOTES_V1.md`

Runtime:
- `src/observer_sandbox/communication.py`
- focused acceptance: `tests/test_communication_exposure_v1.py`

W5 closes the final minimum W0 producer boundary without creating a second production character and without prematurely implementing social cognition or dialogue intelligence.

Canonical chain:
`communication event truth -> communication stimulus availability -> recipient delivery/exposure -> future perception -> appraisal/social inference -> response intention -> utterance/action proposal -> deterministic action authority`.

Preserve:
`uttered/sent != delivered != heard/read != understood != believed != remembered != relationship change != response intention != response action`.

### Direct-utterance exemplar

The first runnable W5 exemplar is direct speech:
- sender and intended recipients must be represented character entities;
- authoritative truth is persisted as `communication_utterance` event + `event_participants`;
- intended recipients receive character-scoped W0 `communication` stimuli with source-event/source-entity provenance;
- an intended recipient receives actual W0 exposure only when co-located with the sender at the utterance boundary;
- a non-co-located intended recipient receives no exposure;
- an unrelated co-located character does not receive targeted communication;
- invalid/non-character/self-recipient misuse fails closed.

W5 intentionally reuses existing stores:
- `events` / `event_participants`;
- dynamic `located_at` state;
- `world_stimuli` / `world_stimulus_scopes`;
- `character_exposures`.

No parallel message database or schema migration was introduced.

### W5 proof boundary

Automated fixture tests use arbitrary temporary character IDs to prove generic architecture/runtime behavior. These fixtures are test data only and are **not** a second canonical production character seed.

Proven:
- communication event truth and participant roles;
- targeted W0 communication stimulus provenance;
- co-location heard exposure;
- non-co-location non-delivery;
- unrelated-actor non-exposure;
- fail-closed participant validation;
- no automatic Character Memory, Mental Cycle/Episode/Artifact, relationship-state, or action-authority mutation;
- character-generic implementation.

Not yet proven and intentionally deferred:
- natural production character-to-character conversation;
- autonomous dialogue generation;
- social interpretation or reply intention;
- relationship adaptation;
- asynchronous/device messaging;
- phone/inbox/contact/network simulation.

Do not fabricate a production NPC or fake conversation to manufacture acceptance.

### Device/message readiness

Future device communication should reuse the same boundary:
`message truth -> represented endpoint/device delivery -> recipient read/access boundary -> W0 device communication exposure`.

Do not prebuild phone/network complexity until a concrete represented consumer requires it.

## Second-character seed gate

**Do not seed the next real production character merely to exercise unfinished foundations.**

The agreed product gate is:
1. W0-W5 minimum world-input foundations complete;
2. audit/close the exposure-to-perception bridge;
3. activate the minimum Mind sequence through MIND-F2..F7;
4. run Foundation Completion Review v2;
5. only after that review may the next real character seed be proposed;
6. that second character then becomes live multi-character acceptance evidence, not a development test dummy.

## Exact next implementation checkpoint — Perception-gap audit

Before MIND-F2, inspect the live source/contracts for the boundary between W0 `character_exposures` and the Mind Engine `perception` input socket.

Canonical contracts currently state:
- W0 stops at exposure;
- exposure is not perception/understanding;
- Mind Foundation distinguishes perceived information from world truth/exposure and reserves a bounded `perception` input socket.

Do **not** assume a new subsystem is missing merely from naming. First audit current source for an existing perception-equivalent bridge.

Decision after audit:
- if an adequate generic exposure -> actor-relative perceived-input bridge already exists, document that evidence and proceed to MIND-F2;
- if the bridge is genuinely missing, implement the smallest generic Perception Runtime needed to convert eligible W0 exposures into bounded actor-relative perceived inputs while preserving provenance and without creating belief, Memory, appraisal, or action authority.

Then continue the pre-authored Mind sequence:
`[Perception bridge if required] -> MIND-F2 Mental Episode Runtime -> MIND-F3 Attention/Appraisal/Active Concerns -> MIND-F4 Intention -> MIND-F5 Planning -> MIND-F6 Social Cognition/Communication -> MIND-F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real character seed`.

## A3.3 — Bounded Multi-Step Destination Intent v1 — DEPLOYED / NATURAL OBSERVATION CONTINUES

A3.3 remains production-green through Deploy #287 and is independent of W5/Mind progression.

It provides actor-known bounded route-purpose awareness (max 4 hops) while exact executable movement remains current deterministic `action_options` authority. No persistent Mind intention/plan exists yet.

Natural production proof for the previously missing inside-to-outside initiation remains under read-only observation. Do not force an outing. If ordinary decisions still fail after reasonable opportunities, inspect post-deploy cognition evidence and make only generic evidence-driven corrections.

When MIND-F4/F5 intention/planning becomes active, reconcile A3.3/interim purpose scaffolding into typed Mind intention/plan flow and remove/reduce duplicate prompt-level planning guidance.

## W4 continuity — already deployed

W4 was implemented before A3.3 and must never again be labeled future work:
- PR #249 — W4 Information / Media Foundation + W4.1 Historical News Provider;
- PR #250 — Creator News observability/generation surface;
- PR #251 — simulation-time Morning 07:00 / Evening 18:00 TV scheduling;
- PR #252 — first-class generic Media Console `consume_media` runtime and W0 exposure bridge.

Publication/exposure remains separate from belief, Memory, Mind and action authority.

## Operational diagnostics — DEPLOYED

- PR #258 — health-probe quoting fix / Deploy #283;
- PR #259 — Diagnostics v1 / Deploy #284;
- PR #260 — path-aware CI/acceptance triggers;
- PR #261 — Diagnostics v2 / Deploy #285;
- PR #262 — deploy-safe/production-truth correction / Deploy #286.

Creator-only Telegram diagnostics remain:
`/logs`, `/logs errors [lines]`, `/logs system [lines]`, `/logs runtime`, `/logs file [lines]`.

The production `observer` user has persistent `systemd-journal` read access.

## Completed minimum World Input stack

- W0 World Stimulus / Exposure Foundation
- W1 Environment / Weather Foundation
- W1.1 Historical Weather Provider
- W2 Commitments / Obligations Foundation
- W3 Money / Economy Foundation
- W3.1 Universe Object Valuation & Creation Rules
- W4 Information / Media Foundation
- W4.1 Historical News Provider
- first-class Media Console consumption / W0 exposure
- **W5 Communication Exposure Foundation v1**

The W0 preferred W1-W5 minimum producer sequence is now complete at foundation level.

## Estate / outside-world lock

Estate-first scope remains active. Broader South Lake Tahoe traversal remains intentionally paused: no public-road edge from Main Security Gate, Tahoe-backcountry edge from Concealed Forest Passage, or water-travel edge from Hidden Dock is open.

## Exact resume point

**W5 Communication Exposure Foundation v1 is production-green through Deploy #288 with no schema migration and no fabricated second character. The immediate new-development step is a read/source-level Perception-gap audit between W0 exposure and the Mind Engine perception socket. Add a minimum Perception Runtime only if repository evidence proves the bridge is absent; otherwise proceed directly to MIND-F2. A3.3 inside-to-outside natural observation continues independently. Do not seed the next real character until the remaining Mind foundations are minimum-complete and Foundation Completion Review v2 authorizes that seed.**
