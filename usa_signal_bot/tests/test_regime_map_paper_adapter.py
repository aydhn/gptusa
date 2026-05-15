import pytest
from usa_signal_bot.regime_map.paper_adapter import attach_regime_map_to_paper_order, paper_order_allowed_by_regime_map

def test_attach_regime_map_to_paper_order():
    order = {"symbol": "SPY"}
    enriched = attach_regime_map_to_paper_order(order, None)
    assert "metadata" in enriched

def test_paper_order_allowed_by_regime_map():
    assert paper_order_allowed_by_regime_map(None) is True
