from __future__ import annotations

import json
import re
import sqlite3
from typing import Any

from .creation_sandbox import get_sandbox_object
from .creator_draft_export import send_text_document


def _display(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", str(value or "").lower()).strip("-")
    return text or "character"


def _profile_rows(conn: sqlite3.Connection, object_id: str):
    return conn.execute(
        """
        SELECT v.field_key,v.value_json,v.mode,v.authority,v.source,
               d.domain,d.label,d.data_type,d.unit,d.sensitivity
        FROM creation_sandbox_profile_values v
        LEFT JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.object_id=?
        ORDER BY COALESCE(d.domain, ''), COALESCE(d.rowid, 999999), v.field_key
        """,
        (object_id,),
    ).fetchall()


def render_sandbox_character_profile_text(
    conn: sqlite3.Connection,
    object_id: str,
) -> tuple[str, str]:
    obj = get_sandbox_object(conn, object_id)
    if obj["creation_type"] != "character" or obj["lifecycle_status"] != "active":
        raise ValueError("Sandbox Character export requires an active Character")

    name = str(obj["identity"].get("name") or object_id)
    filename = f"sandbox-character-{_slug(name)}-full-profile.txt"
    lines = [
        "SANDBOX CHARACTER — FULL PROFILE SNAPSHOT",
        "=" * 72,
        f"Name: {name}",
        f"Object ID: {object_id}",
        f"Sandbox ID: {obj['sandbox_id']}",
        f"Lifecycle: {obj['lifecycle_status']}",
        f"Creation schema version: {obj['schema_version']}",
        "",
        "IDENTITY / CREATION OBJECT",
        "-" * 72,
        f"identity: {_display(obj.get('identity'))}",
        f"properties: {_display(obj.get('properties'))}",
        f"capabilities: {_display(obj.get('capabilities'))}",
        f"resolved_relations: {_display(obj.get('resolved_relations'))}",
        f"provenance: {_display(obj.get('provenance'))}",
        "",
        "PROFILE VALUES",
        "-" * 72,
    ]

    rows = _profile_rows(conn, object_id)
    if not rows:
        lines.append("(none)")
    current_domain: str | None = None
    for row in rows:
        domain = str(row["domain"] or "unregistered")
        if domain != current_domain:
            if current_domain is not None:
                lines.append("")
            lines.append(f"[{domain.upper()}]")
            current_domain = domain
        try:
            value = json.loads(row["value_json"])
        except (TypeError, json.JSONDecodeError):
            value = row["value_json"]
        label = str(row["label"] or row["field_key"])
        unit = f" {row['unit']}" if row["unit"] else ""
        lines.append(
            f"{row['field_key']} | {label}: {_display(value)}{unit} "
            f"| mode={row['mode']} | authority={row['authority']} | source={row['source']}"
        )

    lines.extend(["", "SKILLS", "-" * 72])
    skills = conn.execute(
        """
        SELECT skill_key,category,score,tier,experience,metadata_json
        FROM creation_sandbox_character_skills
        WHERE object_id=?
        ORDER BY COALESCE(category, ''),skill_key
        """,
        (object_id,),
    ).fetchall()
    if skills:
        for row in skills:
            lines.append(
                f"{row['skill_key']} | category={row['category']} | score={row['score']} "
                f"| tier={row['tier']} | experience={row['experience']} | metadata={row['metadata_json']}"
            )
    else:
        lines.append("(none)")

    lines.extend(["", "PREFERENCES", "-" * 72])
    preferences = conn.execute(
        """
        SELECT preference_type,subject,intensity
        FROM creation_sandbox_character_preferences
        WHERE object_id=? ORDER BY preference_type,subject
        """,
        (object_id,),
    ).fetchall()
    if preferences:
        for row in preferences:
            lines.append(
                f"{row['preference_type']}: {row['subject']} | intensity={row['intensity']}"
            )
    else:
        lines.append("(none)")

    lines.extend(["", "HOBBIES", "-" * 72])
    hobbies = conn.execute(
        """
        SELECT name,proficiency,frequency,enjoyment
        FROM creation_sandbox_character_hobbies
        WHERE object_id=? ORDER BY name
        """,
        (object_id,),
    ).fetchall()
    if hobbies:
        for row in hobbies:
            lines.append(
                f"{row['name']} | proficiency={row['proficiency']} | frequency={row['frequency']} "
                f"| enjoyment={row['enjoyment']}"
            )
    else:
        lines.append("(none)")

    lines.extend(["", "HABITS", "-" * 72])
    habits = conn.execute(
        """
        SELECT name,description,frequency,strength
        FROM creation_sandbox_character_habits
        WHERE object_id=? ORDER BY name
        """,
        (object_id,),
    ).fetchall()
    if habits:
        for row in habits:
            lines.append(
                f"{row['name']} | {row['description']} | frequency={row['frequency']} | strength={row['strength']}"
            )
    else:
        lines.append("(none)")

    lines.extend([
        "",
        "BOUNDARY",
        "-" * 72,
        "This is a read-only snapshot of the current approved Sandbox Character profile.",
        "It is not a Creator Studio draft and it does not mutate the Sandbox or canonical Real World.",
        "Live runtime-owned changing state is intentionally outside this profile export.",
    ])
    return filename, "\n".join(lines) + "\n"


def send_sandbox_character_profile_document(
    conn: sqlite3.Connection,
    object_id: str,
    *,
    chat_id: int,
) -> str:
    filename, text = render_sandbox_character_profile_text(conn, object_id)
    return send_text_document(
        chat_id,
        filename,
        text,
        caption="📄 Sandbox Character full profile",
    )


__all__ = [
    "render_sandbox_character_profile_text",
    "send_sandbox_character_profile_document",
]
