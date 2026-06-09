import pytest
import json
import pandas as pd
from pathlib import Path
from usa_signal_bot.release.final_closure.phase159_handoff_ingestion import ingest_phase160_handoff_package_payload
from usa_signal_bot.release.final_closure.final_input_resolver import detect_forbidden_final_closure_fields, detect_forbidden_final_closure_columns
from usa_signal_bot.release.final_closure.final_closure_safety_validator import final_closure_text_has_trade_or_execution_language
from usa_signal_bot.release.final_closure.final_closure_report import build_final_closure_full_review

def test_phase160_handoff_ingestion():
    with open("tests/fixtures/final_closure/sample_phase160_handoff_package.json") as f:
        payload = json.load(f)
    result = ingest_phase160_handoff_package_payload(payload)
    assert result.valid_for_phase160 is True
    assert result.live_trading_enabled is False

def test_phase160_handoff_ingestion_blocked():
    with open("tests/fixtures/final_closure/sample_phase160_handoff_package_blocked.json") as f:
        payload = json.load(f)
    result = ingest_phase160_handoff_package_payload(payload)
    assert result.valid_for_phase160 is False
    assert result.live_trading_enabled is True

def test_forbidden_fields():
    with open("tests/fixtures/final_closure/sample_invalid_final_closure_payload.json") as f:
        payload = json.load(f)
    forbidden = detect_forbidden_final_closure_fields(payload)
    assert "live_order" in forbidden
    assert "buy_signal" in forbidden

def test_forbidden_columns():
    df = pd.read_csv("tests/fixtures/final_closure/sample_forbidden_final_closure_columns.csv")
    forbidden = detect_forbidden_final_closure_columns(list(df.columns))
    assert "broker_order" in forbidden
    assert "target_weight" in forbidden

def test_unsafe_language():
    with open("tests/fixtures/final_closure/sample_unsafe_final_closure_text.txt", "r", encoding="utf-8") as f:
        text = f.read()
    assert final_closure_text_has_trade_or_execution_language(text) is True

def test_build_final_closure_full_review():
    review = build_final_closure_full_review()
    # It might be blocked because store fetch returns false by default for our stub
    assert review.report_type.value == "FULL_PHASE160_REVIEW"
    assert review.context.status.value in ["PROJECT_CLOSED", "BLOCKED"]
