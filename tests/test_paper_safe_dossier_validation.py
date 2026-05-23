from usa_signal_bot.paper_safe_dossier.dossier_validation import (
    validate_paper_safe_dossier_report,
    validate_non_execution_seal_report,
    validate_pre_paper_runtime_map_report,
    validate_no_sensitive_data_in_dossier_payload,
    validate_no_live_execution_language_in_dossier,
    validate_no_active_paper_language_in_dossier,
    validate_no_paper_state_mutation_fields_in_dossier,
    validate_no_broker_execution_fields_in_dossier
)
from usa_signal_bot.paper_safe_dossier.paper_safe_gate_dossier import build_default_paper_safe_dossier
from usa_signal_bot.paper_safe_dossier.non_execution_acceptance_seal import build_default_non_execution_acceptance_seal
from usa_signal_bot.paper_safe_dossier.local_runtime_map import build_default_pre_paper_local_runtime_map

def test_paper_safe_dossier_validation():
    dossier = build_default_paper_safe_dossier()
    report = validate_paper_safe_dossier_report(dossier)
    assert report.warning_count > 0

    dossier.paper_safe_gate_passed = True
    report = validate_paper_safe_dossier_report(dossier)
    assert report.valid

    seal = build_default_non_execution_acceptance_seal()
    report = validate_non_execution_seal_report(seal)
    assert report.valid

    rmap = build_default_pre_paper_local_runtime_map()
    report = validate_pre_paper_runtime_map_report(rmap)
    assert report.valid

    res = validate_no_sensitive_data_in_dossier_payload({"test": "value"})
    assert res.valid

    res = validate_no_sensitive_data_in_dossier_payload({"api_key": "123"})
    assert not res.valid

    res = validate_no_live_execution_language_in_dossier("this is a test")
    assert res.valid

    res = validate_no_live_execution_language_in_dossier("Live approved today")
    assert not res.valid

    res = validate_no_active_paper_language_in_dossier("candidate kesin iyi result")
    assert not res.valid

    res = validate_no_paper_state_mutation_fields_in_dossier({"paper_state_committed": True})
    assert not res.valid

    res = validate_no_broker_execution_fields_in_dossier({"broker_order_id": "ord123"})
    assert not res.valid
