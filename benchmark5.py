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
        original_execute = executor.execute
        def execute_optimized(plan, force=False):
            deleted = []
            skipped = []
            failed = []
            bytes_freed = 0

            from usa_signal_bot.retention.artifact_classifier import artifact_size_bytes

            # Use ThreadPoolExecutor for I/O bound deletion
            with concurrent.futures.ThreadPoolExecutor(max_workers=32) as pool:
                def process_candidate(c):
                    if c.status not in (mock_enums.CleanupCandidateStatus.CANDIDATE, mock_enums.CleanupCandidateStatus.REVIEW_REQUIRED):
                        return c, 0

                    if c.status == mock_enums.CleanupCandidateStatus.REVIEW_REQUIRED and not force:
                        c.warnings.append("Skipped: requires force")
                        c.status = mock_enums.CleanupCandidateStatus.SKIPPED
                        return c, 0

                    p = Path(c.path)
                    try:
                        is_safe, reason = executor.verify_path_is_safe_to_delete(p)
                        if not is_safe:
                            raise ValueError(f"Cannot delete unsafe path: {reason}")

                        if not p.exists():
                            return c, 0

                        freed = artifact_size_bytes(p)
                        if p.is_file():
                            p.unlink()
                        elif p.is_dir():
                            shutil.rmtree(p)

                        c.status = mock_enums.CleanupCandidateStatus.DELETED
                        return c, freed
                    except Exception as e:
                        c.status = mock_enums.CleanupCandidateStatus.FAILED
                        c.errors.append(str(e))
                        return c, 0

                futures = []
                for c in plan.candidates:
                    if c.status in (mock_enums.CleanupCandidateStatus.CANDIDATE, mock_enums.CleanupCandidateStatus.REVIEW_REQUIRED):
                        futures.append(pool.submit(process_candidate, c))
                    else:
                        skipped.append(c.path)

                for f in futures:
                    updated_c, freed = f.result()
                    if updated_c.status == mock_enums.CleanupCandidateStatus.DELETED:
                        deleted.append(updated_c.path)
                        bytes_freed += freed
                    elif updated_c.status == mock_enums.CleanupCandidateStatus.FAILED:
                        failed.append(updated_c.path)
                    else:
                        skipped.append(updated_c.path)

            return bytes_freed
        executor.execute = execute_optimized

    start = time.perf_counter()
    executor.execute(plan)
    end = time.perf_counter()

    return end - start

if __name__ == '__main__':
    count = 1000

    # Wait, the problem is process startup overhead with threads in python or simply the fast local nvme disk in the sandbox
    # Let's try 5000 count to see if we can get a meaningful improvement, or use multiprocessing? No, thread is good for I/O.
    # What if we just use a bulk executor without threads, but avoiding deepcopy and imports?
    pass
