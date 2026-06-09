import pytest
from usa_signal_bot.release.acceptance_scenario_matrix import build_acceptance_scenario_matrix
from usa_signal_bot.release.advanced_dry_run_rehearsal_executor import execute_advanced_dry_run_scenario_matrix
from usa_signal_bot.release.acceptance_evidence_bundle import build_acceptance_evidence_bundle

def test_build_acceptance_evidence_bundle():
    matrix = build_acceptance_scenario_matrix()
    steps = execute_advanced_dry_run_scenario_matrix(matrix)
    bundle = build_acceptance_evidence_bundle(matrix, steps)
    assert bundle.bundle_valid == True
    assert bundle.read_only == True
    assert bundle.local_only == True
    assert len(bundle.evidence_items) == 12
    for item in bundle.evidence_items:
        assert item.valid == True
