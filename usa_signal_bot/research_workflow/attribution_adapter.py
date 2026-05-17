from typing import Any, List
from .workflow_models import RepairQueueItem, ResearchHypothesis, ExperimentPlan, ResearchWorkflowReview
from .repair_queue import create_repair_item_from_failure_assessment
from .hypothesis_tracker import create_hypothesis_from_repair_item
from .experiment_planner import ControlledExperimentPlanner
from ..core.enums import RepairItemType, RepairPriority

def repair_items_from_negative_attribution(attribution_payload: dict[str, Any]) -> List[RepairQueueItem]:
    items = []
    negatives = attribution_payload.get("negative_contributors", [])
    for neg in negatives:
        assessment = {
            "target_name": neg.get("name", "AttributionEntity"),
            "failure_mode": "Negative_Attribution",
            "severity": "MEDIUM",
            "evidence_quality": "HIGH",
            "suggested_remediation": "Review signal or parameter weighting"
        }
        item = create_repair_item_from_failure_assessment(assessment)
        item.item_type = RepairItemType.SIGNAL_FILTER
        items.append(item)
    return items

def hypotheses_from_signal_contribution(attribution_payload: dict[str, Any]) -> List[ResearchHypothesis]:
    items = repair_items_from_negative_attribution(attribution_payload)
    return [create_hypothesis_from_repair_item(i) for i in items]

def experiment_plans_from_attribution_review(attribution_payload: dict[str, Any]) -> List[ExperimentPlan]:
    items = repair_items_from_negative_attribution(attribution_payload)
    hypotheses = hypotheses_from_signal_contribution(attribution_payload)
    planner = ControlledExperimentPlanner()
    return planner.plan_experiments_for_hypotheses(hypotheses, items)

def attach_research_workflow_to_attribution_review(attribution_payload: dict[str, Any], workflow_review: ResearchWorkflowReview) -> dict[str, Any]:
    attribution_payload["research_workflow"] = {
        "review_id": workflow_review.review_id,
        "repair_item_count": len(workflow_review.repair_items),
        "hypothesis_count": len(workflow_review.hypotheses),
        "experiment_plan_count": len(workflow_review.experiment_plans)
    }
    return attribution_payload

def attribution_research_workflow_summary(payload: dict[str, Any]) -> dict[str, Any]:
    wf = payload.get("research_workflow", {})
    return {
        "has_workflow": bool(wf),
        "repair_items": wf.get("repair_item_count", 0)
    }

def attribution_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = attribution_research_workflow_summary(payload)
    if summary["has_workflow"]:
        return f"Attribution attached to Research Workflow. Repair Items: {summary['repair_items']}"
    return "No research workflow attached to attribution."
