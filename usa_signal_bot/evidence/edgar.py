"""SEC EDGAR official JSON client for point-in-time membership/delisting metadata (no HTML scraping).

SEC fair-access rules: <= 10 requests/second and a descriptive User-Agent with contact info
(set ``SEC_USER_AGENT`` or pass ``user_agent``). Responses are cached on disk; time, sleep and the HTTP opener are
injected so tests never touch the network.

Limits (stated honestly): EDGAR gives delisting *filings* (Form 25 / 15-12) per CIK, not index-membership history
(e.g. S&P 500 changes) and not prices. Delisted tickers are absent from ``company_tickers.json``, so their CIKs must
be supplied by the caller. Prices of delisted names are usually missing from free feeds, so survivorship bias is
reduced only for names whose prices can be obtained.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import pandas as pd

COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
DELIST_FORMS = ("25", "25-NSE", "15-12B", "15-12G")


class RateLimiter:
    """Minimum-interval limiter (``max_per_sec`` requests per second)."""

    def __init__(self, max_per_sec: float = 8.0, clock: Callable[[], float] = time.monotonic, sleep: Callable[[float], None] = time.sleep):
        if not 0 < max_per_sec <= 10:
            raise ValueError("SEC allows at most 10 requests/second")
        self._gap = 1.0 / max_per_sec
        self._clock, self._sleep = clock, sleep
        self._last: Optional[float] = None

    def wait(self) -> None:
        now = self._clock()
        if self._last is not None and now - self._last < self._gap:
            self._sleep(self._gap - (now - self._last))
            now = self._last + self._gap
        self._last = now


def _default_opener(url: str, user_agent: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 - fixed https SEC hosts only
        return resp.read()


class EdgarClient:
    def __init__(
        self,
        cache_dir: str | Path,
        user_agent: Optional[str] = None,
        limiter: Optional[RateLimiter] = None,
        opener: Callable[[str, str], bytes] = _default_opener,
        max_age_days: float = 7.0,
        now: Callable[[], float] = time.time,
    ):
        ua = user_agent or os.environ.get("SEC_USER_AGENT", "")
        if "@" not in ua:
            raise ValueError("SEC requires a User-Agent with contact info, e.g. 'Name name@example.com' (SEC_USER_AGENT)")
        self.user_agent, self.cache = ua, Path(cache_dir)
        self.limiter, self._open = limiter or RateLimiter(), opener
        self.max_age, self._now = max_age_days * 86400, now
        self.network_calls = 0

    def _cache_path(self, url: str) -> Path:
        return self.cache / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".json")

    def get_json(self, url: str) -> Any:
        if not url.startswith(("https://www.sec.gov/", "https://data.sec.gov/")):
            raise ValueError("only official SEC hosts are allowed")
        path = self._cache_path(url)
        if path.exists() and self._now() - path.stat().st_mtime <= self.max_age:
            return json.loads(path.read_text(encoding="utf-8"))
        self.limiter.wait()
        self.network_calls += 1
        raw = self._open(url, self.user_agent)
        data = json.loads(raw)
        self.cache.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data), encoding="utf-8")
        os.replace(tmp, path)  # atomic
        return data

    def company_tickers(self) -> Dict[str, int]:
        """Current registrants: ticker -> CIK."""
        raw = self.get_json(COMPANY_TICKERS_URL)
        return {str(v["ticker"]).upper(): int(v["cik_str"]) for v in raw.values()}

    def submissions(self, cik: int) -> Any:
        return self.get_json(SUBMISSIONS_URL.format(cik=int(cik)))


def delisting_date(submissions: Dict[str, Any]) -> Optional[pd.Timestamp]:
    """Earliest delisting-type filing date (Form 25 / 15-12) in the recent-filings block, else None."""
    recent = (submissions.get("filings") or {}).get("recent") or {}
    forms, dates = recent.get("form") or [], recent.get("filingDate") or []
    hits = [pd.Timestamp(d) for f, d in zip(forms, dates) if str(f).upper() in DELIST_FORMS]
    return min(hits) if hits else None


def memberships_from_edgar(
    client: EdgarClient, entries: Iterable[Tuple[str, Optional[int]]], start: str
) -> Tuple[pd.DataFrame, List[str]]:
    """Frame (symbol,start,end) for ``(symbol, cik_or_None)`` entries. Returns (frame, symbols_without_cik).

    A missing CIK is resolved from current ``company_tickers``; unresolved symbols are returned, not guessed.
    The delisting filing date becomes the inclusive membership end.
    """
    current: Optional[Dict[str, int]] = None
    rows, unresolved = [], []
    for sym, cik in entries:
        if cik is None:
            if current is None:
                current = client.company_tickers()
            cik = current.get(sym.upper())
        if cik is None:
            unresolved.append(sym)
            continue
        end = delisting_date(client.submissions(cik))
        rows.append({"symbol": sym, "start": pd.Timestamp(start), "end": end if end is not None else pd.NaT})
    return pd.DataFrame(rows, columns=["symbol", "start", "end"]), unresolved
