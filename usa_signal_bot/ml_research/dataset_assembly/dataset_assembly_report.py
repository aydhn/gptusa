from typing import Any, Dict, List
from datetime import datetime, timezone
import json
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLDatasetAssemblyContext,
    MLDatasetAssemblyFullReview,
    MLDatasetAssemblyStatus,
    MLDatasetAssemblyDecision,
    MLDatasetAssemblyReportType,
    create_ml_dataset_assembly_context_id,
    create_ml_dataset_assembly_full_review_id
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_dataset_assembly_context() -> MLDatasetAssemblyContext:
    return MLDatasetAssemblyContext(
        context_id=create_ml_dataset_assembly_context_id(),
        created_at_utc=_now(),
        status=MLDatasetAssemblyStatus.CREATED,
        decision=MLDatasetAssemblyDecision.RESOLVE_SOURCES
    )

def build_dataset_assembly_full_review() -> MLDatasetAssemblyFullReview:
    return MLDatasetAssemblyFullReview(
        review_id=create_ml_dataset_assembly_full_review_id(),
        created_at_utc=_now(),
        report_type=MLDatasetAssemblyReportType.FULL_PHASE137_REVIEW
    )

def dataset_assembly_full_review_summary(review: MLDatasetAssemblyFullReview) -> Dict[str, Any]:
    summary = {
        "review_id": review.review_id,
        "report_type": review.report_type.value,
        "ready_for_phase138": False,
        "has_context": review.context is not None,
        "has_manifest": review.dataset_manifest is not None,
        "has_leakage_audit": review.leakage_audit is not None,
        "has_readiness_gate": review.readiness_gate is not None
    }
    if review.readiness_gate:
        summary["ready_for_phase138"] = review.readiness_gate.ready_for_phase138
    return summary

def dataset_assembly_limitations_text() -> str:
    return (
        "PHASE 137 LIMITATIONS:\n"
        "- This phase is strictly for ML dataset assembly, split design, and leakage audit.\n"
        "- NO actual ML models are trained or evaluated in this phase.\n"
        "- NO model predictions or trade signals are generated.\n"
        "- NO paper trading or live trading execution is allowed.\n"
        "- NO network fetch, no dashboard, no broker API is used.\n"
        "- Produces only local metadata and research datasets."
    )

def dataset_assembly_full_review_to_text(review: MLDatasetAssemblyFullReview, limit: int = 300) -> str:
    s = json.dumps(dataset_assembly_full_review_summary(review), indent=2)
    text = s + "\n\n" + dataset_assembly_limitations_text()
    if len(text) > limit:
        return text[:limit] + "..."
    return text
