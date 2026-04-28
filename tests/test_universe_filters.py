import pytest
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol, UniverseFilter
from usa_signal_bot.universe.filters import (
    filter_active_symbols, filter_by_asset_type, filter_by_exchange, limit_universe, apply_universe_filter
)
from usa_signal_bot.core.enums import AssetType
from usa_signal_bot.core.exceptions import UniverseValidationError

@pytest.fixture
def sample_universe():
    return UniverseDefinition(
        name="test",
        symbols=[
            UniverseSymbol(symbol="AAPL", active=True, asset_type=AssetType.STOCK, exchange="NASDAQ"),
            UniverseSymbol(symbol="MSFT", active=False, asset_type=AssetType.STOCK, exchange="NASDAQ"),
            UniverseSymbol(symbol="SPY", active=True, asset_type=AssetType.ETF, exchange="NYSE"),
            UniverseSymbol(symbol="QQQ", active=True, asset_type=AssetType.ETF, exchange="NASDAQ")
        ]
    )

def test_filter_active_symbols(sample_universe):
    u = filter_active_symbols(sample_universe)
    assert len(u.symbols) == 3
    assert "MSFT" not in [s.symbol for s in u.symbols]

def test_filter_by_asset_type(sample_universe):
    u = filter_by_asset_type(sample_universe, include_stocks=True, include_etfs=False)
    assert len(u.symbols) == 2
    assert "SPY" not in [s.symbol for s in u.symbols]

    with pytest.raises(UniverseValidationError):
        filter_by_asset_type(sample_universe, include_stocks=False, include_etfs=False)

def test_filter_by_exchange(sample_universe):
    u = filter_by_exchange(sample_universe, ["NYSE"])
    assert len(u.symbols) == 1
    assert u.symbols[0].symbol == "SPY"

def test_limit_universe(sample_universe):
    u = limit_universe(sample_universe, 2)
    assert len(u.symbols) == 2
    assert u.symbols[0].symbol == "AAPL"

def test_apply_universe_filter(sample_universe):
    f = UniverseFilter(include_stocks=True, include_etfs=False, max_symbols=1)
    u = apply_universe_filter(sample_universe, f)
    # active stocks -> AAPL (MSFT is inactive)
    # limited to 1 -> AAPL
    assert len(u.symbols) == 1
    assert u.symbols[0].symbol == "AAPL"
