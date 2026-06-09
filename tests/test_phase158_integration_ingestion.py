import pytest
import json
from usa_signal_bot.release.phase158_integration_ingestion import ingest_full_system_integration_review_payload

def test_ingest_full_system_integration_review_payload():
    with open("tests/fixtures/advanced_acceptance/sample_full_system_integration_review.json", "r") as f:
        payload = json.load(f)

    res = ingest_full_system_integration_review_payload(payload)
    assert res.valid_for_phase159 == True
    assert res.ready_for_phase159 == True
    assert res.live_trading_enabled == False
    assert res.investment_advice == False
