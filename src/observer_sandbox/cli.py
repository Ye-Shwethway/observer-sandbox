from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .actor_selection import resolve_actor_id
from .ai import (
    configure_provider,
    list_models,
    list_providers,
    nanogpt_subscription_usage,
    refresh_catalog,
    resolve_binding,
    set_binding,
)
from .ai_bootstrap import bootstrap_gemini_cognition, bootstrap_groq_cognition
from .autonomy import (
    autonomy_status,
    run_canary_once,
    set_autonomy_enabled,
    set_autonomy_paused,
    set_autonomy_speed,
)
from .creator_control import restore_basic_stats
from .db import connect, migrate
from .model_decision import dry_run_model_decision
from .runtime import initialize, status
from .simulation import run_one_simulated_day, snapshot

DEFAULT_DB = Path(os.environ.get("OBSERVER_SANDBOX_DB", "runtime-data/observer.sqlite3"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sandboxctl")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    sub.add_parser("living-status")
    sub.add_parser("autonomy-status")
    sub.add_parser("simulate-day")

    autonomy = sub.add_parser("autonomy")
    autonomy_sub = autonomy.add_subparsers(dest="autonomy_command", required=True)
    autonomy_sub.add_parser("status")
    autonomy_sub.add_parser("enable")
    autonomy_sub.add_parser("disable")
    autonomy_sub.add_parser("pause")
    autonomy_sub.add_parser("resume")
    autonomy_sub.add_parser("canary-once")
    speed = autonomy_sub.add_parser("speed")
    speed.add_argument("value", type=float)

    creator = sub.add_parser("creator")
    creator_sub = creator.add_subparsers(dest="creator_command", required=True)
    restore = creator_sub.add_parser("restore-basic-stats")
    restore.add_argument("--character")
    restore.add_argument("--requested-by", default="sandboxctl")

    ai = sub.add_parser("ai")
    ai_sub = ai.add_subparsers(dest="ai_command", required=True)
    ai_sub.add_parser("providers")

    models = ai_sub.add_parser("models")
    models.add_argument("provider")
    refresh = ai_sub.add_parser("refresh")
    refresh.add_argument("provider")

    bootstrap_gemini = ai_sub.add_parser("bootstrap-gemini-cognition")
    bootstrap_gemini.add_argument("--character")
    bootstrap_gemini.add_argument("--role", default="cognition")
    bootstrap_gemini.add_argument("--force", action="store_true")

    bootstrap_groq = ai_sub.add_parser("bootstrap-groq-cognition")
    bootstrap_groq.add_argument("--character")
    bootstrap_groq.add_argument("--role", default="cognition")
    bootstrap_groq.add_argument("--force", action="store_true")

    dry_run = ai_sub.add_parser("dry-run-decision")
    dry_run.add_argument("--character")
    dry_run.add_argument("--role", default="cognition")
    ai_sub.add_parser("nanogpt-usage")

    provider = ai_sub.add_parser("provider")
    provider.add_argument("provider")
    provider.add_argument("--enable", action="store_true")
    provider.add_argument("--disable", action="store_true")
    provider.add_argument("--base-url")
    provider.add_argument("--credential-ref")

    bind = ai_sub.add_parser("bind")
    bind.add_argument("scope_type", choices=["global", "character", "engine", "task"])
    bind.add_argument("scope_id")
    bind.add_argument("role")
    bind.add_argument("provider")
    bind.add_argument("model")
    bind.add_argument("--parameters", default="{}", help="JSON object")

    resolve = ai_sub.add_parser("resolve")
    resolve.add_argument("role")
    resolve.add_argument("--character")
    resolve.add_argument("--engine")
    resolve.add_argument("--task")
    return parser


def _with_db(path: Path):
    conn = connect(path)
    migrate(conn)
    return conn


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "init":
        initialize(args.db)
        print(json.dumps({"ok": True, "db": str(args.db)}))
        return
    if args.command == "status":
        print(json.dumps(status(args.db).to_dict(), indent=2, sort_keys=True))
        return
    if args.command == "living-status":
        initialize(args.db)
        with _with_db(args.db) as conn:
            print(json.dumps(snapshot(conn), indent=2, sort_keys=True))
        return
    if args.command == "autonomy-status":
        initialize(args.db)
        with _with_db(args.db) as conn:
            print(json.dumps(autonomy_status(conn), indent=2, sort_keys=True))
        return
    if args.command == "autonomy":
        initialize(args.db)
        with _with_db(args.db) as conn:
            if args.autonomy_command == "status":
                result = autonomy_status(conn)
            elif args.autonomy_command == "enable":
                result = set_autonomy_enabled(conn, True)
            elif args.autonomy_command == "disable":
                result = set_autonomy_enabled(conn, False)
            elif args.autonomy_command == "pause":
                result = set_autonomy_paused(conn, True)
            elif args.autonomy_command == "resume":
                result = set_autonomy_paused(conn, False)
            elif args.autonomy_command == "speed":
                result = set_autonomy_speed(conn, args.value)
            elif args.autonomy_command == "canary-once":
                result = run_canary_once(conn)
            else:
                raise SystemExit("Unknown autonomy command")
            print(json.dumps(result, indent=2, sort_keys=True))
            if args.autonomy_command == "canary-once" and not result.get("ok", False):
                raise SystemExit(1)
        return
    if args.command == "creator":
        initialize(args.db)
        with _with_db(args.db) as conn:
            if args.creator_command == "restore-basic-stats":
                character_id = resolve_actor_id(conn, args.character)
                result = restore_basic_stats(
                    conn,
                    character_id,
                    authority="creator",
                    requested_by=args.requested_by,
                )
            else:
                raise SystemExit("Unknown Creator command")
            print(json.dumps(result, indent=2, sort_keys=True))
        return
    if args.command == "simulate-day":
        initialize(args.db)
        with _with_db(args.db) as conn:
            before = snapshot(conn)
            trace = run_one_simulated_day(conn)
            after = snapshot(conn)
            print(json.dumps({"ok": True, "actions_completed": len(trace), "started_at": before["sim_time"], "ended_at": after["sim_time"], "final_state": after}, indent=2, sort_keys=True))
        return

    initialize(args.db)
    with _with_db(args.db) as conn:
        if args.ai_command == "providers":
            print(json.dumps(list_providers(conn), indent=2, sort_keys=True))
        elif args.ai_command == "models":
            print(json.dumps(list_models(conn, args.provider), indent=2, sort_keys=True))
        elif args.ai_command == "refresh":
            count = refresh_catalog(conn, args.provider)
            print(json.dumps({"ok": True, "provider": args.provider, "model_count": count}))
        elif args.ai_command == "bootstrap-gemini-cognition":
            result = bootstrap_gemini_cognition(conn, character_id=args.character, role=args.role, force=args.force)
            print(json.dumps(result, indent=2, sort_keys=True))
        elif args.ai_command == "bootstrap-groq-cognition":
            result = bootstrap_groq_cognition(conn, character_id=args.character, role=args.role, force=args.force)
            print(json.dumps(result, indent=2, sort_keys=True))
        elif args.ai_command == "dry-run-decision":
            result = dry_run_model_decision(conn, character_id=args.character, role=args.role)
            print(json.dumps(result, indent=2, sort_keys=True))
        elif args.ai_command == "nanogpt-usage":
            print(json.dumps(nanogpt_subscription_usage(conn), indent=2, sort_keys=True))
        elif args.ai_command == "provider":
            if args.enable and args.disable:
                raise SystemExit("Choose only one of --enable or --disable")
            enabled = True if args.enable else False if args.disable else None
            configure_provider(conn, args.provider, enabled=enabled, base_url=args.base_url, credential_ref=args.credential_ref)
            print(json.dumps({"ok": True, "provider": args.provider}))
        elif args.ai_command == "bind":
            parameters = json.loads(args.parameters)
            if not isinstance(parameters, dict):
                raise SystemExit("--parameters must be a JSON object")
            set_binding(conn, scope_type=args.scope_type, scope_id=args.scope_id, role=args.role, provider_id=args.provider, model_id=args.model, parameters=parameters)
            print(json.dumps({"ok": True, "scope": f"{args.scope_type}:{args.scope_id}", "role": args.role}))
        elif args.ai_command == "resolve":
            binding = resolve_binding(conn, role=args.role, character_id=args.character, engine_id=args.engine, task_id=args.task)
            print(json.dumps(binding, indent=2, sort_keys=True))
