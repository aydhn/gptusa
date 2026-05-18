import pytest
from usa_signal_bot.research_execution.workflow_adapter import execution_context_from_experiment_plan, attach_execution_result_to_experiment_plan
from usa_signal_bot.core.enums import ComparisonOutcome
from usa_signal_bot.research_execution.execution_models import ExperimentComparisonReport

def test_execution_context_from_experiment_plan():
    plan = {"experiment_id": "exp_1", "validation_plan": {"data_scope": {"symbols": ["AAPL"]}}}
    ctx = execution_context_from_experiment_plan(plan, {"a": 1})
    assert ctx.experiment_id == "exp_1"
    assert ctx.data_scope["symbols"] == ["AAPL"]
    assert ctx.allowed_to_modify_config is False

def test_attach_execution_result_to_experiment_plan():
    plan = {"experiment_id": "exp_1"}
    report = ExperimentComparisonReport(
        report_id="rep_1", created_at_utc="now", experiment_id="exp_1",
        baseline_run_id="b1", candidate_run_id="c1", outcome=ComparisonOutcome.CANDIDATE_BETTER,
        metric_comparisons=[], gate_evaluations=[], attribution_delta={}, diagnostics_delta={},
        summary={}, warnings=[], errors=[], metadata={}
    )

    updated = attach_execution_result_to_experiment_plan(plan, report)
    assert "execution_result" in updated
    assert updated["execution_result"]["outcome"] == "CANDIDATE_BETTER"
