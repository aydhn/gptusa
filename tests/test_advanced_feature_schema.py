import pytest
import pandas as pd
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_schema import validate_advanced_feature_column_names

def test_schema():
    assert len(validate_advanced_feature_column_names(["close", "ret_1d"])) == 0
    errs = validate_advanced_feature_column_names(["buy_signal", "portfolio_weight"])
    assert len(errs) == 3
