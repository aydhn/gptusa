from typing import Any, Dict, Optional, Tuple
from usa_signal_bot.core.exceptions import PreRehearsalFinalHandoffIngestionError

def ingest_final_handoff_full_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise PreRehearsalFinalHandoffIngestionError("Payload must be a dictionary")
    return payload.copy()

def extract_pre_paper_checkpoint(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("pre_paper_checkpoint")

def extract_sealed_archive_manifest(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("sealed_archive_manifest")

def extract_final_handoff_candidate_id(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("candidate_id")

def extract_pre_paper_checkpoint_decision(payload: Dict[str, Any]) -> Optional[str]:
    checkpoint = extract_pre_paper_checkpoint(payload)
    if checkpoint:
        return checkpoint.get("decision")
    return None

def final_handoff_supports_pre_paper_rehearsal(payload: Dict[str, Any]) -> Tuple[bool, list[str]]:
    warnings = []
    checkpoint = extract_pre_paper_checkpoint(payload)
    if not checkpoint:
        warnings.append("Missing pre_paper_checkpoint")
        return False, warnings

    decision = checkpoint.get("decision")
    if decision != "PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL":
        warnings.append(f"Pre-paper checkpoint decision is not PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL (got {decision})")
        return False, warnings

    archive = extract_sealed_archive_manifest(payload)
    if not archive:
        warnings.append("Missing sealed_archive_manifest")

    return True, warnings

def final_handoff_ingestion_to_text(payload: Dict[str, Any]) -> str:
    candidate_id = extract_final_handoff_candidate_id(payload)
    decision = extract_pre_paper_checkpoint_decision(payload)
    supports, warnings = final_handoff_supports_pre_paper_rehearsal(payload)
    return f"Candidate: {candidate_id}, Decision: {decision}, Supports Pre-Paper: {supports}, Warnings: {warnings}"
