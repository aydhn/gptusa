import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    HandoffEvidenceIndex, ReadinessRehearsalRun, FinalReviewLock,
    create_handoff_evidence_index_id, validate_handoff_evidence_index
)

def required_handoff_evidence_types() -> List[str]:
    return [
        "promotion_dossier_review",
        "final_safety_board_review",
        "staged_readiness_package",
        "readiness_rehearsal_run",
        "stage_rehearsal_results",
        "final_review_lock",
        "observer_governance_review",
        "paper_observer_review",
        "controlled_planning_review",
        "observation_review"
    ]

def collect_handoff_available_evidence_types(promotion_payload: Optional[Dict[str, Any]], run: Optional[ReadinessRehearsalRun], lock: Optional[FinalReviewLock]) -> List[str]:
    available = []
    if promotion_payload:
        available.append("promotion_dossier_review")
        if "board_reviews" in promotion_payload and promotion_payload["board_reviews"]:
            available.append("final_safety_board_review")
        if "readiness_packages" in promotion_payload and promotion_payload["readiness_packages"]:
            available.append("staged_readiness_package")
        if "observer_governance_review" in promotion_payload:
            available.append("observer_governance_review")
        if "paper_observer_review" in promotion_payload:
            available.append("paper_observer_review")
        if "controlled_planning_review" in promotion_payload:
            available.append("controlled_planning_review")
        if "observation_review" in promotion_payload:
            available.append("observation_review")

    if run:
        available.append("readiness_rehearsal_run")
        if run.stage_results:
            available.append("stage_rehearsal_results")

    if lock:
        available.append("final_review_lock")

    return available

def collect_handoff_missing_evidence_types(required: List[str], available: List[str]) -> List[str]:
    return [req for req in required if req not in available]

def collect_handoff_stale_evidence_types(payload: Optional[Dict[str, Any]] = None) -> List[str]:
    # Mock stale logic
    return []

def calculate_handoff_evidence_score(required: List[str], available: List[str], stale: List[str]) -> Optional[float]:
    if not required:
        return 100.0
    valid_count = len([a for a in available if a not in stale])
    return (valid_count / len(required)) * 100.0

def build_handoff_evidence_index(promotion_payload: Optional[Dict[str, Any]] = None, run: Optional[ReadinessRehearsalRun] = None, lock: Optional[FinalReviewLock] = None) -> HandoffEvidenceIndex:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    required = required_handoff_evidence_types()
    available = collect_handoff_available_evidence_types(promotion_payload, run, lock)
    missing = collect_handoff_missing_evidence_types(required, available)
    stale = collect_handoff_stale_evidence_types(promotion_payload)
    score = calculate_handoff_evidence_score(required, available, stale)

    candidate_id = None
    if run and run.candidate_id:
        candidate_id = run.candidate_id
    elif lock and lock.candidate_id:
        candidate_id = lock.candidate_id
    elif promotion_payload and "dossiers" in promotion_payload and promotion_payload["dossiers"]:
        candidate_id = promotion_payload["dossiers"][-1].get("candidate_id")

    index = HandoffEvidenceIndex(
        evidence_index_id=create_handoff_evidence_index_id(),
        created_at_utc=now_utc,
        candidate_id=candidate_id,
        required_evidence_types=required,
        available_evidence_types=available,
        missing_evidence_types=missing,
        stale_evidence_types=stale,
        evidence_refs=[],
        evidence_score=score,
        warnings=[],
        errors=[]
    )
    if missing:
        index.warnings.append(f"Missing evidence types: {len(missing)}")
    if stale:
        index.warnings.append(f"Stale evidence types: {len(stale)}")

    validate_handoff_evidence_index(index)
    return index

def handoff_evidence_index_to_text(index: HandoffEvidenceIndex) -> str:
    return f"Handoff Evidence Index: Score {index.evidence_score} | Missing: {len(index.missing_evidence_types)} | Stale: {len(index.stale_evidence_types)}"
