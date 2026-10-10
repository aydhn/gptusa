"""Post-filing drift (PEAD-style) from cached EDGAR XBRL filing dates. CANDIDATE family.

Data limits (stated honestly): compact XBRL facts carry the 10-K/10-Q FILING date, not the earnings-announcement date
(the press release is usually days to weeks earlier), so the price reaction measured here is partly stale. No consensus
estimates exist, so "surprise" is proxied by (a) ``reaction``: market-relative return over the filing day and the next
day, or (b) ``ni_growth``: sign of year-over-year change in annual (10-K) net income.

Point-in-time: an event filed on date f is mapped to the first trading day p >= f; the signal becomes available at
row p+1 (the reaction window closes at p+1; also covers filings after the close) and persists ``hold`` rows. Weights at
row t are held over t+1, so entry is the day after the information is complete. Long-only tilt on the equal-weight market.
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd

from usa_signal_bot.evidence.factors_rel import _beta
from usa_signal_bot.evidence.fundamentals import EQUITY_TAGS, NET_INCOME_TAGS, SHARES_TAGS, pit_series


def filing_dates(facts: Dict[str, Any]) -> pd.DatetimeIndex:
    """All 10-K/10-Q filing dates present in the cached facts (union over the tags the compact file keeps)."""
    found = set()
    for tags, unit in ((EQUITY_TAGS, "USD"), (NET_INCOME_TAGS, "USD"), (SHARES_TAGS, "shares")):
        found |= set(pit_series(facts, tags, unit=unit).index)
    return pd.DatetimeIndex(sorted(found))


def _event_frames(facts_by_symbol: Dict[str, Dict[str, Any]], prices: pd.DataFrame):
    """(signal-available-row mask of filing events, NI-growth sign at those rows) as dates x symbols frames."""
    idx = prices.index
    mask = pd.DataFrame(False, index=idx, columns=prices.columns)
    nig = pd.DataFrame(np.nan, index=idx, columns=prices.columns)
    for sym, facts in facts_by_symbol.items():
        if sym not in prices.columns:
            continue
        col = mask.columns.get_loc(sym)
        fd = filing_dates(facts)
        fd = fd[(fd >= idx[0]) & (fd <= idx[-1])]
        avail = np.unique(idx.searchsorted(fd, side="left") + 1)
        avail = avail[avail < len(idx)]
        mask.iloc[avail, col] = True
        ni = pit_series(facts, NET_INCOME_TAGS, forms=("10-K",))
        if len(ni) > 1:
            sign = np.sign(ni.diff().dropna())
            sign = sign[(sign.index >= idx[0]) & (sign.index <= idx[-1])]
            sp = idx.searchsorted(sign.index, side="left") + 1
            for p, v in zip(sp, sign.to_numpy()):
                if p < len(idx):
                    nig.iat[p, col] = v
    return mask, nig


def earnings_drift_weights(
    prices: pd.DataFrame, members: pd.DataFrame, facts_by_symbol: Dict[str, Dict[str, Any]],
    mode: str = "reaction", hold: int = 40, tilt: float = 0.5,
) -> pd.DataFrame:
    """Equal-weight market, scaled by (1 + tilt * sign) while a filing signal is active (sign +1/-1), renormalised to 1."""
    base = _beta(prices, members)
    ev_mask, nig = _event_frames(facts_by_symbol, prices)
    if mode == "reaction":
        r = prices.pct_change(fill_method=None)
        ex = r.sub(r.where(members).mean(axis=1), axis=0)
        react = (1.0 + ex.shift(1)) * (1.0 + ex) - 1.0  # closes at row t, uses rows t-1 and t only
        sig = np.sign(react.where(ev_mask))
    elif mode == "ni_growth":
        sig = nig.where(ev_mask)
    else:
        raise ValueError(f"unknown mode {mode}")
    sig = sig.ffill(limit=hold).fillna(0.0)
    w = (base * (1.0 + tilt * sig)).clip(lower=0.0)
    return w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


EARNINGS_GRID = [{"mode": m, "hold": h, "tilt": t} for m in ("reaction", "ni_growth") for h in (20, 60) for t in (0.5, 1.0)]
