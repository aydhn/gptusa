from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    RuntimeMapReplayPlan,
    create_runtime_map_replay_plan_id,
    _now_utc_str,
    validate_runtime_map_replay_plan
)
from usa_signal_bot.paper_readiness_non_execution_board.dossier_ingestion import extract_dossier_candidate_id

def required_runtime_replay_component_names() -> List[str]:
    return [
        "market_data_reader",
        "feature_engine_preview",
        "signal_preview_engine",
        "risk_preview_engine",
        "paper_snapshot_reader",
        "notification_preview",
        "audit_reader",
        "validation_runner",
        "paper_state_writer_blocked",
        "paper_order_creator_blocked",
        "broker_sender_blocked",
        "config_patch_blocked",
        "telegram_real_sender_blocked",
        "active_paper_enabler_blocked",
        "paper_admission_gate_blocked"
    ]

def required_runtime_replay_route_names() -> List[str]:
    return [
        "read_market_data_route",
        "read_signal_preview_route",
        "read_risk_preview_route",
        "read_paper_snapshot_route",
        "notification_preview_route",
        "audit_read_route",
        "validation_read_route",
        "paper_state_write_route",
        "paper_order_create_route",
        "broker_order_send_route",
        "config_patch_route",
        "telegram_real_send_route",
        "active_paper_enable_route",
        "paper_admission_route"
    ]

def build_runtime_map_replay_plan(dossier_payload: Dict[str, Any]) -> RuntimeMapReplayPlan:
    candidate_id = extract_dossier_candidate_id(dossier_payload)
    plan = build_default_runtime_map_replay_plan(candidate_id)
    plan.source_dossier_id = dossier_payload.get("dossier_id")

    rmap = dossier_payload.get("pre_paper_local_runtime_maps", [{}])[0] if "pre_paper_local_runtime_maps" in dossier_payload else {}
    plan.source_runtime_map_id = rmap.get("map_id")

    validate_runtime_map_replay_plan(plan)
    return plan

def build_default_runtime_map_replay_plan(candidate_id: Optional[str] = None) -> RuntimeMapReplayPlan:
    plan = RuntimeMapReplayPlan(
        replay_plan_id=create_runtime_map_replay_plan_id(),
        created_at_utc=_now_utc_str(),
        candidate_id=candidate_id,
        source_runtime_map_id=None,
        source_dossier_id=None,
        required_component_names=required_runtime_replay_component_names(),
        required_route_names=required_runtime_replay_route_names(),
        require_all_dangerous_routes_denied=True,
        allow_read_only_routes=True,
        allow_preview_routes=True,
        allow_dry_run_routes=True,
        execution_enabled=False,
        active_paper_enabled=False,
        paper_admission_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[],
        metadata={}
    )
    return plan

def validate_runtime_map_replay_plan_safety(plan: RuntimeMapReplayPlan) -> List[str]:
    errors = []
    if plan.execution_enabled: errors.append("Execution must be disabled")
    if plan.active_paper_enabled: errors.append("Active paper must be disabled")
    if plan.paper_admission_enabled: errors.append("Paper admission must be disabled")
    if plan.broker_execution_enabled: errors.append("Broker execution must be disabled")
    if plan.paper_state_mutation_enabled: errors.append("Paper state mutation must be disabled")
    if plan.config_patch_enabled: errors.append("Config patch must be disabled")
    if plan.telegram_real_send_enabled: errors.append("Telegram real send must be disabled")
    return errors

def runtime_map_replay_plan_summary(plan: RuntimeMapReplayPlan) -> Dict[str, Any]:
    return {
        "id": plan.replay_plan_id,
        "candidate_id": plan.candidate_id,
        "required_components_count": len(plan.required_component_names),
        "required_routes_count": len(plan.required_route_names),
        "safety_errors": validate_runtime_map_replay_plan_safety(plan)
    }

def runtime_map_replay_plan_to_text(plan: RuntimeMapReplayPlan) -> str:
    summary = runtime_map_replay_plan_summary(plan)
    lines = [
        "--- RUNTIME MAP REPLAY PLAN ---",
        f"ID: {plan.replay_plan_id}",
        f"Candidate: {plan.candidate_id}",
        f"Components Required: {summary['required_components_count']}",
        f"Routes Required: {summary['required_routes_count']}"
    ]
    if summary['safety_errors']:
        lines.append("Safety Errors:")
        for e in summary['safety_errors']:
            lines.append(f"  - {e}")
    else:
        lines.append("Safety: OK (All execution disabled)")
    return "\n".join(lines)
