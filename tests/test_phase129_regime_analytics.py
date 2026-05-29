import pytest
import pandas as pd
from pathlib import Path

from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeTransitionAnalyticsResult,
    RegimeDiagnosticsReadinessGate
)
from usa_signal_bot.regime_classification.diagnostics.regime_labeling_ingestion import ingest_regime_labeling_review_payload
from usa_signal_bot.regime_classification.diagnostics.regime_sequence_input_loader import load_labeled_regime_table_csv, validate_labeled_regime_table
from usa_signal_bot.regime_classification.diagnostics.regime_transition_matrix import build_transition_matrix_for_table
from usa_signal_bot.regime_classification.diagnostics.regime_persistence_analytics import build_persistence_profiles_for_table
from usa_signal_bot.regime_classification.diagnostics.regime_duration_analytics import build_duration_profiles_for_table
from usa_signal_bot.regime_classification.diagnostics.regime_churn_diagnostics import build_churn_diagnostic_for_table
from usa_signal_bot.regime_classification.diagnostics.regime_stability_diagnostics import build_stability_diagnostics_for_table
from usa_signal_bot.regime_classification.diagnostics.regime_diagnostics_safety_validator import validate_regime_diagnostics_dataframe_output_safety, regime_diagnostics_text_has_trade_or_execution_language

def test_regime_labeling_ingestion_valid():
    payload = {
        "context": {
            "ready_for_phase129": True,
            "feature_engineering_ingested": True,
            "heuristic_labels_ready": True,
            "rolling_windows_ready": True,
            "candidates_validated": True,
            "label_stability_profiled": True,
            "readiness_gate_ready": True,
            "activation_allowed": False
        }
    }
    res = ingest_regime_labeling_review_payload(payload)
    assert res.ready_for_phase129 is True
    assert res.valid_for_phase129 is True

def test_regime_labeling_ingestion_unsafe():
    payload = {
        "context": {
            "ready_for_phase129": True,
            "activation_allowed": True,
            "broker_execution_enabled": True
        }
    }
    res = ingest_regime_labeling_review_payload(payload)
    assert res.valid_for_phase129 is False
    assert any("broker" in e.lower() for e in res.errors)

def test_regime_sequence_loader():
    path = Path("tests/fixtures/regime_diagnostics/sample_labeled_regime_table_aapl.csv")
    df = load_labeled_regime_table_csv(path)
    errs = validate_labeled_regime_table(df)
    assert len(errs) == 0
    assert len(df) == 5

def test_forbidden_columns_validation():
    df = pd.DataFrame({"symbol": ["A"], "regime_label_research": ["t"], "buy_signal": [1]})
    errs = validate_labeled_regime_table(df)
    assert len(errs) == 1
    assert "buy_signal" in errs[0]

def test_transition_matrix_builder():
    path = Path("tests/fixtures/regime_diagnostics/sample_labeled_regime_table_aapl.csv")
    df = load_labeled_regime_table_csv(path)
    matrix = build_transition_matrix_for_table("AAPL", df)
    assert matrix.matrix_valid is True
    assert matrix.total_transitions == 4
    assert matrix.self_transition_count == 2
    assert matrix.switch_count == 2

def test_persistence_analytics():
    path = Path("tests/fixtures/regime_diagnostics/sample_labeled_regime_table_aapl.csv")
    df = load_labeled_regime_table_csv(path)
    profiles = build_persistence_profiles_for_table("AAPL", df)
    assert len(profiles) == 2
    trend_p = next(p for p in profiles if p.label_name == "trend")
    assert trend_p.run_count == 2
    assert trend_p.total_periods == 3

def test_duration_analytics():
    path = Path("tests/fixtures/regime_diagnostics/sample_labeled_regime_table_aapl.csv")
    df = load_labeled_regime_table_csv(path)
    profiles = build_duration_profiles_for_table("AAPL", df)
    assert len(profiles) == 2
    trend_p = next(p for p in profiles if p.label_name == "trend")
    assert trend_p.max_duration == 2

def test_churn_diagnostics():
    path = Path("tests/fixtures/regime_diagnostics/sample_labeled_regime_table_aapl.csv")
    df = load_labeled_regime_table_csv(path)
    diag = build_churn_diagnostic_for_table("AAPL", df)
    assert diag.switch_rate == 0.5
    assert diag.low_confidence_count == 1

def test_stability_diagnostics():
    path = Path("tests/fixtures/regime_diagnostics/sample_labeled_regime_table_aapl.csv")
    df = load_labeled_regime_table_csv(path)
    diags = build_stability_diagnostics_for_table("AAPL", df)
    assert len(diags) == 1
    assert diags[0].diagnostic_score > 0

def test_execution_language_safety():
    assert regime_diagnostics_text_has_trade_or_execution_language("This is a buy signal.") is True
    assert regime_diagnostics_text_has_trade_or_execution_language("Regime transition matrix is valid.") is False
