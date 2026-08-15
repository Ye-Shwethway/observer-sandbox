from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .actor_runtime import actor_runtime, migrate_legacy_actor_runtime
from .actor_selection import ensure_default_actor_id, resolve_actor_id
from .ai import seed_builtin_providers
from .composition_schema import seed_action_definitions
from .controlled_h2h_runtime import seed_controlled_h2h_runtime
from .db import connect, get_runtime_state, migrate
from .field_medicine_stabilization import seed_field_medicine_stabilization_runtime
from .inventory import seed_home_inventory
from .profile_schema import seed_profile_field_definitions
from .profile_schema_source_union import seed_source_union_extensions
from .represented_skill_runtime_batch import seed_represented_skill_runtime_batch
from .sexual_state_schema import seed_sexual_state_fields
from .simulation import ensure_sim_clock
from .skill_hierarchy import reconcile_skill_hierarchies
from .skill_practice import seed_skill_practice_foundation
from .skill_progression import maybe_settle_skill_progression
from .tactical_assessment_runtime import seed_tactical_assessment_runtime
from .technology_diagnostic_runtime import seed_technology_diagnostic_runtime
from .world import seed_home_and_darian


@dataclass(slots=True)
class RuntimeStatus:
    healthy: bool
    schema_version: int
    runtime_state: dict[str, object]
    checked_at: str

    def to_dict(self) -> dict[str, object]:
        return {
            "healthy": self.healthy,
            "schema_version": self.schema_version,
            "runtime_state": self.runtime_state,
            "checked_at": self.checked_at,
        }


def _initialize_conn(conn) -> None:
    migrate(conn)
    seed_builtin_providers(conn)
    seed_profile_field_definitions(conn)
    seed_source_union_extensions(conn)
    seed_sexual_state_fields(conn)
    seed_home_and_darian(conn)
    # Canonical character seeds may still contain legacy umbrella Skill keys.
    # Reconcile them immediately into learned component Skills plus derived parent
    # summaries before any progression or cognition surface consumes Skill state.
    reconcile_skill_hierarchies(conn)
    # Stateful inventory migrations emit immutable audit events at simulation
    # time. Establish the canonical clock before inventory seeding so a fresh
    # database and every test/runtime initialization share the same ordering.
    sim_clock = ensure_sim_clock(conn)
    seed_home_inventory(conn)
    seed_action_definitions(conn)
    # Skill-practice semantics own their bounded action definition and
    # purpose-built practice targets. Ordinary use/inspect/research targets are
    # intentionally not reinterpreted as learning evidence.
    seed_skill_practice_foundation(conn)
    # Represented Technology gameplay uses a separate purpose-built target and
    # action. Practice targets are never promoted into application authority.
    seed_technology_diagnostic_runtime(conn)
    # The second represented gameplay exemplar is a distinct Tactical assessment
    # target/action. Existing Tactical training targets remain learning evidence
    # only and are never promoted into application authority.
    seed_tactical_assessment_runtime(conn)
    # Equivalent low-risk applications now enter through one declarative batch
    # runtime. The seeded simulators produce application evidence only; they do
    # not execute movement, consume represented resources, or award Skill XP.
    seed_represented_skill_runtime_batch(conn)
    # Controlled H2H registers reusable action vocabulary only. It deliberately
    # does not fabricate a production sparring partner or session; those must be
    # explicitly represented and authorized in live world state before use.
    seed_controlled_h2h_runtime(conn)
    # Field Medicine stabilization likewise registers only action vocabulary.
    # No casualty, session, casualty state, or medical supplies are fabricated in
    # production merely to exercise the represented consequence foundation.
    seed_field_medicine_stabilization_runtime(conn)
    defaults = {
        "paused": False,
        "speed": 1.0,
        "world_id": "world_observer_universe",
    }
    for key, value in defaults.items():
        conn.execute(
            "INSERT OR IGNORE INTO runtime_state(key, value_json) VALUES(?, ?)",
            (key, json.dumps(value)),
        )
    conn.commit()

    # Activation is cursor-only: existing represented skills bootstrap at the
    # initialization/deploy boundary so historical action evidence cannot become
    # retroactive XP and the first genuinely future practice session is eligible.
    # Repeated initialize/status calls are idempotent after the bootstrap event.
    for row in conn.execute(
        "SELECT entity_id FROM character_profiles WHERE status='active' ORDER BY entity_id"
    ).fetchall():
        maybe_settle_skill_progression(
            conn,
            str(row["entity_id"]),
            as_of_sim_time=sim_clock.isoformat(),
        )

    default_actor_id = ensure_default_actor_id(conn)
    if default_actor_id is not None:
        migrate_legacy_actor_runtime(conn, default_actor_id)


def initialize(db_path: str | Path) -> None:
    with connect(db_path) as conn:
        _initialize_conn(conn)


def status(db_path: str | Path) -> RuntimeStatus:
    with connect(db_path) as conn:
        _initialize_conn(conn)
        version = int(conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0])
        runtime = get_runtime_state(conn)
        default_actor_id = resolve_actor_id(conn)
        default_actor = actor_runtime(conn, default_actor_id)
        # Compatibility projection for operational/readback surfaces. Actor-owned
        # state is authoritative in actor_runtime; these fields are not persisted
        # back into global runtime_state. The projection follows the configured
        # default actor rather than a named-character engine assumption.
        runtime.update({
            "default_actor_id": default_actor_id,
            "autonomy_enabled": default_actor["autonomy_enabled"],
            "autonomy_mode": default_actor["autonomy_mode"],
            "autonomy_pending_action_id": default_actor["pending_action_id"],
            "autonomy_retry": default_actor["retry"],
            "cognition_wake_reason": default_actor["wake_reason"],
            "cognition_wake_stats": default_actor["cognition_stats"],
        })
        return RuntimeStatus(
            healthy=True,
            schema_version=version,
            runtime_state=runtime,
            checked_at=datetime.now(timezone.utc).isoformat(),
        )
