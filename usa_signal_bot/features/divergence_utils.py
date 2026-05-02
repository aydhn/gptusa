import pandas as pd
import numpy as np
from typing import List, Tuple
from usa_signal_bot.core.enums import DivergenceType, DivergenceSource, PivotType, DivergenceStrength, DivergenceConfirmationMode
from usa_signal_bot.features.divergence_models import PivotPoint, DivergencePair

def validate_divergence_windows(left_window: int, right_window: int, max_pivot_distance: int) -> None:
    if left_window <= 0:
        raise ValueError("left_window must be > 0")
    if right_window < 0:
        raise ValueError("right_window must be >= 0")
    if max_pivot_distance < 0:
        raise ValueError("max_pivot_distance must be >= 0")

def pct_change_between_values(v1: float, v2: float) -> float:
    if v1 == 0:
        return 0.0
    return ((v2 - v1) / abs(v1)) * 100.0

def find_confirmed_pivot_highs(series: pd.Series, left_window: int = 2, right_window: int = 2) -> List[PivotPoint]:
    pivots = []
    if len(series) < left_window + right_window + 1:
        return pivots

    for i in range(left_window, len(series) - right_window):
        val = series.iloc[i]
        if pd.isna(val):
            continue

        is_pivot = True
        for j in range(i - left_window, i + right_window + 1):
            if i == j:
                continue
            comp = series.iloc[j]
            if pd.isna(comp) or comp >= val:
                is_pivot = False
                break

        if is_pivot:
            ts = series.index[i]
            if hasattr(ts, 'isoformat'):
                ts = ts.isoformat()
            else:
                ts = str(ts)
            pivots.append(PivotPoint(index=i, value=float(val), pivot_type=PivotType.PRICE_HIGH, timestamp_utc=ts))

    return pivots

def find_confirmed_pivot_lows(series: pd.Series, left_window: int = 2, right_window: int = 2) -> List[PivotPoint]:
    pivots = []
    if len(series) < left_window + right_window + 1:
        return pivots

    for i in range(left_window, len(series) - right_window):
        val = series.iloc[i]
        if pd.isna(val):
            continue

        is_pivot = True
        for j in range(i - left_window, i + right_window + 1):
            if i == j:
                continue
            comp = series.iloc[j]
            if pd.isna(comp) or comp <= val:
                is_pivot = False
                break

        if is_pivot:
            ts = series.index[i]
            if hasattr(ts, 'isoformat'):
                ts = ts.isoformat()
            else:
                ts = str(ts)
            pivots.append(PivotPoint(index=i, value=float(val), pivot_type=PivotType.PRICE_LOW, timestamp_utc=ts))

    return pivots

def find_left_only_pivot_highs(series: pd.Series, left_window: int = 5) -> List[PivotPoint]:
    pivots = []
    if len(series) < left_window + 1:
        return pivots

    for i in range(left_window, len(series)):
        val = series.iloc[i]
        if pd.isna(val):
            continue

        is_pivot = True
        for j in range(i - left_window, i):
            comp = series.iloc[j]
            if pd.isna(comp) or comp >= val:
                is_pivot = False
                break

        if is_pivot:
            ts = series.index[i]
            if hasattr(ts, 'isoformat'):
                ts = ts.isoformat()
            else:
                ts = str(ts)
            pivots.append(PivotPoint(index=i, value=float(val), pivot_type=PivotType.PRICE_HIGH, timestamp_utc=ts))

    return pivots

def find_left_only_pivot_lows(series: pd.Series, left_window: int = 5) -> List[PivotPoint]:
    pivots = []
    if len(series) < left_window + 1:
        return pivots

    for i in range(left_window, len(series)):
        val = series.iloc[i]
        if pd.isna(val):
            continue

        is_pivot = True
        for j in range(i - left_window, i):
            comp = series.iloc[j]
            if pd.isna(comp) or comp <= val:
                is_pivot = False
                break

        if is_pivot:
            ts = series.index[i]
            if hasattr(ts, 'isoformat'):
                ts = ts.isoformat()
            else:
                ts = str(ts)
            pivots.append(PivotPoint(index=i, value=float(val), pivot_type=PivotType.PRICE_LOW, timestamp_utc=ts))

    return pivots

def align_price_and_oscillator_pivots(price_pivots: List[PivotPoint], osc_pivots: List[PivotPoint], max_distance: int = 5) -> List[Tuple[PivotPoint, PivotPoint]]:
    aligned = []
    for pp in price_pivots:
        best_op = None
        best_dist = max_distance + 1

        for op in osc_pivots:
            dist = abs(pp.index - op.index)
            if dist <= max_distance and dist < best_dist:
                best_dist = dist
                best_op = op

        if best_op:
            aligned.append((pp, best_op))

    return aligned

def calculate_divergence_strength(price_change_pct: float, osc_change_pct: float, pivot_distance: int) -> float:
    # A simple scoring mechanism based on price and oscillator change magnitudes
    # The larger the opposing movement, the stronger the divergence
    diff = abs(price_change_pct) + abs(osc_change_pct)
    # Penalize long distances slightly
    score = diff / max(1, (pivot_distance * 0.1))
    # Normalize to 0-100 loosely
    score = min(100.0, max(0.0, score * 5))
    return score

def classify_divergence_strength(score: float) -> DivergenceStrength:
    if score < 20:
        return DivergenceStrength.WEAK
    elif score < 50:
        return DivergenceStrength.MODERATE
    elif score < 80:
        return DivergenceStrength.STRONG
    else:
        return DivergenceStrength.VERY_STRONG

def detect_regular_bullish_divergence(price_lows: List[PivotPoint], osc_lows: List[PivotPoint], source: DivergenceSource, max_pivot_distance: int = 5, min_price_change_pct: float = 0.0, min_osc_change_pct: float = 0.0) -> List[DivergencePair]:
    pairs = []
    aligned = align_price_and_oscillator_pivots(price_lows, osc_lows, max_distance=max_pivot_distance)

    for i in range(len(aligned) - 1):
        pp1, op1 = aligned[i]
        pp2, op2 = aligned[i+1]

        if pp1.index >= pp2.index or op1.index >= op2.index:
            continue

        price_chg = pct_change_between_values(pp1.value, pp2.value)
        osc_chg = pct_change_between_values(op1.value, op2.value)

        # Regular Bullish: Price Lower Low, Osc Higher Low
        if price_chg < -min_price_change_pct and osc_chg > min_osc_change_pct:
            strength = calculate_divergence_strength(price_chg, osc_chg, pp2.index - pp1.index)
            pairs.append(DivergencePair(
                price_pivot_1=pp1, price_pivot_2=pp2,
                osc_pivot_1=op1, osc_pivot_2=op2,
                divergence_type=DivergenceType.REGULAR_BULLISH,
                source=source,
                strength_score=strength,
                confirmation_mode=DivergenceConfirmationMode.UNKNOWN # Will be set by indicator
            ))

    return pairs

def detect_regular_bearish_divergence(price_highs: List[PivotPoint], osc_highs: List[PivotPoint], source: DivergenceSource, max_pivot_distance: int = 5, min_price_change_pct: float = 0.0, min_osc_change_pct: float = 0.0) -> List[DivergencePair]:
    pairs = []
    aligned = align_price_and_oscillator_pivots(price_highs, osc_highs, max_distance=max_pivot_distance)

    for i in range(len(aligned) - 1):
        pp1, op1 = aligned[i]
        pp2, op2 = aligned[i+1]

        if pp1.index >= pp2.index or op1.index >= op2.index:
            continue

        price_chg = pct_change_between_values(pp1.value, pp2.value)
        osc_chg = pct_change_between_values(op1.value, op2.value)

        # Regular Bearish: Price Higher High, Osc Lower High
        if price_chg > min_price_change_pct and osc_chg < -min_osc_change_pct:
            strength = calculate_divergence_strength(price_chg, osc_chg, pp2.index - pp1.index)
            pairs.append(DivergencePair(
                price_pivot_1=pp1, price_pivot_2=pp2,
                osc_pivot_1=op1, osc_pivot_2=op2,
                divergence_type=DivergenceType.REGULAR_BEARISH,
                source=source,
                strength_score=strength,
                confirmation_mode=DivergenceConfirmationMode.UNKNOWN
            ))

    return pairs

def detect_hidden_bullish_divergence(price_lows: List[PivotPoint], osc_lows: List[PivotPoint], source: DivergenceSource, max_pivot_distance: int = 5, min_price_change_pct: float = 0.0, min_osc_change_pct: float = 0.0) -> List[DivergencePair]:
    pairs = []
    aligned = align_price_and_oscillator_pivots(price_lows, osc_lows, max_distance=max_pivot_distance)

    for i in range(len(aligned) - 1):
        pp1, op1 = aligned[i]
        pp2, op2 = aligned[i+1]

        if pp1.index >= pp2.index or op1.index >= op2.index:
            continue

        price_chg = pct_change_between_values(pp1.value, pp2.value)
        osc_chg = pct_change_between_values(op1.value, op2.value)

        # Hidden Bullish: Price Higher Low, Osc Lower Low
        if price_chg > min_price_change_pct and osc_chg < -min_osc_change_pct:
            strength = calculate_divergence_strength(price_chg, osc_chg, pp2.index - pp1.index)
            pairs.append(DivergencePair(
                price_pivot_1=pp1, price_pivot_2=pp2,
                osc_pivot_1=op1, osc_pivot_2=op2,
                divergence_type=DivergenceType.HIDDEN_BULLISH,
                source=source,
                strength_score=strength,
                confirmation_mode=DivergenceConfirmationMode.UNKNOWN
            ))

    return pairs

def detect_hidden_bearish_divergence(price_highs: List[PivotPoint], osc_highs: List[PivotPoint], source: DivergenceSource, max_pivot_distance: int = 5, min_price_change_pct: float = 0.0, min_osc_change_pct: float = 0.0) -> List[DivergencePair]:
    pairs = []
    aligned = align_price_and_oscillator_pivots(price_highs, osc_highs, max_distance=max_pivot_distance)

    for i in range(len(aligned) - 1):
        pp1, op1 = aligned[i]
        pp2, op2 = aligned[i+1]

        if pp1.index >= pp2.index or op1.index >= op2.index:
            continue

        price_chg = pct_change_between_values(pp1.value, pp2.value)
        osc_chg = pct_change_between_values(op1.value, op2.value)

        # Hidden Bearish: Price Lower High, Osc Higher High
        if price_chg < -min_price_change_pct and osc_chg > min_osc_change_pct:
            strength = calculate_divergence_strength(price_chg, osc_chg, pp2.index - pp1.index)
            pairs.append(DivergencePair(
                price_pivot_1=pp1, price_pivot_2=pp2,
                osc_pivot_1=op1, osc_pivot_2=op2,
                divergence_type=DivergenceType.HIDDEN_BEARISH,
                source=source,
                strength_score=strength,
                confirmation_mode=DivergenceConfirmationMode.UNKNOWN
            ))

    return pairs

def latest_divergence_summary(pairs: List[DivergencePair]) -> Tuple[DivergenceType, float]:
    if not pairs:
        return DivergenceType.NONE, 0.0
    # Find the pair with the highest index for price_pivot_2
    latest_pair = max(pairs, key=lambda p: p.price_pivot_2.index)
    return latest_pair.divergence_type, latest_pair.strength_score

def build_divergence_feature_series(df: pd.DataFrame, pairs: List[DivergencePair], prefix: str) -> pd.DataFrame:
    res = df.copy()

    # Initialize columns
    res[f"{prefix}_regular_bullish_divergence"] = 0
    res[f"{prefix}_regular_bearish_divergence"] = 0
    res[f"{prefix}_hidden_bullish_divergence"] = 0
    res[f"{prefix}_hidden_bearish_divergence"] = 0
    res[f"{prefix}_divergence_strength"] = 0.0
    res[f"{prefix}_latest_divergence_code"] = 0

    # Sort pairs by detection index (price_pivot_2.index)
    sorted_pairs = sorted(pairs, key=lambda p: p.price_pivot_2.index)

    # We populate values based on when they are "detected" which is price_pivot_2.index + right_window
    # But for feature series representing the "state" at that bar, we can set the value at the pivot point itself
    # Note: Using confirmed pivot implies looking ahead if we set it at the pivot index.
    # To be safe for feature generation, we place the signal at the pivot index.
    # The indicator will be responsible for documenting the lookahead bias if using confirmed pivots.

    for p in sorted_pairs:
        idx = p.price_pivot_2.index
        if idx >= len(res):
            continue

        strength = p.strength_score

        if p.divergence_type == DivergenceType.REGULAR_BULLISH:
            res.iloc[idx, res.columns.get_loc(f"{prefix}_regular_bullish_divergence")] = 1
            res.iloc[idx, res.columns.get_loc(f"{prefix}_latest_divergence_code")] = 1
            res.iloc[idx, res.columns.get_loc(f"{prefix}_divergence_strength")] = strength
        elif p.divergence_type == DivergenceType.REGULAR_BEARISH:
            res.iloc[idx, res.columns.get_loc(f"{prefix}_regular_bearish_divergence")] = 1
            res.iloc[idx, res.columns.get_loc(f"{prefix}_latest_divergence_code")] = -1
            res.iloc[idx, res.columns.get_loc(f"{prefix}_divergence_strength")] = strength
        elif p.divergence_type == DivergenceType.HIDDEN_BULLISH:
            res.iloc[idx, res.columns.get_loc(f"{prefix}_hidden_bullish_divergence")] = 1
            res.iloc[idx, res.columns.get_loc(f"{prefix}_latest_divergence_code")] = 2
            res.iloc[idx, res.columns.get_loc(f"{prefix}_divergence_strength")] = strength
        elif p.divergence_type == DivergenceType.HIDDEN_BEARISH:
            res.iloc[idx, res.columns.get_loc(f"{prefix}_hidden_bearish_divergence")] = 1
            res.iloc[idx, res.columns.get_loc(f"{prefix}_latest_divergence_code")] = -2
            res.iloc[idx, res.columns.get_loc(f"{prefix}_divergence_strength")] = strength

    return res
