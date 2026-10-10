"""Adjusted-price validation against a corporate-action (split) table."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd


@dataclass(frozen=True)
class PriceIssue:
    symbol: str
    date: pd.Timestamp
    kind: str  # UNEXPLAINED_JUMP | UNADJUSTED_SPLIT | NON_POSITIVE_PRICE
    detail: str


_COMMON_SPLIT_RATIOS = (2.0, 3.0, 4.0, 5.0, 10.0, 20.0)
_SPLIT_DATE_SLACK_DAYS = 3


def _looks_like_split(r: float, tol: float = 0.02) -> bool:
    """True when ``1+r`` is close to the reciprocal of a common (forward or reverse) split ratio."""
    m = 1.0 + r
    return any(abs(m - 1.0 / k) < tol / k or abs(m - k) < tol * k for k in _COMMON_SPLIT_RATIOS)


def validate_adjusted_prices(
    prices: pd.DataFrame,
    splits: Optional[pd.DataFrame] = None,
    jump_threshold: float = 0.4,
    include_large_moves: bool = False,
) -> List[PriceIssue]:
    """Check that ``prices`` (dates x symbols, split-adjusted close) has no residual split artefacts.

    ``splits`` columns: symbol, date, ratio (e.g. 2.0 for a 2-for-1). A move that matches 1/ratio on
    (or within a few days of) a split date means the series was NOT adjusted (UNADJUSTED_SPLIT).
    A big move with no split on file that is shaped like a common split ratio is UNEXPLAINED_JUMP
    (possible missing split row). Any other big one-day move is a real market event (earnings gap,
    the March 2020 crash...) and is only reported as LARGE_MOVE when ``include_large_moves`` is set.
    """
    issues: List[PriceIssue] = []
    split_map: Dict[str, Dict[pd.Timestamp, float]] = {}
    if splits is not None and len(splits):
        for row in splits.itertuples(index=False):
            split_map.setdefault(str(row.symbol), {})[pd.Timestamp(row.date)] = float(row.ratio)
    for sym in prices.columns:
        s = prices[sym].dropna()
        for d in s.index[s <= 0]:
            issues.append(PriceIssue(sym, d, "NON_POSITIVE_PRICE", f"price={s.loc[d]}"))
        s = s[s > 0]
        ret = s.pct_change().dropna()
        for d, r in ret.items():
            if abs(r) < jump_threshold:
                continue
            near = [
                k for sd, k in split_map.get(sym, {}).items()
                if abs((sd - d).days) <= _SPLIT_DATE_SLACK_DAYS
            ]
            if near:
                if any(abs((1.0 + r) - 1.0 / k) < 0.08 or abs((1.0 + r) - k) < 0.08 * k for k in near):
                    issues.append(PriceIssue(sym, d, "UNADJUSTED_SPLIT", f"move={r:.2%}, split ratio={near[0]}"))
            elif _looks_like_split(r):
                issues.append(PriceIssue(sym, d, "UNEXPLAINED_JUMP", f"move={r:.2%}"))
            elif include_large_moves:
                issues.append(PriceIssue(sym, d, "LARGE_MOVE", f"move={r:.2%}"))
    return issues
