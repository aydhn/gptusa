from typing import Any, Dict, List
from usa_signal_bot.core.enums import ShadowAcceptanceGateType, ShadowAcceptanceStatus
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowAcceptanceGate, create_shadow_acceptance_gate_id

def required_shadow_ledger_event_types() -> List[str]:
    return [
        "SESSION_STARTED", "SIGNAL_PREVIEWED", "CANDIDATE_SELECTED",
        "ORDER_INTENT_CREATED", "RISK_GATE_EVALUATED", "FILL_SIMULATED",
        "PNL_UPDATED", "SESSION_COMPLETED"
    ]

def missing_shadow_ledger_event_types(session_payload: Dict[str, Any]) -> List[str]:
    ledger = session_payload.get("ledger", [])
    found = {e.get("type") for e in ledger}
    req = set(required_shadow_ledger_event_types())
    return list(req - found)

def check_shadow_ledger_completeness(session_payload: Dict[str, Any]) -> Dict[str, Any]:
    missing = missing_shadow_ledger_event_types(session_payload)
    return {
        "missing_types": missing,
        "complete": len(missing) == 0
    }

def ledger_completeness_gate(session_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    comp = check_shadow_ledger_completeness(session_payload)
    status = ShadowAcceptanceStatus.PASS if comp["complete"] else ShadowAcceptanceStatus.FAIL
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.LEDGER_COMPLETE),
        gate_type=ShadowAcceptanceGateType.LEDGER_COMPLETE,
        status=status,
        threshold=0,
        observed_value=len(comp["missing_types"]),
        description="Check if all required shadow ledger events exist",
        risk_flags=[], warnings=[], errors=[]
    )

def ledger_completeness_to_text(payload: Dict[str, Any]) -> str:
    return f"Ledger Complete: {payload.get('complete', False)}"
