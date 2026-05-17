from typing import Any, List, Optional
from .workflow_models import RepairQueueItem, ResearchWorkflowReview
from .repair_queue import create_repair_item_from_failure_assessment
from ..core.enums import RepairItemType

def attach_research_workflow_to_backtest_result(result: dict[str, Any], review: Optional[ResearchWorkflowReview] = None) -> dict[str, Any]:
    if review:
        result["research_workflow"] = {
            "review_id": review.review_id,
            "repair_item_count": len(review.repair_items)
        }
    return result

def backtest_research_items_from_failures(result: dict[str, Any]) -> List[RepairQueueItem]:
    items = []
    failures = result.get("failures", [])
    for failure in failures:
        assessment = {
            "target_name": failure.get("name", "BacktestEntity"),
            "failure_mode": failure.get("reason", "BacktestFailure"),
            "severity": "HIGH",
            "evidence_quality": "HIGH",
            "suggested_remediation": "Investigate backtest parameters"
        }
        item = create_repair_item_from_failure_assessment(assessment)
        item.item_type = RepairItemType.STRATEGY_RULE
        items.append(item)
    return items

def backtest_experiment_plan_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {"status": "BACKTEST_ONLY"}

def backtest_research_workflow_warnings(result: dict[str, Any]) -> List[str]:
    failures = len(result.get("failures", []))
    if failures > 0:
        return [f"Detected {failures} backtest failures that should be converted to repair items."]
    return []
