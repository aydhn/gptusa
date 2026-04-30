import pytest
from pathlib import Path

from usa_signal_bot.universe.active import (
    resolve_active_universe,
    active_universe_resolution_to_text,
    write_active_universe_resolution_json
)
from usa_signal_bot.core.exceptions import ActiveUniverseResolutionError

def test_resolve_fallback_to_watchlist(tmp_path):
    # Set up dummy watchlist
    uni_dir = tmp_path / "universe"
    uni_dir.mkdir()
    wl_path = uni_dir / "watchlist.csv"
    wl_path.write_text("symbol,asset_type\nSPY,etf\nAAPL,stock\n")

    res = resolve_active_universe(tmp_path, fallback_to_watchlist=True)
    assert res.source.value == "DEFAULT_WATCHLIST"
    assert res.symbol_count == 2
    assert len(res.warnings) > 0  # Should have warnings about missing snapshots

def test_resolve_explicit_file(tmp_path):
    exp_path = tmp_path / "custom.csv"
    exp_path.write_text("symbol,asset_type\nMSFT,stock\n")

    res = resolve_active_universe(tmp_path, explicit_file=exp_path)
    assert res.source.value == "EXPLICIT_FILE"
    assert res.symbol_count == 1
    assert "MSFT" in [s.symbol for s in res.universe.symbols]

def test_resolve_explicit_file_url_fails(tmp_path):
    # Path traversal / url should fail
    with pytest.raises(ActiveUniverseResolutionError):
        # We can't actually pass a URL string to Path, but we can pass a bad string and check validation
        bad_path = Path("http://example.com/file.csv")
        resolve_active_universe(tmp_path, explicit_file=bad_path)

def test_resolution_to_text_and_json(tmp_path):
    uni_dir = tmp_path / "universe"
    uni_dir.mkdir()
    wl_path = uni_dir / "watchlist.csv"
    wl_path.write_text("symbol,asset_type\nSPY,etf\n")

    res = resolve_active_universe(tmp_path, fallback_to_watchlist=True)

    text = active_universe_resolution_to_text(res)
    assert "=== Active Universe Resolution ===" in text
    assert "SPY" not in text # summary doesn't show symbols
    assert "Total Symbols" in text

    json_path = tmp_path / "res.json"
    write_active_universe_resolution_json(json_path, res)
    assert json_path.exists()
    assert "DEFAULT_WATCHLIST" in json_path.read_text()
