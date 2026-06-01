import pytest
from pathlib import Path
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_scaffolding_store import ensemble_scaffolding_store_dir

def test_store_dir():
    d = ensemble_scaffolding_store_dir(Path("data"))
    assert d.name == "ensemble_scaffolding"
