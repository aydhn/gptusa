from usa_signal_bot.release_packaging.packaging_store import packaging_store_dir
from pathlib import Path

def test_store():
    assert packaging_store_dir(Path("data")).name == "release_packaging"
