from typing import Any

from usa_signal_bot.profiling.profiling_models import (
    ResourceProfile,
    BudgetCalibrationResult,
    ThrottlingRecommendation,
    ThrottlingPlan
)
from usa_signal_bot.core.enums import ThrottlingAction

def adjusted_workload_budget_from_calibration(base_budget: Any, calibration_results: list[BudgetCalibrationResult]) -> Any:
    return base_budget

def apply_throttling_to_local_task(task: Any, recommendations: list[ThrottlingRecommendation]) -> Any:
    task_id = getattr(task, 'task_id', None)
    applicable_recs = [r for r in recommendations if r.task_id == task_id or r.task_id is None]

    if not applicable_recs:
        return task

    for rec in applicable_recs:
        if rec.action == ThrottlingAction.DRY_RUN_ONLY:
            if hasattr(task, 'metadata'):
                task.metadata['throttling_hint'] = 'DRY_RUN_ONLY'

    return task

def taskqueue_budget_hints_from_profiles(profiles: list[ResourceProfile]) -> dict[str, Any]:
    hints = {}
    for p in profiles:
        hints[p.target_name] = {
            "wall_time": p.wall_time_seconds,
            "memory_peak": p.memory_peak_bytes
        }
    return hints

def taskqueue_plan_with_throttling_hints(plan: Any, throttling_plan: ThrottlingPlan) -> Any:
    if hasattr(plan, 'metadata'):
        plan.metadata['throttling_review_count'] = throttling_plan.review_count
        plan.metadata['throttling_warning_count'] = throttling_plan.warning_count

    return plan

def taskqueue_adapter_summary_to_text(summary: dict[str, Any]) -> str:
    lines = ["TaskQueue Adapter Summary:"]
    for k, v in summary.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)
