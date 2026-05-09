import os
import shutil
import datetime
from pathlib import Path
from usa_signal_bot.core.enums import CleanupRunStatus, CleanupCandidateStatus
from usa_signal_bot.retention.retention_models import (
    CleanupPlan, CleanupExecutionResult, CleanupCandidate, create_cleanup_execution_id
)
from usa_signal_bot.retention.protected_paths import is_protected_path

class CleanupExecutor:
    def __init__(self, data_root: Path, project_root: Path | None = None):
        self.data_root = data_root
        self.project_root = project_root

    def verify_path_is_safe_to_delete(self, path: Path) -> tuple[bool, str]:
        try:
            path.resolve().relative_to(self.data_root.resolve())
        except ValueError:
            return False, "Path is outside data_root"

        if is_protected_path(path, self.project_root, self.data_root):
             return False, "Path is protected"

        return True, "Safe"

    def safe_delete_path(self, path: Path, force: bool = False) -> int:
        is_safe, reason = self.verify_path_is_safe_to_delete(path)
        if not is_safe:
            raise ValueError(f"Cannot delete unsafe path: {reason}")

        if not path.exists():
            return 0

        from usa_signal_bot.retention.artifact_classifier import artifact_size_bytes
        size = artifact_size_bytes(path)

        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

        return size

    def execute_candidate(self, candidate: CleanupCandidate, force: bool = False) -> tuple[CleanupCandidate, int]:
        c = CleanupCandidate(**{k: v for k, v in candidate.__dict__.items()})

        if c.status == CleanupCandidateStatus.PROTECTED:
            c.warnings.append("Skipped protected path")
            return c, 0

        if c.status == CleanupCandidateStatus.REVIEW_REQUIRED and not force:
            c.warnings.append("Skipped: requires force")
            c.status = CleanupCandidateStatus.SKIPPED
            return c, 0

        if c.status not in (CleanupCandidateStatus.CANDIDATE, CleanupCandidateStatus.REVIEW_REQUIRED):
            return c, 0

        p = Path(c.path)
        try:
            freed = self.safe_delete_path(p, force)
            c.status = CleanupCandidateStatus.DELETED
            return c, freed
        except Exception as e:
            c.status = CleanupCandidateStatus.FAILED
            c.errors.append(str(e))
            return c, 0

    def execute(self, plan: CleanupPlan, force: bool = False) -> CleanupExecutionResult:
        if plan.dry_run:
            return self.dry_run(plan)

        deleted = []
        skipped = []
        failed = []
        bytes_freed = 0

        for c in plan.candidates:
            if c.status in (CleanupCandidateStatus.CANDIDATE, CleanupCandidateStatus.REVIEW_REQUIRED):
                updated_c, freed = self.execute_candidate(c, force)
                if updated_c.status == CleanupCandidateStatus.DELETED:
                    deleted.append(updated_c.path)
                    bytes_freed += freed
                elif updated_c.status == CleanupCandidateStatus.FAILED:
                    failed.append(updated_c.path)
                else:
                    skipped.append(updated_c.path)
            else:
                 skipped.append(c.path)

        status = CleanupRunStatus.COMPLETED
        if failed:
            status = CleanupRunStatus.PARTIAL_SUCCESS if deleted else CleanupRunStatus.FAILED
        if not deleted and not failed:
            status = CleanupRunStatus.EMPTY

        return CleanupExecutionResult(
            execution_id=create_cleanup_execution_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            status=status,
            dry_run=False,
            plan=plan,
            deleted_paths=deleted,
            skipped_paths=skipped,
            failed_paths=failed,
            bytes_freed=bytes_freed,
            warnings=[],
            errors=[]
        )

    def dry_run(self, plan: CleanupPlan) -> CleanupExecutionResult:
        deleted = []
        skipped = []
        bytes_freed = 0

        for c in plan.candidates:
            if c.status == CleanupCandidateStatus.CANDIDATE:
                deleted.append(c.path)
                bytes_freed += c.size_bytes
            else:
                skipped.append(c.path)

        return CleanupExecutionResult(
            execution_id=create_cleanup_execution_id("dryrun"),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            status=CleanupRunStatus.DRY_RUN_COMPLETED,
            dry_run=True,
            plan=plan,
            deleted_paths=deleted,
            skipped_paths=skipped,
            failed_paths=[],
            bytes_freed=0,
            warnings=[],
            errors=[]
        )
