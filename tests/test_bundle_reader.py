from usa_signal_bot.release_packaging.bundle_reader import read_bundle_json
from pathlib import Path

def test_reader():
    res = read_bundle_json(Path("nonexistent.json"))
    assert res == {}
