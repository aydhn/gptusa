import pytest

from usa_signal_bot.regime_classification.labeling.phase128_models import RegimeLabelingContext
from usa_signal_bot.regime_classification.labeling.regime_feature_engineering_ingestion import ingest_regime_feature_engineering_review_payload
from usa_signal_bot.regime_classification.labeling.regime_label_safety_validator import regime_label_text_has_trade_or_execution_language

def test_ingestion():
    payload = {
        "review_id": "test_1",
        "context": {
            "ready_for_phase128": True,
            "research_data_only": True,
            "activation_allowed": False
        }
    }
    res = ingest_regime_feature_engineering_review_payload(payload)
    assert res.valid_for_phase128 is True

def test_safety_language():
    assert regime_label_text_has_trade_or_execution_language("buy signal generated") is True
    assert regime_label_text_has_trade_or_execution_language("kesin al") is True
    assert regime_label_text_has_trade_or_execution_language("bull regime detected") is False

if __name__ == "__main__":
    test_ingestion()
    test_safety_language()
    print("All tests passed.")
