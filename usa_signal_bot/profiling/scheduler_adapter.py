from typing import Any

from usa_signal_bot.core.enums import ResourceProfileScope, ThrottlingAction
from usa_signal_bot.profiling.profiling_models import ThrottlingPlan

def scheduler_hints_from_throttling_plan(plan: ThrottlingPlan) -> dict[str, Any]:
    hints = {
        "delay_scopes": [],
        "dry_run_scopes": [],
        "review_scopes": []
    }

    for rec in plan.recommendations:
        scope_val = rec.scope.value
        if rec.action == ThrottlingAction.DELAY and scope_val not in hints["delay_scopes"]:
            hints["delay_scopes"].append(scope_val)
        elif rec.action == ThrottlingAction.DRY_RUN_ONLY and scope_val not in hints["dry_run_scopes"]:
            hints["dry_run_scopes"].append(scope_val)
        elif rec.action == ThrottlingAction.REVIEW and scope_val not in hints["review_scopes"]:
            hints["review_scopes"].append(scope_val)

    return hints

def annotate_scheduler_plan_with_resource_hints(plan: Any, throttling_plan: ThrottlingPlan) -> Any:
    hints = scheduler_hints_from_throttling_plan(throttling_plan)
    if hasattr(plan, 'metadata'):
        plan.metadata['throttling_hints'] = hints
    return plan

def should_scheduler_delay_scope(scope: ResourceProfileScope, throttling_plan: ThrottlingPlan) -> bool:
    for rec in throttling_plan.recommendations:
        if rec.scope == scope and rec.action in [ThrottlingAction.DELAY, ThrottlingAction.BLOCK]:
            return True
    return False

def scheduler_adapter_summary_to_text(summary: dict[str, Any]) -> str:
    lines = ["Scheduler Adapter Summary:"]
    for k, v in summary.items():
        if isinstance(v, list):
            lines.append(f"  {k}: {', '.join(v) if v else 'None'}")
        else:
            lines.append(f"  {k}: {v}")
    return "\n".join(lines)
