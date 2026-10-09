"""Download daily adjusted prices with yfinance into the CSV layout read by ``load_csv_market``.

Free, unofficial Yahoo endpoint: personal research use only; data may be revised or missing.
A hand-picked static ticker list is survivorship-biased by construction (see the report warning).
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Iterable, List

import pandas as pd

# Large, liquid US names across sectors (static list -> survivorship bias, stated in the report).
DEFAULT_TICKERS: List[str] = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "JPM", "BAC", "WFC", "C",
    "XOM", "CVX", "COP", "JNJ", "PFE", "MRK", "UNH", "ABT", "PG", "KO",
    "PEP", "WMT", "COST", "HD", "LOW", "MCD", "NKE", "DIS", "CMCSA", "VZ",
    "T", "INTC", "CSCO", "ORCL", "IBM", "TXN", "QCOM", "CAT", "DE", "BA",
    "HON", "GE", "MMM", "UPS", "LMT", "GS", "MS", "AXP", "AMGN", "GILD",
]


def fetch_daily(tickers: Iterable[str], out_dir: str, start: str = "2010-01-01", pause: float = 0.3) -> dict:
    import yfinance as yf  # imported lazily: only needed for downloads

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ok, failed, split_rows = [], [], []
    for sym in tickers:
        try:
            hist = yf.Ticker(sym).history(start=start, auto_adjust=True, actions=True)
        except Exception as exc:  # network / endpoint errors are reported, not hidden
            failed.append((sym, str(exc)[:80]))
            continue
        if hist is None or hist.empty or "Close" not in hist:
            failed.append((sym, "empty"))
            continue
        idx = pd.to_datetime(hist.index).tz_localize(None).normalize()
        frame = pd.DataFrame({"Date": idx, "Adj Close": hist["Close"].to_numpy()})
        frame = frame.dropna().drop_duplicates("Date")
        frame.to_csv(out / f"{sym}.csv", index=False)
        if "Stock Splits" in hist:
            for d, r in hist["Stock Splits"][hist["Stock Splits"] > 0].items():
                split_rows.append((sym, pd.Timestamp(d).tz_localize(None).normalize().date(), float(r)))
        ok.append(sym)
        time.sleep(pause)
    pd.DataFrame(split_rows, columns=["symbol", "date", "ratio"]).to_csv(out / "splits.csv", index=False)
    return {"ok": ok, "failed": failed, "splits": len(split_rows)}
