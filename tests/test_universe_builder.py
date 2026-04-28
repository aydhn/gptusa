import pytest
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol
from usa_signal_bot.universe.builder import merge_universes
from usa_signal_bot.core.enums import AssetType

def test_merge_universes():
    u1 = UniverseDefinition(
        name="U1",
        symbols=[
            UniverseSymbol(symbol="AAPL", asset_type=AssetType.STOCK),
            UniverseSymbol(symbol="MSFT", asset_type=AssetType.STOCK)
        ]
    )
    u2 = UniverseDefinition(
        name="U2",
        symbols=[
            UniverseSymbol(symbol="AAPL", asset_type=AssetType.STOCK), # Duplicate across files
            UniverseSymbol(symbol="GOOGL", asset_type=AssetType.STOCK)
        ]
    )

    merged = merge_universes([u1, u2], "merged")

    assert len(merged.symbols) == 3
    syms = set(s.symbol for s in merged.symbols)
    assert syms == {"AAPL", "MSFT", "GOOGL"}
