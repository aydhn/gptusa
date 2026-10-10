"""Macro regime filter from FRED series (T10Y2Y, VIXCLS, BAA10Y). CANDIDATE family, evaluated like every other.

Look-ahead rule: the macro value used for decision date t is the last value published on or before t-1
(``shift(1)`` after forward-filling onto trading dates), a conservative extra day of lag. Weights at t are then
held over t+1 by ``backtest_weights``. Risk-on: equal-weight market (beta); risk-off: ``off_exposure`` of it (rest cash).
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Optional

import numpy as np
import pandas as pd

from usa_signal_bot.evidence.factors_rel import _beta
from usa_signal_bot.evidence.rates import fetch_fred_csv, load_rate_csv

MACRO_SERIES = ("T10Y2Y", "VIXCLS", "BAA10Y")


def fetch_macro(out_dir: str | Path, series: Iterable[str] = MACRO_SERIES, max_age_days: float = 1.0) -> Dict[str, str]:
    """Download public FRED CSVs into ``out_dir`` (cached while younger than ``max_age_days``). Returns {series: status}."""
    import time

    out = Path(out_dir)
    status: Dict[str, str] = {}
    for sid in series:
        target = out / f"{sid}.csv"
        if target.exists() and time.time() - target.stat().st_mtime <= max_age_days * 86400:
            status[sid] = "cached"
            continue
        try:
            fetch_fred_csv(sid, target)
            status[sid] = "ok"
        except Exception as exc:  # offline etc.: reported, not hidden
            status[sid] = f"error:{str(exc)[:60]}"
    return status


def load_macro(directory: str | Path, series: Iterable[str] = MACRO_SERIES) -> Dict[str, pd.Series]:
    """Load cached FRED CSVs (raw units, e.g. VIX level or spread in percentage points). Missing files are skipped."""
    out: Dict[str, pd.Series] = {}
    for sid in series:
        p = Path(directory) / f"{sid}.csv"
        if p.exists():
            s = load_rate_csv(p, percent=False)
            if not s.empty:
                out[sid] = s
    return out


def lagged_to_trading_days(series: pd.Series, index: pd.DatetimeIndex, lag: int = 1) -> pd.Series:
    """Last published value as of each trading day, then lagged ``lag`` (>=1) trading days: value known at t-1."""
    if lag < 1:
        raise ValueError("lag must be >= 1 (no same-day macro value)")
    s = series.sort_index()
    return s.reindex(s.index.union(index)).ffill().reindex(index).shift(lag)


def risk_on_signal(series: pd.Series, index: pd.DatetimeIndex, signal: str, param: float) -> pd.Series:
    """Boolean risk-on per trading day (NaN signal -> True: stay in the benchmark until a signal exists).

    VIXCLS: on if lagged VIX < ``param``. T10Y2Y: on if lagged spread > ``param``.
    BAA10Y: on if lagged credit spread < its trailing ``int(param)``-day mean (spread not widening).
    """
    x = lagged_to_trading_days(series, index)
    if signal == "VIXCLS":
        on, valid = x < param, x.notna()
    elif signal == "T10Y2Y":
        on, valid = x > param, x.notna()
    elif signal == "BAA10Y":
        w = int(param)
        m = x.rolling(w, min_periods=w).mean()
        on, valid = x < m, m.notna()
    else:
        raise ValueError(f"unknown macro signal {signal}")
    return (on | ~valid).astype(bool)


def macro_regime_weights(
    prices: pd.DataFrame, members: pd.DataFrame, macro: Dict[str, pd.Series], signal: str = "VIXCLS",
    param: float = 25.0, off_exposure: float = 0.0,
) -> pd.DataFrame:
    """Equal-weight market while risk-on, ``off_exposure`` of it (rest idle cash) while risk-off. All-cash if series absent."""
    base = _beta(prices, members)
    if signal not in macro:
        return base * 0.0
    on = risk_on_signal(macro[signal], prices.index, signal, param)
    scale = on.astype(float) + (~on).astype(float) * off_exposure
    return base.mul(scale, axis=0)


MACRO_GRID = (
    [{"signal": "VIXCLS", "param": v, "off_exposure": e} for v in (20.0, 25.0, 30.0) for e in (0.0, 0.5)]
    + [{"signal": "T10Y2Y", "param": t, "off_exposure": e} for t in (0.0, 0.5) for e in (0.0, 0.5)]
    + [{"signal": "BAA10Y", "param": w, "off_exposure": e} for w in (126, 252) for e in (0.0, 0.5)]
)
