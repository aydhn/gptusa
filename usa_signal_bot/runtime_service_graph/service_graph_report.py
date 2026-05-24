from datetime import datetime, timezone
from typing import Any, Dict
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeServiceGraphFullReview,
    create_runtime_service_graph_full_review_id,
    validate_runtime_service_graph_full_review
)
from usa_signal_bot.core.enums import RuntimeServiceGraphReportType
from usa_signal_bot.runtime_service_graph.runtime_registry_ingestion import ingest_runtime_registry_review_payload
from usa_signal_bot.runtime_service_graph.service_graph_builder import build_runtime_service_graph
from usa_signal_bot.runtime_service_graph.safe_orchestration_shell import SafeExecutionOrchestrationShell

def build_runtime_service_graph_full_review() -> RuntimeServiceGraphFullReview:
    ingestion = ingest_runtime_registry_review_payload({"normalized_registry": {}, "safety_policy_valid": True, "registry_normalized": True})
    graph = build_runtime_service_graph(ingestion)

    shell = SafeExecutionOrchestrationShell(graph)
    plan = shell.build_plan()
    result = shell.dry_run(plan)

    review = RuntimeServiceGraphFullReview(
        review_id=create_runtime_service_graph_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=RuntimeServiceGraphReportType.FULL_PHASE103_REVIEW,
        registry_ingestion=ingestion,
        service_graph=graph,
        orchestration_plan=plan,
        dry_run_result=result,
        output_paths={},
        warnings=[],
        errors=[]
    )

    validate_runtime_service_graph_full_review(review)
    return review

def runtime_service_graph_full_review_summary(review: RuntimeServiceGraphFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "graph_valid": review.service_graph.graph_valid,
        "dry_run_passed": review.dry_run_result.passed
    }

def runtime_service_graph_limitations_text() -> str:
    return (
        "LIMITATIONS: Phase 103 does not enable paper trading, real broker execution, "
        "order routing, paper state mutation, scraping, dashboards, or real telegram sends. "
        "It builds a local read-only execution orchestration shell."
    )

def runtime_service_graph_full_review_to_text(review: RuntimeServiceGraphFullReview, limit: int = 300) -> str:
    return (
        f"Review {review.review_id}\n"
        f"Graph Valid: {review.service_graph.graph_valid}\n"
        f"Dry Run Passed: {review.dry_run_result.passed}\n"
        f"{runtime_service_graph_limitations_text()}"
    )
