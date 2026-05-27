import pytest
import pandas as pd
from pathlib import Path
from usa_signal_bot.feature_engine.factor_scoring.phase121_models import *
from usa_signal_bot.feature_engine.factor_scoring.factor_composition_ingestion import *
from usa_signal_bot.feature_engine.factor_scoring.factor_table_input_loader import *
from usa_signal_bot.feature_engine.factor_scoring.factor_scoring_registry import *
from usa_signal_bot.feature_engine.factor_scoring.factor_component_scorer import *
from usa_signal_bot.feature_engine.factor_scoring.individual_factor_scorer import *
from usa_signal_bot.feature_engine.factor_scoring.composite_factor_scorer import *
from usa_signal_bot.feature_engine.factor_scoring.factor_normalization import *
from usa_signal_bot.feature_engine.factor_scoring.factor_winsorization import *
from usa_signal_bot.feature_engine.factor_scoring.cross_sectional_factor_ranks import *
from usa_signal_bot.feature_engine.factor_scoring.factor_distribution_diagnostics import *
from usa_signal_bot.feature_engine.factor_scoring.factor_correlation_diagnostics import *
from usa_signal_bot.feature_engine.factor_scoring.factor_stability_diagnostics import *
from usa_signal_bot.feature_engine.factor_scoring.factor_diagnostics_builder import *
from usa_signal_bot.feature_engine.factor_scoring.factor_table_schema import *
from usa_signal_bot.feature_engine.factor_scoring.factor_table_builder import *
from usa_signal_bot.feature_engine.factor_scoring.factor_computation_validator import *
from usa_signal_bot.feature_engine.factor_scoring.factor_output_safety_validator import *
from usa_signal_bot.feature_engine.factor_scoring.factor_scoring_report import *
from usa_signal_bot.feature_engine.factor_scoring.factor_scoring_store import *
from usa_signal_bot.feature_engine.factor_scoring.factor_scoring_validation import *
from usa_signal_bot.feature_engine.factor_scoring.factor_scoring_reporting import *

def test_phase121_models():
    assert create_factor_scoring_context_id() is not None
    assert create_factor_scoring_full_review_id() is not None

def test_factor_composition_ingestion():
    payload = {
        "review_id": "test",
        "feature_groups_ready": True,
        "factor_candidates_ready": True,
        "selection_metadata_ready": True,
        "factor_readiness_gate_ready": True,
        "ready_for_phase120": True
    }
    res = ingest_factor_composition_review_payload(payload)
    assert res.valid_for_phase121 == True

    payload_invalid = {
        "review_id": "test",
        "feature_groups_ready": True,
        "factor_candidates_ready": True,
        "selection_metadata_ready": True,
        "factor_readiness_gate_ready": True,
        "ready_for_phase120": True,
        "produces_trade_signal": True
    }
    res2 = ingest_factor_composition_review_payload(payload_invalid)
    assert res2.valid_for_phase121 == False

def test_factor_table_input_loader():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"]})
    errs = validate_factor_input_table(df)
    assert len(errs) == 0

    df_forbidden = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "buy_signal": [1]})
    errs_forb = validate_factor_input_table(df_forbidden)
    assert len(errs_forb) > 0

def test_factor_scoring_registry():
    specs = build_factor_scoring_specs()
    assert len(specs) >= 10
    errs = validate_factor_scoring_specs(specs)
    assert len(errs) == 0

def test_factor_component_scorer():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    res = score_component_mean(df, ["a", "b"], "out")
    assert list(res.values) == [2.0, 3.0]

    res2 = score_component_weighted_mean(df, ["a", "b"], {"a": 0.5, "b": 1.5}, "out")
    assert list(res2.values) == [2.5, 3.5]

    res3 = score_component_directional(df, ["a", "b"], {"a": 1, "b": -1})
    assert list(res3.values) == [-1.0, -1.0]

def test_individual_factor_scorer():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"]})
    df_out = add_individual_factor_scores(df)
    assert "momentum_research_factor_raw" in df_out.columns
    assert "trend_research_factor_raw" in df_out.columns
    errs = validate_individual_factor_scores(df_out)
    assert len(errs) == 0

def test_composite_factor_scorer():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"]})
    df_out = add_composite_factor_score(df)
    assert "composite_research_factor_raw" in df_out.columns

def test_factor_normalization():
    s = pd.Series([1, 2, 3])
    zs = factor_zscore(s)
    assert abs(zs.mean()) < 0.001

    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "momentum_research_factor_raw": [1]})
    specs = build_factor_scoring_specs()
    df_out, res = normalize_factor_columns(df, specs)
    assert len(res) > 0

def test_factor_winsorization():
    s = pd.Series([1, 2, 3, 100])
    w = winsorize_factor_series(s, 0.1, 0.9)
    assert w.max() < 100

def test_cross_sectional_factor_ranks():
    tables = {
        "AAPL": pd.DataFrame({"col": [1, 2]}),
        "MSFT": pd.DataFrame({"col": [3, 4]})
    }
    res = add_cross_sectional_factor_zscores(tables, ["col"])
    assert "cs_col_zscore" in res["AAPL"].columns

def test_factor_distribution_diagnostics():
    df = pd.DataFrame({"f1": [1]*20 + [1000]})
    profs = build_factor_distribution_diagnostics(df, ["f1"])
    assert len(profs) == 1
    assert profs[0].outlier_ratio > 0

def test_factor_correlation_diagnostics():
    df = pd.DataFrame({"f1": [1, 2, 3], "f2": [2, 4, 6]})
    profs = build_factor_correlation_diagnostics(df, ["f1", "f2"])
    assert len(profs) > 0
    assert profs[0].quality == FactorScoreQuality.WARNING

def test_factor_stability_diagnostics():
    df = pd.DataFrame({"f1": [1, 1, 1]})
    profs = build_factor_stability_diagnostics(df, ["f1"])
    assert profs[0].stability_score == 0

def test_factor_diagnostics_builder():
    df = pd.DataFrame({"f1": [1, 2, 3]})
    profs = build_factor_diagnostics(df, ["f1"])
    assert len(profs) == 1
    assert FactorDiagnosticsKind.COVERAGE in profs[0].diagnostics_kinds

def test_factor_table_schema():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "momentum_research_factor_raw": [1.0]})
    schema = build_factor_table_schema(df)
    assert schema.schema_valid == True

    df_err = pd.DataFrame({"buy_signal": [1]})
    schema_err = build_factor_table_schema(df_err)
    assert schema_err.schema_valid == False

def test_factor_table_builder():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"]})
    df_out, res = build_factor_table_for_symbol("AAPL", df)
    assert "momentum_research_factor_raw" in df_out.columns
    assert res.produced_trade_signal == False

def test_factor_computation_validator():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "buy_signal": [1]})
    errs = validate_factor_dataframe(df)
    assert len(errs) > 0

def test_factor_output_safety_validator():
    assert factor_output_text_has_trade_or_execution_language("this is a buy signal") == True
    assert factor_output_text_has_trade_or_execution_language("just some factor score") == False

def test_factor_scoring_report():
    rev = build_factor_scoring_full_review()
    assert rev.report_type == FactorScoringReportType.FULL_PHASE121_REVIEW

def test_factor_scoring_validation():
    ctx = build_factor_scoring_context()
    rep = validate_factor_scoring_context_report(ctx)
    assert rep.valid == True
