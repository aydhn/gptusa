from typing import Any
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    FactorValidationIngestionResult,
    ExplainabilityInputBundle,
    FeatureAttributionSpec,
    FeatureAttributionResult,
    FactorContributionProfile,
    FactorInterpretationSummary,
    FactorExplanationReport,
    ResearchReportSection,
    ResearchReportDocument,
    ReportQaRuleResult,
    ExplainabilityContext,
    ExplainabilityFullReview
)
from usa_signal_bot.feature_engine.factor_explainability.explainability_report import explainability_limitations_text as el_text

def factor_validation_ingestion_result_to_text(item: FactorValidationIngestionResult) -> str:
    return f"Ingestion {item.ingestion_id} - valid: {item.valid_for_phase123}"

def explainability_input_bundle_to_text(item: ExplainabilityInputBundle) -> str:
    return f"Bundle {item.bundle_id} - valid: {item.bundle_valid}"

def feature_attribution_spec_to_text(item: FeatureAttributionSpec) -> str:
    return f"Spec {item.spec_id} - factor: {item.factor_name}"

def feature_attribution_result_to_text(item: FeatureAttributionResult) -> str:
    return f"Result {item.attribution_id} - feature: {item.feature_column} - score: {item.attribution_score}"

def factor_contribution_profile_to_text(item: FactorContributionProfile) -> str:
    return f"Profile {item.contribution_id} - count: {item.attribution_count}"

def factor_interpretation_summary_to_text(item: FactorInterpretationSummary) -> str:
    return f"Interpretation {item.interpretation_id} - kind: {item.interpretation_kind.value}"

def factor_explanation_report_to_text(item: FactorExplanationReport, limit: int = 300) -> str:
    return f"Explanation Report {item.explanation_report_id} - valid: {item.report_valid}"

def research_report_section_to_text(item: ResearchReportSection, limit: int = 200) -> str:
    return f"Section {item.section_id} - title: {item.title}"

def research_report_document_to_text(item: ResearchReportDocument, limit: int = 300) -> str:
    return f"Report Document {item.document_id} - QA Status: {item.qa_status.value}"

def report_qa_rule_result_to_text(item: ReportQaRuleResult) -> str:
    return f"QA Rule {item.qa_result_id} - {item.rule_name}: {item.status.value}"

def explainability_context_to_text(item: ExplainabilityContext, limit: int = 300) -> str:
    return f"Explainability Context {item.context_id} - Ready for Phase 124: {item.ready_for_phase124}"

def explainability_full_review_to_text(item: ExplainabilityFullReview, limit: int = 300) -> str:
    return f"Full Review {item.review_id} - Context: {item.context.context_id}"

def explainability_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Explainability Store Summary - Reviews: {summary.get('reviews_count', 0)}"

def explainability_limitations_text() -> str:
    return el_text()
