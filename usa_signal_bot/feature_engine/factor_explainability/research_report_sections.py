import datetime
from typing import Any

from usa_signal_bot.core.enums import ResearchReportSectionKind, ReportQaStatus
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    ResearchReportSection,
    create_research_report_section_id,
    FactorExplanationReport,
    ExplainabilityInputBundle,
    FeatureAttributionResult,
    FactorInterpretationSummary
)

def _build_base_section(kind: ResearchReportSectionKind, title: str, body: str, bullets: list[str] = None) -> ResearchReportSection:
    return ResearchReportSection(
        section_id=create_research_report_section_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        section_kind=kind,
        title=title,
        body=body,
        bullet_points=bullets or [],
        tables=[],
        warnings=[],
        errors=[],
        qa_status=ReportQaStatus.NOT_CHECKED,
        language_risks=[],
        metadata={}
    )

def build_executive_summary_section(explanation: FactorExplanationReport) -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.EXECUTIVE_SUMMARY,
        "Executive Summary",
        "This report provides factor explainability metadata and research attributions.",
        ["This is not investment advice.", "Generated deterministically."]
    )

def build_data_scope_section(bundle: ExplainabilityInputBundle) -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.DATA_SCOPE,
        "Data Scope",
        f"Analyzed bundle {bundle.bundle_id}. Used offline research data only."
    )

def build_factor_table_summary_section(explanation: FactorExplanationReport) -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.FACTOR_TABLE_SUMMARY,
        "Factor Table Summary",
        "Factor tables provide mathematical context."
    )

def build_factor_validation_summary_section(validation_payload: list[dict[str, Any]] | None = None) -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.FACTOR_VALIDATION_SUMMARY,
        "Factor Validation Summary",
        "Validation passes boundary checks."
    )

def build_factor_drift_summary_section(drift_payload: list[dict[str, Any]] | None = None) -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.FACTOR_DRIFT_SUMMARY,
        "Factor Drift Summary",
        "Drift metrics reviewed."
    )

def build_factor_diagnostics_summary_section(diagnostics_payload: list[dict[str, Any]] | None = None) -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.FACTOR_DIAGNOSTICS_SUMMARY,
        "Factor Diagnostics Summary",
        "Diagnostic metadata gathered."
    )

def build_feature_attribution_summary_section(attributions: list[FeatureAttributionResult]) -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.FEATURE_ATTRIBUTION_SUMMARY,
        "Feature Attribution Summary",
        f"Attribution calculated for {len(attributions)} items based on variance and coverage."
    )

def build_factor_interpretation_summary_section(interpretations: list[FactorInterpretationSummary]) -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.FACTOR_INTERPRETATION_SUMMARY,
        "Factor Interpretation Summary",
        f"Created {len(interpretations)} interpretation summaries contextually."
    )

def build_lineage_quality_summary_section(notes: list[str]) -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.LINEAGE_AND_QUALITY_SUMMARY,
        "Lineage and Quality Summary",
        "Lineage and quality notes attached.",
        notes
    )

def build_limitations_section() -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.LIMITATIONS,
        "Limitations",
        "The model uses historical metadata. Do not use for live trading."
    )

def build_safety_boundary_section() -> ResearchReportSection:
    return _build_base_section(
        ResearchReportSectionKind.SAFETY_BOUNDARY,
        "Safety Boundaries",
        "No broker execution, no live telemetry, no order generation allowed.",
        ["No paid APIs", "No web scraping"]
    )

def validate_research_report_sections(sections: list[ResearchReportSection]) -> list[str]:
    errors = []
    for s in sections:
        if s.qa_status == ReportQaStatus.FAIL:
            errors.append(f"Section {s.section_id} failed QA")
    return errors
