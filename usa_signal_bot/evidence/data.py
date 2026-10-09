"""Data sources for the evidence pipeline: local CSV files or a deterministic synthetic market."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class MarketData:
    prices: pd.DataFrame  # split/dividend-adjusted close, dates x symbols (NaN outside life)
    memberships: pd.DataFrame  # symbol, start, end
    splits: pd.DataFrame  # symbol, date, ratio
    label: str  # "SYNTHETIC" or "CSV:<dir>"
    static_universe: bool = False  # True: no point-in-time membership file (survivorship bias)


def synthetic_market(seed: int = 7, n_symbols: int = 30, n_days: int = 2600) -> MarketData:
    """Random-walk market with a common factor, late joiners and delistings. No true alpha by design."""
    rng = np.random.default_rng(seed)
    index = pd.bdate_range("2012-01-02", periods=n_days)
    mkt = rng.normal(0.0004, 0.010, n_days)
    cols = {}
    rows = []
    for i in range(n_symbols):
        beta = rng.uniform(0.6, 1.4)
        idio = rng.normal(0.0, rng.uniform(0.008, 0.02), n_days)
        ret = beta * mkt + idio
        px = 50.0 * np.exp(np.cumsum(ret))
        sym = f"SYN{i:02d}"
        start = 0 if i < n_symbols * 0.7 else int(rng.integers(200, n_days // 2))
        end = None if i % 5 else int(rng.integers(n_days // 2, n_days - 100))
        s = pd.Series(px, index=index, name=sym)
        if start:
            s.iloc[:start] = np.nan
        if end is not None:
            s.iloc[end + 1 :] = np.nan
        cols[sym] = s
        rows.append(
            (sym, index[start], index[end] if end is not None else pd.NaT)
        )
    prices = pd.DataFrame(cols)
    memberships = pd.DataFrame(rows, columns=["symbol", "start", "end"])
    splits = pd.DataFrame(
        [("SYN00", index[int(n_days * 0.35)], 2.0), ("SYN03", index[int(n_days * 0.6)], 3.0)], columns=["symbol", "date", "ratio"]
    )
    return MarketData(prices, memberships, splits, "SYNTHETIC")


def load_csv_market(directory: str, memberships_csv: Optional[str] = None) -> MarketData:
    """Load ``<SYMBOL>.csv`` files (Date + Adj Close/Close). Without a membership file the universe is
    static - which carries survivorship bias; the report states this."""
    base = Path(directory)
    cols = {}
    for path in sorted(base.glob("*.csv")):
        if path.stem.lower() in {"memberships", "splits"}:
            continue
        frame = pd.read_csv(path)
        frame.columns = [str(c).strip().lower().replace(" ", "_") for c in frame.columns]
        px_col = "adj_close" if "adj_close" in frame.columns else "close"
        frame["date"] = pd.to_datetime(frame["date"])
        cols[path.stem.upper()] = frame.set_index("date")[px_col].astype(float).sort_index()
    if not cols:
        raise FileNotFoundError(f"no CSV price files in {directory}")
    prices = pd.DataFrame(cols).sort_index()
    if memberships_csv:
        mem = pd.read_csv(memberships_csv, parse_dates=["start", "end"])
    else:
        first = prices.apply(lambda s: s.first_valid_index())
        last = prices.apply(lambda s: s.last_valid_index())
        mem = pd.DataFrame({"symbol": prices.columns, "start": first.values, "end": last.values})
        mem.loc[mem["end"] == prices.index[-1], "end"] = pd.NaT
    splits_path = base / "splits.csv"
    splits = (
        pd.read_csv(splits_path, parse_dates=["date"])
        if splits_path.exists()
        else pd.DataFrame(columns=["symbol", "date", "ratio"])
    )
    return MarketData(prices, mem, splits, f"CSV:{directory}", static_universe=memberships_csv is None)
