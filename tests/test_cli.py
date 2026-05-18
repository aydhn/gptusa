import pytest
from usa_signal_bot.app.cli import handle_research_execution_info, handle_mock_experiment_run, handle_experiment_harness_run

class MockArgs:
    def __init__(self, run_type=None, mode=None):
        self.run_type = run_type
        self.mode = mode

def test_cli_handlers():
    # Direct handler invocation since running subprocess without full env setup fails
    assert handle_research_execution_info(None) == 0
    assert handle_mock_experiment_run(MockArgs(run_type="baseline")) == 0
    assert handle_experiment_harness_run(MockArgs(mode="mock_only")) == 0

