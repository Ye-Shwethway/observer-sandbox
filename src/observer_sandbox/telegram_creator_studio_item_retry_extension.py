from __future__ import annotations


def install_item_retry_extension(base) -> None:
    original_retry = base._manual_retry_view

    def item_retry_view(conn, user_id: int, expected: str, error: Exception):
        session = base._session(conn, user_id)
        if session and str(session.get("creation_type") or "") == "item":
            mode = {
                "item-batch-description": "batch-ai",
                "item-batch-json": "batch-manual",
                "item-json": "manual",
                "description": "ai",
            }.get(expected)
            if mode is not None:
                text, keyboard = base._prompt_view("item", mode)
                kind = "Item batch" if expected.startswith("item-batch-") else "Item"
                return (
                    f"⚠️ {kind} draft rejected\n"
                    f"{error}\n\n"
                    f"{text}",
                    keyboard,
                )
        return original_retry(conn, user_id, expected, error)

    base._manual_retry_view = item_retry_view


__all__ = ["install_item_retry_extension"]
