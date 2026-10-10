import pytest
import json
import pandas as pd
from pathlib import Path
from usa_signal_bot.release.final_closure.phase159_handoff_ingestion import ingest_phase160_handoff_package_payload
from usa_signal_bot.release.final_closure.final_input_resolver import detect_forbidden_final_closure_fields, detect_forbidden_final_closure_columns
from usa_signal_bot.release.final_closure.final_closure_safety_validator import final_closure_text_has_trade_or_execution_language
from usa_signal_bot.release.final_closure.final_closure_report import build_final_closure_full_review

_SAFE_FLAGS = {
    "live_trading_enabled": False, "paper_trading_enabled": False, "paper_state_mutation_enabled": False,
    "broker_execution_enabled": False, "real_order_creation_enabled": False, "telegram_real_send_enabled": False,
    "strategy_activation_allowed": False, "deployment_allowed": False, "production_patch_allowed": False,
    "network_used": False, "paid_api_used": False, "scraping_used": False, "html_parsing_used": False,
    "dashboard_started": False, "daemon_started": False, "scheduler_enabled": False,
    "actual_target_weights_produced": False, "actual_allocation_produced": False, "order_size_produced": False,
    "capital_deployment_allowed": False, "investment_advice": False,
}


def _valid_payload():
    return {
        "package_valid": True, "ready_for_phase160": True, "read_only": True, "research_data_only": True,
        "final_delivery_handoff_only": True,
        "final_freeze_certificate": {"certificate_valid": True}, "release_candidate_audit": {"audit_valid": True},
        "release_candidate_risk_register": {"register_valid": True}, "acceptance_evidence_bundle": {"bundle_valid": True},
        "phase160_readiness_gate": {"gate_passed": True}, **_SAFE_FLAGS,
    }


def test_phase160_handoff_ingestion():
    result = ingest_phase160_handoff_package_payload(_valid_payload())
    assert result.valid_for_phase160 is True
    assert result.live_trading_enabled is False


def test_phase160_handoff_ingestion_blocked():
    # an empty payload defaults every unsafe flag to True (fail closed)
    result = ingest_phase160_handoff_package_payload({})
    assert result.valid_for_phase160 is False
    assert result.live_trading_enabled is True


def test_forbidden_fields():
    with open("tests/fixtures/final_closure/sample_invalid_final_closure_payload.json") as f:
        payload = json.load(f)
    forbidden = detect_forbidden_final_closure_fields(payload)
    assert "live_order" in forbidden
    assert "buy_signal" in forbidden

def test_forbidden_columns():
    forbidden = detect_forbidden_final_closure_columns(["symbol", "broker_order", "target_weight"])
    assert "broker_order" in forbidden
    assert "target_weight" in forbidden

def test_unsafe_language():
    text = "Bu strateji ile garanti kâr elde edersiniz."
    assert final_closure_text_has_trade_or_execution_language(text) is True

def test_build_final_closure_full_review():
    review = build_final_closure_full_review()
    # It might be blocked because store fetch returns false by default for our stub
    assert review.report_type.value == "FULL_PHASE160_REVIEW"
    assert review.context.status.value in ["PROJECT_CLOSED", "BLOCKED"]
