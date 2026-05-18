import pytest
from usa_signal_bot.core.enums import ResearchRunStatus, ResearchRunType, ExperimentExecutionMode
from usa_signal_bot.research_execution.execution_models import ResearchRun
from usa_signal_bot.research_execution.run_registry import register_research_run, find_run_by_id, latest_run_for_experiment

def create_dummy_run(run_id, experiment_id, created_at):
    return ResearchRun(
        run_id=run_id, created_at_utc=created_at, experiment_id=experiment_id, hypothesis_id=None,
        run_type=ResearchRunType.BASELINE, status=ResearchRunStatus.COMPLETED,
        execution_mode=ExperimentExecutionMode.MOCK_ONLY, context=None, artifacts=[], metrics={},
        started_at_utc="now", completed_at_utc="now", warnings=[], errors=[]
    )

def test_run_registry_operations():
    registry = []
    r1 = create_dummy_run("r1", "exp_1", "2023-01-01T00:00:00Z")
    registry = register_research_run(r1, registry)
    assert find_run_by_id(registry, "r1") == r1
