import pytest
from usa_signal_bot.core.enums import ResearchRunType, ResearchRunStatus
from usa_signal_bot.research_execution.execution_models import ExperimentRunContext, ExperimentExecutionMode
from usa_signal_bot.research_execution.mock_runner import run_mock_experiment

def test_run_mock_experiment():
    ctx = ExperimentRunContext(
        context_id="ctx_1",
        created_at_utc="now",
        experiment_id="exp_1", hypothesis_id=None,
        run_type=ResearchRunType.BASELINE,
        execution_mode=ExperimentExecutionMode.MOCK_ONLY,
        config_snapshot=None, validation_plan={}, acceptance_gates=[], data_scope={},
        allowed_to_modify_config=False, allowed_to_send_orders=False,
        warnings=[], errors=[]
    )
    run = run_mock_experiment(ctx)
    assert run.status == ResearchRunStatus.COMPLETED
    assert "total_net_pnl_usd" in run.metrics
