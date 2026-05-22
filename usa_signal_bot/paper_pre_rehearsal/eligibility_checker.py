from typing import Any, Dict, List
from usa_signal_bot.core.enums import PrePaperDryRehearsalDecision, PrePaperRiskFlag, PrePaperDryRehearsalStatus
from usa_signal_bot.paper_pre_rehearsal.final_handoff_ingestion import final_handoff_supports_pre_paper_rehearsal, extract_sealed_archive_manifest, extract_pre_paper_checkpoint

def evaluate_pre_paper_rehearsal_eligibility(final_handoff_payload: Dict[str, Any]) -> PrePaperDryRehearsalDecision:
    supports, warnings = final_handoff_supports_pre_paper_rehearsal(final_handoff_payload)
    if supports:
        if warnings:
            return PrePaperDryRehearsalDecision.INCONCLUSIVE
        return PrePaperDryRehearsalDecision.RUN_GUARDED_PRE_PAPER_DRY_REHEARSAL

    checkpoint = extract_pre_paper_checkpoint(final_handoff_payload)
    if not checkpoint:
        return PrePaperDryRehearsalDecision.REQUEST_FINAL_HANDOFF_REFRESH

    decision = checkpoint.get("decision")
    if decision in ["BLOCKED", "REJECTED"]:
        return PrePaperDryRehearsalDecision.BLOCK

    if not extract_sealed_archive_manifest(final_handoff_payload):
        return PrePaperDryRehearsalDecision.REQUEST_ARCHIVE_INTEGRITY_REFRESH

    return PrePaperDryRehearsalDecision.REQUEST_MANUAL_REVIEW

def pre_paper_rehearsal_eligibility_reasons(final_handoff_payload: Dict[str, Any]) -> List[str]:
    _, warnings = final_handoff_supports_pre_paper_rehearsal(final_handoff_payload)
    return warnings

def pre_paper_safety_flags_from_final_handoff(payload: Dict[str, Any]) -> List[PrePaperRiskFlag]:
    flags = []
    checkpoint = extract_pre_paper_checkpoint(payload)
    if checkpoint:
        flags.extend([PrePaperRiskFlag(f) for f in checkpoint.get("safety_flags", []) if f in [e.value for e in PrePaperRiskFlag]])
    return flags

def pre_paper_status_from_decision(decision: PrePaperDryRehearsalDecision) -> PrePaperDryRehearsalStatus:
    if decision == PrePaperDryRehearsalDecision.RUN_GUARDED_PRE_PAPER_DRY_REHEARSAL:
        return PrePaperDryRehearsalStatus.READY
    elif decision in [PrePaperDryRehearsalDecision.BLOCK, PrePaperDryRehearsalDecision.REJECT]:
        return PrePaperDryRehearsalStatus.BLOCKED
    return PrePaperDryRehearsalStatus.DRAFT

def eligibility_checker_to_text(payload: Dict[str, Any]) -> str:
    decision = evaluate_pre_paper_rehearsal_eligibility(payload)
    reasons = pre_paper_rehearsal_eligibility_reasons(payload)
    return f"Eligibility Decision: {decision.value}, Reasons: {reasons}"
