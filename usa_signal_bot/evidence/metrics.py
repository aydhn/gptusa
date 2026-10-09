"""Performance metrics and a seeded block-bootstrap confidence interval for the Sharpe ratio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd

TRADING_DAYS = 252


@dataclass(frozen=True)
class PerformanceSummary:
    n_days: int
    cagr: float
    ann_vol: float
    sharpe: float
    max_drawdown: float
    total_return: float


def summarize(returns: pd.Series) -> PerformanceSummary:
    r = returns.dropna().astype(float)
    n = len(r)
    if n == 0:
        return PerformanceSummary(0, 0.0, 0.0, 0.0, 0.0, 0.0)
    equity = (1.0 + r).cumprod()
    total = float(equity.iloc[-1] - 1.0)
    years = n / TRADING_DAYS
    cagr = float(equity.iloc[-1] ** (1.0 / years) - 1.0) if years > 0 and equity.iloc[-1] > 0 else -1.0
    vol = float(r.std(ddof=1) * np.sqrt(TRADING_DAYS)) if n > 1 else 0.0
    sharpe = float(r.mean() / r.std(ddof=1) * np.sqrt(TRADING_DAYS)) if n > 1 and r.std(ddof=1) > 0 else 0.0
    dd = float((equity / equity.cummax() - 1.0).min())
    return PerformanceSummary(n, cagr, vol, sharpe, dd, total)


def sharpe_ci(returns: pd.Series, seed: int = 0, n_boot: int = 1000, block: int = 21) -> Tuple[float, float]:
    """95% moving-block-bootstrap interval of the annualised Sharpe ratio (deterministic for a seed)."""
    r = returns.dropna().to_numpy(dtype=float)
    n = len(r)
    if n < 2 * block:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block))
    starts_max = n - block
    stats = np.empty(n_boot)
    for i in range(n_boot):
        starts = rng.integers(0, starts_max + 1, size=n_blocks)
        sample = np.concatenate([r[s : s + block] for s in starts])[:n]
        sd = sample.std(ddof=1)
        stats[i] = sample.mean() / sd * np.sqrt(TRADING_DAYS) if sd > 0 else 0.0
    return (float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5)))
