import pytest
from usa_signal_bot.advanced_runtime.phase102_models import (
    TransitionReviewIngestionResult, validate_transition_review_ingestion_result
)

def test_transition_review_ingestion_result_validation():
    item = TransitionReviewIngestionResult(
        ingestion_id="test",
        created_at_utc="now",
        source_path=None,
        source_review_id=None,
        available=True,
        advanced_transition_ready=True,
        current_phase=102,
        final_phase=160,
        activation_allowed=True, # should fail
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False,
        valid_for_phase102=False,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )
    with pytest.raises(ValueError):
        validate_transition_review_ingestion_result(item)
