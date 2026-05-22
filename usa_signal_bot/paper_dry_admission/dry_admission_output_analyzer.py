from typing import Any, Dict
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    PaperModeDryAdmissionRun,
    DryAdmissionStep
)
from usa_signal_bot.core.enums import DryAdmissionStepStatus

def count_dry_admission_step_statuses(steps: list[DryAdmissionStep]) -> Dict[str, int]:
    counts = {}
    for status in DryAdmissionStepStatus:
        counts[status.value] = sum(1 for s in steps if s.status == status)
    return counts

def count_dry_admission_safety_flags(run: PaperModeDryAdmissionRun) -> Dict[str, int]:
    counts = {}
    for flag in run.safety_flags:
        counts[flag.value] = counts.get(flag.value, 0) + 1
    return counts

def dry_admission_has_write_attempts(run: PaperModeDryAdmissionRun) -> bool:
    if not run.all_writes_blocked or run.mutation_detected:
        return True
    for step in run.steps:
        if step.write_attempted or step.order_attempted or step.broker_send_attempted or step.config_patch_attempted or step.telegram_real_send_attempted or step.active_paper_enable_attempted:
            return True
    return False

def dry_admission_requires_followup(run: PaperModeDryAdmissionRun) -> bool:
    if run.warnings or run.errors:
        return True
    if run.write_lock_refresh and not run.write_lock_refresh.all_writes_blocked:
        return True
    if run.human_ledger and run.human_ledger.missing_scopes:
        return True
    if dry_admission_has_write_attempts(run):
        return True
    return False

def analyze_dry_admission_run(run: PaperModeDryAdmissionRun) -> dict[str, Any]:
    return {
        "run_id": run.run_id,
        "status": run.status.value,
        "decision": run.decision.value,
        "step_status_counts": count_dry_admission_step_statuses(run.steps),
        "safety_flag_counts": count_dry_admission_safety_flags(run),
        "has_write_attempts": dry_admission_has_write_attempts(run),
        "requires_followup": dry_admission_requires_followup(run)
    }

def dry_admission_output_analyzer_to_text(payload: dict[str, Any]) -> str:
    lines = [
        f"Run ID: {payload.get('run_id')}",
        f"Status: {payload.get('status')}",
        f"Decision: {payload.get('decision')}",
        f"Has Write Attempts: {payload.get('has_write_attempts', True)}",
        f"Requires Followup: {payload.get('requires_followup', True)}"
    ]
    return "\n".join(lines)
