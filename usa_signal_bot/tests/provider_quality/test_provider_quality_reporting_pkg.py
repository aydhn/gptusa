import pytest
from unittest.mock import MagicMock, patch

from usa_signal_bot.provider_quality.provider_quality_reporting import (
    data_quality_score_component_to_text,
    provider_quality_context_to_text,
    provider_quality_full_review_to_text,
    provider_quality_store_summary_to_text,
    provider_quality_limitations_text,
)

def test_data_quality_score_component_to_text():
    # Mock item
    item = MagicMock()
    item.component.value = "Freshness"
    item.score = 95.5
    item.grade.value = "EXCELLENT"
    item.explanation = "Data is very fresh"

    result = data_quality_score_component_to_text(item)
    assert result == "Freshness: 95.5 (EXCELLENT) - Data is very fresh"

def test_provider_quality_context_to_text():
    item = MagicMock()
    item.context_id = "ctx_123"
    item.status.value = "READY"
    item.ingestion.ingestion_id = "ing_123"
    item.data_quality_scores = [1, 2]
    item.trust_profiles = [1]
    item.selection_scores = [1, 2, 3]
    item.rankings = [1, 2]
    item.errors = ["An error occurred"]
    item.warnings = ["A warning occurred"]

    result = provider_quality_context_to_text(item)
    expected = (
        "Provider Quality Context: ctx_123 | Status: READY\n"
        "Ingestion: ing_123\n"
        "Quality Scores: 2\n"
        "Trust Profiles: 1\n"
        "Selection Scores: 3\n"
        "Rankings: 2\n"
        "Errors: ['An error occurred']\n"
        "Warnings: ['A warning occurred']"
    )
    assert result == expected

    # Test without errors/warnings and truncation limit
    item.errors = []
    item.warnings = []

    result_short = provider_quality_context_to_text(item, limit=50)
    expected_short = (
        "Provider Quality Context: ctx_123 | Status: READY\n"
        "Ingestion: ing_123\n"
        "Quality Scores: 2\n"
        "Trust Profiles: 1\n"
        "Selection Scores: 3\n"
        "Rankings: 2"
    )[:50]
    assert result_short == expected_short

def test_provider_quality_full_review_to_text():
    item = MagicMock()
    item.review_id = "rev_123"
    item.context.context_id = "ctx_123"
    item.report_type.value = "FULL"
    item.warnings = [1, 2]
    item.errors = []

    result = provider_quality_full_review_to_text(item)
    expected = (
        "Provider Quality Full Review: rev_123\n"
        "Context ID: ctx_123\n"
        "Report Type: FULL\n"
        "Warnings: 2\n"
        "Errors: 0"
    )
    assert result == expected

    # Test truncation limit
    result_short = provider_quality_full_review_to_text(item, limit=20)
    expected_short = (
        "Provider Quality Full Review: rev_123\n"
        "Context ID: ctx_123\n"
        "Report Type: FULL\n"
        "Warnings: 2\n"
        "Errors: 0"
    )[:20]
    assert result_short == expected_short

def test_provider_quality_store_summary_to_text():
    summary = {
        "contexts_count": 10,
        "reviews_count": 5,
        "data_quality_scores_count": 15,
        "source_trust_profiles_count": 8,
        "provider_selection_scores_count": 12,
        "provider_rankings_count": 3
    }

    result = provider_quality_store_summary_to_text(summary)
    expected = (
        "Provider Quality Store:\n"
        "  Contexts: 10\n"
        "  Reviews: 5\n"
        "  Data Quality Scores: 15\n"
        "  Source Trust Profiles: 8\n"
        "  Selection Scores: 12\n"
        "  Rankings: 3"
    )
    assert result == expected

    # Test empty dict
    result_empty = provider_quality_store_summary_to_text({})
    expected_empty = (
        "Provider Quality Store:\n"
        "  Contexts: 0\n"
        "  Reviews: 0\n"
        "  Data Quality Scores: 0\n"
        "  Source Trust Profiles: 0\n"
        "  Selection Scores: 0\n"
        "  Rankings: 0"
    )
    assert result_empty == expected_empty

def test_provider_quality_limitations_text_real():
    assert 'Phase 109 Limitations' in provider_quality_limitations_text()
