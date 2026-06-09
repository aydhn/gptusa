import pytest
from usa_signal_bot.release.acceptance_scenario_matrix import build_acceptance_scenario_matrix
from usa_signal_bot.release.advanced_dry_run_rehearsal_executor import execute_advanced_dry_run_scenario_matrix

def test_execute_advanced_dry_run_scenario_matrix():
    matrix = build_acceptance_scenario_matrix()
    steps = execute_advanced_dry_run_scenario_matrix(matrix)
    assert len(steps) == 12
    for step in steps:
        assert step.dry_run == True
        assert step.local_fixture_only == True
        assert step.executed_real_side_effect == False
        assert step.used_broker == False
        assert step.mutated_paper_state == False
