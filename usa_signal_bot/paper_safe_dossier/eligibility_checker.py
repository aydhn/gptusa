from typing import Any, Dict, List
from usa_signal_bot.core.enums import PaperSafeDossierDecision, PaperSafeDossierRiskFlag, PaperSafeDossierStatus
from usa_signal_bot.paper_safe_dossier.paper_safe_ingestion import (
    extract_final_paper_safe_gate,
    extract_boundary_replay_result,
    extract_frozen_evidence_integrity_audit,
    paper_safe_gate_supports_dossier
)

def evaluate_paper_safe_dossier_eligibility(paper_safe_payload: Dict[str, Any]) -> PaperSafeDossierDecision:
    gate = extract_final_paper_safe_gate(paper_safe_payload)
    if not gate:
        return PaperSafeDossierDecision.REQUEST_PAPER_SAFE_GATE_REFRESH

    supports, reasons = paper_safe_gate_supports_dossier(paper_safe_payload)
    if not supports:
        return PaperSafeDossierDecision.BLOCK

    decision = gate.get("decision")
    if decision in ["VALIDATED_PAPER_SAFE", "PASS_TO_PAPER_SAFE_DOSSIER"]:
         return PaperSafeDossierDecision.CREATE_PAPER_SAFE_DOSSIER

    if decision in ["REJECT", "BLOCK"]:
         return PaperSafeDossierDecision.REJECT

    return PaperSafeDossierDecision.INCONCLUSIVE

def paper_safe_dossier_eligibility_reasons(paper_safe_payload: Dict[str, Any]) -> List[str]:
    _, reasons = paper_safe_gate_supports_dossier(paper_safe_payload)
    return reasons

def paper_safe_dossier_safety_flags_from_payload(payload: Dict[str, Any]) -> List[PaperSafeDossierRiskFlag]:
    flags = []
    gate = extract_final_paper_safe_gate(payload)
    if gate:
        if gate.get("activation_allowed", False):
            flags.append(PaperSafeDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
        if gate.get("admission_allowed", False):
            flags.append(PaperSafeDossierRiskFlag.ADMISSION_ALLOWED_RISK)
        if gate.get("order_created", False):
            flags.append(PaperSafeDossierRiskFlag.ORDER_CREATED_RISK)
        if gate.get("mutation_detected", False):
             flags.append(PaperSafeDossierRiskFlag.MUTATION_DETECTED_RISK)

    audit = extract_frozen_evidence_integrity_audit(payload)
    if audit and audit.get("tamper_count", 0) > 0:
        flags.append(PaperSafeDossierRiskFlag.FROZEN_EVIDENCE_TAMPER_RISK)

    return flags

def paper_safe_dossier_status_from_decision(decision: PaperSafeDossierDecision) -> PaperSafeDossierStatus:
    if decision == PaperSafeDossierDecision.CREATE_PAPER_SAFE_DOSSIER:
        return PaperSafeDossierStatus.VALIDATED_PAPER_SAFE
    elif decision == PaperSafeDossierDecision.BLOCK:
        return PaperSafeDossierStatus.BLOCKED
    elif decision == PaperSafeDossierDecision.REJECT:
        return PaperSafeDossierStatus.REJECTED
    elif decision in [PaperSafeDossierDecision.REQUEST_PAPER_SAFE_GATE_REFRESH, PaperSafeDossierDecision.REQUEST_NON_EXECUTION_SEAL_REFRESH, PaperSafeDossierDecision.REQUEST_RUNTIME_MAP_REFRESH, PaperSafeDossierDecision.REQUEST_MANUAL_REVIEW]:
        return PaperSafeDossierStatus.REQUEST_CHANGES
    else:
        return PaperSafeDossierStatus.UNKNOWN

def eligibility_checker_to_text(payload: Dict[str, Any]) -> str:
    decision = evaluate_paper_safe_dossier_eligibility(payload)
    reasons = paper_safe_dossier_eligibility_reasons(payload)
    flags = paper_safe_dossier_safety_flags_from_payload(payload)

    lines = [f"Eligibility Decision: {decision.value}"]
    if reasons:
        lines.append(f"Reasons: {', '.join(reasons)}")
    if flags:
        lines.append(f"Safety Flags: {', '.join([f.value for f in flags])}")
    return "\n".join(lines)
