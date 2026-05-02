import pytest
from usa_signal_bot.core.enums import DivergenceType, DivergenceSource, PivotType, DivergenceConfirmationMode, DivergenceStrength
from usa_signal_bot.features.divergence_models import (
    PivotPoint, DivergencePair, DivergenceDetectionConfig, DivergenceDetectionResult,
    validate_divergence_config, pivot_point_to_dict, divergence_pair_to_dict
)

def test_pivot_point_valid():
    p = PivotPoint(index=10, value=150.5, pivot_type=PivotType.PRICE_HIGH)
    assert p.index == 10
    assert p.value == 150.5
    assert p.pivot_type == PivotType.PRICE_HIGH

def test_pivot_point_invalid_index():
    with pytest.raises(ValueError, match="negative"):
        PivotPoint(index=-1, value=150.5, pivot_type=PivotType.PRICE_HIGH)

def test_divergence_pair_valid():
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

    assert pair.divergence_type == DivergenceType.REGULAR_BULLISH
    assert pair.strength_score == 50.0

def test_divergence_pair_invalid_strength():
    pp1 = PivotPoint(index=10, value=100.0, pivot_type=PivotType.PRICE_LOW)
    pp2 = PivotPoint(index=20, value=90.0, pivot_type=PivotType.PRICE_LOW)
    op1 = PivotPoint(index=10, value=30.0, pivot_type=PivotType.OSC_LOW)
    op2 = PivotPoint(index=20, value=40.0, pivot_type=PivotType.OSC_LOW)

    with pytest.raises(ValueError, match="between 0 and 100"):
        DivergencePair(
            price_pivot_1=pp1, price_pivot_2=pp2,
            osc_pivot_1=op1, osc_pivot_2=op2,
            divergence_type=DivergenceType.REGULAR_BULLISH,
            source=DivergenceSource.RSI,
            strength_score=150.0,
            confirmation_mode=DivergenceConfirmationMode.CONFIRMED_PIVOT
        )

def test_validate_divergence_config_invalid_windows():
    cfg = DivergenceDetectionConfig(
        source=DivergenceSource.RSI,
        price_column="close",
        oscillator_column="rsi",
        left_window=0,
        right_window=2,
        max_pivot_distance=5,
        min_price_change_pct=0.0,
        min_osc_change_pct=0.0,
        confirmation_mode=DivergenceConfirmationMode.CONFIRMED_PIVOT
    )
    with pytest.raises(ValueError, match="positive"):
        validate_divergence_config(cfg)
