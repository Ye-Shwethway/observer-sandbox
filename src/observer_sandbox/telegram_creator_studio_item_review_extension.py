from __future__ import annotations

from .creator_studio import active_draft
from .telegram_item_draft_review import item_detail_view, send_item_draft_document


def _item_draft(draft):
    return bool(draft and draft.get("creation_type") == "item")


def install_item_review_extension(base) -> None:
    original_preview = base.draft_preview_view
    original_callback = base.studio_callback_view

    def draft_preview_view(conn, user_id: int, *, notice: str | None = None):
        text, keyboard = original_preview(conn, user_id, notice=notice)
        draft = active_draft(conn, user_id)
        if not _item_draft(draft):
            return text, keyboard

        enhanced = []
        inserted = False
        for row in keyboard:
            callbacks = {button.get("callback_data") for button in row}
            if not inserted and ("sw:cs:reroll" in callbacks or "sw:cs:approve" in callbacks):
                enhanced.append([{"text": "🔎 Review Item Details", "callback_data": "sw:cs:item-detail:0"}])
                enhanced.append([{"text": "📄 Export Full Draft (.txt)", "callback_data": "sw:cs:item-export"}])
                inserted = True
            enhanced.append(row)
        if not inserted:
            enhanced.insert(0, [{"text": "🔎 Review Item Details", "callback_data": "sw:cs:item-detail:0"}])
            enhanced.insert(1, [{"text": "📄 Export Full Draft (.txt)", "callback_data": "sw:cs:item-export"}])
        return text, enhanced

    def studio_callback_view(conn, user_id: int, callback_data: str):
        draft = active_draft(conn, user_id)
        if _item_draft(draft):
            if callback_data.startswith("sw:cs:item-detail:"):
                try:
                    index = int(callback_data.rsplit(":", 1)[-1])
                except ValueError:
                    index = 0
                return item_detail_view(draft, index)
            if callback_data == "sw:cs:item-export":
                try:
                    filename = send_item_draft_document(draft, user_id)
                except Exception as exc:
                    return draft_preview_view(conn, user_id, notice=f"Export failed: {exc}")
                return draft_preview_view(conn, user_id, notice=f"📄 Export sent: {filename}")
        return original_callback(conn, user_id, callback_data)

    base.draft_preview_view = draft_preview_view
    base.studio_callback_view = studio_callback_view


__all__ = ["install_item_review_extension"]
