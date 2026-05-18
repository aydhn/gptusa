from typing import Any
from usa_signal_bot.research_governance.governance_models import GovernanceReview, DecisionBoardResult

def attach_governance_to_workflow_review(workflow_payload: dict[str, Any], governance_review: GovernanceReview) -> dict[str, Any]:
    workflow_payload["governance"] = governance_review.governance_review_id
    return workflow_payload

def workflow_governance_summary(workflow_payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def promotion_decisions_to_experiment_status_hints(results: list[DecisionBoardResult]) -> list[dict[str, Any]]:
    return [{"hint": r.final_decision.value} for r in results]

def research_workflow_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Workflow Adapter"
