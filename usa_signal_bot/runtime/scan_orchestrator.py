import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import PipelineStepName, PipelineStepStatus, RuntimeRunStatus, RuntimeEventType
from usa_signal_bot.runtime.runtime_models import (
    MarketScanRequest, MarketScanResult, PipelineStepConfig, PipelineStepResult, create_runtime_run_id, validate_market_scan_request
)
from usa_signal_bot.runtime.runtime_events import create_runtime_event, RuntimeEvent
from usa_signal_bot.runtime.runtime_lock import RuntimeLockManager
from usa_signal_bot.runtime.safe_stop import SafeStopManager
from usa_signal_bot.runtime.pipeline_steps import PipelineStepRunner

class MarketScanOrchestrator:
    def __init__(
        self,
        data_root: Path,
        lock_manager: Optional[RuntimeLockManager] = None,
        stop_manager: Optional[SafeStopManager] = None,
        step_runner: Optional[PipelineStepRunner] = None
    ):
        self.data_root = data_root
        self.lock_manager = lock_manager or RuntimeLockManager(data_root / "runtime" / "locks")
        self.stop_manager = stop_manager or SafeStopManager(data_root / "runtime" / "stop.json")
        self.step_runner = step_runner or PipelineStepRunner(data_root)
        self.events: List[RuntimeEvent] = []
        self.fail_on_required = True

    def build_default_step_configs(self, request: MarketScanRequest) -> List[PipelineStepConfig]:

        return [
            PipelineStepConfig(step_name=PipelineStepName.PREFLIGHT, required=True),
            PipelineStepConfig(step_name=PipelineStepName.UNIVERSE_RESOLVE, required=True),
            PipelineStepConfig(step_name=PipelineStepName.DATA_REFRESH, required=False),
            PipelineStepConfig(step_name=PipelineStepName.DATA_READINESS, required=False),
            PipelineStepConfig(step_name=PipelineStepName.FEATURE_PIPELINE, required=True),
            PipelineStepConfig(step_name=PipelineStepName.STRATEGY_RUN, required=True),
            PipelineStepConfig(step_name=PipelineStepName.SIGNAL_SCORING, required=False),
            PipelineStepConfig(step_name=PipelineStepName.SIGNAL_RANKING, required=True),
            PipelineStepConfig(step_name=PipelineStepName.CANDIDATE_SELECTION, required=True),
            PipelineStepConfig(step_name=PipelineStepName.RISK_EVALUATION, required=False),
            PipelineStepConfig(step_name=PipelineStepName.PORTFOLIO_CONSTRUCTION, required=False),
            PipelineStepConfig(step_name=PipelineStepName.SCAN_REPORT, required=True),
            PipelineStepConfig(step_name=PipelineStepName.CLEANUP, required=False),
            PipelineStepConfig(step_name=PipelineStepName.NOTIFICATION, required=False),
        ]

    def build_initial_context(self, request: MarketScanRequest, run_id: str) -> Dict[str, Any]:
        return {
            "run_id": run_id,
            "request": request,
        }

    def should_continue_after_step(self, step_result: PipelineStepResult, step_config: PipelineStepConfig) -> bool:
        if step_result.status in (PipelineStepStatus.COMPLETED, PipelineStepStatus.SKIPPED, PipelineStepStatus.PARTIAL_SUCCESS):
            return True
        if step_config.required and self.fail_on_required:
            return False
        return True

    def finalize_scan_result(self, run_id: str, request: MarketScanRequest, context: Dict[str, Any], step_results: List[PipelineStepResult]) -> MarketScanResult:
        status = RuntimeRunStatus.COMPLETED
        for r in step_results:
            if r.status == PipelineStepStatus.FAILED:
                status = RuntimeRunStatus.PARTIAL_SUCCESS
            elif r.status == PipelineStepStatus.STOPPED:
                status = RuntimeRunStatus.STOPPED

        # If required step failed and we stopped execution
        if status != RuntimeRunStatus.STOPPED:
            if any(r.status == PipelineStepStatus.FAILED and r.step_name in [PipelineStepName.PREFLIGHT, PipelineStepName.FEATURE_PIPELINE] for r in step_results):
                status = RuntimeRunStatus.FAILED

        return MarketScanResult(
            run_id=run_id,
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            request=request,
            status=status,
            resolved_symbols=context.get("resolved_symbols", []),
            step_results=step_results,
            signal_count=0,
            candidate_count=0,
            risk_approved_count=0,
            portfolio_allocation_count=0,
        )

    def write_scan_outputs(self, result: MarketScanResult) -> List[Path]:
        # To be implemented by store logic
        return []

    def run_scan(self, request: MarketScanRequest) -> MarketScanResult:
        validate_market_scan_request(request)
        run_id = create_runtime_run_id()

        lock_info = None
        try:
            lock_info = self.lock_manager.acquire(run_id)
            self.events.append(create_runtime_event(run_id, RuntimeEventType.LOCK_ACQUIRED, "Lock acquired"))

            self.stop_manager.check_or_raise()
            self.events.append(create_runtime_event(run_id, RuntimeEventType.RUN_STARTED, f"Scan {run_id} started"))

            step_configs = self.build_default_step_configs(request)
            context = self.build_initial_context(request, run_id)
            step_results = self.execute_steps(step_configs, context, run_id)

            result = self.finalize_scan_result(run_id, request, context, step_results)

            if request.write_outputs:
                self.write_scan_outputs(result)

            self.events.append(create_runtime_event(run_id, RuntimeEventType.RUN_COMPLETED, f"Scan completed with status {result.status.value}"))
            return result

        except Exception as e:
            self.events.append(create_runtime_event(run_id, RuntimeEventType.RUN_FAILED, str(e), severity="error"))
            return MarketScanResult(
                run_id=run_id,
                created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                request=request,
                status=RuntimeRunStatus.FAILED,
                errors=[str(e)]
            )
        finally:
            if lock_info:
                self.lock_manager.release(lock_info)
                self.events.append(create_runtime_event(run_id, RuntimeEventType.LOCK_RELEASED, "Lock released"))

    def execute_steps(self, step_configs: List[PipelineStepConfig], context: Dict[str, Any], run_id: str) -> List[PipelineStepResult]:
        results = []
        for config in step_configs:
            if not config.enabled:
                continue

            if self.stop_manager.is_stop_requested():
                self.events.append(create_runtime_event(run_id, RuntimeEventType.SAFE_STOP_REQUESTED, "Safe stop detected"))
                stop_res = PipelineStepResult(step_name=config.step_name, status=PipelineStepStatus.STOPPED)
                results.append(stop_res)
                break

            self.events.append(create_runtime_event(run_id, RuntimeEventType.STEP_STARTED, f"Step started: {config.step_name}", step_name=config.step_name))

            res = self.step_runner.run_step(config, context)
            results.append(res)

            if res.status == PipelineStepStatus.FAILED:
                self.events.append(create_runtime_event(run_id, RuntimeEventType.STEP_FAILED, f"Step failed: {config.step_name}", step_name=config.step_name, severity="error"))
            else:
                self.events.append(create_runtime_event(run_id, RuntimeEventType.STEP_COMPLETED, f"Step completed: {config.step_name}", step_name=config.step_name))

            if not self.should_continue_after_step(res, config):
                self.events.append(create_runtime_event(run_id, RuntimeEventType.WARNING, f"Stopping pipeline due to failure in required step: {config.step_name}"))
                break

        return results
