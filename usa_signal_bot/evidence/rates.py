"""Cash (T-bill) and inflation rate helpers. Idle cash must earn interest in every backtest / simulated ledger.

Rates are ANNUAL decimals (0.04 = 4%). A constant or a date-indexed Series is accepted. ``load_rate_csv`` reads a
FRED-style CSV (DATE,<series>; percent values; '.' = missing), e.g. DTB3 (3-month T-bill) or CPIAUCSL (index level,
convert with ``yoy_inflation_from_index``). ``fetch_fred_csv`` downloads the official FRED CSV endpoint (no scraping,
no API key); the caller caches it via the output path.
"""

from __future__ import annotations

import urllib.request
from pathlib import Path
from typing import Union

import pandas as pd

RateLike = Union[float, pd.Series]
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"


def load_rate_csv(path: str | Path, percent: bool = True) -> pd.Series:
    df = pd.read_csv(path)
    date_col, val_col = df.columns[0], df.columns[1]
    s = pd.to_numeric(df[val_col], errors="coerce")
    s.index = pd.to_datetime(df[date_col])
    s = s.dropna().sort_index()
    return s / 100.0 if percent else s


def fetch_fred_csv(series_id: str, out_path: str | Path, timeout: int = 30) -> Path:
    if not series_id.replace("_", "").isalnum():
        raise ValueError("bad FRED series id")
    req = urllib.request.Request(FRED_CSV.format(sid=series_id), headers={"User-Agent": "gptusa-research"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - fixed https FRED host
        data = resp.read()
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return out


def yoy_inflation_from_index(level: pd.Series) -> pd.Series:
    """Year-over-year inflation from a price-index level series (monthly CPI -> 12-period change)."""
    return level.pct_change(12).dropna()


def align_rate(rate: RateLike, index: pd.DatetimeIndex) -> pd.Series:
    """Annual rate on every date of ``index`` (constants broadcast; Series forward-filled, no look-ahead; NaN->0)."""
    if isinstance(rate, pd.Series):
        return rate.reindex(rate.index.union(index)).ffill().reindex(index).fillna(0.0)
    return pd.Series(float(rate), index=index)


def daily_from_annual(annual: pd.Series, periods_per_year: int = 252) -> pd.Series:
    return (1.0 + annual) ** (1.0 / periods_per_year) - 1.0


def real_cagr(nominal_cagr: float, inflation_annual: float) -> float:
    """Inflation-adjusted CAGR: (1+nominal)/(1+inflation)-1."""
    return (1.0 + nominal_cagr) / (1.0 + inflation_annual) - 1.0
