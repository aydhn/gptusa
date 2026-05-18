from typing import Any, Tuple

from usa_signal_bot.core.enums import ExperimentExecutionMode
from usa_signal_bot.core.exceptions import LocalExperimentHarnessError
from usa_signal_bot.research_execution.execution_models import ExperimentRunContext, ResearchRun, ExperimentComparisonReport
from usa_signal_bot.research_execution.config_snapshot import build_baseline_config_snapshot, build_candidate_config_snapshot
from usa_signal_bot.research_execution.candidate_overlay import build_candidate_overlay_from_parameter_proposals
from usa_signal_bot.research_execution.run_context import build_baseline_run_context, build_candidate_run_context

class LocalExperimentHarness:
    def __init__(self, execution_mode: ExperimentExecutionMode = ExperimentExecutionMode.MOCK_ONLY, allow_config_mutation: bool = False, allow_order_routing: bool = False):
        self.execution_mode = execution_mode
        self.allow_config_mutation = allow_config_mutation
        self.allow_order_routing = allow_order_routing

        errors = self.validate_harness_safety()
        if errors:
            raise LocalExperimentHarnessError(f"Safety violations in harness init: {errors}")

    def validate_harness_safety(self) -> list[str]:
        errors = []
        if self.allow_config_mutation:
            errors.append("allow_config_mutation MUST be False. Harness does not patch production config.")
        if self.allow_order_routing:
            errors.append("allow_order_routing MUST be False. Harness cannot route live/demo orders.")
        return errors

    def prepare_contexts(self, experiment_plan: dict[str, Any], current_config: dict[str, Any] | None = None) -> Tuple[ExperimentRunContext, ExperimentRunContext]:
        if current_config is None:
            current_config = {}

        baseline_snap = build_baseline_config_snapshot(current_config)

        proposals = experiment_plan.get("parameter_proposals", [])
        overlay = build_candidate_overlay_from_parameter_proposals(proposals)
        candidate_snap = build_candidate_config_snapshot(current_config, overlay)

        baseline_ctx = build_baseline_run_context(experiment_plan, baseline_snap, self.execution_mode)
        candidate_ctx = build_candidate_run_context(experiment_plan, candidate_snap, self.execution_mode)

        return baseline_ctx, candidate_ctx

    def run_baseline(self, context: ExperimentRunContext) -> ResearchRun:
        runner_type = self.select_runner(context)
        if runner_type == "MOCK":
            from usa_signal_bot.research_execution.mock_runner import run_mock_experiment
            return run_mock_experiment(context)
        elif runner_type == "BACKTEST":
            from usa_signal_bot.research_execution.backtest_runner import run_backtest_experiment
            return run_backtest_experiment(context)
        elif runner_type == "WALK_FORWARD":
            from usa_signal_bot.research_execution.walk_forward_runner import run_walk_forward_experiment
            return run_walk_forward_experiment(context)
        else:
            raise LocalExperimentHarnessError(f"Unsupported runner type: {runner_type}")

    def run_candidate(self, context: ExperimentRunContext) -> ResearchRun:
        return self.run_baseline(context)

    def select_runner(self, context: ExperimentRunContext) -> str:
        if context.execution_mode == ExperimentExecutionMode.MOCK_ONLY:
            return "MOCK"
        elif context.execution_mode == ExperimentExecutionMode.BACKTEST_ONLY:
            return "BACKTEST"
        elif context.execution_mode == ExperimentExecutionMode.WALK_FORWARD_ONLY:
            return "WALK_FORWARD"
        else:
            return "MOCK"

    def run_experiment_pair(self, experiment_plan: dict[str, Any], current_config: dict[str, Any] | None = None) -> Tuple[ResearchRun, ResearchRun, ExperimentComparisonReport]:
        baseline_ctx, candidate_ctx = self.prepare_contexts(experiment_plan, current_config)

        baseline_run = self.run_baseline(baseline_ctx)
        candidate_run = self.run_candidate(candidate_ctx)

        from usa_signal_bot.research_execution.result_comparator import compare_research_runs
        report = compare_research_runs(baseline_run, candidate_run)

        return baseline_run, candidate_run, report
