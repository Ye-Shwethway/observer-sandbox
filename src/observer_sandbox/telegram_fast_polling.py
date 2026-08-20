from __future__ import annotations

import json
import os
import time
import urllib.error
from pathlib import Path

from . import telegram_bot as base
from .telegram_command_menu import sync_bot_commands


def _deliver_message_reply(
    token: str,
    chat_id: int,
    reply: str,
    keyboard: list[list[dict[str, str]]] | None,
) -> None:
    """Deliver a plain-text reply while honoring one-shot Creator Studio prompt cleanup."""
    from .telegram_creator_studio import consume_next_input_delivery

    delivery = consume_next_input_delivery()
    if delivery and int(delivery[1]) == int(chat_id):
        action, target_chat_id, target_message_id = delivery
        if action == "edit":
            try:
                base._edit(token, target_chat_id, target_message_id, reply, keyboard)
                return
            except Exception:
                # Keep the response available even if the old prompt can no longer
                # be edited (for example, Telegram aged it out).
                pass
        elif action == "delete":
            try:
                base._api(
                    token,
                    "deleteMessage",
                    {"chat_id": target_chat_id, "message_id": target_message_id},
                    timeout=10,
                )
            except Exception:
                # Prompt cleanup is UX-only and must never discard a valid save.
                pass
    base._send(token, chat_id, reply, keyboard)


def _sync_command_menu(token: str, db_path: str | Path) -> None:
    """Publish the final role-aware help contract as Telegram's command menu."""
    sync_bot_commands(
        base._api,
        token,
        db_path,
        help_renderer=base._help,
        owner_id=base._owner_user_id(),
        allowed_user_ids=base._allowed_user_ids(),
    )


def run_polling(db_path: str | Path = base.DEFAULT_DB) -> None:
    """Telegram polling loop with eager callback acknowledgement.

    Telegram clients keep an inline-button progress spinner visible until
    ``answerCallbackQuery`` is received. The legacy loop acknowledged only after
    DB rendering and ``editMessageText`` completed, making otherwise healthy UI
    navigation feel hung whenever a card took noticeable time to render/edit.

    Authorized callbacks are therefore acknowledged immediately, before any DB
    work. Rendering and message editing still happen synchronously afterward.
    """

    base.load_runtime_secrets()
    token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return

    # Telegram's slash-command menu is runtime-owned. The final role-aware help
    # contract is reconciled on every service start, so deploys that add/remove a
    # documented command refresh the chat menu without a BotFather maintenance step.
    try:
        _sync_command_menu(token, db_path)
    except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError):
        # Menu publication is presentation metadata; a transient Telegram failure
        # must not keep the universe/runtime observer offline.
        pass

    owner_id = base._owner_user_id()
    if owner_id is not None:
        try:
            with base.connect(db_path) as conn:
                base.migrate(conn)
                notify_owner = base._notifications_enabled(conn, owner_id)
            if notify_owner:
                base._send(token, owner_id, base._boot_message())
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError):
            pass

    offset: int | None = None
    backoff = 1.0
    while True:
        try:
            payload: dict[str, object] = {
                "timeout": 20,
                "allowed_updates": json.dumps(["message", "callback_query"]),
            }
            if offset is not None:
                payload["offset"] = offset
            updates = base._api(token, "getUpdates", payload, timeout=30) or []
            backoff = 1.0

            for update in updates:
                offset = int(update["update_id"]) + 1
                callback = update.get("callback_query") or {}
                if callback:
                    sender = callback.get("from") or {}
                    user_id = int(sender.get("id", 0))
                    message = callback.get("message") or {}
                    chat = message.get("chat") or {}
                    callback_id = callback.get("id")

                    if chat.get("type") != "private" or base._user_role(user_id) == "unauthorized":
                        base._api(
                            token,
                            "answerCallbackQuery",
                            {"callback_query_id": callback_id, "text": "Not authorized"},
                            timeout=10,
                        )
                        continue

                    # UI responsiveness contract: clear Telegram's button spinner
                    # before any database work or message edit.
                    try:
                        base._api(
                            token,
                            "answerCallbackQuery",
                            {"callback_query_id": callback_id},
                            timeout=5,
                        )
                    except Exception:
                        # Callback acknowledgement failure must not prevent the
                        # requested navigation/update from being attempted.
                        pass

                    try:
                        callback_data = str(callback.get("data", ""))
                        with base.connect(db_path) as conn:
                            base.migrate(conn)
                            text, keyboard = base._callback_view(
                                conn,
                                user_id,
                                callback_data,
                            )
                            if callback_data.startswith(("sw:cs:manual:f:", "sw:cs:manual:c:")):
                                from .telegram_creator_studio import bind_input_prompt_message

                                bind_input_prompt_message(
                                    conn,
                                    user_id,
                                    int(chat["id"]),
                                    int(message["message_id"]),
                                )
                        base._edit(
                            token,
                            int(chat["id"]),
                            int(message["message_id"]),
                            text,
                            keyboard,
                        )
                    except Exception:
                        try:
                            base._send(
                                token,
                                int(chat["id"]),
                                "Observer action failed safely. The current card was not changed.",
                            )
                        except Exception:
                            pass
                    continue

                message = update.get("message") or {}
                chat = message.get("chat") or {}
                sender = message.get("from") or {}
                text = message.get("text")
                if not text or chat.get("type") != "private":
                    continue
                chat_id = int(chat["id"])
                user_id = int(sender.get("id", chat_id))
                try:
                    reply = base.handle_command(db_path, user_id=user_id, text=text)
                except Exception as exc:
                    reply = f"Observer command failed safely: {type(exc).__name__}"
                command = text.strip().split()[0].split("@", 1)[0].lower() if text.strip() else ""
                keyboard = base._command_keyboard(command)
                _deliver_message_reply(token, chat_id, reply, keyboard)
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError):
            time.sleep(backoff)
            backoff = min(backoff * 2.0, 30.0)


__all__ = ["run_polling"]