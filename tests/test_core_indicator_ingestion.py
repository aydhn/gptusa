import pytest
from usa_signal_bot.feature_engine.advanced_features.core_indicator_ingestion import ingest_core_indicator_review_payload

def test_ingest_core_indicator_review():
    payload = {
        "core_indicators_ready": True,
        "feature_table_ready": True,
        "produces_trade_signal": False,
        "broker_execution_enabled": False,
        "network_used": False,
        "context": {
            "core_indicators_ready": True,
            "rolling_window_engine_ready": True,
            "feature_table_ready": True
        }
    }
    res = ingest_core_indicator_review_payload(payload)
    assert res.valid_for_phase118
    assert res.core_indicators_ready

    # Invalid
    payload2 = {
        "core_indicators_ready": True,
        "produces_trade_signal": True
    }
    res2 = ingest_core_indicator_review_payload(payload2)
    assert not res2.valid_for_phase118
