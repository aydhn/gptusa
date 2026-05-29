import pandas as pd
from usa_signal_bot.regime_classification.labeling.rolling_regime_windows import add_rolling_regime_windows_for_table

def test_rolling_windows():
    df = pd.DataFrame({
        "symbol": ["AAPL"] * 25,
        "regime_label_research": ["bull_regime"] * 10 + ["bear_regime"] * 15,
        "regime_label_confidence": [80.0] * 25
    })

    out_df, results = add_rolling_regime_windows_for_table("AAPL", df)
    assert len(results) == 3 # 20, 60, 120
    assert "regime_label_roll20" in out_df.columns
    assert "regime_confidence_roll20" in out_df.columns

    # Check that after index 10 (warmup min_periods=10 for s20), we get non-nulls
    # The first 9 might be null
    assert pd.isna(out_df["regime_label_roll20"].iloc[0])

    assert results[0].window_name == "short_regime_window_20"
    assert results[0].label_switch_count >= 0
    assert results[0].stability_score > 0
