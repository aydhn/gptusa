import time
import os
import shutil
from pathlib import Path
from usa_signal_bot.retention.cleanup_executor import CleanupExecutor
from usa_signal_bot.retention.retention_models import CleanupPlan, CleanupCandidate
from usa_signal_bot.core.enums import CleanupCandidateStatus, RetentionArtifactType, RetentionPolicyAction
import concurrent.futures

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
                artifact_type=RetentionArtifactType.UNKNOWN,
                path=str(file_path),
                size_bytes=13,
                recommended_action=RetentionPolicyAction.DELETE,
                status=CleanupCandidateStatus.CANDIDATE,
                reason="old",
            )
        )
    return candidates

def run_benchmark(count, use_threads=False):
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

    if use_threads:
        # We will override the executor's execute method temporarily
        original_execute = executor.execute
        def execute_threaded(plan, force=False):
            deleted = []
            skipped = []
            failed = []
            bytes_freed = 0

            with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
                # To maintain original order or handle it simply:
                futures = []
                for c in plan.candidates:
                    if c.status in (CleanupCandidateStatus.CANDIDATE, CleanupCandidateStatus.REVIEW_REQUIRED):
                        futures.append(pool.submit(executor.execute_candidate, c, force))
                    else:
                        futures.append(c)

                for f in futures:
                    if hasattr(f, 'result'):
                        updated_c, freed = f.result()
                        if updated_c.status == CleanupCandidateStatus.DELETED:
                            deleted.append(updated_c.path)
                            bytes_freed += freed
                        elif updated_c.status == CleanupCandidateStatus.FAILED:
                            failed.append(updated_c.path)
                        else:
                            skipped.append(updated_c.path)
                    else:
                        skipped.append(f.path)

            return bytes_freed # Simplified return
        executor.execute = execute_threaded

    start = time.perf_counter()
    executor.execute(plan)
    end = time.perf_counter()

    return end - start

if __name__ == '__main__':
    count = 1000

    # Run once to warm up?

    baseline_time = run_benchmark(count, use_threads=False)
    print(f"Baseline time for {count} files: {baseline_time:.4f}s")

    optimized_time = run_benchmark(count, use_threads=True)
    print(f"Optimized time for {count} files: {optimized_time:.4f}s")

    if baseline_time > 0:
        improvement = (baseline_time - optimized_time) / baseline_time * 100
        print(f"Improvement: {improvement:.2f}%")
