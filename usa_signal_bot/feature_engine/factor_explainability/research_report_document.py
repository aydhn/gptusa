import datetime
import hashlib
from typing import Any

from usa_signal_bot.core.enums import ResearchReportFormat, ReportQaStatus
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    ResearchReportDocument,
    create_research_report_document_id,
    FactorExplanationReport,
    ExplainabilityInputBundle,
    validate_research_report_document
)
from usa_signal_bot.feature_engine.factor_explainability.research_report_sections import (
    build_executive_summary_section,
    build_data_scope_section,
    build_factor_table_summary_section,
    build_factor_validation_summary_section,
    build_factor_drift_summary_section,
    build_factor_diagnostics_summary_section,
    build_feature_attribution_summary_section,
    build_factor_interpretation_summary_section,
    build_lineage_quality_summary_section,
    build_limitations_section,
    build_safety_boundary_section
)

def compute_research_report_hash(document: ResearchReportDocument) -> str:
    content = document.title + str(document.format) + "".join([s.body for s in document.sections])
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def build_research_report_document(explanation: FactorExplanationReport, bundle: ExplainabilityInputBundle, validation_payload: list[dict[str, Any]] | None = None, drift_payload: list[dict[str, Any]] | None = None, diagnostics_payload: list[dict[str, Any]] | None = None) -> ResearchReportDocument:

    sections = [
        build_executive_summary_section(explanation),
        build_data_scope_section(bundle),
        build_factor_table_summary_section(explanation),
        build_factor_validation_summary_section(validation_payload),
        build_factor_drift_summary_section(drift_payload),
        build_factor_diagnostics_summary_section(diagnostics_payload),
        build_feature_attribution_summary_section(explanation.attribution_results),
        build_factor_interpretation_summary_section(explanation.interpretation_summaries),
        build_lineage_quality_summary_section([]),
        build_limitations_section(),
        build_safety_boundary_section()
    ]

    doc = ResearchReportDocument(
        document_id=create_research_report_document_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        title=f"Factor Explainability Research Report - {bundle.bundle_id}",
        format=ResearchReportFormat.MARKDOWN,
        sections=sections,
        source_explanation_report_id=explanation.explanation_report_id,
        source_review_id=bundle.source_review_id,
        rendered_path=None,
        document_hash=None,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        qa_status=ReportQaStatus.NOT_CHECKED,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    doc.document_hash = compute_research_report_hash(doc)
    validate_research_report_document(doc)
    return doc

def research_report_document_summary(document: ResearchReportDocument) -> dict[str, Any]:
    return {"section_count": len(document.sections), "qa_status": document.qa_status.value}

def research_report_document_to_text(document: ResearchReportDocument, limit: int = 300) -> str:
    return f"Research Report Document (ID: {document.document_id}, Status: {document.qa_status.value})"
