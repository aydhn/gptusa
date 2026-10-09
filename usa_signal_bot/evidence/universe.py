"""Point-in-time universe: who was a member on a given date (no look-ahead, no survivorship)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

import pandas as pd


@dataclass(frozen=True)
class Membership:
    symbol: str
    start: pd.Timestamp
    end: Optional[pd.Timestamp] = None  # inclusive; None = still a member


class PointInTimeUniverse:
    """Membership intervals per symbol. ``members(date)`` only uses intervals known by ``date``."""

    def __init__(self, memberships: Iterable[Membership]):
        self._items: List[Membership] = list(memberships)

    @classmethod
    def from_frame(cls, frame: pd.DataFrame) -> "PointInTimeUniverse":
        """Frame columns: symbol, start, end (end may be NaT/empty)."""
        items = []
        for row in frame.itertuples(index=False):
            end = None if pd.isna(row.end) else pd.Timestamp(row.end)
            items.append(Membership(str(row.symbol), pd.Timestamp(row.start), end))
        return cls(items)

    @classmethod
    def static(cls, symbols: Iterable[str], start: pd.Timestamp) -> "PointInTimeUniverse":
        """Static list. NOTE: reintroduces survivorship bias if the list is built today."""
        return cls(Membership(s, pd.Timestamp(start), None) for s in symbols)

    def members(self, date: pd.Timestamp) -> List[str]:
        d = pd.Timestamp(date)
        return sorted({m.symbol for m in self._items if m.start <= d and (m.end is None or d <= m.end)})

    def membership_matrix(self, index: pd.DatetimeIndex, symbols: Iterable[str]) -> pd.DataFrame:
        """Boolean matrix (dates x symbols): True when the symbol was a member that day."""
        cols = list(symbols)
        out = pd.DataFrame(False, index=index, columns=cols)
        for m in self._items:
            if m.symbol not in out.columns:
                continue
            mask = index >= m.start
            if m.end is not None:
                mask = mask & (index <= m.end)
            out.loc[mask, m.symbol] = True
        return out
