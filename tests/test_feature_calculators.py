import pandas as pd
import numpy as np

from usa_signal_bot.feature_engine.core_indicators.return_features import add_daily_return_features, add_rolling_return_features
from usa_signal_bot.feature_engine.core_indicators.moving_average_features import add_moving_average_features
from usa_signal_bot.feature_engine.core_indicators.volatility_features import add_rolling_volatility_features, add_price_range_volatility_features
from usa_signal_bot.feature_engine.core_indicators.true_range_atr_features import add_true_range_atr_features
from usa_signal_bot.feature_engine.core_indicators.rsi_features import add_rsi_features
from usa_signal_bot.feature_engine.core_indicators.macd_features import add_macd_features
from usa_signal_bot.feature_engine.core_indicators.stochastic_features import add_stochastic_features
from usa_signal_bot.feature_engine.core_indicators.bollinger_features import add_bollinger_features
from usa_signal_bot.feature_engine.core_indicators.volume_features import add_volume_features
from usa_signal_bot.feature_engine.core_indicators.price_action_features import add_price_action_features
from usa_signal_bot.feature_engine.core_indicators.gap_range_candle_features import add_gap_range_candle_features

def test_calculators_smoke():
    df = pd.DataFrame({
        "open": np.random.randn(50) + 100,
        "high": np.random.randn(50) + 105,
        "low": np.random.randn(50) + 95,
        "close": np.random.randn(50) + 102,
        "volume": np.random.randint(1000, 10000, 50)
    })

    df = add_daily_return_features(df)
    df = add_rolling_return_features(df)
    df = add_moving_average_features(df)
    df = add_rolling_volatility_features(df)
    df = add_price_range_volatility_features(df)
    df = add_true_range_atr_features(df)
    df = add_rsi_features(df)
    df = add_macd_features(df)
    df = add_stochastic_features(df)
    df = add_bollinger_features(df)
    df = add_volume_features(df)
    df = add_price_action_features(df)
    df = add_gap_range_candle_features(df)

    assert "ret_1d" in df.columns
    assert "sma_5" in df.columns
