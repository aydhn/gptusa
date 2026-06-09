import pytest
from usa_signal_bot.release.acceptance_scenario_matrix import build_acceptance_scenario_matrix
from usa_signal_bot.release.advanced_dry_run_rehearsal_executor import execute_advanced_dry_run_scenario_matrix
from usa_signal_bot.release.acceptance_evidence_bundle import build_acceptance_evidence_bundle
from usa_signal_bot.release.safety_acceptance_report import build_safety_acceptance_report

def test_build_safety_acceptance_report():
    matrix = build_acceptance_scenario_matrix()
    steps = execute_advanced_dry_run_scenario_matrix(matrix)
    bundle = build_acceptance_evidence_bundle(matrix, steps)
    report = build_safety_acceptance_report(bundle, steps)
    assert report.passed == True
    assert report.dry_run_only == True
    assert report.no_real_side_effects == True
    assert report.not_deployment_approval == True
