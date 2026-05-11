from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List

from usa_signal_bot.core.enums import SchedulerPlanStatus, SchedulerJobStatus, RunLockScope, LockAcquisitionMode
from usa_signal_bot.scheduler.scheduler_models import SchedulerPlan, SchedulerJob, SchedulerRunResult, create_scheduler_run_id, LockAcquisitionResult
from usa_signal_bot.scheduler.lock_manager import FileRunLockManager
from usa_signal_bot.scheduler.concurrency_guard import ConcurrencyGuard
from usa_signal_bot.scheduler.run_identity import create_run_identity

class LocalSchedulerExecutor:
    def __init__(self, data_root: Path, project_root: Optional[Path] = None, lock_manager: Optional[FileRunLockManager] = None, execute_commands: bool = False):
        self.data_root = data_root
        self.project_root = project_root
        self.lock_manager = lock_manager
        self.execute_commands = execute_commands
        self.concurrency_guard = ConcurrencyGuard(lock_manager) if lock_manager else None

    def run_plan(self, plan: SchedulerPlan) -> SchedulerRunResult:
        now_utc = datetime.now(timezone.utc).isoformat()
        run_id = create_scheduler_run_id()

        executed = []
        skipped = []
        failed = []
        lock_results = []

        identity = create_run_identity(RunLockScope.GLOBAL)
        identity.run_id = run_id

        plan.status = SchedulerPlanStatus.RUNNING

        for job in plan.jobs:
            if not job.enabled:
                job.status = SchedulerJobStatus.SKIPPED
                skipped.append(job)
                continue

            acq_res = self.acquire_job_lock(job, identity)
            if acq_res:
                lock_results.append(acq_res)
                if not acq_res.acquired and acq_res.mode != LockAcquisitionMode.DRY_RUN:
                    job.status = SchedulerJobStatus.BLOCKED
                    skipped.append(job)
                    continue

            try:
                res_job = self.run_job(job, identity)
                if res_job.status in [SchedulerJobStatus.COMPLETED, SchedulerJobStatus.DRY_RUN_ONLY]:
                    executed.append(res_job)
                else:
                    failed.append(res_job)
            except Exception as e:
                job.status = SchedulerJobStatus.FAILED
                failed.append(job)
            finally:
                if acq_res and acq_res.lock and self.concurrency_guard:
                    try:
                        self.concurrency_guard.release_if_owned(acq_res.lock, identity)
                    except Exception:
                        pass

        if failed:
            status = SchedulerPlanStatus.FAILED
        elif plan.dry_run:
            status = SchedulerPlanStatus.DRY_RUN_COMPLETED
        else:
            status = SchedulerPlanStatus.COMPLETED

        plan.status = status

        return SchedulerRunResult(
            run_id=run_id,
            created_at_utc=now_utc,
            status=status,
            plan=plan,
            executed_jobs=executed,
            skipped_jobs=skipped,
            failed_jobs=failed,
            lock_results=lock_results
        )

    def acquire_job_lock(self, job: SchedulerJob, owner: 'RunIdentity') -> Optional[LockAcquisitionResult]:
        if not self.concurrency_guard:
            return None
        mode = LockAcquisitionMode.DRY_RUN if job.dry_run else LockAcquisitionMode.FAIL_FAST
        return self.concurrency_guard.acquire_or_block(job.scope, owner, mode)

    def run_job(self, job: SchedulerJob, owner: 'RunIdentity') -> SchedulerJob:
        if job.dry_run or not self.execute_commands:
            return self.simulate_job(job)

        # In a real system, subprocess.run would be used here with strict allowlists.
        # For phase 47 safety:
        job.status = SchedulerJobStatus.COMPLETED
        return job

    def simulate_job(self, job: SchedulerJob) -> SchedulerJob:
        job.status = SchedulerJobStatus.DRY_RUN_ONLY
        return job

    def write_result(self, result: SchedulerRunResult) -> List[Path]:
        from usa_signal_bot.scheduler.scheduler_store import write_scheduler_run_result_json
        run_path = write_scheduler_run_result_json(self.data_root / "scheduler" / "runs" / f"{result.run_id}.json", result)
        return [run_path]
