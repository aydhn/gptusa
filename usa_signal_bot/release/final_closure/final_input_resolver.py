from typing import Any, Dict, List, Optional
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalInputReference,
    create_final_input_reference_id,
    generate_timestamp,
    FinalInputKind,
    FinalClosureRiskFlag
)

FORBIDDEN_FIELDS = {
    "broker_order",
    "paper_order",
    "live_order",
    "sent_to_broker",
    "strategy_active",
    "deployment_enabled",
    "production_patch",
    "live_signal",
    "buy_signal",
    "sell_signal",
    "target_weight",
    "portfolio_weight",
    "actual_target_weight",
    "allocation",
    "actual_allocation",
    "capital_allocation",
    "position_size",
    "order_size",
    "real_order",
    "telegram_sent"
}

def detect_forbidden_final_closure_fields(payload: dict[str, Any]) -> List[str]:
    detected = []

    def _search(obj: Any):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in FORBIDDEN_FIELDS:
                    detected.append(k)
                _search(v)
        elif isinstance(obj, list):
            for item in obj:
                _search(item)

    _search(payload)
    return list(set(detected))

def detect_forbidden_final_closure_columns(columns: List[str]) -> List[str]:
    return [c for c in columns if c in FORBIDDEN_FIELDS]

def build_final_input_references(payloads: dict[str, Any]) -> List[FinalInputReference]:
    refs = []

    # Mapping of keys to FinalInputKind
    mapping = {
        "phase160_handoff_package": FinalInputKind.PHASE160_HANDOFF_PACKAGE,
        "final_freeze_certificate": FinalInputKind.FINAL_FREEZE_CERTIFICATE,
        "release_candidate_audit": FinalInputKind.RELEASE_CANDIDATE_AUDIT,
        "release_candidate_risk_register": FinalInputKind.RELEASE_CANDIDATE_RISK_REGISTER,
        "acceptance_evidence_bundle": FinalInputKind.ACCEPTANCE_EVIDENCE_BUNDLE,
        "phase160_readiness_gate": FinalInputKind.PHASE160_READINESS_GATE,
        "advanced_acceptance_full_review": FinalInputKind.ADVANCED_ACCEPTANCE_FULL_REVIEW,
        "final_freeze_boundary": FinalInputKind.FINAL_FREEZE_BOUNDARY,
        "final_freeze_checklist": FinalInputKind.FINAL_FREEZE_CHECKLIST,
    }

    for key, payload in payloads.items():
        kind = mapping.get(key, FinalInputKind.UNKNOWN)
        forbidden = detect_forbidden_final_closure_fields(payload) if isinstance(payload, dict) else []

        valid = len(forbidden) == 0
        risk_flags = [FinalClosureRiskFlag.FORBIDDEN_FINAL_CLOSURE_FIELD] if not valid else []
        errors = ["Forbidden fields detected"] if not valid else []

        ref = FinalInputReference(
            input_ref_id=create_final_input_reference_id(),
            created_at_utc=generate_timestamp(),
            input_kind=kind,
            source_artifact_name=key,
            source_path=None,
            source_hash=None,
            available=True,
            read_only=True,
            required=kind != FinalInputKind.UNKNOWN,
            valid=valid,
            forbidden_fields_detected=forbidden,
            research_data_only=True,
            final_closure_only=True,
            warnings=[],
            errors=errors,
            risk_flags=risk_flags,
            metadata={}
        )
        refs.append(ref)

    return refs

def validate_final_input_references(items: List[FinalInputReference]) -> List[str]:
    errors = []
    for item in items:
        if not item.valid:
            errors.append(f"Input reference {item.source_artifact_name} is invalid due to forbidden fields: {item.forbidden_fields_detected}")
    return errors

def final_input_resolver_summary(items: List[FinalInputReference]) -> Dict[str, Any]:
    return {
        "total_inputs": len(items),
        "valid_inputs": len([i for i in items if i.valid]),
        "invalid_inputs": len([i for i in items if not i.valid])
    }

def final_input_resolver_to_text(items: List[FinalInputReference], limit: int = 300) -> str:
    summary = final_input_resolver_summary(items)
    return f"Final Input Resolver: Total {summary['total_inputs']}, Valid {summary['valid_inputs']}"
