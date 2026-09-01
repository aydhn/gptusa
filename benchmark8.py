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

            # Use ThreadPoolExecutor for I/O bound deletion, but process in batches
            # Let's write the execution in chunks.

            def process_candidate(c):
                # ... same logic ...
                # Actually, ThreadPoolExecutor context startup overhead is real. Let's just create a pool of workers and map the candidate list

                # To maintain original deepcopy behavior?
                updated_c = CleanupCandidate(**{k: v for k, v in c.__dict__.items()})

                if updated_c.status == mock_enums.CleanupCandidateStatus.PROTECTED:
                    updated_c.warnings.append("Skipped protected path")
                    return updated_c, 0

                if updated_c.status == mock_enums.CleanupCandidateStatus.REVIEW_REQUIRED and not force:
                    updated_c.warnings.append("Skipped: requires force")
                    updated_c.status = mock_enums.CleanupCandidateStatus.SKIPPED
                    return updated_c, 0

                p = Path(updated_c.path)
                try:
                    is_safe, reason = executor.verify_path_is_safe_to_delete(p)
                    if not is_safe:
                        raise ValueError(f"Cannot delete unsafe path: {reason}")

                    if not p.exists():
                        return updated_c, 0

                    freed = artifact_size_bytes(p)
                    if p.is_file():
                        p.unlink()
                    elif p.is_dir():
                        shutil.rmtree(p)

                    updated_c.status = mock_enums.CleanupCandidateStatus.DELETED
                    return updated_c, freed
                except Exception as e:
                    updated_c.status = mock_enums.CleanupCandidateStatus.FAILED
                    updated_c.errors.append(str(e))
                    return updated_c, 0

            # Using threads makes it slower in NVMe environments but faster in network/NFS?
            # The prompt mentions: N+1 Issue: Candidate Execution in Loop.
            # "A bulk execute method would be more efficient."

            with concurrent.futures.ThreadPoolExecutor(max_workers=32) as pool:
                # To reduce overhead, we might batch process or just use map

                # Only process valid candidates
                valid_candidates = []
                for c in plan.candidates:
                    if c.status in (mock_enums.CleanupCandidateStatus.CANDIDATE, mock_enums.CleanupCandidateStatus.REVIEW_REQUIRED):
                        valid_candidates.append(c)
                    else:
                        skipped.append(c.path)

                results = pool.map(process_candidate, valid_candidates, chunksize=100)

                for updated_c, freed in results:
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
    count = 2000

    baseline_time = run_benchmark(count, optimized=False)
    print(f"Baseline time for {count} files: {baseline_time:.4f}s")

    optimized_time = run_benchmark(count, optimized=True)
    print(f"Optimized time for {count} files: {optimized_time:.4f}s")

    if baseline_time > 0:
        improvement = (baseline_time - optimized_time) / baseline_time * 100
        print(f"Improvement: {improvement:.2f}%")
