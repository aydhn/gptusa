from typing import Any, Dict, List
import json
from usa_signal_bot.release.phase159_models import (
    AdvancedAcceptanceInputReference,
    create_advanced_acceptance_input_reference_id,
    generate_timestamp,
    AdvancedAcceptanceInputKind,
    AdvancedAcceptanceRiskFlag
)

def detect_forbidden_advanced_acceptance_fields(payload: Dict[str, Any]) -> List[str]:
    forbidden = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "production_patch",
        "live_signal", "buy_signal", "sell_signal", "target_weight",
        "portfolio_weight", "actual_target_weight", "allocation",
        "actual_allocation", "capital_allocation", "position_size",
        "order_size", "real_order", "telegram_sent"
    ]
    detected = []

    def _search(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k in forbidden:
                    detected.append(k)
                _search(v)
        elif isinstance(d, list):
            for item in d:
                _search(item)

    _search(payload)
    return list(set(detected))

def detect_forbidden_advanced_acceptance_columns(columns: List[str]) -> List[str]:
    forbidden = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "production_patch",
        "live_signal", "buy_signal", "sell_signal", "target_weight",
        "portfolio_weight", "actual_target_weight", "allocation",
        "actual_allocation", "capital_allocation", "position_size",
        "order_size", "real_order", "telegram_sent"
    ]
    return [c for c in columns if c in forbidden]

def build_advanced_acceptance_input_references(payloads: Dict[str, Any]) -> List[AdvancedAcceptanceInputReference]:
    refs = []

    mapping = {
        "full_system_integration_review": AdvancedAcceptanceInputKind.FULL_SYSTEM_INTEGRATION_REVIEW,
        "phase159_readiness_gate": AdvancedAcceptanceInputKind.PHASE159_READINESS_GATE,
        "integration_safety_boundary": AdvancedAcceptanceInputKind.INTEGRATION_SAFETY_BOUNDARY,
        "final_delivery_preparation_checklist": AdvancedAcceptanceInputKind.FINAL_DELIVERY_PREPARATION_CHECKLIST,
        "acceptance_rehearsal_result": AdvancedAcceptanceInputKind.ACCEPTANCE_REHEARSAL_RESULT,
        "system_artifact_inventory": AdvancedAcceptanceInputKind.SYSTEM_ARTIFACT_INVENTORY,
        "integration_dependency_graph": AdvancedAcceptanceInputKind.INTEGRATION_DEPENDENCY_GRAPH,
        "integration_reports": AdvancedAcceptanceInputKind.INTEGRATION_REPORTS,
        "quality_scorecard": AdvancedAcceptanceInputKind.QUALITY_SCORECARD,
        "observability_metrics": AdvancedAcceptanceInputKind.OBSERVABILITY_METRICS,
        "notification_dry_run_report": AdvancedAcceptanceInputKind.NOTIFICATION_DRY_RUN_REPORT
    }

    for key, payload in payloads.items():
        if not payload:
            continue

        kind = mapping.get(key, AdvancedAcceptanceInputKind.UNKNOWN)
        forbidden = detect_forbidden_advanced_acceptance_fields(payload)

        valid = len(forbidden) == 0
        risk_flags = []
        if not valid:
            risk_flags.append(AdvancedAcceptanceRiskFlag.FORBIDDEN_ACCEPTANCE_FIELD)

        ref = AdvancedAcceptanceInputReference(
            input_ref_id=create_advanced_acceptance_input_reference_id(),
            created_at_utc=generate_timestamp(),
            input_kind=kind,
            source_artifact_name=key,
            source_path=None,
            source_hash=None,
            available=True,
            read_only=True,
            required=kind in [AdvancedAcceptanceInputKind.FULL_SYSTEM_INTEGRATION_REVIEW, AdvancedAcceptanceInputKind.PHASE159_READINESS_GATE],
            valid=valid,
            forbidden_fields_detected=forbidden,
            research_data_only=True,
            advanced_acceptance_only=True,
            warnings=[],
            errors=[],
            risk_flags=risk_flags,
            metadata={}
        )
        refs.append(ref)

    return refs

def validate_advanced_acceptance_input_references(items: List[AdvancedAcceptanceInputReference]) -> List[str]:
    errors = []
    has_review = False
    has_gate = False

    for item in items:
        if not item.valid:
            errors.append(f"Input reference {item.input_ref_id} is invalid: forbidden fields {item.forbidden_fields_detected}")
        if item.input_kind == AdvancedAcceptanceInputKind.FULL_SYSTEM_INTEGRATION_REVIEW:
            has_review = True
        if item.input_kind == AdvancedAcceptanceInputKind.PHASE159_READINESS_GATE:
            has_gate = True

    if not has_review:
        errors.append("FULL_SYSTEM_INTEGRATION_REVIEW input is missing")
    if not has_gate:
        errors.append("PHASE159_READINESS_GATE input is missing")

    return errors

def advanced_acceptance_input_resolver_summary(items: List[AdvancedAcceptanceInputReference]) -> Dict[str, Any]:
    return {
        "count": len(items),
        "valid_count": sum(1 for i in items if i.valid),
        "invalid_count": sum(1 for i in items if not i.valid),
        "missing_required": len(validate_advanced_acceptance_input_references(items)) > 0
    }

def advanced_acceptance_input_resolver_to_text(items: List[AdvancedAcceptanceInputReference], limit: int = 300) -> str:
    lines = ["Advanced Acceptance Inputs:"]
    for item in items[:limit]:
        lines.append(f" - {item.source_artifact_name} ({item.input_kind.value}): Valid={item.valid}")
    if len(items) > limit:
        lines.append(f" ... and {len(items) - limit} more.")
    return "\n".join(lines)
