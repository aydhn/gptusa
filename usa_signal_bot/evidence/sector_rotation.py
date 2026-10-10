"""Sector-ETF rotation (momentum / low-vol among the SPDR sector ETFs, SPY as benchmark). CANDIDATE family.

Weights at t use prices up to the close of t (held t+1). ETFs not yet trading (XLRE, XLC) are excluded by the
``prices.notna()`` mask. SPY is the benchmark, never a rotation candidate.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

from usa_signal_bot.evidence.factors_rel import _rebalance_every
from usa_signal_bot.evidence.strategies import _equal_weight

SECTOR_ETFS: List[str] = ["XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB", "XLRE", "XLC"]
BENCH_ETF = "SPY"


def fetch_etf_prices(out_dir: str | Path = "data/etf", start: str = "2005-01-01", max_age_days: float = 1.0) -> dict:
    """Download sector ETFs + SPY with the existing yfinance helper (cached CSVs in ``out_dir``)."""
    from usa_signal_bot.evidence.fetch import fetch_daily

    return fetch_daily(SECTOR_ETFS + [BENCH_ETF], str(out_dir), start=start, max_age_days=max_age_days)


def load_etf_prices(directory: str | Path) -> pd.DataFrame:
    """Dates x ETF adjusted closes from ``<SYM>.csv`` (Date, Adj Close) files. Empty frame if none found."""
    cols: Dict[str, pd.Series] = {}
    for sym in SECTOR_ETFS + [BENCH_ETF]:
        p = Path(directory) / f"{sym}.csv"
        if p.exists():
            df = pd.read_csv(p)
            s = pd.Series(df.iloc[:, 1].to_numpy(dtype=float), index=pd.to_datetime(df.iloc[:, 0]))
            cols[sym] = s[~s.index.duplicated(keep="last")].sort_index()
    return pd.DataFrame(cols).sort_index()


def _candidates(prices: pd.DataFrame) -> pd.DataFrame:
    mask = prices.notna().copy()
    if BENCH_ETF in mask:
        mask[BENCH_ETF] = False
    return mask


def _top_n_equal(score: pd.DataFrame, mask: pd.DataFrame, top_n: int) -> pd.DataFrame:
    s = score.where(mask)
    rank = s.rank(axis=1, ascending=False, method="first")
    return _equal_weight((rank <= top_n) & s.notna())


def sector_momentum_weights(
    prices: pd.DataFrame, members: pd.DataFrame, lookback: int = 126, top_n: int = 3, rebalance: int = 21
) -> pd.DataFrame:
    """Hold the ``top_n`` sector ETFs by ``lookback``-day return (skipping the last 5 days), equal weight."""
    score = prices.shift(5) / prices.shift(lookback) - 1.0
    return _rebalance_every(_top_n_equal(score, _candidates(prices), top_n), rebalance)


def sector_lowvol_weights(
    prices: pd.DataFrame, members: pd.DataFrame, window: int = 126, top_n: int = 4, rebalance: int = 21
) -> pd.DataFrame:
    """Hold the ``top_n`` lowest-volatility sector ETFs, equal weight."""
    vol = prices.pct_change(fill_method=None).rolling(window, min_periods=window).std()
    return _rebalance_every(_top_n_equal(-vol, _candidates(prices), top_n), rebalance)


def spy_benchmark_weights(prices: pd.DataFrame) -> pd.DataFrame:
    w = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    if BENCH_ETF in prices:
        w[BENCH_ETF] = prices[BENCH_ETF].notna().astype(float)
    return w


ETF_FAMILIES = {
    "Sektör momentum (ETF)": (sector_momentum_weights, [{"lookback": lb, "top_n": n} for lb in (63, 126, 252) for n in (2, 3, 4)]),
    "Sektör düşük oynaklık (ETF)": (sector_lowvol_weights, [{"window": w, "top_n": n} for w in (63, 126, 252) for n in (3, 4)]),
}
