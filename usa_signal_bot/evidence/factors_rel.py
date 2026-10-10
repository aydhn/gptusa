"""Benchmark-relative families: keep the equal-weight market (beta) and add small, cheap tilts / risk scaling.

All long-only, no leverage, weights at t use information up to the close of t. Idle cash (weights summing to < 1) earns
the cash rate in ``backtest_weights``. These are CANDIDATES evaluated like every other family (walk-forward, costs,
purge, DSR/SPA vs the benchmark); nothing here is assumed to work.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from usa_signal_bot.evidence.factors import _z, factor_mix_weights
from usa_signal_bot.evidence.strategies import _equal_weight


def _beta(prices: pd.DataFrame, members: pd.DataFrame) -> pd.DataFrame:
    return _equal_weight(members & prices.notna())


def _rebalance_every(weights: pd.DataFrame, every: int) -> pd.DataFrame:
    """Hold weights fixed between rebalance dates (every ``every`` rows) to cut turnover."""
    if every <= 1:
        return weights
    mask = pd.Series(np.arange(len(weights)) % every == 0, index=weights.index)
    return weights.where(mask, np.nan).ffill().fillna(0.0)


def _market_index(prices: pd.DataFrame, members: pd.DataFrame) -> pd.Series:
    return (1.0 + prices.pct_change(fill_method=None).where(members).mean(axis=1).fillna(0.0)).cumprod()


def beta_tilt_weights(
    prices: pd.DataFrame, members: pd.DataFrame, window: int = 252, tilt: float = 0.5, rebalance: int = 21
) -> pd.DataFrame:
    """Equal-weight members, multiplied by (1 + tilt * clipped factor-mix z-score), renormalised to 1."""
    base = _beta(prices, members)
    z = _z(_factor_score(prices, members, window)).clip(-1.5, 1.5).fillna(0.0)
    w = (base * (1.0 + tilt * z)).clip(lower=0.0)
    w = w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return _rebalance_every(w, rebalance)


def _factor_score(prices: pd.DataFrame, members: pd.DataFrame, window: int) -> pd.DataFrame:
    mom = prices.shift(21) / prices.shift(window) - 1.0
    r = prices.pct_change(fill_method=None)
    vol = r.rolling(window // 2, min_periods=window // 2).std()
    dist = prices / prices.rolling(window, min_periods=window).max() - 1.0
    stab = r.rolling(window, min_periods=window).mean() / r.rolling(window, min_periods=window).std().replace(0, np.nan)
    parts = [_z(x.where(members & prices.notna())) for x in (mom, -vol, -dist, stab)]
    return sum(parts) / len(parts)


def low_turnover_mix_weights(
    prices: pd.DataFrame, members: pd.DataFrame, window: int = 252, top_frac: float = 0.4, rebalance: int = 63
) -> pd.DataFrame:
    """Diversified factor mix (wide top fraction) rebalanced quarterly."""
    return _rebalance_every(factor_mix_weights(prices, members, window, top_frac), rebalance)


def vol_target_beta_weights(
    prices: pd.DataFrame, members: pd.DataFrame, target_vol_pct: int = 12, window: int = 63
) -> pd.DataFrame:
    """Equal-weight market scaled down (never up) so trailing annualised vol <= target; remainder in cash."""
    base = _beta(prices, members)
    gross = (base.shift(1).fillna(0.0) * prices.pct_change(fill_method=None).fillna(0.0)).sum(axis=1)
    realized = gross.rolling(window, min_periods=window).std() * np.sqrt(252)
    scale = (target_vol_pct / 100.0 / realized.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    return _rebalance_every(base.mul(scale, axis=0), 5)


def regime_beta_weights(
    prices: pd.DataFrame, members: pd.DataFrame, trend_window: int = 200, risk_off_exposure: float = 0.5
) -> pd.DataFrame:
    """Equal-weight market at 100% while the member index is above its SMA, else ``risk_off_exposure`` (rest cash)."""
    base = _beta(prices, members)
    idx = _market_index(prices, members)
    on = (idx > idx.rolling(trend_window, min_periods=trend_window).mean())
    scale = on.astype(float) + (~on).astype(float) * risk_off_exposure
    scale[idx.rolling(trend_window, min_periods=trend_window).mean().isna()] = 1.0  # no signal yet: stay in the benchmark
    return base.mul(scale, axis=0)
