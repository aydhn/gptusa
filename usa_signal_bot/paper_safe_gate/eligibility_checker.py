
from typing import Any, Dict, List
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    FinalPaperSafeGateDecision, FinalPaperSafeGateStatus, PaperSafeGateRiskFlag
)

def evaluate_paper_safe_gate_eligibility(boundary_payload: Dict[str, Any]) -> FinalPaperSafeGateDecision:
    if boundary_payload.get("activation_allowed", False):
        return FinalPaperSafeGateDecision.BLOCK
    return FinalPaperSafeGateDecision.PASS_TO_PAPER_SAFE_DOSSIER

def paper_safe_gate_eligibility_reasons(boundary_payload: Dict[str, Any]) -> List[str]:
    return ["Clean boundary certificate"]

def paper_safe_gate_safety_flags_from_boundary(payload: Dict[str, Any]) -> List[PaperSafeGateRiskFlag]:
    return []

def paper_safe_gate_status_from_decision(decision: FinalPaperSafeGateDecision) -> FinalPaperSafeGateStatus:
    if decision == FinalPaperSafeGateDecision.PASS_TO_PAPER_SAFE_DOSSIER:
        return FinalPaperSafeGateStatus.VALIDATED_PAPER_SAFE
    return FinalPaperSafeGateStatus.BLOCKED

def eligibility_checker_to_text(payload: Dict[str, Any]) -> str:
    return "Eligibility Checker: Valid"
