import pytest
from usa_signal_bot.ml_research.foundation.final_closure_ingestion import ingest_final_closure_review_payload

def test_ingest_payload_safe():
    res = ingest_final_closure_review_payload({})
    assert res.valid_for_phase136 is True

def test_ingest_payload_unsafe():
    res = ingest_final_closure_review_payload({"invalid": True})
    assert res.valid_for_phase136 is False
