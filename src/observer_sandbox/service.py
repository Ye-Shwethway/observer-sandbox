from __future__ import annotations

import os
import signal
import threading
import time
from pathlib import Path

from .actor_runtime import pending_action
from .agility_progression_activation import maybe_settle_agility_progression
from .autonomy_intent import autonomy_tick
from .autonomy_recovery import recover_decision_livelock
from .body_composition_progression import maybe_settle_body_composition
from .body_measurement_progression import maybe_settle_body_measurements
from .db import connect
from .habit_adaptation import settle_habit_adaptation
from .height_lifecycle import maybe_settle_height_lifecycle
from .historical_weather_provider import ensure_weather_for_sim_time, load_weather_provider_config
from .hobby_interest_lifecycle import settle_hobby_interest_lifecycle
from .information_media import ensure_historical_tv_news_for_sim_time
from .personality_plasticity import settle_personality_plasticity
from .physical_attribute_progression import maybe_settle_physical_attribute_batch
from .physical_presentation import refresh_physical_presentation
from .preference_adaptation import settle_preference_adaptation
from .profile_change_observer import capture_profile_change_state, observe_profile_changes
from .runtime import initialize
from .secrets import load_runtime_secrets
from .sexual_anatomy_physiology_lifecycle import maybe_settle_sexual_anatomy_physiology_lifecycle
from .simulation import snapshot
from .skill_progression import maybe_settle_skill_progression
from .stamina_progression_activation import maybe_settle_stamina_progression
from .strength_progression_activation import maybe_settle_strength_progression
from .telegram_runtime_bot import run_polling
from .telegram_notifications import dispatch_action_completion
from .telegram_profile_notifications import dispatch_profile_change_notifications

DB_PATH = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))
RUNNING = True


def _stop(_signum, _frame) -> None:
    global RUNNING
    RUNNING = False


def _active_actor_ids(conn) -> list[str]:
    return [row[0] for row in conn.execute("SELECT actor_id FROM actor_runtime WHERE autonomy_enabled=1 ORDER BY actor_id").fetchall()]


def _sync_registered_weather(conn, sim_time: str) -> None:
    """Synchronize every enabled regional provider against shared universe time.

    Each provider remains independently cached/fallback-isolated by the existing
    Historical Weather Provider contract. A failing region must not block another
    region or character autonomy.
    """
    config = load_weather_provider_config()
    for provider in config.get("providers") or []:
        if not provider.get("enabled", True):
            continue
        try:
            ensure_weather_for_sim_time(
                conn,
                sim_time=sim_time,
                config={"providers": [provider]},
            )
        except Exception:
            continue


def _sync_scheduled_news(conn, sim_time: str) -> None:
    """Materialize the latest due shared-world TV bulletin without character authority."""
    try:
        ensure_historical_tv_news_for_sim_time(conn, sim_time)
    except Exception:
        # External news/editorial failure must never stop world autonomy. The
        # scheduler records a bounded retry state and can recover on a later loop.
        pass


def _autonomy_tick_with_recovery(conn, actor_id: str):
    """Run one autonomy boundary and recover only repeated deterministic livelocks."""
    result = autonomy_tick(conn, actor_id=actor_id)
    if result.get("state") in {"decision_error", "backoff"}:
        recovered = recover_decision_livelock(conn, actor_id)
        if recovered is not None:
            return recovered
    return result


def main() -> None:
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    initialize(DB_PATH)
    load_runtime_secrets()

    telegram_thread: threading.Thread | None = None
    if os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip():
        telegram_thread = threading.Thread(target=run_polling, args=(DB_PATH,), name="telegram-observer", daemon=True)
        telegram_thread.start()

    while RUNNING:
        try:
            with connect(DB_PATH) as conn:
                actor_ids = _active_actor_ids(conn)
                if actor_ids:
                    try:
                        world_now = snapshot(conn, actor_ids[0])
                        world_sim_time = str(world_now["sim_time"])
                        _sync_registered_weather(conn, world_sim_time)
                        _sync_scheduled_news(conn, world_sim_time)
                    except Exception:
                        pass

                for actor_id in actor_ids:
                    pending_before = pending_action(conn, actor_id)
                    before = snapshot(conn, actor_id) if pending_before else None
                    result = _autonomy_tick_with_recovery(conn, actor_id)
                    if result.get("state") == "completed" and pending_before and before:
                        after = result["after"]
                        profile_before = capture_profile_change_state(conn, actor_id)

                        try:
                            settle_habit_adaptation(
                                conn,
                                actor_id,
                                action_name=str(pending_before["action"]),
                                location_id=str(pending_before["place_id"]),
                                target_id=(
                                    str(pending_before["target"])
                                    if pending_before.get("target") is not None
                                    else None
                                ),
                                ended_sim_time=str(after["sim_time"]),
                            )
                            conn.commit()
                        except Exception:
                            conn.rollback()

                        try:
                            settle_hobby_interest_lifecycle(
                                conn,
                                actor_id,
                                action_name=str(pending_before["action"]),
                                target_id=(
                                    str(pending_before["target"])
                                    if pending_before.get("target") is not None
                                    else None
                                ),
                                ended_sim_time=str(after["sim_time"]),
                            )
                            conn.commit()
                        except Exception:
                            conn.rollback()

                        try:
                            settle_preference_adaptation(
                                conn,
                                actor_id,
                                action_name=str(pending_before["action"]),
                                target_id=(
                                    str(pending_before["target"])
                                    if pending_before.get("target") is not None
                                    else None
                                ),
                                ended_sim_time=str(after["sim_time"]),
                            )
                            conn.commit()
                        except Exception:
                            conn.rollback()

                        try:
                            settle_personality_plasticity(
                                conn,
                                actor_id,
                                action_name=str(pending_before["action"]),
                                ended_sim_time=str(after["sim_time"]),
                            )
                            conn.commit()
                        except Exception:
                            conn.rollback()

                        for settle in (maybe_settle_strength_progression, maybe_settle_stamina_progression, maybe_settle_agility_progression):
                            try:
                                settle(conn, actor_id, as_of_sim_time=str(after["sim_time"]), state=after)
                                after = snapshot(conn, actor_id)
                            except Exception:
                                pass

                        try:
                            maybe_settle_physical_attribute_batch(
                                conn,
                                actor_id,
                                as_of_sim_time=str(after["sim_time"]),
                                state=after,
                            )
                            after = snapshot(conn, actor_id)
                        except Exception:
                            pass

                        try:
                            maybe_settle_height_lifecycle(
                                conn,
                                actor_id,
                                as_of_sim_time=str(after["sim_time"]),
                                state=after,
                            )
                            after = snapshot(conn, actor_id)
                        except Exception:
                            pass

                        try:
                            maybe_settle_body_composition(
                                conn,
                                actor_id,
                                as_of_sim_time=str(after["sim_time"]),
                                state=after,
                            )
                            after = snapshot(conn, actor_id)
                        except Exception:
                            pass

                        try:
                            maybe_settle_body_measurements(
                                conn,
                                actor_id,
                                as_of_sim_time=str(after["sim_time"]),
                                state=after,
                            )
                            after = snapshot(conn, actor_id)
                        except Exception:
                            pass

                        try:
                            maybe_settle_skill_progression(
                                conn,
                                actor_id,
                                as_of_sim_time=str(after["sim_time"]),
                            )
                        except Exception:
                            pass

                        try:
                            maybe_settle_sexual_anatomy_physiology_lifecycle(
                                conn,
                                actor_id,
                                as_of_sim_time=str(after["sim_time"]),
                                state=after,
                            )
                            after = snapshot(conn, actor_id)
                        except Exception:
                            pass

                        try:
                            refresh_physical_presentation(
                                conn,
                                actor_id,
                                as_of_sim_time=str(after["sim_time"]),
                            )
                        except Exception:
                            pass

                        profile_after = capture_profile_change_state(conn, actor_id)
                        observe_profile_changes(
                            conn,
                            actor_id,
                            profile_before,
                            profile_after,
                            sim_time=str(after["sim_time"]),
                        )

                        next_result = _autonomy_tick_with_recovery(conn, actor_id)
                        next_pending = next_result.get("pending") if next_result.get("state") == "planned" else None
                        dispatch_action_completion(
                            conn,
                            action_id=str(result["action_id"]),
                            action=pending_before,
                            before=before,
                            after=after,
                            next_action=next_pending,
                        )
                        dispatch_profile_change_notifications(
                            conn,
                            actor_id=actor_id,
                            before=profile_before,
                            current=profile_after,
                            sim_time=str(after["sim_time"]),
                        )
        except Exception:
            raise
        time.sleep(2)


if __name__ == "__main__":
    main()
