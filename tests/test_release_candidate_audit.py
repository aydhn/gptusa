import pytest
from usa_signal_bot.release.acceptance_scenario_matrix import build_acceptance_scenario_matrix
from usa_signal_bot.release.advanced_dry_run_rehearsal_executor import execute_advanced_dry_run_scenario_matrix
from usa_signal_bot.release.acceptance_evidence_bundle import build_acceptance_evidence_bundle
from usa_signal_bot.release.regression_acceptance_report import build_regression_acceptance_report
from usa_signal_bot.release.safety_acceptance_report import build_safety_acceptance_report
from usa_signal_bot.release.release_candidate_risk_register import build_release_candidate_risk_register
from usa_signal_bot.release.release_candidate_audit import build_release_candidate_audit

def test_release_candidate_audit():
    matrix = build_acceptance_scenario_matrix()
    steps = execute_advanced_dry_run_scenario_matrix(matrix)
    bundle = build_acceptance_evidence_bundle(matrix, steps)

    reports = [
        build_regression_acceptance_report(bundle, steps),
        build_safety_acceptance_report(bundle, steps)
    ]

    risk_register = build_release_candidate_risk_register(reports, steps)
    assert risk_register.blocking_risk_count == 0
    assert risk_register.release_candidate_blocked == False

    audit = build_release_candidate_audit(reports, risk_register)
    assert audit.audit_passed == True
    assert audit.not_deployment_approval == True
    assert audit.not_trading_approval == True
    assert audit.not_investment_advice == True
