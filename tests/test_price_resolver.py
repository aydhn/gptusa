import pytest
from usa_signal_bot.paper.price_resolver import LocalPriceResolver
from pathlib import Path

def test_price_resolver_empty(tmp_path):
    # Empty cache dir should just return None
    resolver = LocalPriceResolver(tmp_path)

    assert resolver.resolve_latest_price("AAPL", "1d") is None
    assert resolver.resolve_price_at_or_after("AAPL", "2026-01-01T00:00:00Z") is None
    assert resolver.resolve_bar_for_order("AAPL", "1d", "MARKET") is None
    assert resolver.resolve_many_latest(["AAPL"]) == {}
