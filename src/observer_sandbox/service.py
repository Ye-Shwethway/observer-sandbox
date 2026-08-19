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
from .runtime_diagnostics import runtime_logger
from .secrets import load_runtime_secrets
from .sexual_anatomy_physiology_lifecycle import maybe_settle_sexual_anatomy_physiology_lifecycle
from .simulation import snapshot
from .skill_progression import maybe_settle_skill_progression
from .stamina_progression_activation import maybe_settle_stamina_progression
from .strength_progression_activation import maybe_settle_strength_progression
from .telegram_runtime_bot import run_polling
from .telegram_notifications import dispatch_action_completion
from .telegram_profile_notifications import dispatch_profile_change_notifications
from .telegram_sandbox_notifications import dispatch_owner_sandbox_notifications

DB_PATH = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))
RUNNING = True
_LOG = runtime_logger()


def _stop(signum, _frame) -> None:
    global RUNNING
    _LOG.info("service_stop_signal signal=%s", signum)
    RUNNING = False


def _active_actor_ids(conn) -> list[str]:
    return [row[0] for row in conn.execute("SELECT actor_id FROM actor_runtime WHERE autonomy_enabled=1 ORDER BY actor_id").fetchall()]


def _sync_registered_weather(conn, sim_time: str) -> None:
    config = load_weather_provider_config()
    for provider in config.get("providers") or []:
        if not provider.get("enabled", True):
            continue
        try:
            ensure_weather_for_sim_time(conn, sim_time=sim_time, config={"providers": [provider]})
        except Exception:
            _LOG.warning(
                "weather_sync_failed provider=%s sim_time=%s",
                provider.get("id") or provider.get("provider_id") or "unknown",
                sim_time,
                exc_info=True,
            )


def _sync_scheduled_news(conn, sim_time: str) -> None:
    try:
        ensure_historical_tv_news_for_sim_time(conn, sim_time)
    except Exception:
        _LOG.warning("scheduled_news_sync_failed sim_time=%s", sim_time, exc_info=True)


def _autonomy_tick_with_recovery(conn, actor_id: str):
    result = autonomy_tick(conn, actor_id=actor_id)
    if result.get("state") in {"decision_error", "backoff"}:
        _LOG.warning("autonomy_tick_degraded actor_id=%s state=%s", actor_id, result.get("state"))
        recovered = recover_decision_livelock(conn, actor_id)
        if recovered is not None:
            _LOG.info("autonomy_tick_recovered actor_id=%s state=%s", actor_id, recovered.get("state"))
            return recovered
    return result


def _log_recoverable(stage: str, actor_id: str) -> None:
    _LOG.exception("recoverable_runtime_error stage=%s actor_id=%s", stage, actor_id)


def main() -> None:
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    _LOG.info("service_starting db=%s pid=%s", DB_PATH, os.getpid())
    initialize(DB_PATH)
    load_runtime_secrets()

    telegram_thread: threading.Thread | None = None
    if os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip():
        telegram_thread = threading.Thread(target=run_polling, args=(DB_PATH,), name="telegram-observer", daemon=True)
        telegram_thread.start()
        _LOG.info("telegram_polling_thread_started thread=%s", telegram_thread.name)
    else:
        _LOG.warning("telegram_bot_token_absent polling_disabled=true")

    _LOG.info("service_ready pid=%s", os.getpid())
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
                        _LOG.exception("world_sync_boundary_failed actor_id=%s", actor_ids[0])

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
                                target_id=str(pending_before["target"]) if pending_before.get("target") is not None else None,
                                ended_sim_time=str(after["sim_time"]),
                            )
                            conn.commit()
                        except Exception:
                            conn.rollback()
                            _log_recoverable("habit_adaptation", actor_id)

                        try:
                            settle_hobby_interest_lifecycle(
                                conn,
                                actor_id,
                                action_name=str(pending_before["action"]),
                                target_id=str(pending_before["target"]) if pending_before.get("target") is not None else None,
                                ended_sim_time=str(after["sim_time"]),
                            )
                            conn.commit()
                        except Exception:
                            conn.rollback()
                            _log_recoverable("hobby_interest_lifecycle", actor_id)

                        try:
                            settle_preference_adaptation(
                                conn,
                                actor_id,
                                action_name=str(pending_before["action"]),
                                target_id=str(pending_before["target"]) if pending_before.get("target") is not None else None,
                                ended_sim_time=str(after["sim_time"]),
                            )
                            conn.commit()
                        except Exception:
                            conn.rollback()
                            _log_recoverable("preference_adaptation", actor_id)

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
                            _log_recoverable("personality_plasticity", actor_id)

                        for settle in (maybe_settle_strength_progression, maybe_settle_stamina_progression, maybe_settle_agility_progression):
                            try:
                                settle(conn, actor_id, as_of_sim_time=str(after["sim_time"]), state=after)
                                after = snapshot(conn, actor_id)
                            except Exception:
                                _log_recoverable(settle.__name__, actor_id)

                        try:
                            maybe_settle_physical_attribute_batch(conn, actor_id, as_of_sim_time=str(after["sim_time"]), state=after)
                            after = snapshot(conn, actor_id)
                        except Exception:
                            _log_recoverable("physical_attribute_batch", actor_id)

                        try:
                            maybe_settle_height_lifecycle(conn, actor_id, as_of_sim_time=str(after["sim_time"]), state=after)
                            after = snapshot(conn, actor_id)
                        except Exception:
                            _log_recoverable("height_lifecycle", actor_id)

                        try:
                            maybe_settle_body_composition(conn, actor_id, as_of_sim_time=str(after["sim_time"]), state=after)
                            after = snapshot(conn, actor_id)
                        except Exception:
                            _log_recoverable("body_composition", actor_id)

                        try:
                            maybe_settle_body_measurements(conn, actor_id, as_of_sim_time=str(after["sim_time"]), state=after)
                            after = snapshot(conn, actor_id)
                        except Exception:
                            _log_recoverable("body_measurements", actor_id)

                        try:
                            maybe_settle_skill_progression(conn, actor_id, as_of_sim_time=str(after["sim_time"]))
                        except Exception:
                            _log_recoverable("skill_progression", actor_id)

                        try:
                            maybe_settle_sexual_anatomy_physiology_lifecycle(
                                conn,
                                actor_id,
                                as_of_sim_time=str(after["sim_time"]),
                                state=after,
                            )
                            after = snapshot(conn, actor_id)
                        except Exception:
                            _log_recoverable("sexual_anatomy_physiology_lifecycle", actor_id)

                        try:
                            refresh_physical_presentation(conn, actor_id, as_of_sim_time=str(after["sim_time"]))
                        except Exception:
                            _log_recoverable("physical_presentation", actor_id)

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

                dispatch_owner_sandbox_notifications(conn)
        except Exception:
            _LOG.critical("service_loop_fatal", exc_info=True)
            raise
        time.sleep(2)

    _LOG.info("service_stopped_cleanly pid=%s", os.getpid())


if __name__ == "__main__":
    main()
