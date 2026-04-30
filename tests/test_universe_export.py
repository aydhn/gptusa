import pytest
import json
from usa_signal_bot.universe.export import export_universe_csv, export_universe_json, export_symbols_txt, export_symbols_json, build_export_path
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol
from usa_signal_bot.core.exceptions import UniverseExportError

@pytest.fixture
def sample_universe():
    return UniverseDefinition(name="test", symbols=[UniverseSymbol(symbol="AAPL"), UniverseSymbol(symbol="MSFT", active=False)])

def test_export_universe_csv(tmp_path, sample_universe):
    path = tmp_path / "export.csv"
    export_universe_csv(sample_universe, path)
    assert path.exists()

def test_export_universe_json(tmp_path, sample_universe):
    path = tmp_path / "export.json"
    export_universe_json(sample_universe, path)
    assert path.exists()
    with open(path) as f:
        data = json.load(f)
        assert len(data["symbols"]) == 2

def test_export_symbols_txt(tmp_path, sample_universe):
    path = tmp_path / "export.txt"
    export_symbols_txt(sample_universe, path, active_only=True)
    assert path.exists()
    with open(path) as f:
        content = f.read().strip()
        assert content == "AAPL"

def test_build_export_path(tmp_path):
    path = build_export_path(tmp_path, "my_export", "csv")
    assert path.parent.name == "exports"
    assert path.name == "my_export.csv"

def test_path_traversal_protection(tmp_path, sample_universe):
    with pytest.raises(UniverseExportError):
        from usa_signal_bot.universe.export import _ensure_safe_export_path
        _ensure_safe_export_path(tmp_path / ".." / "sneaky.csv", tmp_path)
