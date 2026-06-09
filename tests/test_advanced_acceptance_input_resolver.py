import pytest
from usa_signal_bot.release.advanced_acceptance_input_resolver import detect_forbidden_advanced_acceptance_fields, build_advanced_acceptance_input_references

def test_detect_forbidden_advanced_acceptance_fields():
    payload = {"target_weight": 0.5, "safe_key": "safe_val"}
    res = detect_forbidden_advanced_acceptance_fields(payload)
    assert "target_weight" in res
    assert "safe_key" not in res

def test_build_advanced_acceptance_input_references():
    payloads = {
        "full_system_integration_review": {"data": "test"},
        "phase159_readiness_gate": {"data": "test2"}
    }
    refs = build_advanced_acceptance_input_references(payloads)
    assert len(refs) == 2
    assert refs[0].valid == True
    assert refs[1].valid == True
