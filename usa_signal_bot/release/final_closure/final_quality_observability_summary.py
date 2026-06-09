from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalQualityObservabilitySummary,
    create_final_quality_observability_summary_id,
    generate_timestamp
)
import hashlib
import json

def compute_final_quality_observability_summary_hash(summary: FinalQualityObservabilitySummary) -> str:
    state = {
        "quality_metrics": sorted(summary.quality_metrics),
        "observability_metrics": sorted(summary.observability_metrics),
        "acceptance_scores": sorted(summary.acceptance_scores),
        "no_network_export": summary.no_network_export,
        "no_external_push": summary.no_external_push
    }
    data = json.dumps(state, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_quality_observability_summary() -> FinalQualityObservabilitySummary:
    summary = FinalQualityObservabilitySummary(
        summary_id=create_final_quality_observability_summary_id(),
        created_at_utc=generate_timestamp(),
        quality_metrics=["phase160_final_artifact_index_score", "phase160_final_system_audit_score", "phase160_project_closure_score"],
        observability_metrics=["latest_final_delivery_certificate_count", "latest_project_closure_manifest_count"],
        acceptance_scores=["phase160_non_execution_compliance_score"],
        summary_valid=True,
        no_network_export=True,
        no_external_push=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    summary.summary_hash = compute_final_quality_observability_summary_hash(summary)
    return summary

def validate_final_quality_observability_summary(summary: FinalQualityObservabilitySummary) -> List[str]:
    errors = []
    if not summary.summary_valid:
        errors.append("Quality observability summary is invalid.")
    if not summary.no_network_export:
        errors.append("Network export must be disabled.")
    if not summary.no_external_push:
        errors.append("External push must be disabled.")
    return errors

def final_quality_observability_summary_to_text(summary: FinalQualityObservabilitySummary, limit: int = 300) -> str:
    return f"Final Quality & Observability Summary: Valid={summary.summary_valid}, No Network Export={summary.no_network_export}"
