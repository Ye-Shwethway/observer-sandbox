# Historical Weather Provider v1 — Acceptance Contract

Status: ACTIVE ACCEPTANCE

Canonical architecture: `docs/HISTORICAL_WEATHER_PROVIDER_V1.md`

The slice passes only if all of the following remain true:

1. Universe simulation time, never the host wall clock, selects the historical provider date/hour.
2. The configured South Lake Tahoe coordinate is explicitly a city-area weather sampling anchor and does not establish an exact canonical Estate address/location.
3. Open-Meteo payloads are normalized into the existing W1 `environment_states` contract before any W0 or cognition-facing use.
4. Daily response caching prevents network fetches on every autonomy/service wake.
5. Same simulation hour synchronization is idempotent.
6. W1 remains authoritative for location containment and direct outdoor ambient exposure; indoor locations do not receive ambient weather merely because the Estate has weather.
7. Historical provider synchronization never auto-creates Character Memory, Mind cycles, relationship state, mood, intentions, plans or actions.
8. Provider/API failure does not stop core autonomy.
9. Procedural fallback is deterministic for the same sampling anchor + simulation hour and is explicitly marked synthetic.
10. A synthetic fallback may be superseded by exact historical data after retry cooldown/recovery.
11. Weather provider configuration contains no named-character behavior policy.
12. Character exposure remains separate from environment state/stimulus creation.
13. Forecast or weather-app knowledge is not implied by ambient weather truth; future phone/TV/internet delivery must use represented information/media exposure.
14. Schema migration is idempotent and the provider cache retains source/error provenance without becoming simulation truth itself.
15. Final full PR CI is green before merge, and runtime-affecting merge receives the normal production deploy/verification.
