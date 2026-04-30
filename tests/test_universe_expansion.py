import pytest
from pathlib import Path
from usa_signal_bot.universe.expansion import expand_universe, UniverseExpansionRequest
from usa_signal_bot.core.enums import UniverseLayer, UniverseSourceType
from usa_signal_bot.universe.sources import UniverseSource
from usa_signal_bot.core.exceptions import UniverseSourceError

@pytest.fixture
def mock_sources(tmp_path):
    # Create simple CSVs
    p1 = tmp_path / "p1.csv"
    with open(p1, "w") as f:
         f.write("symbol,asset_type,active\nAAPL,stock,true\n")

    p2 = tmp_path / "p2.csv"
    with open(p2, "w") as f:
         f.write("symbol,asset_type,active\nSPY,etf,true\n")

    s1 = UniverseSource("id1", "s1", UniverseSourceType.PRESET, UniverseLayer.CORE, str(p1))
    s2 = UniverseSource("id2", "s2", UniverseSourceType.PRESET, UniverseLayer.WATCHLIST, str(p2))
    return [s1, s2]

def test_expand_universe(tmp_path, mock_sources):
    req = UniverseExpansionRequest("test", mock_sources, write_snapshot=False)
    res = expand_universe(req, tmp_path)

    assert res.success is True
    assert len(res.universe.symbols) == 2

def test_expand_universe_include_layers(tmp_path, mock_sources):
    req = UniverseExpansionRequest(
        "test",
        mock_sources,
        include_layers=[UniverseLayer.CORE],
        write_snapshot=False
    )
    res = expand_universe(req, tmp_path)

    assert res.success is True
    assert len(res.universe.symbols) == 1
    assert res.universe.symbols[0].symbol == "AAPL"

def test_expand_universe_max_symbols(tmp_path, mock_sources):
    req = UniverseExpansionRequest("test", mock_sources, max_symbols=1, write_snapshot=False)
    res = expand_universe(req, tmp_path)

    assert res.success is True
    assert len(res.universe.symbols) == 1
