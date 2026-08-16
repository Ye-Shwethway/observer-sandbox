# World Venue, Service & Resource Contract v1

Status: PLANNING AUTHORITY — IMPLEMENTATION NOT YET AUTHORIZED

## Purpose

This document refines WF-7 and WF-8. It defines how outside destinations become useful places with represented capabilities/resources and how shortages can create real reasons for travel.

## Venue principle

A venue is a location with represented service/facility semantics. It is not a special parallel world object and should reuse the generic location/entity/relation model.

Minimum venue metadata:
- functional category;
- location identity;
- access policy;
- operating schedule/current open state where relevant;
- represented service capabilities;
- represented facilities/resources.

## Service capability model

Services should be identified by stable machine-readable capabilities, for example:
- `sell_food`
- `serve_meal`
- `medical_care`
- `sell_medicine`
- `fuel_vehicle` (later)
- `lodging`
- `recreation`

Capabilities say what a venue can support; they do not themselves perform state mutation. Ordinary actions/transactions remain authoritative runtime operations.

## Operating schedule

A venue may declare bounded weekly/daily operating windows. Current open/closed state should be derived from schedule + simulation time unless explicitly overridden by represented state.

V1 does not need holiday calendars, staffing rotas, or exceptional closure engines unless required by a concrete use case.

## Resource authority

Resources must have authoritative existence/location rather than appear because cognition requests them.

Minimum dimensions where meaningful:
- resource/item identity;
- authoritative location or container;
- quantity/availability;
- ownership;
- portable vs fixture;
- consumable vs durable;
- existing effect/use metadata.

Reuse current inventory/item-effect contracts wherever possible.

## Location versus ownership

A resource can be located at a store but owned by the business/venue; an actor can purchase it and then carry it. These transitions must not be modeled by changing `contains` semantics.

Location, ownership, carriage and equipment remain distinct relations/state.

## Availability

Availability should be deterministic:
- finite quantity where meaningful;
- boolean/service availability for resources where exact units add no value;
- unavailable resources are excluded or fail validation;
- cognition cannot create stock.

## Depletion

Actions that consume resources update authoritative quantity/inventory state and emit appropriate state/event evidence.

Examples:
- eating consumes represented food;
- purchasing transfers stock and later money;
- using a finite household supply reduces it.

Do not implement depletion for decorative fixtures that do not need it.

## Replenishment

V1 may use simple explicit producers:
- authored restock event;
- deterministic periodic restock;
- transaction-driven transfer.

Do not build supply-chain simulation merely to keep one grocery shelf stocked.

## Venue admission rule

Add a venue only when it supports a simulation loop, such as:
- obtaining food/resources;
- receiving a service;
- recreation/activity;
- healthcare;
- travel support;
- social/story relevance.

Avoid world growth by directory cataloguing.

## First public venue exemplar

The first Tahoe venue should exercise the complete dependency chain:
1. it exists as a reachable regional node;
2. route/access/open state are authoritative;
3. it exposes at least one service/resource capability;
4. actor cognition can discover that capability through a bounded relevant query;
5. a deterministic action can use/obtain the represented resource/service;
6. persistent state changes follow.

A grocery/store is a strong candidate because it connects hunger/household stock, travel, venue hours, resources and later economy.

## Household resource loop

Estate resources should eventually participate in the same generic model as public-world stock.

Target loop:

`Estate supply decreases -> actor detects relevant shortage -> reachable venue capability is queried -> actor travels -> resource obtained -> Estate/inventory stock changes`

This loop should not require special-case Darian logic.

## Cognition projection

Provide only:
- nearby/reachable task-relevant venues;
- service capability summaries;
- relevant open/access state;
- relevant available resource summary;
- estimated travel cost when useful.

Do not inject full inventories or every Tahoe venue into each cognition call.

## Deferred depth

Not v1:
- product catalog realism;
- supply chains;
- vendor negotiation;
- detailed medical workflows;
- reservations;
- delivery logistics;
- dynamic pricing;
- fuel until vehicle foundation;
- exhaustive Tahoe businesses.

## Dependency relationship

WF-7 depends on reachable regional geography and access/time. WF-8 depends on venue/place/resource authority. Together they prepare the first practical world-need loop and provide direct prerequisites for Basic World Economy v1.