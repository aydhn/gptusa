import pytest
import pandas as pd
from usa_signal_bot.feature_engine.advanced_features.cross_sectional_alignment import align_feature_tables_by_timestamp

def test_alignment():
    t1 = pd.DataFrame({"timestamp": ["1", "2", "3"], "val": [1,2,3]})
    t2 = pd.DataFrame({"timestamp": ["2", "3", "4"], "val": [4,5,6]})
    aligned, res = align_feature_tables_by_timestamp({"A": t1, "B": t2})
    assert len(aligned["A"]) == 2
    assert "2" in aligned["A"]["timestamp"].values
