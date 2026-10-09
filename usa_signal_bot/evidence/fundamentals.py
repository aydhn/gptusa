"""Point-in-time fundamentals from SEC EDGAR XBRL ``companyfacts`` (official JSON, via EdgarClient).

Look-ahead rule: a fact is usable only from its FILING date (``filed``); for restated periods the ORIGINAL (earliest
filed) value is kept, so later restatements never leak into the past. Values are forward-filled from their filing date.
Quality/value here are classic ratios (ROE, book-to-price); they still inherit EDGAR's coverage limits (US filers only,
tag variation between companies, no data before ~2009 for many small filers).

KNOWN DEFECT: yfinance prices are adjusted for splits as of TODAY while reported share counts are as filed at the time,
so book_to_price is distorted around splits (shares*price jumps). Treat results as indicative; fix needs split-aware
share counts (Aşama: use evidence/corporate_actions split table to rescale shares).
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

import numpy as np
import pandas as pd

from usa_signal_bot.evidence.edgar import EdgarClient

COMPANY_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
EQUITY_TAGS = ("StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest")
NET_INCOME_TAGS = ("NetIncomeLoss", "ProfitLoss")
SHARES_TAGS = ("EntityCommonStockSharesOutstanding", "WeightedAverageNumberOfSharesOutstandingBasic")


def company_facts(client: EdgarClient, cik: int) -> Dict[str, Any]:
    return client.get_json(COMPANY_FACTS_URL.format(cik=int(cik)))


def pit_series(facts: Dict[str, Any], tags: Iterable[str], unit: str = "USD", forms: Optional[tuple] = ("10-K", "10-Q")) -> pd.Series:
    """Series indexed by FILING date: originally-filed value per period end, first matching tag wins.

    Returns an empty Series when no tag/unit is present.
    """
    gaap = (facts.get("facts") or {}).get("us-gaap") or {}
    dei = (facts.get("facts") or {}).get("dei") or {}
    for tag in tags:
        node = gaap.get(tag) or dei.get(tag)
        rows: List[Dict[str, Any]] = ((node or {}).get("units") or {}).get(unit) or []
        rows = [r for r in rows if r.get("filed") and r.get("val") is not None and (forms is None or r.get("form") in forms)]
        if not rows:
            continue
        df = pd.DataFrame(rows)
        df["filed"] = pd.to_datetime(df["filed"])
        df["end"] = pd.to_datetime(df["end"])
        first = df.sort_values("filed").drop_duplicates("end", keep="first")  # original, not restated, value
        s = first.set_index("filed")["val"].astype(float).sort_index()
        return s[~s.index.duplicated(keep="last")]
    return pd.Series(dtype=float)


def align_to_dates(series: pd.Series, index: pd.DatetimeIndex) -> pd.Series:
    """Forward-fill filing-dated values onto trading dates (NaN before the first filing)."""
    if series.empty:
        return pd.Series(np.nan, index=index)
    return series.reindex(series.index.union(index)).ffill().reindex(index)


def fundamental_frames(facts_by_symbol: Dict[str, Dict[str, Any]], prices: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Dates x symbols frames: ``book_to_price`` (equity / (shares * price)) and ``roe`` (annualised NI / equity).

    Net income from 10-Q filings is a quarterly/YTD figure and is not de-cumulated here; ROE therefore uses only the
    most recent 10-K value (``forms=("10-K",)``), which is conservative but unambiguous.
    """
    btp = pd.DataFrame(np.nan, index=prices.index, columns=prices.columns)
    roe = btp.copy()
    for sym, facts in facts_by_symbol.items():
        if sym not in prices.columns:
            continue
        equity = align_to_dates(pit_series(facts, EQUITY_TAGS), prices.index)
        shares = align_to_dates(pit_series(facts, SHARES_TAGS, unit="shares"), prices.index)
        ni = align_to_dates(pit_series(facts, NET_INCOME_TAGS, forms=("10-K",)), prices.index)
        eq_10k = align_to_dates(pit_series(facts, EQUITY_TAGS, forms=("10-K",)), prices.index)
        mcap = shares * prices[sym]
        btp[sym] = (equity / mcap).where(mcap > 0)
        roe[sym] = (ni / eq_10k).where(eq_10k > 0)
    return {"book_to_price": btp, "roe": roe}
