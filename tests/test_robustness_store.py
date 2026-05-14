
from usa_signal_bot.cost_robustness.robustness_store import robustness_store_summary
from pathlib import Path
def test_store():
    # we don't want to create files, just test function works with dummy path
    summary = robustness_store_summary(Path("data"))
    assert 'reviews_count' in summary
