import pytest
from usa_signal_bot.universe.models import UniverseSymbol, UniverseDefinition
from usa_signal_bot.universe.validator import (
    validate_universe_symbol, validate_universe_definition, assert_universe_valid
)
from usa_signal_bot.core.enums import AssetType
from usa_signal_bot.core.exceptions import UniverseValidationError

def test_validate_universe_symbol():
    s1 = UniverseSymbol(symbol="AAPL", asset_type=AssetType.STOCK)
    issues = validate_universe_symbol(s1)
    assert len(issues) == 0

def test_validate_universe_definition():
    u = UniverseDefinition(
        name="Test",
        symbols=[
            UniverseSymbol(symbol="AAPL", asset_type=AssetType.STOCK),
            UniverseSymbol(symbol="MSFT", asset_type=AssetType.STOCK),
            UniverseSymbol(symbol="AAPL", asset_type=AssetType.STOCK) # dupe
        ]
    )

    report = validate_universe_definition(u)
    assert report.total_rows == 3
    assert report.valid_rows == 3
    assert len(report.duplicate_symbols) == 1
    assert "AAPL" in report.duplicate_symbols
    assert report.passed is True # Dupes are warnings

    assert_universe_valid(report) # Should not raise
