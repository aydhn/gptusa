from typing import Dict, Any, Optional
from usa_signal_bot.runtime_lifecycle.phase104_models import (
    RuntimeLifecycleFullReview,
    create_runtime_lifecycle_full_review_id,
    _now_str,
    ServiceGraphIngestionResult
)
from usa_signal_bot.core.enums import RuntimeLifecycleReportType
from usa_signal_bot.runtime_lifecycle.lifecycle_manager import RuntimeLifecycleManager
from usa_signal_bot.runtime_lifecycle.service_graph_ingestion import _empty_ingestion_result

def build_runtime_lifecycle_full_review(
    manager: Optional[RuntimeLifecycleManager] = None,
    ingestion_result: Optional[ServiceGraphIngestionResult] = None
) -> RuntimeLifecycleFullReview:

    if not manager:
        manager = RuntimeLifecycleManager()

    context = manager.run_lifecycle_dry_run()
    ingestion = ingestion_result or _empty_ingestion_result("No ingestion provided")

    return RuntimeLifecycleFullReview(
        review_id=create_runtime_lifecycle_full_review_id(),
        created_at_utc=_now_str(),
        report_type=RuntimeLifecycleReportType.FULL_PHASE104_REVIEW,
        service_graph_ingestion=ingestion,
        lifecycle_context=context,
        startup_report=context.startup_report,
        readiness_matrix=context.readiness_matrix,
        readiness_gate=context.readiness_gate,
        output_paths={},
        warnings=context.warnings,
        errors=context.errors
    )

def runtime_lifecycle_full_review_summary(review: RuntimeLifecycleFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "gate_decision": review.readiness_gate.decision.value,
        "ready_for_phase105": review.lifecycle_context.ready_for_phase105
    }

def runtime_lifecycle_limitations_text() -> str:
    from usa_signal_bot.runtime_lifecycle.lifecycle_reporting import runtime_lifecycle_limitations_text as _text
    return _text()

def runtime_lifecycle_full_review_to_text(review: RuntimeLifecycleFullReview, limit: int = 300) -> str:
    from usa_signal_bot.runtime_lifecycle.lifecycle_reporting import runtime_lifecycle_full_review_to_text as _text
    return _text(review, limit)
