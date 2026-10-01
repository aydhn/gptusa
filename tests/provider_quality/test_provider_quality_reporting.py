import pytest
from unittest.mock import MagicMock
from usa_signal_bot.provider_quality.provider_quality_reporting import (
    data_quality_score_component_to_text,
    provider_quality_context_to_text,
    provider_quality_full_review_to_text,
    provider_quality_store_summary_to_text,
    provider_quality_limitations_text
)

def test_data_quality_score_component_to_text():
    c = MagicMock()
    c.component.value = 'Test Component'
    c.score = 95.5
    c.grade.value = 'A'
    c.explanation = 'Good'
    res = data_quality_score_component_to_text(c)
    assert 'Test Component: 95.5 (A) - Good' in res

def test_provider_quality_context_to_text():
    ctx = MagicMock()
    ctx.context_id = 'ctx_1'
    ctx.status.value = 'VALIDATED'
    ctx.ingestion.ingestion_id = 'ingest_1'
    ctx.data_quality_scores = [1, 2]
    ctx.trust_profiles = [1]
    ctx.selection_scores = [1, 2, 3]
    ctx.rankings = [1]
    ctx.errors = ['error 1']
    ctx.warnings = ['warn 1']
    res = provider_quality_context_to_text(ctx)
    assert 'Provider Quality Context: ctx_1 | Status: VALIDATED' in res
    assert 'Errors: [\'error 1\']' in res

def test_provider_quality_full_review_to_text():
    rev = MagicMock()
    rev.review_id = 'rev_1'
    rev.context.context_id = 'ctx_1'
    rev.report_type.value = 'FULL'
    rev.warnings = ['w1']
    rev.errors = ['e1', 'e2']
    res = provider_quality_full_review_to_text(rev)
    assert 'Provider Quality Full Review: rev_1' in res
    assert 'Errors: 2' in res

def test_provider_quality_store_summary_to_text():
    summary = {
        'contexts_count': 10,
        'reviews_count': 5,
        'data_quality_scores_count': 20,
        'source_trust_profiles_count': 15,
        'provider_selection_scores_count': 30,
        'provider_rankings_count': 2
    }
    res = provider_quality_store_summary_to_text(summary)
    assert 'Provider Quality Store:' in res
    assert 'Contexts: 10' in res

def test_provider_quality_limitations_text():
    res = provider_quality_limitations_text()
    assert 'Phase 109 Limitations:' in res
