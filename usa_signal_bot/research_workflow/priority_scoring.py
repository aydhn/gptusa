from typing import Any, List
from .workflow_models import RepairQueueItem, ResearchHypothesis, ExperimentPlan
from ..core.enums import RepairPriority, ResearchRiskLevel

def score_repair_item_priority(item: RepairQueueItem) -> float:
    score = 0.0
    if item.priority == RepairPriority.CRITICAL: score += 0.40
    elif item.priority == RepairPriority.HIGH: score += 0.25
    elif item.priority == RepairPriority.MEDIUM: score += 0.15
    elif item.priority == RepairPriority.LOW: score += 0.05

    if item.evidence_quality == "HIGH": score += 0.25
    elif item.evidence_quality == "MEDIUM": score += 0.15
    elif item.evidence_quality == "LOW": score -= 0.10

    return min(1.0, max(0.0, score))

def score_hypothesis_priority(hypothesis: ResearchHypothesis) -> float:
    score = 0.0
    if hypothesis.confidence.value == "HIGH": score += 0.40
    elif hypothesis.confidence.value == "MODERATE": score += 0.20
    elif hypothesis.confidence.value == "LOW": score -= 0.10
    elif hypothesis.confidence.value == "INSUFFICIENT_EVIDENCE": score -= 0.30

    if len(hypothesis.evidence_refs) > 2: score += 0.20
    elif len(hypothesis.evidence_refs) > 0: score += 0.10

    return min(1.0, max(0.0, score))

def score_experiment_priority(plan: ExperimentPlan) -> float:
    score = 0.5 # base score
    if plan.risk_level == ResearchRiskLevel.CRITICAL: score -= 0.30
    elif plan.risk_level == ResearchRiskLevel.HIGH: score -= 0.10
    elif plan.risk_level == ResearchRiskLevel.LOW: score += 0.10

    return min(1.0, max(0.0, score))

def priority_score_to_repair_priority(score: float) -> RepairPriority:
    if score >= 0.8: return RepairPriority.CRITICAL
    if score >= 0.5: return RepairPriority.HIGH
    if score >= 0.3: return RepairPriority.MEDIUM
    if score > 0.0: return RepairPriority.LOW
    return RepairPriority.DEFERRED

def priority_scoring_summary(items: List[RepairQueueItem], hypotheses: List[ResearchHypothesis], plans: List[ExperimentPlan]) -> dict[str, Any]:
    return {
        "avg_item_score": sum(score_repair_item_priority(i) for i in items) / len(items) if items else 0.0,
        "avg_hyp_score": sum(score_hypothesis_priority(h) for h in hypotheses) / len(hypotheses) if hypotheses else 0.0,
        "avg_plan_score": sum(score_experiment_priority(p) for p in plans) / len(plans) if plans else 0.0
    }

def priority_scoring_to_text(payload: dict[str, Any]) -> str:
    return (f"Avg Item Score: {payload['avg_item_score']:.2f}\n"
            f"Avg Hyp Score: {payload['avg_hyp_score']:.2f}\n"
            f"Avg Plan Score: {payload['avg_plan_score']:.2f}")
