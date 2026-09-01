import pytest
from unittest.mock import patch, MagicMock

import usa_signal_bot.provider_quality.provider_cache_ingestion as ingestion

def test_provider_cache_supports_phase109_valid():
    payload = {
        "context": {
            "provider_cache_ready": True,
            "metadata_only": True
        }
    }
    valid, warnings = ingestion.provider_cache_supports_phase109(payload)
    assert valid is True
    assert len(warnings) == 0

def test_provider_cache_supports_phase109_invalid():
    payload = {
        "context": {
            "provider_cache_ready": False,
            "metadata_only": False
        }
    }
    valid, warnings = ingestion.provider_cache_supports_phase109(payload)
    assert valid is False
    assert len(warnings) == 2
    assert "provider_cache_ready is false" in warnings
    assert "metadata_only is false" in warnings

def test_extract_provider_cache_context():
    payload = {"context": {"key": "value"}}
    assert ingestion.extract_provider_cache_context(payload) == {"key": "value"}
    assert ingestion.extract_provider_cache_context({}) is None

def test_extract_source_comparisons():
    payload = {"source_comparisons": [{"id": 1}]}
    assert ingestion.extract_source_comparisons(payload) == [{"id": 1}]
    assert ingestion.extract_source_comparisons({}) == []

def test_extract_confidence_hints():
    payload = {"confidence_hints": [{"id": 1}]}
    assert ingestion.extract_confidence_hints(payload) == [{"id": 1}]
    assert ingestion.extract_confidence_hints({}) == []

@patch("usa_signal_bot.provider_quality.provider_cache_ingestion.create_provider_cache_ingestion_id")
def test_ingest_provider_cache_review_payload_no_context(mock_create_id):
    mock_create_id.return_value = "mock_id"
    payload = {"review_id": "rev1"}
    result = ingestion.ingest_provider_cache_review_payload(payload, source_path="path")

    assert result.ingestion_id == "mock_id"
    assert result.source_path == "path"
    assert result.source_review_id == "rev1"
    assert result.source_context_id is None
    assert result.available is False
    assert result.provider_cache_ready is False
    assert result.valid_for_phase109 is False
    assert "No provider cache context found in payload" in result.errors

@patch("usa_signal_bot.provider_quality.provider_cache_ingestion.create_provider_cache_ingestion_id")
def test_ingest_provider_cache_review_payload_with_context(mock_create_id):
    mock_create_id.return_value = "mock_id"
    payload = {
        "review_id": "rev1",
        "context": {
            "context_id": "ctx1",
            "provider_cache_ready": True,
            "metadata_only": True,
            "stale_fresh_policy_valid": True,
            "fallback_dry_run_ready": True,
            "source_comparison_ready": True,
        }
    }
    result = ingestion.ingest_provider_cache_review_payload(payload, source_path="path")

    assert result.ingestion_id == "mock_id"
    assert result.source_path == "path"
    assert result.source_review_id == "rev1"
    assert result.source_context_id == "ctx1"
    assert result.available is True
    assert result.provider_cache_ready is True
    assert result.valid_for_phase109 is True
    assert len(result.errors) == 0
    assert len(result.warnings) == 0

def test_provider_cache_ingestion_to_text():
    mock_result = MagicMock()
    mock_result.ingestion_id = "test_id"
    mock_result.valid_for_phase109 = True
    mock_result.provider_cache_ready = False

    text = ingestion.provider_cache_ingestion_to_text(mock_result)
    assert text == "Ingestion ID: test_id | Valid: True | Cache Ready: False"

def test_ingest_latest_provider_cache_review_from_store():
    # It returns None currently since it passes
    assert ingestion.ingest_latest_provider_cache_review_from_store(None) is None
