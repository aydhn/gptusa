import pytest
from usa_signal_bot.release.acceptance_scenario_matrix import build_acceptance_scenario_matrix
from usa_signal_bot.release.advanced_dry_run_rehearsal_executor import execute_advanced_dry_run_scenario_matrix
from usa_signal_bot.release.acceptance_evidence_bundle import build_acceptance_evidence_bundle
from usa_signal_bot.release.regression_acceptance_report import build_regression_acceptance_report
from usa_signal_bot.release.release_candidate_risk_register import build_release_candidate_risk_register
from usa_signal_bot.release.release_candidate_audit import build_release_candidate_audit
from usa_signal_bot.release.final_freeze_checklist import build_final_freeze_checklist
from usa_signal_bot.release.final_freeze_boundary import build_final_freeze_boundary_rules, build_final_freeze_boundary_result
from usa_signal_bot.release.final_freeze_certificate import build_final_freeze_certificate
from usa_signal_bot.release.phase160_handoff_contract import build_phase160_handoff_contract

def test_phase160_handoff_contract():
    matrix = build_acceptance_scenario_matrix()
    steps = execute_advanced_dry_run_scenario_matrix(matrix)
    bundle = build_acceptance_evidence_bundle(matrix, steps)
    reports = [build_regression_acceptance_report(bundle, steps)]
    risk_register = build_release_candidate_risk_register(reports, steps)
    audit = build_release_candidate_audit(reports, risk_register)
    checklist = build_final_freeze_checklist(audit, bundle)
    boundary = build_final_freeze_boundary_result(build_final_freeze_boundary_rules())
    cert = build_final_freeze_certificate(audit, checklist, boundary)

    contract = build_phase160_handoff_contract(cert, audit)
    assert contract.contract_valid == True
    assert contract.read_only == True
    assert contract.live_trading_allowed == False
    assert contract.deployment_allowed == False
