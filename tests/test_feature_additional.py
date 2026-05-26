from usa_signal_bot.feature_engine.feature_foundation_store import feature_foundation_store_summary
from usa_signal_bot.feature_engine.feature_safety_validator import validate_feature_foundation_context_safety, feature_text_has_trade_or_execution_language
from usa_signal_bot.feature_engine.feature_foundation_validation import validate_no_execution_language_in_feature_text
from usa_signal_bot.feature_engine.feature_foundation_report import build_feature_foundation_context
from pathlib import Path

def test_feature_text_language():
    assert feature_text_has_trade_or_execution_language("buy signal") is True
    assert feature_text_has_trade_or_execution_language("this is a safe string") is False

def test_validate_no_execution_language():
    report = validate_no_execution_language_in_feature_text("we have a strong buy opportunity")
    assert report.valid is False

def test_store_summary(tmp_path):
    summary = feature_foundation_store_summary(tmp_path)
    assert summary["contexts"] == 0
    assert summary["reviews"] == 0

def test_safety_validator_catches_unsafe_context():
    ctx = build_feature_foundation_context()
    ctx.produces_trade_signal = True
    errors = validate_feature_foundation_context_safety(ctx)
    assert len(errors) > 0
    assert "produces_trade_signal is true" in str(errors)
