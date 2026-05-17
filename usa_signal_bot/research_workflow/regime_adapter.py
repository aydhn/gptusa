from typing import Any, List
from .workflow_models import RepairQueueItem, ResearchHypothesis, ExperimentPlan, ResearchWorkflowReview
from .repair_queue import create_repair_item_from_failure_assessment
from .hypothesis_tracker import create_hypothesis_from_repair_item
from .experiment_planner import ControlledExperimentPlanner
from ..core.enums import RepairItemType

def repair_items_from_regime_failures(payload: dict[str, Any]) -> List[RepairQueueItem]:
    items = []
    failures = payload.get("regime_failures", [])
    for failure in failures:
        assessment = {
            "target_name": failure.get("rule_name", "RegimeGate"),
            "failure_mode": failure.get("failure_mode", "RegimeMismatch"),
            "severity": failure.get("severity", "HIGH"),
            "evidence_quality": "HIGH",
            "suggested_remediation": "Adjust regime thresholds"
        }
        item = create_repair_item_from_failure_assessment(assessment)
        item.item_type = RepairItemType.REGIME_GATE
        items.append(item)
    return items

def hypotheses_from_regime_transition_failures(payload: dict[str, Any]) -> List[ResearchHypothesis]:
    items = repair_items_from_regime_failures(payload)
    return [create_hypothesis_from_repair_item(i) for i in items]

def experiment_plans_for_regime_gates(payload: dict[str, Any]) -> List[ExperimentPlan]:
    items = repair_items_from_regime_failures(payload)
    hypotheses = hypotheses_from_regime_transition_failures(payload)
    planner = ControlledExperimentPlanner()
    return planner.plan_experiments_for_hypotheses(hypotheses, items)

def attach_research_workflow_to_regime_review(payload: dict[str, Any], workflow_review: ResearchWorkflowReview) -> dict[str, Any]:
    payload["research_workflow_review_id"] = workflow_review.review_id
    payload["research_workflow_metadata"] = {
        "repair_items": len(workflow_review.repair_items),
        "hypotheses": len(workflow_review.hypotheses)
    }
    return payload

def regime_workflow_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"has_workflow": "research_workflow_review_id" in payload}
