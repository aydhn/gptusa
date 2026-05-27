from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import (
    FeatureEnrichmentStatus,
    FeatureEnrichmentDecision,
    FeatureEnrichmentFamily,
    EventAwareFeatureKind,
    QualityAwareFeatureKind,
    CalendarAwareFeatureKind,
    FeatureInteractionKind,
    FeatureConfidenceLevel,
    FeatureFreshnessStatus,
    FeatureEnrichmentQuality,
    FeatureEnrichmentRiskFlag,
    FeatureEnrichmentReportType,
)

def _uuid_str() -> str:
    return str(uuid.uuid4())

def _now_str() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class AdvancedFeatureIngestionResult:
    ingestion_id: str
    created_at_utc: str
    available: bool
    advanced_features_ready: bool
    cross_sectional_features_ready: bool
    multi_symbol_feature_table_ready: bool
    ready_for_phase119: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
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
    valid_for_phase119: bool
    source_path: str | None = None
    source_review_id: str | None = None
    source_context_id: str | None = None
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureEnrichmentSpec:
    spec_id: str
    created_at_utc: str
    name: str
    family: FeatureEnrichmentFamily
    kind: str
    local_pandas_only: bool
    requires_network: bool
    requires_paid_api: bool
    requires_scraping: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    input_columns: list[str] = field(default_factory=list)
    output_columns: list[str] = field(default_factory=list)
    required_metadata_inputs: list[str] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureInteractionSpec:
    interaction_id: str
    created_at_utc: str
    name: str
    interaction_kind: FeatureInteractionKind
    left_feature: str
    output_column: str
    local_pandas_only: bool
    safe_for_research_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    right_feature: str | None = None
    conditioning_feature: str | None = None
    parameters: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureConfidenceProfile:
    confidence_id: str
    created_at_utc: str
    symbol: str
    confidence_score: float
    confidence_level: FeatureConfidenceLevel
    warning_count: int
    metadata_only: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    feature_columns: list[str] = field(default_factory=list)
    provider_quality_score: float | None = None
    source_trust_score: float | None = None
    freshness_score: float | None = None
    anomaly_penalty: float | None = None
    lineage_completeness_score: float | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureFreshnessProfile:
    freshness_id: str
    created_at_utc: str
    symbol: str
    status: FeatureFreshnessStatus
    freshness_score: float
    stale_feature_count: int
    unknown_timestamp_count: int
    latest_feature_timestamp: str | None = None
    latest_source_timestamp: str | None = None
    age_days: float | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureEnrichmentRequest:
    request_id: str
    created_at_utc: str
    include_event_features: bool
    include_quality_features: bool
    include_calendar_features: bool
    include_interactions: bool
    metadata_only: bool
    dry_run_only: bool
    research_data_only: bool
    compute_values: bool
    allow_network: bool
    allow_paid_api: bool
    allow_scraping: bool
    allow_html_parsing: bool
    allow_broker: bool
    allow_order: bool
    allow_paper_mutation: bool
    allow_telegram_real_send: bool
    allow_dashboard: bool
    symbols: list[str] = field(default_factory=list)
    input_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureEnrichmentResult:
    result_id: str
    created_at_utc: str
    event_feature_count: int
    quality_feature_count: int
    calendar_feature_count: int
    interaction_feature_count: int
    quality: FeatureEnrichmentQuality
    metadata_only: bool
    dry_run_only: bool
    research_data_only: bool
    computed_values: bool
    produced_trade_signal: bool
    produced_order_decision: bool
    produced_portfolio_weights: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    passed: bool
    request_id: str | None = None
    symbols: list[str] = field(default_factory=list)
    enriched_feature_columns: list[str] = field(default_factory=list)
    interaction_feature_columns: list[str] = field(default_factory=list)
    confidence_profiles: list[FeatureConfidenceProfile] = field(default_factory=list)
    freshness_profiles: list[FeatureFreshnessProfile] = field(default_factory=list)
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class EnrichedFeatureTableResult:
    table_id: str
    created_at_utc: str
    symbol: str
    rows: int
    quality: FeatureEnrichmentQuality
    metadata_only: bool
    research_data_only: bool
    produced_trade_signal: bool
    produced_order_decision: bool
    produced_portfolio_weights: bool
    network_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    columns: list[str] = field(default_factory=list)
    base_feature_columns: list[str] = field(default_factory=list)
    enriched_feature_columns: list[str] = field(default_factory=list)
    interaction_feature_columns: list[str] = field(default_factory=list)
    feature_family_counts: dict[str, int] = field(default_factory=dict)
    null_summary: dict[str, Any] = field(default_factory=dict)
    confidence_profile: FeatureConfidenceProfile | None = None
    freshness_profile: FeatureFreshnessProfile | None = None
    output_path: str | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureEnrichmentAudit:
    audit_id: str
    created_at_utc: str
    enriched_feature_column_count: int
    interaction_feature_column_count: int
    computation_deterministic: bool
    local_only: bool
    no_network: bool
    no_broker: bool
    no_order: bool
    no_paper_mutation: bool
    no_trade_signal: bool
    no_portfolio_weights: bool
    symbols: list[str] = field(default_factory=list)
    input_hashes: dict[str, str] = field(default_factory=dict)
    context_hashes: dict[str, str] = field(default_factory=dict)
    output_hashes: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureEnrichmentContext:
    context_id: str
    created_at_utc: str
    status: FeatureEnrichmentStatus
    decision: FeatureEnrichmentDecision
    ingestion: AdvancedFeatureIngestionResult
    event_enrichment_ready: bool
    quality_enrichment_ready: bool
    calendar_enrichment_ready: bool
    interactions_ready: bool
    enriched_feature_table_ready: bool
    ready_for_phase120: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
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
    source_advanced_feature_review_id: str | None = None
    enrichment_specs: list[FeatureEnrichmentSpec] = field(default_factory=list)
    interaction_specs: list[FeatureInteractionSpec] = field(default_factory=list)
    requests: list[FeatureEnrichmentRequest] = field(default_factory=list)
    results: list[FeatureEnrichmentResult] = field(default_factory=list)
    feature_tables: list[EnrichedFeatureTableResult] = field(default_factory=list)
    audits: list[FeatureEnrichmentAudit] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FeatureEnrichmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureEnrichmentFullReview:
    review_id: str
    created_at_utc: str
    report_type: FeatureEnrichmentReportType
    ingestion: AdvancedFeatureIngestionResult
    context: FeatureEnrichmentContext
    enrichment_specs: list[FeatureEnrichmentSpec] = field(default_factory=list)
    interaction_specs: list[FeatureInteractionSpec] = field(default_factory=list)
    results: list[FeatureEnrichmentResult] = field(default_factory=list)
    feature_tables: list[EnrichedFeatureTableResult] = field(default_factory=list)
    audits: list[FeatureEnrichmentAudit] = field(default_factory=list)
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def create_advanced_feature_ingestion_id() -> str:
    return f"adv_ingest_{_uuid_str()}"

def create_feature_enrichment_spec_id() -> str:
    return f"spec_{_uuid_str()}"

def create_feature_interaction_spec_id() -> str:
    return f"int_spec_{_uuid_str()}"

def create_feature_confidence_profile_id() -> str:
    return f"conf_{_uuid_str()}"

def create_feature_freshness_profile_id() -> str:
    return f"fresh_{_uuid_str()}"

def create_feature_enrichment_request_id() -> str:
    return f"enr_req_{_uuid_str()}"

def create_feature_enrichment_result_id() -> str:
    return f"enr_res_{_uuid_str()}"

def create_enriched_feature_table_id() -> str:
    return f"enr_tbl_{_uuid_str()}"

def create_feature_enrichment_audit_id() -> str:
    return f"enr_aud_{_uuid_str()}"

def create_feature_enrichment_context_id() -> str:
    return f"enr_ctx_{_uuid_str()}"

def create_feature_enrichment_full_review_id() -> str:
    return f"enr_rev_{_uuid_str()}"

# Simplified _to_dict methods (in practice use dataclasses.asdict or custom logic)
import dataclasses

def advanced_feature_ingestion_result_to_dict(item: AdvancedFeatureIngestionResult) -> dict:
    return dataclasses.asdict(item)

def feature_enrichment_spec_to_dict(item: FeatureEnrichmentSpec) -> dict:
    return dataclasses.asdict(item)

def feature_interaction_spec_to_dict(item: FeatureInteractionSpec) -> dict:
    return dataclasses.asdict(item)

def feature_confidence_profile_to_dict(item: FeatureConfidenceProfile) -> dict:
    return dataclasses.asdict(item)

def feature_freshness_profile_to_dict(item: FeatureFreshnessProfile) -> dict:
    return dataclasses.asdict(item)

def feature_enrichment_request_to_dict(item: FeatureEnrichmentRequest) -> dict:
    return dataclasses.asdict(item)

def feature_enrichment_result_to_dict(item: FeatureEnrichmentResult) -> dict:
    return dataclasses.asdict(item)

def enriched_feature_table_result_to_dict(item: EnrichedFeatureTableResult) -> dict:
    return dataclasses.asdict(item)

def feature_enrichment_audit_to_dict(item: FeatureEnrichmentAudit) -> dict:
    return dataclasses.asdict(item)

def feature_enrichment_context_to_dict(item: FeatureEnrichmentContext) -> dict:
    return dataclasses.asdict(item)

def feature_enrichment_full_review_to_dict(item: FeatureEnrichmentFullReview) -> dict:
    return dataclasses.asdict(item)

def validate_advanced_feature_ingestion_result(item: AdvancedFeatureIngestionResult) -> None:
    if not item.advanced_features_ready:
        item.errors.append("advanced_features_ready must be true")
    if not item.cross_sectional_features_ready:
        item.errors.append("cross_sectional_features_ready must be true")
    if not item.multi_symbol_feature_table_ready:
        item.errors.append("multi_symbol_feature_table_ready must be true")
    if not item.ready_for_phase119:
        item.errors.append("ready_for_phase119 must be true")
    if not item.research_data_only:
        item.errors.append("research_data_only must be true")

    if item.activation_allowed: item.errors.append("activation_allowed must be false")
    if item.active_paper_enabled: item.errors.append("active_paper_enabled must be false")
    if item.broker_execution_enabled: item.errors.append("broker_execution_enabled must be false")
    if item.order_creation_enabled: item.errors.append("order_creation_enabled must be false")
    if item.paper_state_mutation_enabled: item.errors.append("paper_state_mutation_enabled must be false")
    if item.telegram_real_send_enabled: item.errors.append("telegram_real_send_enabled must be false")
    if item.scraping_enabled: item.errors.append("scraping_enabled must be false")
    if item.html_parse_enabled: item.errors.append("html_parse_enabled must be false")
    if item.paid_api_enabled: item.errors.append("paid_api_enabled must be false")
    if item.dashboard_enabled: item.errors.append("dashboard_enabled must be false")
    if item.network_default_enabled: item.errors.append("network_default_enabled must be false")
    if item.produces_trade_signal: item.errors.append("produces_trade_signal must be false")
    if item.produces_order_decision: item.errors.append("produces_order_decision must be false")
    if item.produces_portfolio_weights: item.errors.append("produces_portfolio_weights must be false")
    if item.network_used: item.errors.append("network_used must be false")
    if item.paid_api_used: item.errors.append("paid_api_used must be false")
    if item.scraping_used: item.errors.append("scraping_used must be false")
    if item.html_parsing_used: item.errors.append("html_parsing_used must be false")
    if item.broker_used: item.errors.append("broker_used must be false")
    if item.order_created: item.errors.append("order_created must be false")
    if item.paper_state_mutated: item.errors.append("paper_state_mutated must be false")
    if item.telegram_real_sent: item.errors.append("telegram_real_sent must be false")
    if item.dashboard_started: item.errors.append("dashboard_started must be false")

def validate_feature_enrichment_spec(item: FeatureEnrichmentSpec) -> None:
    if item.requires_network: item.errors.append("requires_network must be false")
    if item.requires_paid_api: item.errors.append("requires_paid_api must be false")
    if item.requires_scraping: item.errors.append("requires_scraping must be false")

def validate_feature_interaction_spec(item: FeatureInteractionSpec) -> None:
    pass

def validate_feature_confidence_profile(item: FeatureConfidenceProfile) -> None:
    if item.confidence_score < 0.0 or item.confidence_score > 100.0:
        item.errors.append("confidence_score must be between 0 and 100")

def validate_feature_freshness_profile(item: FeatureFreshnessProfile) -> None:
    if item.freshness_score < 0.0 or item.freshness_score > 100.0:
        item.errors.append("freshness_score must be between 0 and 100")

def validate_feature_enrichment_request(item: FeatureEnrichmentRequest) -> None:
    if item.allow_network: item.errors.append("allow_network must be false")

def validate_feature_enrichment_result(item: FeatureEnrichmentResult) -> None:
    if item.produced_trade_signal: item.errors.append("produced_trade_signal must be false")
    if item.produced_order_decision: item.errors.append("produced_order_decision must be false")
    if item.produced_portfolio_weights: item.errors.append("produced_portfolio_weights must be false")

def validate_enriched_feature_table_result(item: EnrichedFeatureTableResult) -> None:
    pass

def validate_feature_enrichment_audit(item: FeatureEnrichmentAudit) -> None:
    if not item.no_network: item.errors.append("no_network must be true")
    if not item.no_broker: item.errors.append("no_broker must be true")
    if not item.no_order: item.errors.append("no_order must be true")
    if not item.no_paper_mutation: item.errors.append("no_paper_mutation must be true")
    if not item.no_trade_signal: item.errors.append("no_trade_signal must be true")
    if not item.no_portfolio_weights: item.errors.append("no_portfolio_weights must be true")

def validate_feature_enrichment_context(item: FeatureEnrichmentContext) -> None:
    pass

def validate_feature_enrichment_full_review(item: FeatureEnrichmentFullReview) -> None:
    pass
