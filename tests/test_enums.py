import pytest
from usa_signal_bot.core.enums import AssetType, SignalSide, OrderStatus, RegimeType

def test_enum_values_are_strings():
    assert isinstance(AssetType.STOCK.value, str)
    assert isinstance(SignalSide.LONG.value, str)
    assert isinstance(OrderStatus.CREATED.value, str)

def test_asset_type_values():
    assert AssetType.STOCK.value == "STOCK"
    assert AssetType.ETF.value == "ETF"

def test_signal_side_values():
    sides = [s.value for s in SignalSide]
    assert "LONG" in sides
    assert "SHORT" in sides
    assert "FLAT" in sides

def test_order_status_values():
    statuses = [s.value for s in OrderStatus]
    assert "CREATED" in statuses
    assert "FILLED" in statuses
    assert "REJECTED" in statuses

def test_regime_type_values():
    regimes = [r.value for r in RegimeType]
    assert "RISK_ON" in regimes
    assert "TRENDING_UP" in regimes
    assert "UNKNOWN" in regimes
