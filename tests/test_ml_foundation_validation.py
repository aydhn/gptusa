import pytest
from usa_signal_bot.ml_research.foundation.ml_foundation_validation import (
    validate_ml_foundation_context_report, validate_no_execution_language_in_ml_foundation_text,
    validate_no_forbidden_ml_foundation_columns
)
from usa_signal_bot.ml_research.foundation.ml_foundation_report import build_ml_foundation_context

def test_validate_ml_foundation_context_report():
    ctx = build_ml_foundation_context()
    rep = validate_ml_foundation_context_report(ctx)
    assert rep.valid is True
    assert rep.error_count == 0

def test_validate_no_execution_language():
    res = validate_no_execution_language_in_ml_foundation_text("This has a kesin al signal.")
    assert res.valid is False
    assert res.error_count == 1

def test_validate_no_forbidden_columns():
    errors = validate_no_forbidden_ml_foundation_columns(["buy_feature", "good_feature"])
    assert len(errors) == 1
    assert "buy_feature" in errors[0]
