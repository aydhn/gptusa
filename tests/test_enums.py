import pytest
from usa_signal_bot.core.enums import AssetType, SignalSide, OrderStatus, RegimeType, SignalScoreComponent, SignalQualityStatus, SignalRejectionReason, ConfluenceDirection, ConfluenceStrength, SignalAggregationMode

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

def test_signal_score_component():
    assert SignalScoreComponent.STRATEGY_BASE == "STRATEGY_BASE"
    assert SignalScoreComponent.CONFLUENCE == "CONFLUENCE"

def test_signal_quality_status():
    assert SignalQualityStatus.ACCEPTED == "ACCEPTED"
    assert SignalQualityStatus.REJECTED == "REJECTED"

def test_signal_rejection_reason():
    assert SignalRejectionReason.LOW_CONFIDENCE == "LOW_CONFIDENCE"
    assert SignalRejectionReason.CONFLICTING_SIGNAL == "CONFLICTING_SIGNAL"

def test_confluence_direction():
    assert ConfluenceDirection.LONG_BIAS == "LONG_BIAS"
    assert ConfluenceDirection.SHORT_BIAS == "SHORT_BIAS"
    assert ConfluenceDirection.CONFLICTED == "CONFLICTED"

def test_confluence_strength():
    assert ConfluenceStrength.WEAK == "WEAK"
    assert ConfluenceStrength.VERY_STRONG == "VERY_STRONG"

def test_signal_aggregation_mode():
    assert SignalAggregationMode.BY_SYMBOL_TIMEFRAME == "BY_SYMBOL_TIMEFRAME"
    assert SignalAggregationMode.GLOBAL == "GLOBAL"
