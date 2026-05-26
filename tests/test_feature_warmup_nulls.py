import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.core_indicators.feature_warmup_nulls import (
    count_warmup_nulls, feature_null_summary, drop_warmup_rows
)

def test_feature_warmup_nulls():
    df = pd.DataFrame({
        "a": [np.nan, np.nan, 3, 4, 5],
        "b": [np.nan, 2, 3, 4, np.nan]
    })
    c = count_warmup_nulls(df, ["a", "b"])
    assert c == 2
