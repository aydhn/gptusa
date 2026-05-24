from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    LifecycleReviewIngestionResult,
    create_lifecycle_review_ingestion_id,
    validate_lifecycle_review_ingestion_result
)
from usa_signal_bot.core.exceptions import LifecycleReviewIngestionError

def test_lifecycle_review_ingestion_validation():
    item = LifecycleReviewIngestionResult(
        ingestion_id=create_lifecycle_review_ingestion_id(),
        created_at_utc="now",
        lifecycle_ready=False
    )
    try:
        validate_lifecycle_review_ingestion_result(item)
    except LifecycleReviewIngestionError:
        pass

    item.lifecycle_ready = True
    item.ready_for_phase105 = True
    item.readiness_gate_passed = True
    item.startup_checks_passed = True
    item.all_required_services_ready = True
    validate_lifecycle_review_ingestion_result(item)
