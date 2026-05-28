import pytest
from pathlib import Path
from usa_signal_bot.regime_classification.feature_engineering.regime_feature_engineering_store import (
    write_regime_feature_engineering_full_review_json,
    read_regime_feature_engineering_full_review_json
)
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureEngineeringFullReview

def test_store_review(tmp_path):
    rev = RegimeFeatureEngineeringFullReview(review_id="test_review")
    path = tmp_path / "review.json"
    write_regime_feature_engineering_full_review_json(path, rev)

    data = read_regime_feature_engineering_full_review_json(path)
    assert data["review_id"] == "test_review"
