"""Cross-sectional strategies on point-in-time fundamentals (frames from fundamentals.fundamental_frames)."""

from __future__ import annotations

import pandas as pd

from usa_signal_bot.evidence.factors import _top, _z


def value_fundamental_weights(prices: pd.DataFrame, members: pd.DataFrame, book_to_price: pd.DataFrame, top_frac: float = 0.3) -> pd.DataFrame:
    """Hold the highest book-to-price members (positive values only), equal weight."""
    score = book_to_price.where(book_to_price > 0)
    return _top(score, members, prices, top_frac)


def quality_fundamental_weights(prices: pd.DataFrame, members: pd.DataFrame, roe: pd.DataFrame, top_frac: float = 0.3) -> pd.DataFrame:
    return _top(roe, members, prices, top_frac)


def value_quality_weights(prices: pd.DataFrame, members: pd.DataFrame, book_to_price: pd.DataFrame, roe: pd.DataFrame, top_frac: float = 0.3) -> pd.DataFrame:
    mask = members & prices.notna()
    mix = (_z(book_to_price.where(mask & (book_to_price > 0))) + _z(roe.where(mask))) / 2.0
    return _top(mix, members, prices, top_frac)
