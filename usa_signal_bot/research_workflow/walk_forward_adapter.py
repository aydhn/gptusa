from typing import Any, List, Optional, Dict
from .workflow_models import RepairQueueItem, ResearchWorkflowReview
from .repair_queue import create_repair_item_from_failure_assessment
from ..core.enums import RepairItemType, RepairPriority

def attach_research_workflow_to_walk_forward_result(result: dict[str, Any], reviews_by_window: Optional[Dict[str, ResearchWorkflowReview]] = None) -> dict[str, Any]:
    if reviews_by_window:
        result["research_workflow_windows"] = {k: v.review_id for k, v in reviews_by_window.items()}
    return result

def walk_forward_research_items_from_window_failures(result: dict[str, Any]) -> Dict[str, List[RepairQueueItem]]:
    res = {}
    windows = result.get("windows", {})
    for w_name, w_data in windows.items():
        if w_data.get("oos_failure", False):
            assessment = {
                "target_name": result.get("strategy_id", "WFStrategy"),
                "failure_mode": "OOS_Failure",
                "severity": "HIGH",
                "evidence_quality": "HIGH",
                "suggested_remediation": "Investigate overfit in WF window"
            }
            item = create_repair_item_from_failure_assessment(assessment)
            item.item_type = RepairItemType.STRATEGY_RULE
            item.priority = RepairPriority.HIGH
            res[w_name] = [item]
    return res

def walk_forward_experiment_plan_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {"status": "WALK_FORWARD_ONLY"}

def walk_forward_research_workflow_warnings(result: dict[str, Any]) -> List[str]:
    failures = sum(1 for w in result.get("windows", {}).values() if w.get("oos_failure", False))
    if failures > 0:
        return [f"Detected {failures} OOS failures across walk-forward windows."]
    return []
