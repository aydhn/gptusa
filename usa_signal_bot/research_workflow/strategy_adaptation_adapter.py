from typing import Any, List
from .workflow_models import RepairQueueItem, ResearchHypothesis, ExperimentPlan, ResearchWorkflowReview
from .repair_queue import create_repair_item_from_failure_assessment
from .hypothesis_tracker import create_hypothesis_from_repair_item
from .experiment_planner import ControlledExperimentPlanner
from ..core.enums import RepairItemType

def repair_items_from_strategy_gates(payload: dict[str, Any]) -> List[RepairQueueItem]:
    items = []
    failures = payload.get("strategy_gate_failures", [])
    for failure in failures:
        assessment = {
            "target_name": failure.get("target_strategy", "StrategyRule"),
            "failure_mode": failure.get("failure_mode", "GateFailure"),
            "severity": failure.get("severity", "MEDIUM"),
            "evidence_quality": "HIGH",
            "suggested_remediation": "Review strategy parameters"
        }
        item = create_repair_item_from_failure_assessment(assessment)
        item.item_type = RepairItemType.STRATEGY_RULE
        items.append(item)
    return items

def hypotheses_from_strategy_conflicts(payload: dict[str, Any]) -> List[ResearchHypothesis]:
    items = repair_items_from_strategy_gates(payload)
    return [create_hypothesis_from_repair_item(i) for i in items]

def experiment_plans_for_strategy_gating(payload: dict[str, Any]) -> List[ExperimentPlan]:
    items = repair_items_from_strategy_gates(payload)
    hypotheses = hypotheses_from_strategy_conflicts(payload)
    planner = ControlledExperimentPlanner()
    return planner.plan_experiments_for_hypotheses(hypotheses, items)

def attach_research_workflow_to_strategy_adaptation_review(payload: dict[str, Any], workflow_review: ResearchWorkflowReview) -> dict[str, Any]:
    payload["research_workflow_review_id"] = workflow_review.review_id
    return payload

def strategy_adaptation_workflow_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"has_workflow": "research_workflow_review_id" in payload}
