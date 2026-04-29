import pytest
from pathlib import Path
from usa_signal_bot.data.downloader import MarketDataDownloader
from usa_signal_bot.data.provider_registry import create_default_provider_registry
from usa_signal_bot.storage.file_store import LocalFileStore
from usa_signal_bot.data.models import MarketDataRequest
from usa_signal_bot.core.exceptions import DataProviderError
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol

@pytest.fixture
def downloader(tmp_path):
    registry = create_default_provider_registry()
    store = LocalFileStore(tmp_path)
    return MarketDataDownloader(registry, store, tmp_path)

def test_downloader_mock_provider(downloader):
    req = MarketDataRequest(symbols=["AAPL"], timeframe="1d", provider_name="mock")
    resp = downloader.download(req)
    assert resp.success is True
    assert resp.bar_count() == 1
    assert resp.bars[0].symbol == "AAPL"

def test_download_for_symbols(downloader):
    resp = downloader.download_for_symbols(["MSFT"], "1d", provider_name="mock")
    assert resp.success is True
    assert resp.bars[0].symbol == "MSFT"

def test_download_empty_symbols_raises(downloader):
    with pytest.raises(DataProviderError):
        downloader.download_for_symbols([], "1d")

def test_download_for_universe(downloader):
    symbols = [
        UniverseSymbol(symbol="AAPL", active=True),
        UniverseSymbol(symbol="MSFT", active=True),
        UniverseSymbol(symbol="INACTIVE", active=False)
    ]
    universe = UniverseDefinition(name="test", symbols=symbols)

    resp = downloader.download_for_universe(universe, "1d", provider_name="mock", limit=1)
    # Should only fetch AAPL due to limit
    assert resp.success is True
    assert len(resp.symbols_returned()) == 1
    assert resp.symbols_returned()[0] == "AAPL"

def test_write_download_summary(downloader, tmp_path):
    req = MarketDataRequest(symbols=["AAPL"], timeframe="1d", provider_name="mock")
    resp = downloader.download(req)
    path = downloader.write_download_summary(resp)
    assert path.exists()
