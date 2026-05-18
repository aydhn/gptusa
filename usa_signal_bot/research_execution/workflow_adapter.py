from typing import Any
from usa_signal_bot.research_execution.execution_models import ExperimentRunContext, ExperimentComparisonReport, ResearchExecutionReview
from usa_signal_bot.research_execution.config_snapshot import build_baseline_config_snapshot

def execution_context_from_experiment_plan(plan_payload: dict[str, Any], current_config: dict[str, Any] | None = None) -> ExperimentRunContext:
    if current_config is None:
        current_config = {}
    snap = build_baseline_config_snapshot(current_config)
    from usa_signal_bot.research_execution.run_context import build_baseline_run_context
    return build_baseline_run_context(plan_payload, snap)

def attach_execution_result_to_experiment_plan(plan_payload: dict[str, Any], comparison_report: ExperimentComparisonReport) -> dict[str, Any]:
    import copy
    updated = copy.deepcopy(plan_payload)
    updated["execution_result"] = {
        "report_id": comparison_report.report_id,
        "outcome": comparison_report.outcome.value,
        "baseline_run_id": comparison_report.baseline_run_id,
        "candidate_run_id": comparison_report.candidate_run_id,
    }
    return updated

def attach_execution_review_to_workflow_review(workflow_payload: dict[str, Any], execution_review: ResearchExecutionReview) -> dict[str, Any]:
    import copy
    updated = copy.deepcopy(workflow_payload)
    updated["execution_review"] = {
        "review_id": execution_review.review_id,
        "report_type": execution_review.report_type.value,
        "run_count": len(execution_review.runs)
    }
    return updated

def workflow_execution_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "has_execution_result": "execution_result" in payload,
        "outcome": payload.get("execution_result", {}).get("outcome")
    }

def workflow_adapter_to_text(payload: dict[str, Any]) -> str:
    res = payload.get("execution_result", {})
    return f"--- WORKFLOW ADAPTER ---\nAttached Execution Outcome: {res.get('outcome', 'None')}"
