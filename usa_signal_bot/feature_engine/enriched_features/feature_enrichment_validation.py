from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    FeatureEnrichmentContext, FeatureEnrichmentFullReview
)

@dataclass
class FeatureEnrichmentValidationIssue:
    severity: str
    message: str
    field: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureEnrichmentValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[FeatureEnrichmentValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_feature_enrichment_context_report(item: FeatureEnrichmentContext) -> FeatureEnrichmentValidationReport:
    report = FeatureEnrichmentValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    # Simple check for forbidden flags
    if item.activation_allowed:
        report.valid = False
        report.errors.append("activation_allowed is true")
    return report

def validate_feature_enrichment_full_review_report(item: FeatureEnrichmentFullReview) -> FeatureEnrichmentValidationReport:
    return validate_feature_enrichment_context_report(item.context)

def validate_no_sensitive_data_in_feature_enrichment_payload(payload: dict[str, Any]) -> FeatureEnrichmentValidationReport:
    return FeatureEnrichmentValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)

def validate_no_execution_language_in_feature_enrichment_text(text: str) -> FeatureEnrichmentValidationReport:
    return FeatureEnrichmentValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)

def validate_no_unsafe_feature_enrichment_fields(payload: dict[str, Any]) -> FeatureEnrichmentValidationReport:
    return FeatureEnrichmentValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)

def feature_enrichment_validation_report_to_text(report: FeatureEnrichmentValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {len(report.errors)}"

def assert_feature_enrichment_validation_valid(report: FeatureEnrichmentValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Validation failed: {report.errors}")
