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


def validate_adjusted_prices(
    prices: pd.DataFrame,
    splits: Optional[pd.DataFrame] = None,
    jump_threshold: float = 0.4,
) -> List[PriceIssue]:
    """Check that ``prices`` (dates x symbols, split-adjusted close) has no residual split artefacts.

    ``splits`` columns: symbol, date, ratio (e.g. 2.0 for a 2-for-1). A one-day move beyond
    ``jump_threshold`` that is not near any split ratio is flagged UNEXPLAINED_JUMP; a move that
    matches 1/ratio on a split date means the series was NOT adjusted (UNADJUSTED_SPLIT).
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
            ratio = split_map.get(sym, {}).get(d)
            if ratio is not None and abs((1.0 + r) - 1.0 / ratio) < 0.08:
                issues.append(PriceIssue(sym, d, "UNADJUSTED_SPLIT", f"move={r:.2%}, split ratio={ratio}"))
            elif ratio is None:
                issues.append(PriceIssue(sym, d, "UNEXPLAINED_JUMP", f"move={r:.2%}"))
    return issues
