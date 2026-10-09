"""Simple long-only strategies. Weights at date t use only information up to the close of t."""

from __future__ import annotations

import pandas as pd


def _equal_weight(selected: pd.DataFrame) -> pd.DataFrame:
    n = selected.sum(axis=1).replace(0, float("nan"))
    return selected.astype(float).div(n, axis=0).fillna(0.0)


def sma_trend_weights(prices: pd.DataFrame, members: pd.DataFrame, window: int) -> pd.DataFrame:
    """Hold member symbols whose close is above their ``window``-day SMA, equal weight (cash otherwise)."""
    sma = prices.rolling(window, min_periods=window).mean()
    selected = (prices > sma) & members & prices.notna()
    return _equal_weight(selected)


def momentum_weights(
    prices: pd.DataFrame,
    members: pd.DataFrame,
    lookback: int,
    skip: int = 21,
    top_frac: float = 0.3,
) -> pd.DataFrame:
    """Cross-sectional ``lookback``-``skip`` momentum: hold the top ``top_frac`` of members, equal weight."""
    score = prices.shift(skip) / prices.shift(lookback) - 1.0
    score = score.where(members & prices.notna())
    rank = score.rank(axis=1, ascending=False, pct=True)
    selected = (rank <= top_frac) & score.notna()
    return _equal_weight(selected)


def equal_weight_benchmark(prices: pd.DataFrame, members: pd.DataFrame) -> pd.DataFrame:
    """Equal-weight all current members (point-in-time) - the do-nothing-clever baseline."""
    return _equal_weight(members & prices.notna())
