import pytest
from pathlib import Path
from usa_signal_bot.regime_classification.foundation.regime_foundation_store import regime_foundation_store_dir, regime_foundation_contexts_dir

def test_store_dirs(tmp_path):
    root = tmp_path / "data"
    assert regime_foundation_store_dir(root).exists()
    assert regime_foundation_contexts_dir(root).exists()
