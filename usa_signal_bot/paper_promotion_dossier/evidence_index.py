from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from .dossier_models import PromotionEvidenceIndex, create_promotion_evidence_index_id
from .observer_governance_ingestion import extract_observer_governance_evidence_refs, extract_observer_governance_candidate_id

def required_promotion_dossier_evidence_types() -> List[str]:
    return [
        "observer_governance_review",
        "observer_vs_paper_comparison",
        "observer_review",
        "controlled_planning_review",
        "observation_review",
        "dry_run_bridge_review",
        "quarantine_review",
        "shadow_governance_review",
        "release_sandbox_review",
        "final_human_approval_queue"
    ]

def build_promotion_evidence_index(observer_governance_payload: Dict[str, Any]) -> PromotionEvidenceIndex:
    candidate_id = extract_observer_governance_candidate_id(observer_governance_payload)
    evidence_refs = extract_observer_governance_evidence_refs(observer_governance_payload)

    required = required_promotion_dossier_evidence_types()
    available = collect_available_evidence_types(observer_governance_payload)
    missing = collect_missing_evidence_types(required, available)
    stale = collect_stale_evidence_types(observer_governance_payload)
    score = calculate_evidence_index_score(required, available, stale)

    warnings = []
    if missing:
        warnings.append("Missing required evidence types.")
    if stale:
        warnings.append("Some evidence is stale.")

    return PromotionEvidenceIndex(
        evidence_index_id=create_promotion_evidence_index_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        evidence_refs=evidence_refs,
        required_evidence_types=required,
        available_evidence_types=available,
        missing_evidence_types=missing,
        stale_evidence_types=stale,
        evidence_score=score,
        warnings=warnings,
        errors=[],
        metadata={"source": "observer_governance"}
    )

def collect_available_evidence_types(payload: Dict[str, Any]) -> List[str]:
    # Mock behavior from payload
    return payload.get("available_evidence_types", ["observer_governance_review"])

def collect_missing_evidence_types(required: List[str], available: List[str]) -> List[str]:
    return [r for r in required if r not in available]

def collect_stale_evidence_types(payload: Dict[str, Any]) -> List[str]:
    return payload.get("stale_evidence_types", [])

def calculate_evidence_index_score(required: List[str], available: List[str], stale: List[str]) -> Optional[float]:
    if not required:
        return 0.0
    valid_available = [a for a in available if a not in stale and a in required]
    return (len(valid_available) / len(required)) * 100.0

def promotion_evidence_index_to_text(index: PromotionEvidenceIndex) -> str:
    return f"Evidence Index {index.evidence_index_id} Score: {index.evidence_score}. Missing: {len(index.missing_evidence_types)}. Stale: {len(index.stale_evidence_types)}."
