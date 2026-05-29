import pytest
import pandas as pd
from usa_signal_bot.regime_classification.feature_engineering.market_state_input_loader import (
    validate_market_state_input_table
)

def test_validate_market_state_input_table_valid():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "close": [150.0]})
    errors = validate_market_state_input_table(df)
    assert len(errors) == 0

def test_validate_market_state_input_table_invalid():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "buy_signal": [1.0]})
    errors = validate_market_state_input_table(df)
    assert len(errors) > 0
    assert any("Forbidden" in e for e in errors)
