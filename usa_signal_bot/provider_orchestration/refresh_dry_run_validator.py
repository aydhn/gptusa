from typing import Any
from usa_signal_bot.provider_orchestration.phase110_models import RefreshPlanReport

def validate_refresh_plan_safety(report: RefreshPlanReport) -> list[str]:
    errors = []
    if report.network_allowed_now: errors.append("network_allowed_now must be False")
    if not report.dry_run_only: errors.append("dry_run_only must be True")
    if report.network_used: errors.append("network_used must be False")
    return errors

def refresh_plan_has_network_requirement(report: RefreshPlanReport) -> bool:
    return report.network_allowed_now or report.network_used

def refresh_plan_has_execution_risk(report: RefreshPlanReport) -> bool:
    return not report.dry_run_only

def refresh_dry_run_validator_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors)}

def refresh_dry_run_validator_to_text(errors: list[str]) -> str:
    if not errors: return "Refresh Plan is SAFE (dry-run only)."
    return "Refresh Plan is UNSAFE:\n" + "\n".join(errors)
