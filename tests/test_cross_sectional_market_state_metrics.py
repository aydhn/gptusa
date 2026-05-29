import pytest
import pandas as pd
from usa_signal_bot.regime_classification.feature_engineering.cross_sectional_market_state_metrics import (
    add_cross_sectional_market_state_metrics
)

def test_add_cross_sectional_market_state_metrics():
    tables = {
        "AAPL": pd.DataFrame({"close": [150.0]}),
        "MSFT": pd.DataFrame({"close": [250.0]})
    }

    out_tables = add_cross_sectional_market_state_metrics(tables)
    assert "cross_sectional_dispersion_context" in out_tables["AAPL"].columns
