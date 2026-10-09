"""Trend/volatility regime from a benchmark price series (uses data up to t only)."""

from __future__ import annotations

from typing import Dict

import pandas as pd

RISK_ON, NEUTRAL, RISK_OFF = "RISK_ON", "NEUTRAL", "RISK_OFF"

DEFAULT_EXPOSURE: Dict[str, float] = {RISK_ON: 1.0, NEUTRAL: 0.6, RISK_OFF: 0.2}


def classify_regime(benchmark: pd.Series, trend_window: int = 200, vol_window: int = 20) -> pd.Series:
    """RISK_OFF below the trend line; NEUTRAL above it but in a high-volatility state; else RISK_ON.

    High volatility = 20d realised vol above its trailing 80th percentile (252d). Early history
    without enough data is NEUTRAL.
    """
    sma = benchmark.rolling(trend_window, min_periods=trend_window).mean()
    vol = benchmark.pct_change(fill_method=None).rolling(vol_window, min_periods=vol_window).std()
    vol_cut = vol.rolling(252, min_periods=60).quantile(0.8)
    out = pd.Series(NEUTRAL, index=benchmark.index, dtype=object)
    known = sma.notna() & vol_cut.notna()
    trend_up = benchmark > sma
    high_vol = vol > vol_cut
    out[known & ~trend_up] = RISK_OFF
    out[known & trend_up & high_vol] = NEUTRAL
    out[known & trend_up & ~high_vol] = RISK_ON
    return out
