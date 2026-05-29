import pytest
import pandas as pd
from usa_signal_bot.regime_classification.feature_engineering.unsupervised_candidate_preparation import (
    prepare_unsupervised_regime_candidates
)

def test_prepare_unsupervised_regime_candidates():
    tables = {
        "AAPL": pd.DataFrame({
            "timestamp": ["2023-01-01"],
            "regime_volatility_state_feature": [0.5]
        })
    }
    res = prepare_unsupervised_regime_candidates(tables)
    assert res.candidate_count > 0
    assert res.score_count > 0
    assert res.model_training_used is False
    assert res.produces_trade_signal is False
