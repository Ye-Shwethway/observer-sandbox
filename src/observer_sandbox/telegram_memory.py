from __future__ import annotations

from datetime import datetime
from typing import Any

from .character_memory import list_memories, memory_overview


PAGE_SIZE = 6


def _fmt_time(value: Any) -> str:
    if not value:
        return "Unknown"
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).strftime("%d-%m-%Y %I:%M %p")
    except ValueError:
        return str(value)


def _character_name(conn, character_id: str) -> str:
    row = conn.execute("SELECT name FROM entities WHERE id=? AND entity_type='character'", (character_id,)).fetchone()
    return str(row[0]) if row is not None else character_id


def memory_view(
    conn,
    character_id: str,
    *,
    memory_type: str = "all",
    page: int = 0,
) -> tuple[str, list[list[dict[str, str]]]]:
    kind = memory_type if memory_type in {"episodic", "semantic"} else "all"
    memories = list_memories(
        conn,
        character_id,
        memory_type=None if kind == "all" else kind,
        limit=200,
    )
    overview = memory_overview(conn, character_id)
    page_count = max(1, (len(memories) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(int(page), page_count - 1))
    start = page * PAGE_SIZE
    visible = memories[start:start + PAGE_SIZE]
    character_name = _character_name(conn, character_id)

    lines = [
        f"🧠 {character_name} · MEMORY",
        "━━━━━━━━━━━━━━━━━━",
        f"Active {overview['total']} · Episodic {overview['episodic']} · Knowledge {overview['semantic']}",
        f"Latest encoded  {_fmt_time(overview['latest_encoded'])}",
        f"View  {kind.title()} · Page {page + 1}/{page_count}",
        "",
    ]
    if not visible:
        lines.append("No represented memories yet. New completed experiences will appear here dynamically.")
    else:
        for item in visible:
            icon = "🎞" if item["type"] == "episodic" else "📚"
            lines.append(f"{icon} {_fmt_time(item['event_sim_time'])}")
            lines.append(f"• {str(item['summary']).replace('_', ' ').title()}")
            lines.append(
                f"  Salience {item['salience']:.2f} · Confidence {item['confidence']:.2f} · Recalled {item['recall_count']}×"
            )
            related = item.get("related_entities") or []
            if related:
                names: list[str] = []
                for relation in related[:3]:
                    row = conn.execute("SELECT name FROM entities WHERE id=?", (relation["entity_id"],)).fetchone()
                    names.append(str(row[0]) if row is not None else str(relation["entity_id"]))
                lines.append(f"  Related: {', '.join(names)}")
            lines.append("")
        while lines and lines[-1] == "":
            lines.pop()

    return "\n".join(lines), _keyboard(character_id, kind=kind, page=page, page_count=page_count)


def memory_callback_view(conn, callback_data: str) -> tuple[str, list[list[dict[str, str]]]] | None:
    if not callback_data.startswith("mem:"):
        return None
    parts = callback_data.split(":")
    if len(parts) != 4:
        return "Unknown memory destination.", None
    _, character_id, kind, raw_page = parts
    try:
        page = int(raw_page)
    except ValueError:
        page = 0
    return memory_view(conn, character_id, memory_type=kind, page=page)


def _keyboard(
    character_id: str,
    *,
    kind: str,
    page: int,
    page_count: int,
) -> list[list[dict[str, str]]]:
    selectors = [
        {"text": f"{'✓ ' if kind == 'all' else ''}All", "callback_data": f"mem:{character_id}:all:0"},
        {"text": f"{'✓ ' if kind == 'episodic' else ''}Episodes", "callback_data": f"mem:{character_id}:episodic:0"},
        {"text": f"{'✓ ' if kind == 'semantic' else ''}Knowledge", "callback_data": f"mem:{character_id}:semantic:0"},
    ]
    keyboard: list[list[dict[str, str]]] = [selectors]
    if page_count > 1:
        row: list[dict[str, str]] = []
        if page > 0:
            row.append({"text": "◀ Prev", "callback_data": f"mem:{character_id}:{kind}:{page - 1}"})
        row.append({"text": f"{page + 1}/{page_count}", "callback_data": f"mem:{character_id}:{kind}:{page}"})
        if page + 1 < page_count:
            row.append({"text": "Next ▶", "callback_data": f"mem:{character_id}:{kind}:{page + 1}"})
        keyboard.append(row)
    keyboard.append([{"text": "← Character", "callback_data": f"char:{character_id}"}])
    keyboard.append([{"text": "⌂ Observer Home", "callback_data": "nav:home"}])
    return keyboard
