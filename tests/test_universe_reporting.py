import pytest
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol
from usa_signal_bot.universe.reporting import summarize_universe, universe_summary_to_text
from usa_signal_bot.core.enums import AssetType

def test_summarize_universe():
    u = UniverseDefinition(
        name="U1",
        symbols=[
            UniverseSymbol(symbol="AAPL", active=True, asset_type=AssetType.STOCK, exchange="NASDAQ", sector="Tech"),
            UniverseSymbol(symbol="MSFT", active=False, asset_type=AssetType.STOCK, exchange="NASDAQ"),
            UniverseSymbol(symbol="SPY", active=True, asset_type=AssetType.ETF, exchange="NYSE")
        ]
    )

    summary = summarize_universe(u)
    assert summary.total_symbols == 3
    assert summary.active_symbols == 2
    assert summary.inactive_count == 1
    assert summary.stock_count == 2
    assert summary.etf_count == 1
    assert summary.exchanges.get("NASDAQ") == 2
    assert summary.exchanges.get("NYSE") == 1
    assert summary.sectors.get("Tech") == 1

    text = universe_summary_to_text(summary)
    assert "Total Symbols : 3" in text
    assert "Active        : 2" in text
    assert "NASDAQ: 2" in text
