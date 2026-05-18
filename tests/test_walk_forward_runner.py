import pytest
from usa_signal_bot.core.enums import ResearchRunType, ResearchRunStatus, ExperimentExecutionMode
from usa_signal_bot.research_execution.execution_models import ExperimentRunContext
from usa_signal_bot.research_execution.walk_forward_runner import run_walk_forward_experiment

def test_run_walk_forward_experiment_placeholder():
    ctx = ExperimentRunContext(
        context_id="ctx_1", created_at_utc="now", experiment_id="exp_1", hypothesis_id=None,
        run_type=ResearchRunType.BASELINE, execution_mode=ExperimentExecutionMode.WALK_FORWARD_ONLY,
        config_snapshot=None, validation_plan={}, acceptance_gates=[], data_scope={},
        allowed_to_modify_config=False, allowed_to_send_orders=False, warnings=[], errors=[]
    )
    run = run_walk_forward_experiment(ctx)
    assert run.status == ResearchRunStatus.COMPLETED
