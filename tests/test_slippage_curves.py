import pytest
from usa_signal_bot.transaction_costs.slippage_curves import (
    build_default_slippage_curve,
    build_conservative_slippage_curve,
    evaluate_slippage_curve,
    classify_order_size_class
)
from usa_signal_bot.core.enums import OrderSizeClass

def test_default_curve_monotonic():
    curve = build_default_slippage_curve()
    points = curve.points
    for i in range(len(points)-1):
        assert points[i].slippage_bps <= points[i+1].slippage_bps

def test_interpolation():
    curve = build_default_slippage_curve()
    val = evaluate_slippage_curve(curve, 0.5)
    assert val == 15.0
    val_mid = evaluate_slippage_curve(curve, 0.3)
    assert val_mid > 5.0 and val_mid < 15.0

def test_order_size_class():
    assert classify_order_size_class(0.05) == OrderSizeClass.MICRO
    assert classify_order_size_class(0.2) == OrderSizeClass.SMALL
    assert classify_order_size_class(0.6) == OrderSizeClass.MEDIUM
    assert classify_order_size_class(2.0) == OrderSizeClass.LARGE
    assert classify_order_size_class(15.0) == OrderSizeClass.OVERSIZED
