import pytest
from usa_signal_bot.universe.presets import list_preset_files, load_preset_universe, load_all_presets

def test_list_and_load_presets(tmp_path):
    # Setup
    pdir = tmp_path / "universe" / "presets"
    pdir.mkdir(parents=True)

    p1 = pdir / "test_preset.csv"
    with open(p1, "w") as f:
        f.write("symbol,asset_type\nAAPL,stock\n")

    files = list_preset_files(tmp_path)
    assert len(files) == 1

    res = load_preset_universe(tmp_path, "test_preset")
    assert len(res.universe.symbols) == 1

    all_res = load_all_presets(tmp_path)
    assert len(all_res) == 1
