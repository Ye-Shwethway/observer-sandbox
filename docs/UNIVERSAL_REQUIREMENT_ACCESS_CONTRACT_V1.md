# Universal Requirement & Access Contract v1

Status: **IMPLEMENTATION CANDIDATE — I5.5**  
Date: 2026-08-20

## Purpose

Provide one deterministic typed prerequisite language for later Item interactions, Location access, Quest/state gates and related runtime checks while preserving a hard separation between:

- what a thing **is** or how it is graded;
- what an actor **must satisfy** for one interaction;
- whether an actor is **authorized** to enter/use a place;
- whether the place/service is **currently operating**.

Core rule:

> **Item Grade describes the item. Requirement Grade describes the interaction. Location Grade does not grant access.**

---

## Existing primitive reused

`src/observer_sandbox/action_conditions.py` already established useful fail-closed comparison behavior for bounded field conditions.

I5.5 reuses those comparison semantics but does not overload the old `all[field_key,operator,value]` shape into a universal policy language.

New implementation:
`src/observer_sandbox/requirements.py`.

---

## Requirement Context

`RequirementContext` is an explicit projection of authoritative evidence needed by one evaluation.

It may contain:
- domain/dimension grade results;
- raw represented values;
- learned/represented skill references;
- available Item references;
- equipped Item references;
- owned references;
- resident Location references;
- authorized Location references;
- represented quest/world/operating state facts.

The evaluator never invents missing context. Missing authoritative evidence fails closed.

---

## Typed leaf predicates

V1 supports:

### `minimum_grade`

Requires:
- domain;
- dimension;
- minimum grade.

Example:

```json
{
  "type": "minimum_grade",
  "domain": "character",
  "dimension": "strength",
  "minimum": "A"
}
```

The evaluator uses the registered cross-domain grade ordering from I5.4.

A grade from another domain/dimension is not substituted automatically.

### `value_compare`

Compares one represented raw value with a bounded operator.

### `has_skill`

Requires one represented skill reference.

### `has_item`

Requires one available/possessed Item reference in the supplied context.

### `equipped`

Requires an explicitly equipped Item reference.

### `owns`

Requires ownership; ownership remains distinct from possession/storage/equipment.

### `resident_of`

Requires represented residency for one Location.

### `authorized_for`

Requires represented actor authorization for one Location.

### `state_compare`

Compares a represented quest/world/runtime state fact through the same bounded comparison semantics.

---

## Composition

A requirement may be:
- one typed leaf;
- exactly one non-empty `all` composition;
- exactly one non-empty `any` composition.

Nested compositions are allowed.

Malformed shapes, unknown leaf types, unknown fields and unsupported comparison operators raise deterministic contract errors rather than silently authorize the interaction.

`all` returns the actual failed leaves.

An unsatisfied `any` returns structured branch failures so a later UI/cognition projection can explain why no alternative was available.

---

## Access policy

Access authority is separate from ordinary requirements.

V1 modes:
- `public`;
- `owner_or_resident`;
- `authorized`;
- `restricted`;
- `requirements`.

### Public

Entry authority does not depend on Character or Location grade.

### Owner or resident

The actor must have represented ownership or residency.

### Authorized

The actor must have an explicit represented authorization.

### Restricted

Fails closed. A future slice may define a more specific route/credential policy rather than guessing how to bypass a restricted boundary.

### Requirements

Delegates to the typed requirement evaluator. This supports grade-gated, quest/state-gated or composite access without making grade itself the access authority.

---

## Operating state

Operating state remains separate from access policy.

V1 represented states:
- `open`;
- `closed`;
- `locked`;
- `blocked`.

`evaluate_location_entry()` composes the two independent results:

`access allowed AND operating state open -> entry allowed`.

Examples:
- a public shop that is closed remains inaccessible now;
- a private Estate gate may be physically open but still reject a non-owner/non-resident;
- a high-grade public Location still admits a low-grade Character unless an explicit access requirement says otherwise.

---

## Item Grade versus interaction requirement

A 55 lb fixed dumbbell derives an S `item/resistance_load` grade under I5.4.

That does **not** imply:
- S Character Strength to curl it;
- S Character Strength to carry it;
- S Character Strength to move it a few inches;
- any universal actor requirement at all.

Each future action definition must declare its own actor requirement if one is needed.

This prevents Item classification from becoming accidental gameplay authorization.

---

## Location Grade versus access

Location completeness grade describes represented simulation completeness only.

An L4/A Location may be public or private.

An L1/D Location may still be private/restricted.

No grade evaluator changes ownership, residency, authorization, topology or operating state.

---

## Failure semantics

Fail closed when:
- required grade dimension is absent;
- raw/state value is absent;
- required Item/skill/equipment/ownership/residency/authorization reference is absent;
- a comparison is malformed;
- a policy mode is unknown;
- a composition is empty/malformed;
- operating state is unsupported.

Failure output is structured and deterministic.

---

## Boundaries / non-goals

I5.5 does not yet:
- wire every existing Real World action to the new universal requirement engine;
- migrate existing Action Conditions v1;
- implement credentials/keys/cards as a full taxonomy;
- implement criminal/trespass consequences;
- add time-window/calendar syntax;
- add arbitrary scripting/executable expressions;
- make Location access editable in Telegram;
- persist new access policy tables;
- mutate canonical world topology/access state.

Later Item/Location schemas consume this contract explicitly where needed.

---

## Acceptance

`tests/test_universal_requirements_access_v1.py` proves:
- public access is independent of grade;
- private owner/resident access rejects an unauthorized high-grade actor;
- Character grade requirements use the explicitly named Character dimension;
- S Item grade is not imported into Character requirements;
- deterministic nested `all` / `any` composition;
- missing evidence fails closed;
- possession, equipment, ownership and authorization remain distinct;
- authorized/restricted modes are explicit;
- unmet grade/authorization access returns structured failures;
- operating state composes separately from access;
- comparison semantics remain fail closed;
- malformed contracts reject rather than authorize.

Next slice after green CI:

**I5.6 — Universal Item Schema v1.**
