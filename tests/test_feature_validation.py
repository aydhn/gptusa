import pytest
import pandas as pd
import numpy as np

from usa_signal_bot.features.validation import (
    validate_feature_rows, validate_feature_dataframe,
    assert_features_valid, FeatureValidationIssue
)
from usa_signal_bot.features.output_contract import FeatureRow
from usa_signal_bot.core.enums import FeatureValidationStatus
from usa_signal_bot.core.exceptions import FeatureValidationError

def test_validate_feature_rows():
    rows = [FeatureRow("2023-01-01", "AAPL", "1d", {"f1": 1.0, "f2": 2.0})]
    rep = validate_feature_rows(rows, ["f1", "f2"])
    assert rep.status == FeatureValidationStatus.VALID

    rows2 = [FeatureRow("2023-01-01", "", "1d", {"f1": 1.0})]
    rep2 = validate_feature_rows(rows2, ["f1"])
    assert rep2.status == FeatureValidationStatus.WARNING

    rows3 = [FeatureRow("2023-01-01", "AAPL", "1d", {"f1": float('inf')})]
    rep3 = validate_feature_rows(rows3, ["f1"])
    assert rep3.status == FeatureValidationStatus.INVALID

    rows4 = [FeatureRow("2023-01-01", "AAPL", "1d", {"f1": np.nan})]
    rep4 = validate_feature_rows(rows4, ["f1"])
    assert rep4.status == FeatureValidationStatus.INVALID
    assert rep4.nan_ratio == 1.0

def test_assert_features_valid():
    from usa_signal_bot.features.validation import FeatureValidationReport

    rep = FeatureValidationReport(FeatureValidationStatus.INVALID, 0, 0, 0.0, [], [], ["error"])
    with pytest.raises(FeatureValidationError):
        assert_features_valid(rep)

    rep2 = FeatureValidationReport(FeatureValidationStatus.WARNING, 0, 0, 0.0, [], ["warn"], [])
    with pytest.raises(FeatureValidationError):
        assert_features_valid(rep2, allow_warnings=False)

    assert_features_valid(rep2, allow_warnings=True)

def test_detect_out_of_range_oscillators():
    from usa_signal_bot.features.validation import detect_out_of_range_oscillators
    import pandas as pd
    df = pd.DataFrame({"symbol": ["AAPL", "AAPL"], "timeframe": ["1d", "1d"], "rsi": [105.0, 50.0], "stoch": [-5.0, 20.0]})
    issues = detect_out_of_range_oscillators(df, ["rsi", "stoch"])
    assert len(issues) == 2

def test_detect_extreme_momentum_values():
    from usa_signal_bot.features.validation import detect_extreme_momentum_values
    import pandas as pd
    df = pd.DataFrame({"symbol": ["AAPL", "AAPL"], "timeframe": ["1d", "1d"], "roc": [1005.0, 50.0], "momentum": [-2000.0, 20.0]})
    issues = detect_extreme_momentum_values(df, ["roc", "momentum"], absolute_threshold=1000.0)
    assert len(issues) == 2
