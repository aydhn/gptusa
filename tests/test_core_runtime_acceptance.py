
from usa_signal_bot.core_runtime_acceptance.core_runtime_acceptance import (
    build_core_runtime_acceptance_report,
    required_core_runtime_acceptance_items
)
from usa_signal_bot.core_runtime_acceptance.phase105_models import LifecycleReviewIngestionResult

def test_build_core_runtime_acceptance_report():
    lifecycle = LifecycleReviewIngestionResult(
        ingestion_id="lri_123",
        created_at_utc="now",
        valid_for_phase105=True
    )
    report = build_core_runtime_acceptance_report(lifecycle, [])
    assert report.core_runtime_accepted == True
    assert len(report.items) == len(required_core_runtime_acceptance_items())
