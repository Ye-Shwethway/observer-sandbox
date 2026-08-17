# W4 Information / Media Foundation v1

Status: ACTIVE IMPLEMENTATION CONTRACT

## Purpose

Represent published information and media separately from objective world truth and separately from character knowledge.

Canonical chain:

`source/world evidence -> information item -> publication/availability -> represented media device/channel -> W0 stimulus -> actual exposure -> later perception/appraisal -> later Memory/Mind`

Hard separation:

`published/reported != objectively true != exposed != understood != believed != remembered != thought != intended != actionable authority`.

An information item authoritatively represents that content was published or made available. It does **not** make every claim contained in that content objectively true.

## Minimum model

W4 v1 provides:
- generic information sources/publishers with provenance and credibility metadata;
- generic information items with publication time, source URL/reference, language and verification status;
- media publications with bounded availability windows;
- ordered source-item provenance for each publication;
- represented media-device mapping;
- W0 `information` / `media` stimulus production;
- explicit, deterministic exposure recording only when a represented consumption path proves the signal reached the actor boundary.

## TV exemplar

The first represented access path reuses the existing `object_media_console` world object and maps it as a television/media device. W4 does not create a duplicate TV object and therefore does not bypass W3.1 object-value coverage.

A TV publication creates a W0 information stimulus scoped to that represented device. Merely publishing a bulletin or being in the same room does not create exposure. `record_tv_exposure` requires the actor to be co-located with the represented device and represents an explicit compatible TV-consumption context.

Exposure does not create Memory or Mind state.

## Credibility and provenance

Source credibility is source metadata, not a character belief score and not a truth probability. Initial values remain deliberately shallow, with `unknown` acceptable when no stronger represented evidence exists.

External provider records preserve provider id/reference, source URL, outlet identity and provider provenance.

## AI editorial boundary

AI may select, summarize, format and narrate supplied authoritative source records into a television bulletin. AI output alone does not establish external objective truth.

Every generated story must preserve a supplied `source_item_id`. Unknown source references are rejected.

If the configured news-generation model is missing or inference fails, W4 falls back to a deterministic bulletin compiled from represented source records. News generation failure must not freeze simulation or fabricate replacement facts.

## AI binding

News editorial generation uses the existing provider/model registry and binding architecture with an independent role:

- scope type: `engine`
- scope id: `information_media`
- role: `news_generation`

This binding is independent from character cognition primary/fallback bindings.

Telegram uses the same provider catalog, candidate selection, real model probe and explicit Save & Activate pattern as Character AI settings.

## Telegram AI settings UX

Creator Settings -> AI Settings is grouped into:
- Character AI — primary cognition + cognition fallback;
- News Generation AI — one independent editorial binding.

All currently registered provider families remain eligible. Candidate selection never changes the active binding; Test Model is a real structured inference; only a successfully tested candidate may be saved.

## Non-goals

W4 does not implement:
- character belief or opinion;
- automatic media interests/preferences;
- media-to-mood modifiers;
- automatic memory encoding;
- Mental Episodes, appraisal or plans;
- communication/messages;
- social-media feeds or recommendation algorithms;
- a full browser/internet/network simulation;
- AI-generated objective world facts.

## Acceptance

W4 is accepted when:
- information/source/publication persistence is idempotent and character-generic;
- reported content is not treated as objective claim truth;
- the existing Media Console is represented as the TV exemplar;
- a TV publication produces a scoped W0 information/media stimulus;
- no exposure is recorded by publication or Telegram observation alone;
- explicit TV consumption records exposure only for a co-located actor;
- exposure creates no Memory/Mind state;
- news AI has an independent provider/model binding with real non-mutating probe and explicit activation;
- provider failure has a deterministic source-backed fallback;
- existing character cognition bindings are unchanged by news configuration.
