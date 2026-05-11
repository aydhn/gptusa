from typing import List, Optional, Tuple
from datetime import datetime, timezone

from usa_signal_bot.core.enums import SchedulerJobType, SchedulerJobStatus, RunLockScope, SchedulerPlanStatus
from usa_signal_bot.scheduler.scheduler_models import SchedulerJob, SchedulerPlan, create_scheduler_job_id, create_scheduler_plan_id
from usa_signal_bot.scheduler.lock_manager import FileRunLockManager

def default_scheduler_jobs() -> List[SchedulerJob]:
    return [
        SchedulerJob(
            job_id=create_scheduler_job_id("observability-health"),
            job_type=SchedulerJobType.OBSERVABILITY_HEALTH,
            name="observability-health",
            command="python -m usa_signal_bot operational-health",
            scope=RunLockScope.OBSERVABILITY,
            enabled=True,
            status=SchedulerJobStatus.CREATED,
            dry_run=True,
            depends_on=[]
        ),
        SchedulerJob(
            job_id=create_scheduler_job_id("retention-review"),
            job_type=SchedulerJobType.RETENTION_REVIEW,
            name="retention-review",
            command="python -m usa_signal_bot cleanup-dry-run",
            scope=RunLockScope.RETENTION,
            enabled=True,
            status=SchedulerJobStatus.CREATED,
            dry_run=True,
            depends_on=[]
        ),
        SchedulerJob(
            job_id=create_scheduler_job_id("incident-review"),
            job_type=SchedulerJobType.INCIDENT_REVIEW,
            name="incident-review",
            command="python -m usa_signal_bot incident-info",
            scope=RunLockScope.INCIDENT,
            enabled=True,
            status=SchedulerJobStatus.CREATED,
            dry_run=True,
            depends_on=[]
        ),
        SchedulerJob(
            job_id=create_scheduler_job_id("regression-smoke"),
            job_type=SchedulerJobType.REGRESSION_SMOKE,
            name="regression-smoke",
            command="python -m usa_signal_bot smoke",
            scope=RunLockScope.REGRESSION,
            enabled=True,
            status=SchedulerJobStatus.CREATED,
            dry_run=True,
            depends_on=[]
        ),
        SchedulerJob(
            job_id=create_scheduler_job_id("maintenance-check"),
            job_type=SchedulerJobType.MAINTENANCE_CHECK,
            name="maintenance-check",
            command="python -m usa_signal_bot maintenance-review",
            scope=RunLockScope.MAINTENANCE,
            enabled=True,
            status=SchedulerJobStatus.CREATED,
            dry_run=True,
            depends_on=[]
        )
    ]

def build_scheduler_plan(job_types: Optional[List[SchedulerJobType]] = None, dry_run: bool = True, lock_manager: Optional[FileRunLockManager] = None) -> SchedulerPlan:
    now_utc = datetime.now(timezone.utc).isoformat()
    plan_id = create_scheduler_plan_id()

    all_jobs = default_scheduler_jobs()
    if job_types:
        selected_jobs = [j for j in all_jobs if j.job_type in job_types]
    else:
        selected_jobs = all_jobs

    valid, warnings, errors = validate_scheduler_dependencies(selected_jobs)

    status = SchedulerPlanStatus.CREATED
    if errors:
        status = SchedulerPlanStatus.FAILED
    elif not selected_jobs:
        status = SchedulerPlanStatus.EMPTY

    for j in selected_jobs:
        j.dry_run = dry_run
        j.status = SchedulerJobStatus.PLANNED

    return SchedulerPlan(
        plan_id=plan_id,
        created_at_utc=now_utc,
        status=status,
        dry_run=dry_run,
        jobs=selected_jobs,
        warnings=warnings,
        errors=errors
    )

def validate_scheduler_dependencies(jobs: List[SchedulerJob]) -> Tuple[bool, List[str], List[str]]:
    job_ids = {j.name for j in jobs}
    errors = []

    for job in jobs:
        for dep in job.depends_on:
            if dep not in job_ids:
                errors.append(f"Job '{job.name}' depends on '{dep}' which is not in the plan")

    # cycle detection could go here
    if errors:
        return False, [], errors
    return True, [], []

def topological_sort_jobs(jobs: List[SchedulerJob]) -> List[SchedulerJob]:
    # Very simple stub, all default jobs have no dependencies
    return list(jobs)

def scheduler_jobs_to_text(jobs: List[SchedulerJob]) -> str:
    lines = []
    for j in jobs:
        lines.append(f"  - [{j.status.value}] {j.name} (Scope: {j.scope.value}, DryRun: {j.dry_run})")
    return "\n".join(lines)

def scheduler_plan_to_text(plan: SchedulerPlan) -> str:
    lines = [
        f"Scheduler Plan {plan.plan_id} at {plan.created_at_utc}",
        f"Status: {plan.status.value} | DryRun: {plan.dry_run}",
        f"Jobs ({len(plan.jobs)}):",
        scheduler_jobs_to_text(plan.jobs)
    ]
    if plan.errors:
        lines.append("Errors:")
        for e in plan.errors:
            lines.append(f"  - {e}")
    if plan.warnings:
        lines.append("Warnings:")
        for w in plan.warnings:
            lines.append(f"  - {w}")
    return "\n".join(lines)
