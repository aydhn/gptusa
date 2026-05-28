import pytest
import pandas as pd
from usa_signal_bot.regime_classification.feature_engineering.candidate_distance_context import (
    add_candidate_distance_context_columns
)
from usa_signal_bot.regime_classification.feature_engineering.regime_candidate_definitions import build_default_regime_candidate_definitions

def test_add_candidate_distance_context_columns():
    df = pd.DataFrame({"dummy": [1]})
    defs = build_default_regime_candidate_definitions()
    out_df = add_candidate_distance_context_columns(df, defs)
    assert "risk_on_candidate_distance" in out_df.columns
