from __future__ import annotations

from typing import Any, Mapping

from .item_metrics import DEFAULT_ITEM_METRIC_REGISTRY, ItemMetricError


def _fmt_number(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def item_metric_lines(modules: Mapping[str, Any], *, heading: str = "PERFORMANCE METRICS") -> list[str]:
    metrics = modules.get("metrics") if isinstance(modules, Mapping) else None
    if not isinstance(metrics, Mapping) or not metrics:
        return []
    lines = [heading]
    for metric_id in sorted(metrics):
        raw = metrics[metric_id]
        if not isinstance(raw, Mapping):
            continue
        try:
            spec = DEFAULT_ITEM_METRIC_REGISTRY.spec(metric_id)
        except ItemMetricError:
            continue
        value = raw.get("value")
        unit = raw.get("unit")
        if value is None or unit is None:
            continue
        lines.append(f"• {spec.label}: {_fmt_number(value)} {unit}")
    return lines if len(lines) > 1 else []


__all__ = ["item_metric_lines"]
