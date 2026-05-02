import pytest
import pandas as pd
from usa_signal_bot.core.enums import DivergenceType, DivergenceSource, PivotType, DivergenceStrength, DivergenceConfirmationMode
from usa_signal_bot.features.divergence_models import PivotPoint, DivergencePair
from usa_signal_bot.features.divergence_utils import (
    find_confirmed_pivot_highs, find_confirmed_pivot_lows,
    find_left_only_pivot_highs, find_left_only_pivot_lows,
    align_price_and_oscillator_pivots, detect_regular_bullish_divergence,
    detect_regular_bearish_divergence, detect_hidden_bullish_divergence,
    detect_hidden_bearish_divergence, calculate_divergence_strength,
    classify_divergence_strength, build_divergence_feature_series, validate_divergence_windows
)

def test_find_confirmed_pivot_highs():
    s = pd.Series([10, 11, 12, 11, 10, 15, 14, 13])
    # with left=2, right=2
    # index 2 is 12 (neighbors: 10,11, 11,10) -> True
    # index 5 is 15 (neighbors: 11,10, 14,13) -> True
    pivots = find_confirmed_pivot_highs(s, 2, 2)
    assert len(pivots) == 2
    assert pivots[0].index == 2
    assert pivots[0].value == 12
    assert pivots[1].index == 5
    assert pivots[1].value == 15

def test_find_confirmed_pivot_lows():
    s = pd.Series([15, 12, 10, 12, 14, 9, 12, 15])
    # index 2 is 10 (neighbors 15,12, 12,14) -> True
    # index 5 is 9 (neighbors 12,14, 12,15) -> True
    pivots = find_confirmed_pivot_lows(s, 2, 2)
    assert len(pivots) == 2
    assert pivots[0].index == 2
    assert pivots[0].value == 10
    assert pivots[1].index == 5
    assert pivots[1].value == 9

def test_align_price_and_oscillator_pivots():
    pp1 = PivotPoint(index=10, value=100.0, pivot_type=PivotType.PRICE_LOW)
    pp2 = PivotPoint(index=20, value=90.0, pivot_type=PivotType.PRICE_LOW)

    op1 = PivotPoint(index=12, value=30.0, pivot_type=PivotType.OSC_LOW)
    op2 = PivotPoint(index=22, value=40.0, pivot_type=PivotType.OSC_LOW)

    aligned = align_price_and_oscillator_pivots([pp1, pp2], [op1, op2], max_distance=5)
    assert len(aligned) == 2
    assert aligned[0][0] == pp1 and aligned[0][1] == op1
    assert aligned[1][0] == pp2 and aligned[1][1] == op2

def test_detect_regular_bullish_divergence():
    # Price Lower Low
    pp1 = PivotPoint(index=10, value=100.0, pivot_type=PivotType.PRICE_LOW)
    pp2 = PivotPoint(index=20, value=90.0, pivot_type=PivotType.PRICE_LOW)

    # Osc Higher Low
    op1 = PivotPoint(index=10, value=30.0, pivot_type=PivotType.OSC_LOW)
    op2 = PivotPoint(index=20, value=40.0, pivot_type=PivotType.OSC_LOW)

    pairs = detect_regular_bullish_divergence([pp1, pp2], [op1, op2], DivergenceSource.RSI, 5)
    assert len(pairs) == 1
    assert pairs[0].divergence_type == DivergenceType.REGULAR_BULLISH

def test_calculate_divergence_strength():
    s = calculate_divergence_strength(-10.0, 33.3, 10)
    assert 0 <= s <= 100

def test_classify_divergence_strength():
    assert classify_divergence_strength(10) == DivergenceStrength.WEAK
    assert classify_divergence_strength(30) == DivergenceStrength.MODERATE
    assert classify_divergence_strength(60) == DivergenceStrength.STRONG
    assert classify_divergence_strength(90) == DivergenceStrength.VERY_STRONG

def test_build_divergence_feature_series():
    df = pd.DataFrame(index=range(30))
    pp1 = PivotPoint(index=10, value=100.0, pivot_type=PivotType.PRICE_LOW)
    pp2 = PivotPoint(index=20, value=90.0, pivot_type=PivotType.PRICE_LOW)
    op1 = PivotPoint(index=10, value=30.0, pivot_type=PivotType.OSC_LOW)
    op2 = PivotPoint(index=20, value=40.0, pivot_type=PivotType.OSC_LOW)

    pair = DivergencePair(
        price_pivot_1=pp1, price_pivot_2=pp2,
        osc_pivot_1=op1, osc_pivot_2=op2,
        divergence_type=DivergenceType.REGULAR_BULLISH,
        source=DivergenceSource.RSI,
        strength_score=50.0,
        confirmation_mode=DivergenceConfirmationMode.CONFIRMED_PIVOT
    )

    res = build_divergence_feature_series(df, [pair], "test")
    assert "test_regular_bullish_divergence" in res.columns
    assert res["test_regular_bullish_divergence"].iloc[20] == 1
    assert res["test_latest_divergence_code"].iloc[20] == 1
    assert res["test_divergence_strength"].iloc[20] == 50.0
