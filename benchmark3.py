class DummyEnum:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if hasattr(other, 'value'):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)

import sys
from unittest.mock import MagicMock

mock_enums = MagicMock()
mock_enums.CleanupRunStatus.COMPLETED = DummyEnum('COMPLETED')
mock_enums.CleanupRunStatus.PARTIAL_SUCCESS = DummyEnum('PARTIAL_SUCCESS')
mock_enums.CleanupRunStatus.FAILED = DummyEnum('FAILED')
mock_enums.CleanupRunStatus.EMPTY = DummyEnum('EMPTY')
mock_enums.CleanupRunStatus.DRY_RUN_COMPLETED = DummyEnum('DRY_RUN_COMPLETED')

mock_enums.CleanupCandidateStatus.CANDIDATE = DummyEnum('CANDIDATE')
mock_enums.CleanupCandidateStatus.REVIEW_REQUIRED = DummyEnum('REVIEW_REQUIRED')
mock_enums.CleanupCandidateStatus.DELETED = DummyEnum('DELETED')
mock_enums.CleanupCandidateStatus.FAILED = DummyEnum('FAILED')
mock_enums.CleanupCandidateStatus.PROTECTED = DummyEnum('PROTECTED')
mock_enums.CleanupCandidateStatus.SKIPPED = DummyEnum('SKIPPED')

mock_enums.RetentionArtifactType.UNKNOWN = DummyEnum('UNKNOWN')
mock_enums.RetentionPolicyAction.DELETE = DummyEnum('DELETE')

sys.modules['usa_signal_bot.core.enums'] = mock_enums

import time
import os
import shutil
import concurrent.futures
from pathlib import Path
from usa_signal_bot.retention.cleanup_executor import CleanupExecutor
from usa_signal_bot.retention.retention_models import CleanupPlan, CleanupCandidate

def create_dummy_files(data_root, count):
    if data_root.exists():
        shutil.rmtree(data_root)
    data_root.mkdir(parents=True, exist_ok=True)

    candidates = []
    for i in range(count):
        file_path = data_root / f"file_{i}.txt"
        file_path.write_text("dummy content")

        candidates.append(
            CleanupCandidate(
                candidate_id=f"c_{i}",
                artifact_type=mock_enums.RetentionArtifactType.UNKNOWN,
                path=str(file_path),
                size_bytes=13,
                recommended_action=mock_enums.RetentionPolicyAction.DELETE,
                status=mock_enums.CleanupCandidateStatus.CANDIDATE,
                reason="old",
            )
        )
    return candidates

def run_benchmark(count, optimized=False):
    data_root = Path("benchmark_data")
    project_root = Path(".")

    candidates = create_dummy_files(data_root, count)
    plan = CleanupPlan(
        plan_id="p1",
        created_at_utc="now",
        dry_run=False,
        candidates=candidates,
        total_candidate_count=len(candidates),
        total_candidate_size_bytes=len(candidates) * 13,
        protected_count=0,
        delete_candidate_count=len(candidates),
        review_required_count=0,
        warnings=[],
        errors=[]
    )

    executor = CleanupExecutor(data_root, project_root)

    if optimized:
        # Instead of calling execute_candidate in a loop, let's execute in a batch
        # And avoid doing artifact_size_bytes again if we know it or delay the import
        # Wait, the overhead in original execution might be `import artifact_size_bytes` inside a loop!
        original_execute = executor.execute
        def execute_optimized(plan, force=False):
            deleted = []
            skipped = []
            failed = []
            bytes_freed = 0

            # move import outside loop?
            # actually we'll just write our own optimized version
            from usa_signal_bot.retention.artifact_classifier import artifact_size_bytes

            for c in plan.candidates:
                if c.status in (mock_enums.CleanupCandidateStatus.CANDIDATE, mock_enums.CleanupCandidateStatus.REVIEW_REQUIRED):
                    # We can inline execute_candidate or parts of it
                    c_status = c.status
                    if c_status == mock_enums.CleanupCandidateStatus.PROTECTED:
                        c.warnings.append("Skipped protected path")
                        skipped.append(c.path)
                        continue
                    if c_status == mock_enums.CleanupCandidateStatus.REVIEW_REQUIRED and not force:
                        c.warnings.append("Skipped: requires force")
                        c.status = mock_enums.CleanupCandidateStatus.SKIPPED
                        skipped.append(c.path)
                        continue

                    p = Path(c.path)
                    try:
                        # safe_delete_path inline logic to avoid import per file
                        is_safe, reason = executor.verify_path_is_safe_to_delete(p)
                        if not is_safe:
                            raise ValueError(f"Cannot delete unsafe path: {reason}")

                        if not p.exists():
                            freed = 0
                        else:
                            freed = artifact_size_bytes(p)
                            if p.is_file():
                                p.unlink()
                            elif p.is_dir():
                                shutil.rmtree(p)

                        c.status = mock_enums.CleanupCandidateStatus.DELETED
                        deleted.append(c.path)
                        bytes_freed += freed
                    except Exception as e:
                        c.status = mock_enums.CleanupCandidateStatus.FAILED
                        c.errors.append(str(e))
                        failed.append(c.path)
                else:
                    skipped.append(c.path)

            return bytes_freed
        executor.execute = execute_optimized

    start = time.perf_counter()
    executor.execute(plan)
    end = time.perf_counter()

    return end - start

if __name__ == '__main__':
    count = 1000

    baseline_time = run_benchmark(count, optimized=False)
    print(f"Baseline time for {count} files: {baseline_time:.4f}s")

    optimized_time = run_benchmark(count, optimized=True)
    print(f"Optimized time for {count} files: {optimized_time:.4f}s")

    if baseline_time > 0:
        improvement = (baseline_time - optimized_time) / baseline_time * 100
        print(f"Improvement: {improvement:.2f}%")
