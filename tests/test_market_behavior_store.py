from pathlib import Path
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import MarketBehaviorFullReview
from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_store import (
    write_market_behavior_full_review_json, read_market_behavior_full_review_json,
    market_behavior_store_dir
)

def test_market_behavior_store(tmp_path):
    rev = MarketBehaviorFullReview()
    d = market_behavior_store_dir(tmp_path)
    f = d / "test_rev.json"

    write_market_behavior_full_review_json(f, rev)
    assert f.exists()

    data = read_market_behavior_full_review_json(f)
    assert data["review_id"] == rev.review_id
