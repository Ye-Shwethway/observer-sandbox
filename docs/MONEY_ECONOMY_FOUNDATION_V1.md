# W3 — Money / Economy Foundation v1

Status: IMPLEMENTATION CONTRACT

## Purpose

W3 introduces authoritative in-universe financial truth and deterministic affordability while preserving the Observer Sandbox cognition boundary. The active v1 runtime stays deliberately small, but the persistence spine is shaped so later Jobs/Careers, employers, companies, governments, property, investments and larger regional/global economy systems can attach without replacing the foundation.

This is a fictional simulation ledger. It has no connection to real banking, payment or market systems.

## Canonical separation

`economic truth != financial notice availability != exposure != perception/interpretation != memory != concern/thought != intention/plan != action proposal != action authority`

A low balance does not mean a character is worried. A large balance does not change behavior. Economy state may satisfy or fail deterministic resource validation only.

## W3 v1 represented concepts

### Economic entity

An economic entity is the ownership/accounting identity used by W3. It may link to a represented world entity. Initial generic types are character, household, company, organization, government, trust and other.

The first represented exemplar is Darian Thorne. This is a factual seed, not a character-specific behavior rule.

### Financial account

Accounts hold authoritative spendable monetary balances by currency. Amounts are stored in integer minor units rather than floating point values.

`net worth != spendable account balance`

W3 v1 does not implement real banks, cards, interest, credit scoring or foreign-exchange conversion.

### Economic transaction and ledger entries

A transaction is an immutable header with one or more signed account entries. Account balances are authoritative cached state changed atomically with the ledger entries.

The header + entries shape is intentionally expandable to later payroll, split settlement, taxes and multi-party transactions. V1 helpers only need bounded opening-balance, debit/credit and same-currency transfer semantics.

One-sided entries are permitted only as represented boundary flows such as canonical opening balances or future explicitly authored income/expense sources. They are not evidence that an unrepresented counterparty exists.

### Assets, liabilities and valuations

Assets and liabilities are distinct from account balances. An asset may link to a represented world entity, which is the socket used by the later object/world valuation program.

Valuations are append-only facts with method, time and provenance. A later valuation may supersede an earlier one for a calculation without destroying valuation history.

V1 net worth for one currency is:

`non-closed monetary balances + latest active asset valuations - active/defaulted liabilities`

No automatic FX conversion exists.

### Global-economy expansion socket

The schema deliberately permits future economic entities, assets and aggregate valuations beyond one character. It does **not** yet claim that the complete world economy is represented.

Later macroeconomic work must distinguish at minimum:
- gross real/non-financial asset value;
- financial claims between represented entities;
- liabilities;
- consolidated net wealth;
- valuation date/method/currency.

This avoids double-counting a company asset and the financial claim on that same value when computing measures such as world total wealth.

## Deterministic affordability

Affordability is a resource-authority check. A proposed purchase or paid action may only settle when the selected spendable account can cover the authoritative amount and all other domain conditions are satisfied.

A failed affordability check mutates neither money nor the represented purchased resource.

Future purchase settlement should preserve the earlier economy contract:

`validate venue/service/stock -> validate authoritative price -> validate payer funds -> settle ledger -> settle resource transfer -> emit auditable state/events`

The economy ledger alone does not fabricate stock, ownership transfer or service outcomes.

## W0 financial notices

W3 may explicitly publish a W0 stimulus with `stimulus_type=financial`. Publication only makes the represented financial signal available to the scoped character.

W3 never automatically records exposure and never creates Character Memory, Mind artifacts, concerns, intentions, plans or action proposals.

A concrete future phone, statement, bank interface or communication path must be represented before its delivery semantics are claimed.

## Initial Darian wealth seed

Creator-approved opening scale:
- Thorne Estate valuation: USD 16.5M;
- investment assets: USD 6.5M;
- primary liquid holdings: USD 1.8M;
- other personal assets: USD 0.7M;
- aggregate liabilities: USD 0.5M;
- resulting seeded net worth: **USD 25.0M**.

The Estate is linked to `loc_thorne_estate`; the other categories remain aggregate economic assets until their underlying objects/instruments are represented.

The seed is idempotent. Runtime reinitialization must not reset a live account balance after transactions have changed it.

## Object valuation follow-up

W3 v1 provides the socket but does not assign prices/values to every existing universe object.

The next bounded valuation slice should:
1. inventory every currently represented value-bearing location/object/item/resource;
2. classify whether it is an independently valued asset, a component already included in a parent asset, a consumable/stock item, or economically immaterial;
3. assign canonical or rule-derived values with currency, valuation method, provenance and effective simulation time;
4. prevent double-counting components already included in a property/business valuation;
5. define creation-time valuation rules so new represented objects do not silently enter the universe without an explicit economic-value policy;
6. keep authored price, replacement value, market valuation and owner net-worth contribution distinct where necessary.

This backfill/rule program is deliberately separate from W3 core so the financial authority can remain small and reusable.

## Deferred

Not activated by W3 v1:
- jobs or salaries;
- recurring bills/payables;
- banks/cards/payment instruments;
- loans/interest/credit products beyond liability facts;
- taxes;
- dynamic markets or pricing;
- securities trading;
- business P&L;
- FX conversion;
- inflation;
- regional or world total-wealth computation;
- automatic financial anxiety or money-seeking behavior.

Those systems should plug into W3 rather than replace it.
