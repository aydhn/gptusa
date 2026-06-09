import pytest
from usa_signal_bot.release.acceptance_scenario_matrix import build_acceptance_scenario_matrix
from usa_signal_bot.release.advanced_dry_run_rehearsal_executor import execute_advanced_dry_run_scenario_matrix
from usa_signal_bot.release.acceptance_evidence_bundle import build_acceptance_evidence_bundle
from usa_signal_bot.release.regression_acceptance_report import build_regression_acceptance_report
from usa_signal_bot.release.release_candidate_risk_register import build_release_candidate_risk_register
from usa_signal_bot.release.release_candidate_audit import build_release_candidate_audit
from usa_signal_bot.release.final_freeze_checklist import build_final_freeze_checklist

def test_final_freeze_checklist():
    matrix = build_acceptance_scenario_matrix()
    steps = execute_advanced_dry_run_scenario_matrix(matrix)
    bundle = build_acceptance_evidence_bundle(matrix, steps)
    reports = [build_regression_acceptance_report(bundle, steps)]
    risk_register = build_release_candidate_risk_register(reports, steps)
    audit = build_release_candidate_audit(reports, risk_register)

    checklist = build_final_freeze_checklist(audit, bundle)
    assert checklist.checklist_valid == True
    assert checklist.ready_for_final_delivery_audit == True
    assert checklist.not_deployment_approval == True
    assert checklist.failed_count == 0
