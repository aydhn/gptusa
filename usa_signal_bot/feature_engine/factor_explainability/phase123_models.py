import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.core.enums import (
    FactorExplainabilityStatus,
    FactorExplainabilityDecision,
    FeatureAttributionMethod,
    AttributionDirection,
    FactorInterpretationKind,
    ResearchReportSectionKind,
    ResearchReportFormat,
    ReportQaStatus,
    ReportLanguageRiskKind,
    FactorExplainabilityQuality,
    FactorExplainabilityRiskFlag,
    FactorExplainabilityReportType
)

@dataclass
class FactorValidationIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    factor_validation_ready: bool
    drift_monitoring_ready: bool
    factor_versioning_ready: bool
    factor_store_hardened: bool
    ready_for_phase123: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    paid_api_enabled: bool
    dashboard_enabled: bool
    network_default_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    valid_for_phase123: bool
    risk_flags: list[FactorExplainabilityRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class ExplainabilityInputBundle:
    bundle_id: str
    created_at_utc: str
    source_review_id: str | None
    factor_table_paths: dict[str, str]
    validation_result_refs: list[str]
    drift_report_refs: list[str]
    diagnostics_refs: list[str]
    manifest_ref: str | None
    schema_signature_ref: str | None
    version_ref: str | None
    available: bool
    research_data_only: bool
    bundle_valid: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorExplainabilityRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureAttributionSpec:
    spec_id: str
    created_at_utc: str
    factor_name: str
    factor_column: str
    input_feature_columns: list[str]
    attribution_method: FeatureAttributionMethod
    normalize_attributions: bool
    quality_weighted: bool
    confidence_weighted: bool
    lineage_weighted: bool
    deterministic: bool
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorExplainabilityRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureAttributionResult:
    attribution_id: str
    created_at_utc: str
    symbol: str
    factor_name: str
    factor_column: str
    feature_column: str
    attribution_score: float
    normalized_attribution_score: float
    attribution_direction: AttributionDirection
    method: FeatureAttributionMethod
    coverage_ratio: float | None
    quality_score: float | None
    confidence_score: float | None
    lineage_score: float | None
    explanation_text: str
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorExplainabilityRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorContributionProfile:
    contribution_id: str
    created_at_utc: str
    symbol: str
    factor_name: str
    factor_column: str
    top_positive_features: list[dict[str, Any]]
    top_negative_features: list[dict[str, Any]]
    neutral_features: list[dict[str, Any]]
    contribution_coverage_ratio: float
    total_abs_attribution: float
    attribution_count: int
    quality: FactorExplainabilityQuality
    explanation_text: str
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorExplainabilityRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorInterpretationSummary:
    interpretation_id: str
    created_at_utc: str
    symbol: str | None
    factor_name: str
    factor_column: str
    interpretation_kind: FactorInterpretationKind
    short_summary: str
    diagnostic_summary: str
    drift_summary: str
    lineage_quality_summary: str
    limitations: list[str]
    confidence_notes: list[str]
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorExplainabilityRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FactorExplanationReport:
    explanation_report_id: str
    created_at_utc: str
    symbol: str | None
    factor_names: list[str]
    attribution_results: list[FeatureAttributionResult]
    contribution_profiles: list[FactorContributionProfile]
    interpretation_summaries: list[FactorInterpretationSummary]
    quality: FactorExplainabilityQuality
    report_valid: bool
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorExplainabilityRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ResearchReportSection:
    section_id: str
    created_at_utc: str
    section_kind: ResearchReportSectionKind
    title: str
    body: str
    bullet_points: list[str]
    tables: list[dict[str, Any]]
    warnings: list[str]
    errors: list[str]
    qa_status: ReportQaStatus
    language_risks: list[ReportLanguageRiskKind]
    metadata: dict[str, Any]

@dataclass
class ResearchReportDocument:
    document_id: str
    created_at_utc: str
    title: str
    format: ResearchReportFormat
    sections: list[ResearchReportSection]
    source_explanation_report_id: str | None
    source_review_id: str | None
    rendered_path: str | None
    document_hash: str | None
    research_metadata_only: bool
    investment_advice: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    qa_status: ReportQaStatus
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorExplainabilityRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ReportQaRuleResult:
    qa_result_id: str
    created_at_utc: str
    rule_name: str
    status: ReportQaStatus
    passed: bool
    language_risk: ReportLanguageRiskKind | None
    matched_terms: list[str]
    field: str | None
    message: str
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class ExplainabilityContext:
    context_id: str
    created_at_utc: str
    status: FactorExplainabilityStatus
    decision: FactorExplainabilityDecision
    source_factor_validation_review_id: str | None
    ingestion: FactorValidationIngestionResult
    input_bundle: ExplainabilityInputBundle
    attribution_specs: list[FeatureAttributionSpec]
    attribution_results: list[FeatureAttributionResult]
    contribution_profiles: list[FactorContributionProfile]
    interpretation_summaries: list[FactorInterpretationSummary]
    explanation_report: FactorExplanationReport
    research_report: ResearchReportDocument
    qa_results: list[ReportQaRuleResult]
    attribution_ready: bool
    contribution_ready: bool
    interpretation_ready: bool
    research_report_ready: bool
    report_qa_passed: bool
    ready_for_phase124: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    paid_api_enabled: bool
    dashboard_enabled: bool
    network_default_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[FactorExplainabilityRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ExplainabilityFullReview:
    review_id: str
    created_at_utc: str
    report_type: FactorExplainabilityReportType
    ingestion: FactorValidationIngestionResult
    context: ExplainabilityContext
    input_bundle: ExplainabilityInputBundle
    attribution_specs: list[FeatureAttributionSpec]
    explanation_report: FactorExplanationReport
    research_report: ResearchReportDocument
    qa_results: list[ReportQaRuleResult]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def create_factor_validation_ingestion_id() -> str:
    return f"FVI-{uuid.uuid4().hex[:8]}"

def create_explainability_input_bundle_id() -> str:
    return f"EIB-{uuid.uuid4().hex[:8]}"

def create_feature_attribution_spec_id() -> str:
    return f"FAS-{uuid.uuid4().hex[:8]}"

def create_feature_attribution_result_id() -> str:
    return f"FAR-{uuid.uuid4().hex[:8]}"

def create_factor_contribution_profile_id() -> str:
    return f"FCP-{uuid.uuid4().hex[:8]}"

def create_factor_interpretation_summary_id() -> str:
    return f"FIS-{uuid.uuid4().hex[:8]}"

def create_factor_explanation_report_id() -> str:
    return f"FER-{uuid.uuid4().hex[:8]}"

def create_research_report_section_id() -> str:
    return f"RRS-{uuid.uuid4().hex[:8]}"

def create_research_report_document_id() -> str:
    return f"RRD-{uuid.uuid4().hex[:8]}"

def create_report_qa_rule_result_id() -> str:
    return f"RQA-{uuid.uuid4().hex[:8]}"

def create_explainability_context_id() -> str:
    return f"EXC-{uuid.uuid4().hex[:8]}"

def create_explainability_full_review_id() -> str:
    return f"EFR-{uuid.uuid4().hex[:8]}"

def _to_dict_safe(obj: Any) -> dict:
    if hasattr(obj, '__dataclass_fields__'):
        return {k: _to_dict_safe(getattr(obj, k)) for k in obj.__dataclass_fields__}
    elif isinstance(obj, list):
        return [_to_dict_safe(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: _to_dict_safe(v) for k, v in obj.items()}
    elif hasattr(obj, 'value'):
        return obj.value
    else:
        return obj

def factor_validation_ingestion_result_to_dict(item: FactorValidationIngestionResult) -> dict:
    return _to_dict_safe(item)

def explainability_input_bundle_to_dict(item: ExplainabilityInputBundle) -> dict:
    return _to_dict_safe(item)

def feature_attribution_spec_to_dict(item: FeatureAttributionSpec) -> dict:
    return _to_dict_safe(item)

def feature_attribution_result_to_dict(item: FeatureAttributionResult) -> dict:
    return _to_dict_safe(item)

def factor_contribution_profile_to_dict(item: FactorContributionProfile) -> dict:
    return _to_dict_safe(item)

def factor_interpretation_summary_to_dict(item: FactorInterpretationSummary) -> dict:
    return _to_dict_safe(item)

def factor_explanation_report_to_dict(item: FactorExplanationReport) -> dict:
    return _to_dict_safe(item)

def research_report_section_to_dict(item: ResearchReportSection) -> dict:
    return _to_dict_safe(item)

def research_report_document_to_dict(item: ResearchReportDocument) -> dict:
    return _to_dict_safe(item)

def report_qa_rule_result_to_dict(item: ReportQaRuleResult) -> dict:
    return _to_dict_safe(item)

def explainability_context_to_dict(item: ExplainabilityContext) -> dict:
    return _to_dict_safe(item)

def explainability_full_review_to_dict(item: ExplainabilityFullReview) -> dict:
    return _to_dict_safe(item)

def validate_factor_validation_ingestion_result(item: FactorValidationIngestionResult) -> None:
    if not item.factor_validation_ready: item.errors.append("factor_validation_ready false")
    if not item.drift_monitoring_ready: item.errors.append("drift_monitoring_ready false")
    if not item.factor_versioning_ready: item.errors.append("factor_versioning_ready false")
    if not item.factor_store_hardened: item.errors.append("factor_store_hardened false")
    if not item.ready_for_phase123: item.errors.append("ready_for_phase123 false")
    if not item.research_data_only: item.errors.append("research_data_only false")
    if item.activation_allowed: item.errors.append("activation_allowed true")
    if item.strategy_activation_allowed: item.errors.append("strategy_activation_allowed true")
    if item.active_paper_enabled: item.errors.append("active_paper_enabled true")
    if item.broker_execution_enabled: item.errors.append("broker_execution_enabled true")
    if item.order_creation_enabled: item.errors.append("order_creation_enabled true")
    if item.paper_state_mutation_enabled: item.errors.append("paper_state_mutation_enabled true")
    if item.telegram_real_send_enabled: item.errors.append("telegram_real_send_enabled true")
    if item.scraping_enabled: item.errors.append("scraping_enabled true")
    if item.html_parse_enabled: item.errors.append("html_parse_enabled true")
    if item.paid_api_enabled: item.errors.append("paid_api_enabled true")
    if item.dashboard_enabled: item.errors.append("dashboard_enabled true")
    if item.network_default_enabled: item.errors.append("network_default_enabled true")
    if item.produces_trade_signal: item.errors.append("produces_trade_signal true")
    if item.produces_order_decision: item.errors.append("produces_order_decision true")
    if item.produces_portfolio_weights: item.errors.append("produces_portfolio_weights true")
    if item.network_used: item.errors.append("network_used true")
    if item.paid_api_used: item.errors.append("paid_api_used true")
    if item.scraping_used: item.errors.append("scraping_used true")
    if item.html_parsing_used: item.errors.append("html_parsing_used true")
    if item.broker_used: item.errors.append("broker_used true")
    if item.order_created: item.errors.append("order_created true")
    if item.paper_state_mutated: item.errors.append("paper_state_mutated true")
    if item.telegram_real_sent: item.errors.append("telegram_real_sent true")
    if item.dashboard_started: item.errors.append("dashboard_started true")

def validate_explainability_input_bundle(item: ExplainabilityInputBundle) -> None:
    pass

def validate_feature_attribution_spec(item: FeatureAttributionSpec) -> None:
    pass

def validate_feature_attribution_result(item: FeatureAttributionResult) -> None:
    if not (0 <= item.attribution_score <= 100): item.errors.append("Attribution score out of bounds")
    if not (0 <= item.normalized_attribution_score <= 1): item.errors.append("Normalized attribution score out of bounds")

def validate_factor_contribution_profile(item: FactorContributionProfile) -> None:
    pass

def validate_factor_interpretation_summary(item: FactorInterpretationSummary) -> None:
    pass

def validate_factor_explanation_report(item: FactorExplanationReport) -> None:
    pass

def validate_research_report_document(item: ResearchReportDocument) -> None:
    if item.qa_status == ReportQaStatus.FAIL: item.errors.append("Report text has unsafe execution language")

def validate_report_qa_rule_result(item: ReportQaRuleResult) -> None:
    pass

def validate_explainability_context(item: ExplainabilityContext) -> None:
    if not item.report_qa_passed: item.ready_for_phase124 = False

def validate_explainability_full_review(item: ExplainabilityFullReview) -> None:
    pass
