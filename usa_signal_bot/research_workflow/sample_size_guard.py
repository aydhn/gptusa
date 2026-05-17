from typing import Any, List, Optional
from .workflow_models import ResearchHypothesis
from ..core.enums import AcceptanceGateStatus, HypothesisConfidence

def estimate_sample_size_from_evidence_refs(evidence_refs: List[str]) -> Optional[int]:
    # Placeholder for actual extraction logic if evidence refs contain counts
    # If not explicitly parseable, return None
    return len(evidence_refs) if evidence_refs else None

def sample_size_sufficiency_status(sample_size: Optional[int], min_required: int = 30) -> AcceptanceGateStatus:
    if sample_size is None:
        return AcceptanceGateStatus.INSUFFICIENT_DATA
    if sample_size < min_required:
        return AcceptanceGateStatus.WARNING
    return AcceptanceGateStatus.PASS

def build_sample_size_warning(sample_size: Optional[int], min_required: int = 30) -> Optional[str]:
    status = sample_size_sufficiency_status(sample_size, min_required)
    if status == AcceptanceGateStatus.WARNING:
        return f"Low sample size ({sample_size} < {min_required}). Results may not be statistically significant."
    elif status == AcceptanceGateStatus.INSUFFICIENT_DATA:
        return "Insufficient data to estimate sample size."
    return None

def apply_sample_size_guard_to_hypothesis(hypothesis: ResearchHypothesis, sample_size: Optional[int]) -> ResearchHypothesis:
    status = sample_size_sufficiency_status(sample_size)
    if status == AcceptanceGateStatus.WARNING:
        hypothesis.confidence = HypothesisConfidence.LOW
        hypothesis.warnings.append(build_sample_size_warning(sample_size))
    elif status == AcceptanceGateStatus.INSUFFICIENT_DATA:
        hypothesis.confidence = HypothesisConfidence.INSUFFICIENT_EVIDENCE
        hypothesis.warnings.append("Insufficient data to evaluate sample size.")
    return hypothesis

def sample_size_guard_summary(hypotheses: List[ResearchHypothesis]) -> dict[str, Any]:
    low_count = sum(1 for h in hypotheses if h.confidence == HypothesisConfidence.LOW)
    insuf_count = sum(1 for h in hypotheses if h.confidence == HypothesisConfidence.INSUFFICIENT_EVIDENCE)
    return {
        "total_hypotheses": len(hypotheses),
        "low_sample_warnings": low_count,
        "insufficient_data": insuf_count
    }

def sample_size_guard_to_text(payload: dict[str, Any]) -> str:
    return f"Sample Size Guard: {payload['low_sample_warnings']} warnings, {payload['insufficient_data']} insufficient data among {payload['total_hypotheses']} hypotheses."
