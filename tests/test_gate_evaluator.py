import pytest
from usa_signal_bot.research_execution.gate_evaluator import evaluate_min_sample_size_gate
from usa_signal_bot.research_execution.execution_models import ResearchRun
from usa_signal_bot.core.enums import ResearchRunType, ResearchRunStatus, ExperimentExecutionMode

def create_run(metrics):
    return ResearchRun(
        run_id="r1", created_at_utc="now", experiment_id="exp1", hypothesis_id=None,
        run_type=ResearchRunType.BASELINE, status=ResearchRunStatus.COMPLETED,
        execution_mode=ExperimentExecutionMode.MOCK_ONLY, context=None, artifacts=[],
        metrics=metrics, started_at_utc="now", completed_at_utc="now", warnings=[], errors=[]
    )

def test_evaluate_min_sample_size_gate():
    c = create_run({"trade_count": 50})
    gate_payload = {"threshold": 30}
    res = evaluate_min_sample_size_gate(gate_payload, c)
    assert res.passed is True
