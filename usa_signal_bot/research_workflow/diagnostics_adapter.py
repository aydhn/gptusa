from typing import Any, List
from .workflow_models import RepairQueueItem, ResearchHypothesis, ExperimentPlan, ResearchWorkflowReview
from .repair_queue import create_repair_items_from_diagnostics
from .hypothesis_tracker import create_hypotheses_from_repair_queue
from .experiment_planner import ControlledExperimentPlanner

def repair_queue_from_diagnostic_review(diagnostic_payload: dict[str, Any]) -> List[RepairQueueItem]:
    return create_repair_items_from_diagnostics(diagnostic_payload)

def hypotheses_from_diagnostic_review(diagnostic_payload: dict[str, Any]) -> List[ResearchHypothesis]:
    items = repair_queue_from_diagnostic_review(diagnostic_payload)
    return create_hypotheses_from_repair_queue(items)

def experiment_plans_from_diagnostic_review(diagnostic_payload: dict[str, Any]) -> List[ExperimentPlan]:
    planner = ControlledExperimentPlanner()
    items = repair_queue_from_diagnostic_review(diagnostic_payload)
    hypotheses = create_hypotheses_from_repair_queue(items)
    return planner.plan_experiments_for_hypotheses(hypotheses, items)

def attach_research_workflow_to_diagnostics_review(diagnostic_payload: dict[str, Any], workflow_review: ResearchWorkflowReview) -> dict[str, Any]:
    diagnostic_payload["research_workflow"] = {
        "review_id": workflow_review.review_id,
        "repair_item_count": len(workflow_review.repair_items),
        "hypothesis_count": len(workflow_review.hypotheses),
        "experiment_plan_count": len(workflow_review.experiment_plans)
    }
    return diagnostic_payload

def diagnostics_research_workflow_summary(payload: dict[str, Any]) -> dict[str, Any]:
    wf = payload.get("research_workflow", {})
    return {
        "has_workflow": bool(wf),
        "repair_items": wf.get("repair_item_count", 0)
    }

def diagnostics_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = diagnostics_research_workflow_summary(payload)
    if summary["has_workflow"]:
        return f"Diagnostics attached to Research Workflow. Repair Items: {summary['repair_items']}"
    return "No research workflow attached to diagnostics."
