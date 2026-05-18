import pytest
from usa_signal_bot.core.enums import ExperimentExecutionMode, ComparisonOutcome
from usa_signal_bot.core.exceptions import LocalExperimentHarnessError
from usa_signal_bot.research_execution.experiment_harness import LocalExperimentHarness

def test_experiment_harness_safety_violation():
    with pytest.raises(LocalExperimentHarnessError):
        LocalExperimentHarness(allow_config_mutation=True)

def test_experiment_harness_run_experiment_pair():
    harness = LocalExperimentHarness(execution_mode=ExperimentExecutionMode.MOCK_ONLY)
    plan = {
        "experiment_id": "exp_harness",
        "parameter_proposals": [
            {"target_parameter": "strategy.threshold", "proposed_value": 0.5}
        ]
    }
    b_run, c_run, report = harness.run_experiment_pair(plan, current_config={"strategy": {"threshold": 0.1}})
    assert b_run.run_type.value == "BASELINE"
    assert c_run.run_type.value == "CANDIDATE"
