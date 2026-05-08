from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from pathlib import Path

from usa_signal_bot.regression.regression_models import (
    ReleaseRehearsalResult,
    RegressionRunRequest,
    RegressionRunResult,
    ReleaseCandidateStatus,
    ReleaseRehearsalScope,
    create_release_rehearsal_id,
    RegressionRunStatus,
    RegressionStepStatus
)
from usa_signal_bot.regression.regression_harness import EndToEndRegressionHarness
from usa_signal_bot.regression.regression_store import write_release_rehearsal_result_json, build_release_rehearsal_dir

class ReleaseCandidateRehearsalRunner:
    def __init__(self, data_root: Path, project_root: Optional[Path] = None):
        self.data_root = Path(data_root)
        self.project_root = Path(project_root) if project_root else self.data_root.parent

    def run(self, scope: ReleaseRehearsalScope = ReleaseRehearsalScope.GOLDEN_SAMPLE, update_baseline: bool = False, write_outputs: bool = True) -> ReleaseRehearsalResult:
        rehearsal_id = create_release_rehearsal_id()
        req = self.build_regression_request(scope, update_baseline, write_outputs)

        harness = EndToEndRegressionHarness(self.data_root, self.project_root)
        reg_result = harness.run(req)

        passed = sum(1 for s in reg_result.step_results if s.status == RegressionStepStatus.PASSED)
        warnings = sum(1 for s in reg_result.step_results if s.status == RegressionStepStatus.WARNING)
        failed = sum(1 for s in reg_result.step_results if s.status == RegressionStepStatus.FAILED)
        blocked = sum(1 for s in reg_result.step_results if s.status == RegressionStepStatus.BLOCKED)

        status = reg_result.release_candidate_status
        req_acts = self.build_required_actions(reg_result)
        opt_acts = self.build_optional_actions(reg_result)

        res = ReleaseRehearsalResult(
            rehearsal_id=rehearsal_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            scope=scope,
            status=status,
            regression_result=reg_result,
            passed_steps=passed,
            warning_steps=warnings,
            failed_steps=failed,
            blocked_steps=blocked,
            required_actions=req_acts,
            optional_actions=opt_acts
        )

        if write_outputs:
            self.write_result(res)

        return res

    def build_regression_request(self, scope: ReleaseRehearsalScope, update_baseline: bool, write_outputs: bool) -> RegressionRunRequest:
        import uuid
        return RegressionRunRequest(
            request_id=f"req_{uuid.uuid4().hex[:8]}",
            scope=scope,
            dataset_name="golden_small_us",
            use_existing_golden=True,
            update_baseline=update_baseline,
            compare_snapshots=True,
            write_outputs=write_outputs,
            fail_on_snapshot_drift=False,
            max_allowed_warnings=20
        )

    def build_required_actions(self, regression_result: RegressionRunResult) -> List[str]:
        actions = []
        if regression_result.status in (RegressionRunStatus.FAILED, RegressionRunStatus.BLOCKED):
            actions.append("Fix failing regression steps before attempting a live release.")
        if regression_result.snapshot_comparison.get("status") == "DRIFT" and regression_result.request.fail_on_snapshot_drift:
             actions.append("Investigate and resolve critical snapshot drift, or update baselines if drift is expected.")
        return actions

    def build_optional_actions(self, regression_result: RegressionRunResult) -> List[str]:
        actions = []
        if regression_result.snapshot_comparison.get("status") == "DRIFT" and not regression_result.request.fail_on_snapshot_drift:
             actions.append("Review snapshot drift to ensure changes are intentional.")
        if any(s.status == RegressionStepStatus.WARNING for s in regression_result.step_results):
            actions.append("Review warnings in step results to prevent future failures.")
        return actions

    def write_result(self, result: ReleaseRehearsalResult) -> List[Path]:
        reh_dir = build_release_rehearsal_dir(self.data_root, result.rehearsal_id)
        res_file = write_release_rehearsal_result_json(reh_dir / "rehearsal.json", result)
        result.output_paths["rehearsal_json"] = str(res_file)
        return [res_file]
