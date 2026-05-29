from usa_signal_bot.regime_classification.alignment.alignment_readiness_gate import build_regime_alignment_readiness_gate
from usa_signal_bot.regime_classification.alignment.market_behavior_ingestion import ingest_market_behavior_review_payload
import json
def test_gate():
    with open("tests/fixtures/regime_alignment/sample_market_behavior_review.json") as f:
        payload = json.load(f)
    ingestion = ingest_market_behavior_review_payload(payload)
    gate = build_regime_alignment_readiness_gate(ingestion, [], [], [], [])
    assert gate.ready_for_phase132
