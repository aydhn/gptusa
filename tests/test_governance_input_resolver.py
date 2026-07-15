import pytest
import sys
import importlib
from unittest.mock import patch
from usa_signal_bot.portfolio.risk_reporting.governance_input_resolver import (
    build_portfolio_risk_input_references,
    detect_forbidden_portfolio_risk_columns
)

def test_build_portfolio_risk_input_references():
    payloads = {"optimizer_policy": {"a": 1}}
    refs = build_portfolio_risk_input_references(payloads)
    assert len(refs) == 1
    assert not refs[0].forbidden_columns_detected

def test_detect_forbidden_portfolio_risk_columns():
    cols = ["symbol", "target_weight", "score"]
    forbidden = detect_forbidden_portfolio_risk_columns(cols)
    assert "target_weight" in forbidden


def test_pandas_import_error():
    import usa_signal_bot.portfolio.risk_reporting.governance_input_resolver as gir

    with patch.dict('sys.modules', {'pandas': None}):
        importlib.reload(gir)
        assert gir.pd is None

    importlib.reload(gir)
