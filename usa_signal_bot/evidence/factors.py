"""Cross-sectional factor, regime-filter and vol-target strategy families (price-derived only; long-only, no leverage).

Weights at date t use information up to the close of t. Fundamental data (true value/quality) is not available from
free price feeds here, so ``value``/``quality`` are PRICE-DERIVED PROXIES and are labelled as such in reports.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from usa_signal_bot.evidence.strategies import _equal_weight


def _top(score: pd.DataFrame, members: pd.DataFrame, prices: pd.DataFrame, top_frac: float) -> pd.DataFrame:
    score = score.where(members & prices.notna())
    rank = score.rank(axis=1, ascending=False, pct=True)
    return _equal_weight((rank <= top_frac) & score.notna())


def _z(score: pd.DataFrame) -> pd.DataFrame:
    mu = score.mean(axis=1)
    sd = score.std(axis=1).replace(0, np.nan)
    return score.sub(mu, axis=0).div(sd, axis=0)


def low_vol_weights(prices: pd.DataFrame, members: pd.DataFrame, window: int = 126, top_frac: float = 0.3) -> pd.DataFrame:
    vol = prices.pct_change(fill_method=None).rolling(window, min_periods=window).std()
    return _top(-vol, members, prices, top_frac)


def value_proxy_weights(prices: pd.DataFrame, members: pd.DataFrame, window: int = 252, top_frac: float = 0.3) -> pd.DataFrame:
    """Proxy: price far BELOW its trailing ``window``-day high (cheap relative to own history)."""
    dist = prices / prices.rolling(window, min_periods=window).max() - 1.0  # <= 0
    return _top(-dist, members, prices, top_frac)


def quality_proxy_weights(prices: pd.DataFrame, members: pd.DataFrame, window: int = 252, top_frac: float = 0.3) -> pd.DataFrame:
    """Proxy: smooth, steady trailing return (mean/std of daily returns)."""
    r = prices.pct_change(fill_method=None)
    stab = r.rolling(window, min_periods=window).mean() / r.rolling(window, min_periods=window).std().replace(0, np.nan)
    return _top(stab, members, prices, top_frac)


def factor_mix_weights(
    prices: pd.DataFrame, members: pd.DataFrame, window: int = 252, top_frac: float = 0.3, skip: int = 21
) -> pd.DataFrame:
    """Equal-weight z-score mix of momentum (window-skip), low-vol, value proxy and quality proxy."""
    mom = prices.shift(skip) / prices.shift(window) - 1.0
    r = prices.pct_change(fill_method=None)
    vol = r.rolling(window // 2, min_periods=window // 2).std()
    dist = prices / prices.rolling(window, min_periods=window).max() - 1.0
    stab = r.rolling(window, min_periods=window).mean() / r.rolling(window, min_periods=window).std().replace(0, np.nan)
    parts = [_z(x.where(members & prices.notna())) for x in (mom, -vol, -dist, stab)]
    mix = sum(parts) / len(parts)
    return _top(mix, members, prices, top_frac)


def regime_filtered_mix_weights(
    prices: pd.DataFrame, members: pd.DataFrame, window: int = 252, top_frac: float = 0.3, trend_window: int = 200
) -> pd.DataFrame:
    """Factor mix, moved to cash while the equal-weight member index is below its ``trend_window`` SMA."""
    base = factor_mix_weights(prices, members, window, top_frac)
    idx = (1.0 + prices.pct_change(fill_method=None).where(members).mean(axis=1).fillna(0.0)).cumprod()
    risk_on = (idx > idx.rolling(trend_window, min_periods=trend_window).mean()).astype(float)
    return base.mul(risk_on, axis=0)


def vol_targeted_mix_weights(
    prices: pd.DataFrame, members: pd.DataFrame, window: int = 252, top_frac: float = 0.3, target_vol_pct: int = 10
) -> pd.DataFrame:
    """Factor mix scaled down (never up: no leverage) so trailing 63d annualised vol <= target."""
    base = factor_mix_weights(prices, members, window, top_frac)
    gross = (base.shift(1).fillna(0.0) * prices.pct_change(fill_method=None).fillna(0.0)).sum(axis=1)
    realized = gross.rolling(63, min_periods=63).std() * np.sqrt(252)
    scale = (target_vol_pct / 100.0 / realized.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    return base.mul(scale, axis=0)
