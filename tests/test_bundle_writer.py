from usa_signal_bot.release_packaging.bundle_writer import bundle_root_dir
from pathlib import Path

def test_writer():
    assert bundle_root_dir(Path("data")).name == "release_bundles"
