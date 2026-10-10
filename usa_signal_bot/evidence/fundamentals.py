"""Point-in-time fundamentals from SEC EDGAR XBRL ``companyfacts`` (official JSON, via EdgarClient).

Look-ahead rule: a fact is usable only from its FILING date (``filed``); for restated periods the ORIGINAL (earliest
filed) value is kept, so later restatements never leak into the past. Values are forward-filled from their filing date.
Quality/value here are classic ratios (ROE, book-to-price); they still inherit EDGAR's coverage limits (US filers only,
tag variation between companies, no data before ~2009 for many small filers).

Split handling: yfinance prices are adjusted for splits as of TODAY while reported share counts are as filed, so pass the
split table (symbol,date,ratio) to ``fundamental_frames``; ``split_adjust_shares`` rescales filed counts to today's basis.
Without ``splits`` book_to_price is distorted around splits.
"""

from __future__ import annotations

from pathlib import Path
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


def split_adjust_shares(shares: pd.Series, splits: Optional[pd.DataFrame], symbol: str) -> pd.Series:
    """Restate as-filed share counts on today's split-adjusted basis (matches yfinance adjusted prices).

    Each value filed on date ``d`` is multiplied by the product of split ratios (``ratio`` 2.0 = 2-for-1) of splits
    dated AFTER ``d``. Splits on/before the filing date are already in the filed count.
    """
    if shares.empty or splits is None or len(splits) == 0:
        return shares
    sp = splits[splits["symbol"] == symbol]
    if sp.empty:
        return shares
    dates = pd.to_datetime(sp["date"]).to_numpy()
    ratios = sp["ratio"].astype(float).to_numpy()
    factors = [float(np.prod(ratios[dates > np.datetime64(d)])) for d in shares.index]
    return shares * np.array(factors)


def fundamental_frames(
    facts_by_symbol: Dict[str, Dict[str, Any]], prices: pd.DataFrame, splits: Optional[pd.DataFrame] = None
) -> Dict[str, pd.DataFrame]:
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
        shares_raw = split_adjust_shares(pit_series(facts, SHARES_TAGS, unit="shares"), splits, sym)
        shares = align_to_dates(shares_raw, prices.index)
        ni = align_to_dates(pit_series(facts, NET_INCOME_TAGS, forms=("10-K",)), prices.index)
        eq_10k = align_to_dates(pit_series(facts, EQUITY_TAGS, forms=("10-K",)), prices.index)
        mcap = shares * prices[sym]
        btp[sym] = (equity / mcap).where(mcap > 0)
        roe[sym] = (ni / eq_10k).where(eq_10k > 0)
    return {"book_to_price": btp, "roe": roe}




def compact_facts(facts: Dict[str, Any]) -> Dict[str, Any]:
    """Keep only the tags/units this module reads (companyfacts files are several MB each)."""
    out: Dict[str, Any] = {"facts": {"us-gaap": {}, "dei": {}}}
    gaap = (facts.get("facts") or {}).get("us-gaap") or {}
    dei = (facts.get("facts") or {}).get("dei") or {}
    keep = [("us-gaap", t, gaap) for t in EQUITY_TAGS + NET_INCOME_TAGS + SHARES_TAGS[1:]] + [("dei", SHARES_TAGS[0], dei)]
    for ns, tag, src in keep:
        node = src.get(tag)
        if not node:
            continue
        units = {u: [{k: r.get(k) for k in ("filed", "end", "val", "form")} for r in rows if r.get("form") in ("10-K", "10-Q")]
                 for u, rows in (node.get("units") or {}).items() if u in ("USD", "shares")}
        out["facts"][ns][tag] = {"units": units}
    return out


def fetch_fundamentals(client: EdgarClient, symbols: Iterable[str], out_dir: str | Path) -> Dict[str, str]:
    """Download compact companyfacts per symbol (official EDGAR JSON, <=10 req/s). Returns {symbol: status}."""
    import json
    from pathlib import Path as _P

    out = _P(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tickers = client.company_tickers()
    status: Dict[str, str] = {}
    for sym in symbols:
        target = out / f"{sym}.json"
        if target.exists():
            status[sym] = "cached"
            continue
        cik = tickers.get(sym.upper()) or tickers.get(sym.upper().replace(".", "-"))
        if cik is None:
            status[sym] = "no_cik"
            continue
        try:
            target.write_text(json.dumps(compact_facts(company_facts(client, cik))), encoding="utf-8")
            status[sym] = "ok"
        except Exception as exc:  # 404 for filers without XBRL facts etc.: report, do not hide
            status[sym] = f"error:{str(exc)[:60]}"
    return status


def load_fundamentals(directory: str | Path) -> Dict[str, Dict[str, Any]]:
    import json
    from pathlib import Path as _P

    return {p.stem.upper(): json.loads(p.read_text(encoding="utf-8")) for p in _P(directory).glob("*.json")}
