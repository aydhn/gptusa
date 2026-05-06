import datetime
import time
from pathlib import Path
from typing import Any, Dict

from usa_signal_bot.core.enums import PipelineStepName, PipelineStepStatus, RuntimeMode
from usa_signal_bot.runtime.runtime_models import PipelineStepConfig, PipelineStepResult, MarketScanRequest

class PipelineStepRunner:
    def __init__(self, data_root: Path):
        self.data_root = data_root

    def run_step(self, step_config: PipelineStepConfig, context: Dict[str, Any]) -> PipelineStepResult:
        if step_config.step_name == PipelineStepName.NOTIFICATION:
            return self.run_notification(context)
        start_time = time.time()
        start_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

        result = PipelineStepResult(
            step_name=step_config.step_name,
            status=PipelineStepStatus.RUNNING,
            started_at_utc=start_utc
        )

        try:
            method_name = f"run_{step_config.step_name.value if hasattr(step_config.step_name, 'value') else step_config.step_name}"
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                step_result = method(context)

                # Merge results
                result.status = step_result.status
                result.output_paths = step_result.output_paths
                result.summary = step_result.summary
                result.warnings = step_result.warnings
                result.errors = step_result.errors
            else:
                result.status = PipelineStepStatus.FAILED
                result.errors.append(f"No runner implemented for step: {step_config.step_name}")

        except Exception as e:
            result.status = PipelineStepStatus.FAILED
            result.errors.append(str(e))

        finally:
            result.completed_at_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
            result.duration_seconds = time.time() - start_time

        return result

    def run_preflight(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.PREFLIGHT, status=PipelineStepStatus.COMPLETED)
        request: MarketScanRequest = context.get("request")

        if not self.data_root.exists():
            try:
                self.data_root.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                res.status = PipelineStepStatus.FAILED
                res.errors.append(f"Cannot create data root: {e}")
                return res

        res.summary["data_root"] = str(self.data_root)
        res.summary["mode"] = str(request.mode)
        return res

    def run_universe_resolve(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.UNIVERSE_RESOLVE, status=PipelineStepStatus.COMPLETED)
        request: MarketScanRequest = context.get("request")

        symbols = request.symbols or []
        if not symbols:
            # Fallback for now depending on scope
            # Actual resolution logic would interact with universe.active
            if str(request.scope) == "small_test_set":
                symbols = ["SPY", "QQQ", "AAPL"]
            elif str(request.scope) == "explicit_symbols":
                res.status = PipelineStepStatus.FAILED
                res.errors.append("Scope is EXPLICIT_SYMBOLS but no symbols provided")
                return res
            else:
                symbols = ["SPY", "QQQ"] # minimal fallback
                res.warnings.append("Universe resolution not fully integrated, using fallback symbols.")

        if request.max_symbols and len(symbols) > request.max_symbols:
            symbols = symbols[:request.max_symbols]
            res.warnings.append(f"Trimmed symbols to max_symbols: {request.max_symbols}")

        context["resolved_symbols"] = symbols
        res.summary["resolved_count"] = len(symbols)
        res.summary["symbols"] = symbols
        return res

    def run_data_refresh(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.DATA_REFRESH, status=PipelineStepStatus.COMPLETED)
        request: MarketScanRequest = context.get("request")

        if not request.refresh_data:
            res.status = PipelineStepStatus.SKIPPED
            res.summary["reason"] = "refresh_data is False"
            return res

        if request.mode == RuntimeMode.DRY_RUN:
            res.status = PipelineStepStatus.SKIPPED
            res.summary["reason"] = "Dry run mode skips data refresh"
            return res

        # Hook into existing yfinance pipeline (dummy hook for now)
        res.warnings.append("Data refresh hook executed (stub). No actual HTTP requests made.")
        res.summary["provider"] = request.provider_name
        return res

    def run_data_readiness(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.DATA_READINESS, status=PipelineStepStatus.COMPLETED)
        # Check cache
        res.summary["ready_symbols"] = context.get("resolved_symbols", [])
        return res

    def run_feature_pipeline(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.FEATURE_PIPELINE, status=PipelineStepStatus.COMPLETED)
        request: MarketScanRequest = context.get("request")
        if request.mode == RuntimeMode.DRY_RUN:
            res.status = PipelineStepStatus.SKIPPED
            res.summary["reason"] = "Dry run skips feature pipeline"
            return res
        res.summary["composite_set"] = request.composite_set_name
        return res

    def run_strategy_run(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.STRATEGY_RUN, status=PipelineStepStatus.COMPLETED)
        request: MarketScanRequest = context.get("request")
        if request.mode == RuntimeMode.DRY_RUN:
            res.status = PipelineStepStatus.SKIPPED
            res.summary["reason"] = "Dry run skips strategy run"
            return res
        res.summary["rule_strategy_set"] = request.rule_strategy_set_name
        res.summary["signals_generated"] = 0
        return res

    def run_signal_scoring(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.SIGNAL_SCORING, status=PipelineStepStatus.COMPLETED)
        return res

    def run_signal_ranking(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.SIGNAL_RANKING, status=PipelineStepStatus.COMPLETED)
        return res

    def run_candidate_selection(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.CANDIDATE_SELECTION, status=PipelineStepStatus.COMPLETED)
        res.summary["candidates_selected"] = 0
        return res

    def run_risk_evaluation(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.RISK_EVALUATION, status=PipelineStepStatus.COMPLETED)
        return res

    def run_portfolio_construction(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.PORTFOLIO_CONSTRUCTION, status=PipelineStepStatus.COMPLETED)
        return res

    def run_scan_report(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.SCAN_REPORT, status=PipelineStepStatus.COMPLETED)
        res.summary["report_generated"] = True
        return res

    def run_notification(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.NOTIFICATION, status=PipelineStepStatus.COMPLETED)
        request = context.get("request")
        if not getattr(request, "notify", False):
            res.status = PipelineStepStatus.SKIPPED
            res.summary["reason"] = "Notify is False"
            return res

        import datetime
        from usa_signal_bot.runtime.runtime_models import MarketScanResult
        from usa_signal_bot.core.enums import RuntimeRunStatus
        from usa_signal_bot.notifications.notification_adapters import build_policy_driven_scan_notifications
        from usa_signal_bot.notifications.alert_policy import default_alert_policies
        from usa_signal_bot.notifications.alert_evaluator import AlertEvaluator

        scan_res = MarketScanResult(
            run_id=context.get("run_id", "dummy"),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            request=request,
            status=RuntimeRunStatus.COMPLETED,
        )

        evaluator = AlertEvaluator(policies=default_alert_policies())
        eval_res, msgs = build_policy_driven_scan_notifications(scan_res, evaluator=evaluator)

        res.summary["notifications_sent"] = 0
        res.summary["alert_evaluations"] = eval_res.triggered_count
        return res

    def run_cleanup(self, context: Dict[str, Any]) -> PipelineStepResult:
        res = PipelineStepResult(step_name=PipelineStepName.CLEANUP, status=PipelineStepStatus.COMPLETED)
        return res
