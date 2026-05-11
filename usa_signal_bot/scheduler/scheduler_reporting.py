from pathlib import Path
from typing import Dict, Any, Optional

from usa_signal_bot.scheduler.scheduler_models import (
    RunIdentity, RunLock, LockAcquisitionResult, ConcurrencyDecisionResult,
    SchedulerJob, SchedulerPlan, SchedulerRunResult
)
from usa_signal_bot.scheduler.stale_lock_detector import StaleLockReport
from usa_signal_bot.scheduler.scheduler_validation import SchedulerValidationReport
from usa_signal_bot.scheduler.atomic_io import atomic_write_text

def run_identity_to_text(identity: RunIdentity) -> str:
    return f"Run: {identity.run_id} | Owner: {identity.owner} | Host: {identity.hostname}:{identity.process_id}"

def run_lock_to_text(lock: RunLock) -> str:
    return f"Lock [{lock.status.value}] Scope: {lock.scope.value} | Owner: {lock.owner.owner} | Acq: {lock.acquired_at_utc}"

def lock_acquisition_result_to_text(result: LockAcquisitionResult) -> str:
    return f"AcqResult [{result.status.value}] Scope: {result.scope.value} | Acquired: {result.acquired} | Mode: {result.mode.value}"

def concurrency_decision_to_text(result: ConcurrencyDecisionResult) -> str:
    return f"Concurrency [{result.decision.value}] Scope: {result.scope.value} | Reason: {result.reason}"

def scheduler_job_to_text(job: SchedulerJob) -> str:
    return f"Job [{job.status.value}] {job.name} (Scope: {job.scope.value}, DryRun: {job.dry_run})"

def scheduler_plan_to_text(plan: SchedulerPlan, limit: int = 50) -> str:
    lines = [
        f"Scheduler Plan {plan.plan_id} at {plan.created_at_utc}",
        f"Status: {plan.status.value} | DryRun: {plan.dry_run}",
        f"Jobs ({len(plan.jobs)}):"
    ]
    for j in plan.jobs[:limit]:
        lines.append(f"  - {scheduler_job_to_text(j)}")
    if len(plan.jobs) > limit:
        lines.append(f"  ... and {len(plan.jobs) - limit} more jobs")

    return "\n".join(lines)

def scheduler_run_result_to_text(result: SchedulerRunResult, limit: int = 50) -> str:
    lines = [
        f"Scheduler Run {result.run_id} at {result.created_at_utc}",
        f"Status: {result.status.value}",
        f"Executed: {len(result.executed_jobs)} | Skipped: {len(result.skipped_jobs)} | Failed: {len(result.failed_jobs)}"
    ]
    if result.executed_jobs:
        lines.append("\nExecuted Jobs:")
        for j in result.executed_jobs[:limit]:
            lines.append(f"  - {scheduler_job_to_text(j)}")
    if result.failed_jobs:
        lines.append("\nFailed Jobs:")
        for j in result.failed_jobs:
            lines.append(f"  - {scheduler_job_to_text(j)}")

    lines.append("\n" + scheduler_limitations_text())
    return "\n".join(lines)

def stale_lock_report_to_text(report: StaleLockReport) -> str:
    from usa_signal_bot.scheduler.stale_lock_detector import stale_lock_report_to_text as _st
    return _st(report)

def scheduler_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return (
        "Scheduler Store Summary:\n"
        f"  - Plans: {summary.get('plans_count', 0)}\n"
        f"  - Runs: {summary.get('runs_count', 0)}\n"
        f"  - Active Locks: {summary.get('locks_count', 0)}"
    )

def scheduler_limitations_text() -> str:
    return (
        "--- SCHEDULER LIMITATIONS ---\n"
        "- This is a LOCAL scheduler only. It does not install system daemons, cron jobs, or services.\n"
        "- NO BROKER execution occurs here. No live or demo orders are generated.\n"
        "- NO Telegram real sends occur from the scheduler by default.\n"
        "- The output of these tasks does NOT constitute investment advice."
    )

def write_scheduler_report_json(path: Path, result: SchedulerRunResult, validation_report: Optional[SchedulerValidationReport] = None) -> Path:
    from usa_signal_bot.scheduler.scheduler_store import write_scheduler_run_result_json
    # Validation report could be bundled if needed, but for now just writing the run result is fine.
    return write_scheduler_run_result_json(path, result)
