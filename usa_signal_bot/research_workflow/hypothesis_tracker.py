from typing import Any, List, Optional
import datetime
from .workflow_models import ResearchHypothesis, RepairQueueItem, create_research_hypothesis_id
from ..core.enums import HypothesisStatus, HypothesisConfidence, ExperimentScope

def create_hypothesis_from_repair_item(item: RepairQueueItem) -> ResearchHypothesis:
    hypothesis_id = create_research_hypothesis_id()
    now_utc = datetime.datetime.utcnow().isoformat() + "Z"

    scope = ExperimentScope.UNKNOWN
    try:
        if item.target_scope:
            scope = ExperimentScope(item.target_scope)
    except ValueError:
        pass

    return ResearchHypothesis(
        hypothesis_id=hypothesis_id,
        created_at_utc=now_utc,
        status=HypothesisStatus.DRAFT,
        confidence=classify_hypothesis_confidence(item.evidence_quality, len(item.evidence_refs)),
        title=f"Hypothesis for {item.title}",
        hypothesis_statement=f"Applying {item.suggested_safe_action} will mitigate {','.join(item.source_failure_modes)}",
        target_scope=scope,
        target_name=item.target_name,
        expected_effect="Improve risk-adjusted performance locally.",
        expected_risk="May overfit to historical data.",
        null_condition="The change yields no statistically significant improvement.",
        success_criteria=["OOS improvement > 0"],
        failure_criteria=["OOS degradation", "Cost drag increased"],
        evidence_refs=item.evidence_refs,
        linked_repair_item_ids=[item.item_id],
        linked_experiment_ids=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def create_hypotheses_from_repair_queue(items: List[RepairQueueItem]) -> List[ResearchHypothesis]:
    return [create_hypothesis_from_repair_item(i) for i in items]

def update_hypothesis_status(hypothesis: ResearchHypothesis, status: HypothesisStatus, rationale: Optional[str] = None) -> ResearchHypothesis:
    hypothesis.status = status
    if rationale:
        hypothesis.metadata["status_change_rationale"] = rationale
    return hypothesis

def classify_hypothesis_confidence(evidence_quality: Optional[str], event_count: Optional[int] = None) -> HypothesisConfidence:
    if event_count is not None and event_count == 0:
        return HypothesisConfidence.INSUFFICIENT_EVIDENCE
    if evidence_quality:
        eq_upper = evidence_quality.upper()
        if eq_upper == "HIGH": return HypothesisConfidence.HIGH
        if eq_upper in ["MODERATE", "MEDIUM"]: return HypothesisConfidence.MODERATE
        if eq_upper == "LOW": return HypothesisConfidence.LOW
    return HypothesisConfidence.UNKNOWN

def hypothesis_ready_for_experiment(hypothesis: ResearchHypothesis) -> bool:
    return hypothesis.status in [HypothesisStatus.DRAFT, HypothesisStatus.READY_FOR_EXPERIMENT] and hypothesis.confidence != HypothesisConfidence.INSUFFICIENT_EVIDENCE

def hypothesis_tracker_summary(hypotheses: List[ResearchHypothesis]) -> dict[str, Any]:
    return {
        "total_hypotheses": len(hypotheses),
        "by_status": {s.value: len([h for h in hypotheses if h.status == s]) for s in HypothesisStatus},
        "by_confidence": {c.value: len([h for h in hypotheses if h.confidence == c]) for c in HypothesisConfidence}
    }

def hypothesis_tracker_to_text(hypotheses: List[ResearchHypothesis], limit: int = 100) -> str:
    summary = hypothesis_tracker_summary(hypotheses)
    lines = [f"Hypothesis Tracker Summary: {summary['total_hypotheses']} items", "-"*40]

    for h in hypotheses[:limit]:
        lines.append(f"[{h.confidence.value}] {h.title} ({h.status.value})")
        lines.append(f"  Statement: {h.hypothesis_statement}")
        lines.append(f"  Null Condition: {h.null_condition}")
        lines.append("")

    if len(hypotheses) > limit:
        lines.append(f"... and {len(hypotheses) - limit} more items.")

    return "\n".join(lines)
