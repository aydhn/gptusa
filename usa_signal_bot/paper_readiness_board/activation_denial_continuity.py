
from typing import Any, List, Optional
from usa_signal_bot.core.enums import PaperReadinessBoardRiskFlag
from usa_signal_bot.paper_readiness_board.readiness_board_models import (
    PaperReadinessBoardReview, WriteBlockedRuntimeAdapterProof, ActivationFirewallEvent, PaperReadinessBoardGate
)

def board_activation_denial_flags(payload: dict) -> List[PaperReadinessBoardRiskFlag]:
    flags = []
    if not payload.get("activation_denied", True): flags.append(PaperReadinessBoardRiskFlag.ACTIVATION_DENIAL_MISSING)
    if payload.get("activation_allowed", False): flags.append(PaperReadinessBoardRiskFlag.ACTIVATION_ALLOWED_RISK)
    return flags

def board_activation_denial_is_preserved(payload: dict) -> bool:
    return payload.get("activation_denied", True) and not payload.get("activation_allowed", False)

def validate_board_activation_denial_continuity(board_review: PaperReadinessBoardReview = None, proof: WriteBlockedRuntimeAdapterProof = None, events: List[ActivationFirewallEvent] = None) -> List[str]:
    errs = []
    if board_review and not board_review.activation_denied: errs.append("Review activation_denied is false.")
    if board_review and board_review.activation_allowed: errs.append("Review activation_allowed is true.")
    if proof and not proof.all_writes_blocked: errs.append("Proof writes not blocked.")
    if events and any(not e.blocked for e in events): errs.append("Firewall events not all blocked.")
    return errs

def board_activation_denial_continuity_summary(payload: dict) -> dict:
    return {"preserved": board_activation_denial_is_preserved(payload)}

def board_activation_denial_continuity_to_text(payload: dict) -> str:
    return f"Continuity Preserved: {board_activation_denial_is_preserved(payload)}"

def collect_board_safety_flags(board_review: PaperReadinessBoardReview = None, proof: WriteBlockedRuntimeAdapterProof = None, activation_events: List[ActivationFirewallEvent] = None) -> List[PaperReadinessBoardRiskFlag]:
    flags = []
    if board_review and board_review.activation_allowed: flags.append(PaperReadinessBoardRiskFlag.ACTIVATION_ALLOWED_RISK)
    if proof and not proof.all_writes_blocked: flags.append(PaperReadinessBoardRiskFlag.WRITE_ATTEMPT_NOT_BLOCKED)
    if activation_events and any(not e.blocked for e in activation_events): flags.append(PaperReadinessBoardRiskFlag.ACTIVATION_FIREWALL_BYPASS_RISK)
    return list(set(flags))

def board_has_blocking_flags(flags: List[PaperReadinessBoardRiskFlag]) -> bool:
    return len(flags) > 0

def validate_board_safety(board_review: PaperReadinessBoardReview = None, proof: WriteBlockedRuntimeAdapterProof = None, activation_events: List[ActivationFirewallEvent] = None) -> List[str]:
    flags = collect_board_safety_flags(board_review, proof, activation_events)
    if flags:
        return [f"Safety issue found: {f.value}" for f in flags]
    return []

def board_safety_summary(flags: List[PaperReadinessBoardRiskFlag]) -> dict:
    return {"safe": len(flags) == 0, "flags": [f.value for f in flags]}

def board_safety_validator_to_text(payload: dict) -> str:
    return str(payload)

def analyze_board_confidence(confirmation_payload: dict, gates: List[PaperReadinessBoardGate]) -> dict:
    score = board_confidence_score(confirmation_payload, gates)
    return {
        "score": score,
        "level": board_confidence_level(score, []),
        "evidence_refs": board_evidence_refs(confirmation_payload)
    }

def board_confidence_score(confirmation_payload: dict, gates: List[PaperReadinessBoardGate]) -> Optional[float]:
    if not gates: return 0.0
    passed = sum(1 for g in gates if g.status.value == "PASS")
    return passed / len(gates)

def board_confidence_level(score: Optional[float], flags: List[PaperReadinessBoardRiskFlag]) -> str:
    if flags: return "LOW"
    if score is None: return "UNKNOWN"
    if score >= 0.9: return "HIGH"
    if score >= 0.5: return "MEDIUM"
    return "LOW"

def board_evidence_refs(confirmation_payload: dict) -> List[str]:
    return ["evidence_from_payload"]

def board_missing_evidence(payload: dict) -> List[str]:
    return []

def board_confidence_analyzer_to_text(payload: dict) -> str:
    return str(payload)
