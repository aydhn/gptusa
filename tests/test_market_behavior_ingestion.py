from usa_signal_bot.regime_classification.alignment.market_behavior_ingestion import ingest_market_behavior_review_payload
import json

def test_ingest_valid():
    with open("tests/fixtures/regime_alignment/sample_market_behavior_review.json") as f:
        payload = json.load(f)
    res = ingest_market_behavior_review_payload(payload)
    assert res.valid_for_phase131
    assert res.ready_for_phase131

def test_ingest_blocked():
    with open("tests/fixtures/regime_alignment/sample_market_behavior_review_blocked.json") as f:
        payload = json.load(f)
    res = ingest_market_behavior_review_payload(payload)
    assert not res.valid_for_phase131
