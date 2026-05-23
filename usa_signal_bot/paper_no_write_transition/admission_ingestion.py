from typing import Any, Optional
from usa_signal_bot.core.exceptions import NoWriteTransitionAdmissionIngestionError
import json

def ingest_admission_review_full_report(payload: dict[str, Any]) -> dict[str, Any]:
    if not payload:
        raise NoWriteTransitionAdmissionIngestionError("Payload is empty")
    return payload.copy()

def extract_paper_mode_admission_review(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("paper_mode_admission_review")

def extract_final_no_write_transition_checkpoint(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("final_no_write_transition_checkpoint")

def extract_admission_evidence_seal(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("admission_evidence_seal")

def extract_ledger_reconciliation(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("ledger_reconciliation")

def extract_admission_candidate_id(payload: dict[str, Any]) -> Optional[str]:
    return payload.get("candidate_id")

def extract_admission_decision(payload: dict[str, Any]) -> Optional[str]:
    return payload.get("decision")

def admission_review_supports_no_write_transition(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    warnings = []

    if payload.get("activation_allowed") is True:
        warnings.append("activation_allowed is true")
        return False, warnings

    if payload.get("transition_allowed") is True:
        warnings.append("transition_allowed is true")
        return False, warnings

    if payload.get("mutation_detected") is True:
        warnings.append("mutation_detected is true")
        return False, warnings

    if payload.get("all_writes_blocked") is False:
        warnings.append("all_writes_blocked is false")
        return False, warnings

    if not extract_admission_evidence_seal(payload):
        warnings.append("missing admission_evidence_seal")
        return False, warnings

    if not extract_final_no_write_transition_checkpoint(payload):
        warnings.append("missing final_no_write_transition_checkpoint")
        return False, warnings

    decision = extract_admission_decision(payload)
    if decision not in ["PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT", "CONTINUE_TO_NO_WRITE_TRANSITION_DOSSIER"]:
        warnings.append(f"Invalid decision for transition: {decision}")
        return False, warnings

    return True, []

def admission_ingestion_to_text(payload: dict[str, Any]) -> str:
    supports, warnings = admission_review_supports_no_write_transition(payload)
    text = f"Admission Review Ingestion:\n"
    text += f"Candidate ID: {extract_admission_candidate_id(payload)}\n"
    text += f"Decision: {extract_admission_decision(payload)}\n"
    text += f"Supports No-Write Transition: {supports}\n"
    if warnings:
        text += f"Warnings: {', '.join(warnings)}\n"
    return text
