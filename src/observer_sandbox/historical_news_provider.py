from __future__ import annotations

import gzip
import hashlib
import io
import json
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, Callable


GDELT_GAL_URL = "https://storage.googleapis.com/data.gdeltproject.org/gdeltv3/gal/{stamp}.gal.json.gz"


class HistoricalNewsProviderError(RuntimeError):
    pass


def _utc(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _default_fetch(url: str, timeout: float = 12.0) -> bytes | None:
    request = urllib.request.Request(url, headers={"User-Agent": "observer-sandbox/0.0.1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise HistoricalNewsProviderError(f"GDELT HTTP {exc.code}: {exc.reason}") from exc
    except Exception as exc:
        raise HistoricalNewsProviderError(str(exc)) from exc


def _records(blob: bytes) -> list[dict[str, Any]]:
    try:
        raw = gzip.GzipFile(fileobj=io.BytesIO(blob)).read().decode("utf-8", errors="replace")
    except Exception as exc:
        raise HistoricalNewsProviderError("GDELT GAL payload could not be decompressed") from exc
    result: list[dict[str, Any]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("url") and value.get("title"):
            result.append(value)
    return result


def gdelt_historical_articles(
    sim_time: str | datetime,
    *,
    lookback_minutes: int = 90,
    limit: int = 40,
    fetch: Callable[[str], bytes | None] = _default_fetch,
) -> list[dict[str, Any]]:
    """Return bounded GAL evidence preceding universe simulation time.

    GAL is published as per-minute historical files. Missing minute files are
    normal, so 404s are treated as gaps rather than provider failure.
    """
    end = _utc(sim_time).replace(second=0, microsecond=0)
    minutes = max(15, min(int(lookback_minutes), 180))
    wanted = max(1, min(int(limit), 100))
    seen: set[str] = set()
    results: list[dict[str, Any]] = []

    for offset in range(minutes + 1):
        minute = end - timedelta(minutes=offset)
        stamp = minute.strftime("%Y%m%d%H%M00")
        blob = fetch(GDELT_GAL_URL.format(stamp=stamp))
        if not blob:
            continue
        for raw in _records(blob):
            url = str(raw.get("url") or "").strip()
            if not url or url in seen:
                continue
            seen.add(url)
            title = str(raw.get("title") or "").strip()
            if not title:
                continue
            outlet = str(raw.get("outletName") or raw.get("domain") or "Unknown outlet").strip()
            published = str(raw.get("date") or minute.isoformat())
            description = str(raw.get("description") or raw.get("descriptionLong") or "").strip()
            provider_ref = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
            results.append(
                {
                    "provider_id": "gdelt_gal",
                    "provider_ref": provider_ref,
                    "title": title,
                    "summary": description,
                    "source_url": url,
                    "source_name": outlet,
                    "source_domain": str(raw.get("domain") or ""),
                    "published_at": published,
                    "language": raw.get("language") or raw.get("lang"),
                    "provenance": {"dataset": "GDELT Article List", "gal_stamp": stamp},
                }
            )
            if len(results) >= wanted:
                return results
    return results
