from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from pathlib import Path

from usa_signal_bot.regression.regression_models import (
    RegressionRunRequest,
    RegressionRunResult,
    RegressionStepName,
    RegressionStepStatus,
    RegressionStepResult,
    RegressionRunStatus,
    ReleaseCandidateStatus,
    ReleaseRehearsalScope,
    create_regression_run_id,
    GoldenSnapshot
)
from usa_signal_bot.regression.regression_steps import RegressionStepRunner
from usa_signal_bot.regression.golden_snapshots import compare_golden_snapshots, write_or_update_baseline_snapshot, load_baseline_snapshot
from usa_signal_bot.regression.regression_store import baseline_snapshot_dir, write_regression_run_result_json, build_regression_run_dir

class EndToEndRegressionHarness:
    def __init__(self, data_root: Path, project_root: Optional[Path] = None, step_runner: Optional[RegressionStepRunner] = None):
        self.data_root = Path(data_root)
        self.project_root = Path(project_root) if project_root else self.data_root.parent
        self.step_runner = step_runner or RegressionStepRunner(self.data_root, self.project_root)
        self.baseline_dir = baseline_snapshot_dir(self.data_root)
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

    def run(self, request: RegressionRunRequest) -> RegressionRunResult:
        run_id = create_regression_run_id()
        steps = self.build_step_plan(request)
        context = self.build_initial_context(request, run_id)

        step_results = self.execute_steps(steps, context)
        snapshot_comparison = self.compare_step_snapshots(context, step_results)

        run_status = self.decide_regression_status(step_results, snapshot_comparison, request)
        release_status = self.decide_release_candidate_status(run_status, step_results, snapshot_comparison)

        result = self.build_result(run_id, request, context, step_results, snapshot_comparison)
        result.status = run_status
        result.release_candidate_status = release_status

        if request.write_outputs:
            self.write_result(result)

        return result

    def build_step_plan(self, request: RegressionRunRequest) -> List[RegressionStepName]:
        if request.scope == ReleaseRehearsalScope.SMOKE_ONLY:
            return [
                RegressionStepName.GENERATE_GOLDEN_FIXTURES,
                RegressionStepName.LOAD_GOLDEN_DATASET,
                RegressionStepName.RISK_REHEARSAL,
                RegressionStepName.PAPER_DRY_RUN_REHEARSAL,
                RegressionStepName.QUALITY_GATE_REHEARSAL,
                RegressionStepName.NOTIFICATION_DRY_RUN_REHEARSAL
            ]
        elif request.scope == ReleaseRehearsalScope.GOLDEN_SAMPLE:
            return [
                RegressionStepName.GENERATE_GOLDEN_FIXTURES,
                RegressionStepName.LOAD_GOLDEN_DATASET,
                RegressionStepName.DATA_CACHE_REHEARSAL,
                RegressionStepName.FEATURE_REHEARSAL,
                RegressionStepName.STRATEGY_REHEARSAL,
                RegressionStepName.RANKING_REHEARSAL,
                RegressionStepName.RISK_REHEARSAL,
                RegressionStepName.PORTFOLIO_REHEARSAL,
                RegressionStepName.BASKET_BACKTEST_REHEARSAL,
                RegressionStepName.PAPER_DRY_RUN_REHEARSAL,
                RegressionStepName.PAPER_ANALYTICS_REHEARSAL,
                RegressionStepName.COMPARISON_REHEARSAL,
                RegressionStepName.QUALITY_GATE_REHEARSAL,
                RegressionStepName.NOTIFICATION_DRY_RUN_REHEARSAL,
                RegressionStepName.RELEASE_REHEARSAL_REPORT
            ]
        elif request.scope == ReleaseRehearsalScope.FULL_LOCAL_STACK:
            return [
                RegressionStepName.GENERATE_GOLDEN_FIXTURES,
                RegressionStepName.LOAD_GOLDEN_DATASET,
                RegressionStepName.DATA_CACHE_REHEARSAL,
                RegressionStepName.FEATURE_REHEARSAL,
                RegressionStepName.STRATEGY_REHEARSAL,
                RegressionStepName.RANKING_REHEARSAL,
                RegressionStepName.RISK_REHEARSAL,
                RegressionStepName.PORTFOLIO_REHEARSAL,
                RegressionStepName.BASKET_BACKTEST_REHEARSAL,
                RegressionStepName.PAPER_DRY_RUN_REHEARSAL,
                RegressionStepName.PAPER_ANALYTICS_REHEARSAL,
                RegressionStepName.COMPARISON_REHEARSAL,
                RegressionStepName.QUALITY_GATE_REHEARSAL,
                RegressionStepName.NOTIFICATION_DRY_RUN_REHEARSAL,
                RegressionStepName.SNAPSHOT_COMPARISON,
                RegressionStepName.RELEASE_REHEARSAL_REPORT
            ]
        elif request.scope == ReleaseRehearsalScope.QUALITY_GATE_ONLY:
            return [
                 RegressionStepName.QUALITY_GATE_REHEARSAL
            ]
        return []

    def build_initial_context(self, request: RegressionRunRequest, run_id: str) -> Dict[str, Any]:
        from usa_signal_bot.regression.golden_dataset import GoldenDatasetManager
        mgr = GoldenDatasetManager(self.data_root)
        spec = mgr.default_spec()
        spec.name = request.dataset_name
        return {
            "run_id": run_id,
            "request": request,
            "dataset_name": request.dataset_name,
            "dataset_spec": spec
        }

    def execute_steps(self, steps: List[RegressionStepName], context: Dict[str, Any]) -> List[RegressionStepResult]:
        results = []
        for step in steps:
            res = self.step_runner.run_step(step, context)
            results.append(res)
            if res.status in (RegressionStepStatus.FAILED, RegressionStepStatus.BLOCKED):
                break
        return results

    def compare_step_snapshots(self, context: Dict[str, Any], step_results: List[RegressionStepResult]) -> Dict[str, Any]:
        req: RegressionRunRequest = context["request"]
        if not req.compare_snapshots:
            return {"status": "SKIPPED", "message": "Snapshot comparison disabled by request"}

        comparisons = {}
        for res in step_results:
            if not res.snapshot:
                continue

            baseline = load_baseline_snapshot(self.baseline_dir, res.snapshot.name)
            comp = compare_golden_snapshots(baseline, res.snapshot)
            comparisons[res.snapshot.name] = comp

            if req.update_baseline:
                write_or_update_baseline_snapshot(self.baseline_dir, res.snapshot, update=True)

        drift_count = sum(1 for c in comparisons.values() if c.get("status") == "DRIFT")
        missing_count = sum(1 for c in comparisons.values() if c.get("status") in ("MISSING_BASELINE", "MISSING_CURRENT"))

        status = "MATCH"
        if drift_count > 0:
             status = "DRIFT"
        elif missing_count > 0:
             status = "MISSING_BASELINE"

        return {
            "status": status,
            "comparisons": comparisons,
            "drift_count": drift_count,
            "missing_count": missing_count
        }

    def decide_regression_status(self, step_results: List[RegressionStepResult], snapshot_comparison: Dict[str, Any], request: RegressionRunRequest) -> RegressionRunStatus:
        if not step_results:
             return RegressionRunStatus.EMPTY

        failed = sum(1 for r in step_results if r.status == RegressionStepStatus.FAILED)
        blocked = sum(1 for r in step_results if r.status == RegressionStepStatus.BLOCKED)
        warnings = sum(1 for r in step_results if r.status == RegressionStepStatus.WARNING)

        if blocked > 0:
            return RegressionRunStatus.BLOCKED
        if failed > 0:
            return RegressionRunStatus.FAILED

        if request.fail_on_snapshot_drift and snapshot_comparison.get("status") == "DRIFT":
            return RegressionRunStatus.FAILED

        if warnings > request.max_allowed_warnings:
             return RegressionRunStatus.PARTIAL_SUCCESS

        return RegressionRunStatus.COMPLETED

    def decide_release_candidate_status(self, status: RegressionRunStatus, step_results: List[RegressionStepResult], snapshot_comparison: Dict[str, Any]) -> ReleaseCandidateStatus:
        if status == RegressionRunStatus.COMPLETED:
            if snapshot_comparison.get("status") == "DRIFT":
                 return ReleaseCandidateStatus.PASSED_WITH_WARNINGS
            return ReleaseCandidateStatus.PASSED
        elif status == RegressionRunStatus.PARTIAL_SUCCESS:
            return ReleaseCandidateStatus.PASSED_WITH_WARNINGS
        elif status == RegressionRunStatus.FAILED:
            return ReleaseCandidateStatus.FAILED
        elif status == RegressionRunStatus.BLOCKED:
            return ReleaseCandidateStatus.BLOCKED
        return ReleaseCandidateStatus.UNKNOWN

    def build_result(self, run_id: str, request: RegressionRunRequest, context: Dict[str, Any], step_results: List[RegressionStepResult], snapshot_comparison: Dict[str, Any]) -> RegressionRunResult:
        res = RegressionRunResult(
            run_id=run_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=RegressionRunStatus.NOT_STARTED,
            request=request,
            dataset_spec=context.get("dataset_spec"),
            step_results=step_results,
            snapshot_comparison=snapshot_comparison
        )
        return res

    def write_result(self, result: RegressionRunResult) -> List[Path]:
        run_dir = build_regression_run_dir(self.data_root, result.run_id)
        res_file = write_regression_run_result_json(run_dir / "result.json", result)
        result.output_paths["result_json"] = str(res_file)
        return [res_file]
