import pytest
from usa_signal_bot.release.acceptance_scenario_matrix import build_acceptance_scenario_matrix

def test_build_acceptance_scenario_matrix():
    matrix = build_acceptance_scenario_matrix()
    assert matrix.matrix_valid == True
    assert matrix.dry_run_only == True
    assert matrix.local_fixture_only == True
    assert len(matrix.scenarios) == 12
    for s in matrix.scenarios:
        assert s.dry_run == True
        assert s.local_fixture_only == True
