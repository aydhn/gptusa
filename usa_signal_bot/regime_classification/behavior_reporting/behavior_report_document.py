import hashlib
import json
from typing import Any

from usa_signal_bot.core.enums import BehaviorReportFormat
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    BehaviorReportDocument, RegimeTransitionIngestionResult, MarketBehaviorProfile,
    RegimeBehaviorSummary, RegimeDiagnosticsInterpretation
)
from usa_signal_bot.regime_classification.behavior_reporting.behavior_report_sections import (
    build_behavior_executive_summary_section, build_behavior_data_scope_section,
    build_transition_matrix_summary_section, build_persistence_summary_section,
    build_duration_churn_summary_section, build_stability_summary_section,
    build_market_behavior_profiles_section, build_cross_symbol_behavior_section,
    build_diagnostic_interpretation_section, build_behavior_limitations_section,
    build_behavior_safety_boundary_section
)

def build_behavior_report_document(
    ingestion: RegimeTransitionIngestionResult,
    profiles: list[MarketBehaviorProfile],
    summaries: list[RegimeBehaviorSummary],
    interpretations: list[RegimeDiagnosticsInterpretation],
    format: BehaviorReportFormat = BehaviorReportFormat.MARKDOWN
) -> BehaviorReportDocument:
    doc = BehaviorReportDocument()
    doc.title = "Market Behavior Report"
    doc.format = format

    doc.sections = [
        build_behavior_executive_summary_section(profiles, summaries),
        build_behavior_data_scope_section(ingestion),
        build_transition_matrix_summary_section(summaries),
        build_persistence_summary_section(summaries),
        build_duration_churn_summary_section(summaries),
        build_stability_summary_section(summaries),
        build_market_behavior_profiles_section(profiles),
        build_cross_symbol_behavior_section(profiles),
        build_diagnostic_interpretation_section(interpretations),
        build_behavior_limitations_section(),
        build_behavior_safety_boundary_section()
    ]

    doc.document_hash = compute_behavior_report_hash(doc)
    return doc

def compute_behavior_report_hash(document: BehaviorReportDocument) -> str:
    content = f"{document.title}_{document.format.value}_{len(document.sections)}"
    for s in document.sections:
        content += f"_{s.title}_{s.body}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def validate_behavior_report_document(document: BehaviorReportDocument) -> list[str]:
    errs = []
    if not document.research_metadata_only: errs.append("research_metadata_only must be true")
    if document.investment_advice: errs.append("investment_advice must be false")
    if document.produces_trade_signal: errs.append("produces_trade_signal must be false")
    if document.produces_order_decision: errs.append("produces_order_decision must be false")
    if document.produces_portfolio_weights: errs.append("produces_portfolio_weights must be false")
    return errs

def behavior_report_document_summary(document: BehaviorReportDocument) -> dict[str, Any]:
    return {"title": document.title, "sections": len(document.sections)}

def behavior_report_document_to_text(document: BehaviorReportDocument, limit: int = 300) -> str:
    return f"Document: {document.title} ({len(document.sections)} sections)"
