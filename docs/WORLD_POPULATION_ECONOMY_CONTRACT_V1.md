# Ambient Population & Basic World Economy Contract v1

Status: PLANNING AUTHORITY — IMPLEMENTATION NOT YET AUTHORIZED

## Purpose

This document refines WF-9 and WF-10. It defines the lightest world-process layer needed for public places to feel occupied and for outside resource acquisition to have persistent economic consequences.

## Population tiers

Observer Sandbox should distinguish:

### Tier A — persistent named characters
Full character entities with ordinary profile/runtime/cognition where justified.

### Tier B — ambient presence
Lightweight place-level representation of people who matter physically/operationally but do not require independent identities or LLM cognition.

Examples:
- store staff present;
- a few patrons in a cafe;
- pedestrians on a public connector;
- crowd level at a park.

Ambient presence is not a hidden named NPC database.

## Ambient state

Minimum useful place-level state may include:
- occupancy/count band or bounded count;
- role/category presence such as `staff`, `patrons`, `pedestrians`;
- service staffing availability when required;
- effective time window or producer source.

Use the least detailed representation that affects behavior.

## Ambient behavior boundary

Ambient presence may:
- make a venue operationally staffed;
- provide generic social/environmental context;
- satisfy a service precondition when no named agent is needed;
- influence crowd/availability semantics later.

It may not:
- invent persistent personal memories/relationships;
- perform free-form autonomous LLM actions;
- silently become a named character after the fact without explicit promotion/creation;
- stand in for a specific known person.

## Population evolution

V1 may derive ambient presence from venue schedules and simple time-based occupancy profiles. City demographic simulation is unnecessary.

The important rule is that presence changes through represented deterministic producers rather than fresh prompt invention every cognition.

## Money authority

Money is persistent authoritative state associated with an actor/account/entity, not a narrative estimate.

V1 needs only the minimum representation for bounded transactions:
- balance;
- currency identity;
- payer/payee;
- amount;
- transaction reason/reference.

Do not create a banking subsystem unless later features require one.

## Price authority

Prices for represented goods/services are authored/runtime facts. The LLM may choose whether to buy; it does not set the authoritative price.

V1 may use static prices. Dynamic markets are deferred.

## Purchase transaction

Minimum transaction flow:

`validate venue/service/stock -> validate price -> validate payer balance -> transfer money -> transfer/decrement resource -> emit auditable event/state changes`

All steps must settle atomically enough that partial purchase state cannot leave money/resource inconsistent.

## Service payment

For non-item services, transaction completion records the payment and then invokes/authorizes the represented service action/effect contract. Payment alone must not fabricate an unimplemented service outcome.

## Income/replenishment

WF-10 does not require a job system.

If sustained simulation requires incoming money, use one explicit bounded source with clear authority, such as an authored account balance/replenishment or later represented income event. Do not invent employment merely to close the accounting loop.

## First economy proof

A strong first proof is a grocery/resource purchase:
1. Estate resource shortage exists through ordinary depletion;
2. actor identifies a reachable open venue with relevant stock;
3. actor travels there;
4. ambient staff presence can satisfy ordinary service availability without a named cashier agent;
5. price/balance/stock validate;
6. purchase transfers money and resource authoritatively;
7. actor can return with the acquired resource;
8. all resulting state remains observable/auditable.

This completes a meaningful outside-world loop without macroeconomics.

## Cognition projection

Only expose decision-relevant summaries:
- whether a venue is staffed/usable;
- approximate local crowd context if relevant;
- actor available balance where needed for current choices;
- exact or compact relevant price/stock information.

Do not send transaction history, all balances, all prices, or ambient population across the region.

## Deferred depth

Not v1:
- salaries/jobs;
- taxes;
- banking products;
- credit/debt;
- investment;
- macroeconomics;
- market-driven pricing;
- business profit/loss;
- population demographics;
- thousands of autonomous NPCs;
- citywide social networks.

## Program completion criterion

WF-9 and WF-10 complete the first World Foundation Expansion program when a character can leave a represented private property, traverse a bounded regional world, encounter operational public venues, obtain a finite represented resource through an authoritative transaction, and return with persistent world consequences—without requiring the LLM to invent topology, access, population, stock, price, or state mutation.