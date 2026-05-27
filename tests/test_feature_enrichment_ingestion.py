import pytest
import json
from pathlib import Path
from usa_signal_bot.feature_engine.factor_composition.feature_enrichment_ingestion import (
    ingest_feature_enrichment_review_payload
)

def test_ingest_feature_enrichment_review_payload_valid():
    payload = {
        "review_id": "test1",
        "context": {
            "event_enrichment_ready": True,
            "quality_enrichment_ready": True,
            "calendar_enrichment_ready": True,
            "interactions_ready": True,
            "enriched_feature_table_ready": True,
            "ready_for_phase119": True,
            "research_data_only": True
        }
    }
    result = ingest_feature_enrichment_review_payload(payload)
    assert result.valid_for_phase120 is True
    assert len(result.errors) == 0

def test_ingest_feature_enrichment_review_payload_invalid():
    with open('tests/fixtures/factor_composition/sample_invalid_factor_composition_payload.json') as f:
        payload = json.load(f)
    result = ingest_feature_enrichment_review_payload(payload)
    assert result.valid_for_phase120 is False
    assert any("event_enrichment_ready is false" in err for err in result.errors)
