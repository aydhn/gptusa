from unittest.mock import MagicMock
from usa_signal_bot.provider_quality.provider_quality_reporting import (
    data_quality_score_component_to_text,
    provider_quality_context_to_text,
    provider_quality_full_review_to_text,
    provider_quality_store_summary_to_text,
)

def test_data_quality_score_component_to_text():
    mock_component = MagicMock()
    mock_component.component.value = "ACCURACY"
    mock_component.score = 95.5
    mock_component.grade.value = "A"
    mock_component.explanation = "Good data"

    result = data_quality_score_component_to_text(mock_component)
    assert result == "ACCURACY: 95.5 (A) - Good data"

def test_provider_quality_context_to_text():
    mock_context = MagicMock()
    mock_context.context_id = "ctx_123"
    mock_context.status.value = "COMPLETED"
    mock_context.ingestion.ingestion_id = "ing_123"
    mock_context.data_quality_scores = [1, 2]
    mock_context.trust_profiles = [1]
    mock_context.selection_scores = [1, 2, 3]
    mock_context.rankings = [1]
    mock_context.errors = ["err1"]
    mock_context.warnings = ["warn1"]

    result = provider_quality_context_to_text(mock_context)

    assert "Provider Quality Context: ctx_123 | Status: COMPLETED" in result
    assert "Ingestion: ing_123" in result
    assert "Quality Scores: 2" in result
    assert "Trust Profiles: 1" in result
    assert "Selection Scores: 3" in result
    assert "Rankings: 1" in result
    assert "Errors: ['err1']" in result
    assert "Warnings: ['warn1']" in result

def test_provider_quality_full_review_to_text():
    mock_review = MagicMock()
    mock_review.review_id = "rev_123"
    mock_review.context.context_id = "ctx_123"
    mock_review.report_type.value = "FULL"
    mock_review.warnings = [1, 2]
    mock_review.errors = [1]

    result = provider_quality_full_review_to_text(mock_review)

    assert "Provider Quality Full Review: rev_123" in result
    assert "Context ID: ctx_123" in result
    assert "Report Type: FULL" in result
    assert "Warnings: 2" in result
    assert "Errors: 1" in result

def test_provider_quality_store_summary_to_text():
    summary = {
        'contexts_count': 10,
        'reviews_count': 5,
        'data_quality_scores_count': 20,
        'source_trust_profiles_count': 15,
        'provider_selection_scores_count': 25,
        'provider_rankings_count': 30
    }

    result = provider_quality_store_summary_to_text(summary)

    assert "Provider Quality Store:" in result
    assert "Contexts: 10" in result
    assert "Reviews: 5" in result
    assert "Data Quality Scores: 20" in result
    assert "Source Trust Profiles: 15" in result
    assert "Selection Scores: 25" in result
    assert "Rankings: 30" in result
