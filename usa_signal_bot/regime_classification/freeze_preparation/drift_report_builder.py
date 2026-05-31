from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.core.enums import DriftReportSectionKind, DriftReportQaStatus
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    RegimeMonitoringIngestionResult,
    MonitoringValidationResult,
    DriftReportSection,
    DriftReportDocument,
    create_drift_report_section_id,
    create_drift_report_document_id,
    _now_utc_str
)
from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_hashing import compute_text_hash

def build_drift_report_sections(
    ingestion: RegimeMonitoringIngestionResult,
    validation: MonitoringValidationResult,
    baseline: Optional[Dict[str, Any]],
    snapshot: Optional[Dict[str, Any]],
    drift_result: Optional[Dict[str, Any]],
    degradation_diagnostics: List[Dict[str, Any]],
    degradation_profiles: List[Dict[str, Any]]
) -> List[DriftReportSection]:

    sections = []

    # EXECUTIVE_SUMMARY
    sections.append(DriftReportSection(
        section_id=create_drift_report_section_id(),
        created_at_utc=_now_utc_str(),
        section_kind=DriftReportSectionKind.EXECUTIVE_SUMMARY,
        title="Executive Summary",
        body="This report details regime monitoring drift tracking.",
        bullet_points=[],
        tables=[],
        warnings=[],
        errors=[],
        qa_status=DriftReportQaStatus.NOT_CHECKED,
        language_risks=[],
        metadata={}
    ))

    # BASELINE_SUMMARY
    b_body = f"Baseline data entries: {len(baseline.get('metrics', [])) if baseline else 0}"
    sections.append(DriftReportSection(
        section_id=create_drift_report_section_id(),
        created_at_utc=_now_utc_str(),
        section_kind=DriftReportSectionKind.BASELINE_SUMMARY,
        title="Baseline Summary",
        body=b_body,
        bullet_points=[],
        tables=[],
        warnings=[],
        errors=[],
        qa_status=DriftReportQaStatus.NOT_CHECKED,
        language_risks=[],
        metadata={}
    ))

    # SAFETY_BOUNDARY
    sections.append(DriftReportSection(
        section_id=create_drift_report_section_id(),
        created_at_utc=_now_utc_str(),
        section_kind=DriftReportSectionKind.SAFETY_BOUNDARY,
        title="Safety Boundary",
        body="This is research data only. No execution, no investment advice.",
        bullet_points=[],
        tables=[],
        warnings=[],
        errors=[],
        qa_status=DriftReportQaStatus.NOT_CHECKED,
        language_risks=[],
        metadata={}
    ))

    return sections

def build_drift_report_document(
    ingestion: RegimeMonitoringIngestionResult,
    validation: MonitoringValidationResult,
    baseline: Optional[Dict[str, Any]],
    snapshot: Optional[Dict[str, Any]],
    drift_result: Optional[Dict[str, Any]],
    degradation_diagnostics: List[Dict[str, Any]],
    degradation_profiles: List[Dict[str, Any]]
) -> DriftReportDocument:

    sections = build_drift_report_sections(ingestion, validation, baseline, snapshot, drift_result, degradation_diagnostics, degradation_profiles)

    doc = DriftReportDocument(
        document_id=create_drift_report_document_id(),
        created_at_utc=_now_utc_str(),
        title="Drift Report",
        sections=sections,
        source_review_id=ingestion.source_review_id,
        rendered_markdown=None,
        rendered_text=None,
        rendered_json=None,
        document_hash=None,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        qa_status=DriftReportQaStatus.NOT_CHECKED,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    doc.rendered_text = render_drift_report_text(doc)
    doc.rendered_markdown = render_drift_report_markdown(doc)
    doc.rendered_json = render_drift_report_json(doc)
    doc.document_hash = compute_drift_report_hash(doc)

    return doc

def render_drift_report_markdown(document: DriftReportDocument) -> str:
    lines = [f"# {document.title}\n"]
    for sec in document.sections:
        lines.append(f"## {sec.title}")
        lines.append(f"{sec.body}\n")
    return "\n".join(lines)

def render_drift_report_text(document: DriftReportDocument) -> str:
    lines = [f"Title: {document.title}\n"]
    for sec in document.sections:
        lines.append(f"--- {sec.title} ---")
        lines.append(f"{sec.body}\n")
    return "\n".join(lines)

def render_drift_report_json(document: DriftReportDocument) -> Dict[str, Any]:
    return {
        "title": document.title,
        "sections": [{"title": s.title, "body": s.body} for s in document.sections]
    }

def compute_drift_report_hash(document: DriftReportDocument) -> str:
    return compute_text_hash(document.rendered_text or "")

def validate_drift_report_document(document: DriftReportDocument) -> List[str]:
    from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_safety_validator import validate_drift_report_safety
    return validate_drift_report_safety(document)

def drift_report_document_summary(document: DriftReportDocument) -> Dict[str, Any]:
    return {"document_id": document.document_id, "sections": len(document.sections)}

def drift_report_document_to_text(document: DriftReportDocument, limit: int = 300) -> str:
    return f"Drift Report {document.document_id} - Sections: {len(document.sections)}"[:limit]
