from pathlib import Path
from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_store import research_freeze_store_dir

def test_research_freeze_store_dir(tmp_path):
    d = research_freeze_store_dir(tmp_path)
    assert d.exists()
    assert d.name == "freeze_preparation"
