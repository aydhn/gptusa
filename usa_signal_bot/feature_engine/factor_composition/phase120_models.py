from dataclasses import dataclass, field, asdict
from typing import Any
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import (
    FeatureGroupKind,
    FactorCandidateKind,
    FeatureSelectionStatus,
    FeatureSelectionReason,
    FactorReadinessStatus,
    FactorReadinessRuleKind,
    FactorCompositionStatus,
    FactorCompositionDecision,
    FactorCompositionQuality,
    FactorCompositionRiskFlag,
    FactorCompositionReportType
)

def _uuid_str() -> str:
    return str(uuid.uuid4())

def _now_str() -> str:
    return datetime.now(timezone.utc).isoformat()

def create_feature_enrichment_ingestion_id() -> str: return f"fc_ing_{_uuid_str()}"
def create_feature_group_definition_id() -> str: return f"fg_def_{_uuid_str()}"
def create_feature_group_profile_id() -> str: return f"fg_prof_{_uuid_str()}"
def create_factor_component_id() -> str: return f"fc_comp_{_uuid_str()}"
def create_factor_candidate_id() -> str: return f"fc_cand_{_uuid_str()}"
def create_factor_composition_spec_id() -> str: return f"fc_spec_{_uuid_str()}"
def create_feature_coverage_profile_id() -> str: return f"fc_cov_{_uuid_str()}"
def create_feature_redundancy_profile_id() -> str: return f"fc_red_{_uuid_str()}"
def create_feature_stability_profile_id() -> str: return f"fc_stab_{_uuid_str()}"
def create_feature_selection_metadata_id() -> str: return f"fc_sel_{_uuid_str()}"
def create_factor_readiness_rule_id() -> str: return f"fc_rule_{_uuid_str()}"
def create_factor_readiness_gate_id() -> str: return f"fc_gate_{_uuid_str()}"
def create_factor_composition_context_id() -> str: return f"fc_ctx_{_uuid_str()}"
def create_factor_composition_full_review_id() -> str: return f"fc_rev_{_uuid_str()}"

@dataclass
class FeatureEnrichmentIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
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
    valid_for_phase120: bool
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureGroupDefinition:
    group_id: str
    created_at_utc: str
    group_name: str
    group_kind: FeatureGroupKind
    feature_columns: list[str] = field(default_factory=list)
    required: bool = False
    description: str = ""
    safe_for_research_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureGroupProfile:
    profile_id: str
    created_at_utc: str
    group_id: str | None
    group_name: str
    group_kind: FeatureGroupKind
    available_features: list[str] = field(default_factory=list)
    missing_features: list[str] = field(default_factory=list)
    coverage_ratio: float = 0.0
    average_missingness: float = 0.0
    average_stability_score: float = 0.0
    average_redundancy_score: float = 0.0
    average_confidence_score: float = 0.0
    group_quality: FactorCompositionQuality = FactorCompositionQuality.UNKNOWN
    selected_feature_count: int = 0
    warning_count: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FactorComponent:
    component_id: str
    created_at_utc: str
    component_name: str
    source_group_name: str | None
    source_feature_columns: list[str] = field(default_factory=list)
    transform: str = ""
    weight_hint: float | None = None
    direction_hint: str = ""
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FactorCandidateDefinition:
    factor_id: str
    created_at_utc: str
    factor_name: str
    factor_kind: FactorCandidateKind
    components: list[FactorComponent] = field(default_factory=list)
    input_feature_columns: list[str] = field(default_factory=list)
    output_column: str = ""
    description: str = ""
    composition_method: str = ""
    normalization_required: bool = False
    diagnostics_required: bool = False
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    implementation_phase: int | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FactorCompositionSpec:
    spec_id: str
    created_at_utc: str
    factor_candidates: list[FactorCandidateDefinition] = field(default_factory=list)
    feature_groups: list[FeatureGroupDefinition] = field(default_factory=list)
    composition_version: str = "1.0"
    local_pandas_only: bool = True
    research_data_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureCoverageProfile:
    coverage_id: str
    created_at_utc: str
    symbol: str
    feature_columns: list[str] = field(default_factory=list)
    row_count: int = 0
    feature_count: int = 0
    available_feature_count: int = 0
    missing_feature_count: int = 0
    average_coverage_ratio: float = 0.0
    low_coverage_features: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureRedundancyProfile:
    redundancy_id: str
    created_at_utc: str
    symbol: str
    feature_columns: list[str] = field(default_factory=list)
    high_redundancy_pairs: list[dict[str, Any]] = field(default_factory=list)
    average_abs_correlation: float | None = None
    max_abs_correlation: float | None = None
    redundancy_score: float = 0.0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureStabilityProfile:
    stability_id: str
    created_at_utc: str
    symbol: str
    feature_columns: list[str] = field(default_factory=list)
    stability_scores: dict[str, float] = field(default_factory=dict)
    low_stability_features: list[str] = field(default_factory=list)
    average_stability_score: float = 0.0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FeatureSelectionMetadata:
    selection_id: str
    created_at_utc: str
    symbol: str
    feature_column: str
    group_name: str | None
    selection_status: FeatureSelectionStatus
    selection_reasons: list[FeatureSelectionReason] = field(default_factory=list)
    coverage_ratio: float = 0.0
    missingness_ratio: float = 0.0
    stability_score: float = 0.0
    redundancy_score: float = 0.0
    confidence_score: float | None = None
    freshness_score: float | None = None
    lineage_score: float | None = None
    selected_for_factor_candidates: list[str] = field(default_factory=list)
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FactorReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: FactorReadinessRuleKind
    name: str
    status: FactorReadinessStatus
    required: bool
    expected_value: Any | None = None
    observed_value: Any | None = None
    passed: bool = False
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FactorReadinessGate:
    gate_id: str
    created_at_utc: str
    status: FactorReadinessStatus
    rules: list[FactorReadinessRule] = field(default_factory=list)
    factor_candidates: list[FactorCandidateDefinition] = field(default_factory=list)
    feature_groups: list[FeatureGroupDefinition] = field(default_factory=list)
    selection_metadata_count: int = 0
    ready_for_phase121: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FactorCompositionContext:
    context_id: str
    created_at_utc: str
    status: FactorCompositionStatus
    decision: FactorCompositionDecision
    source_feature_enrichment_review_id: str | None
    ingestion: FeatureEnrichmentIngestionResult
    feature_groups: list[FeatureGroupDefinition] = field(default_factory=list)
    group_profiles: list[FeatureGroupProfile] = field(default_factory=list)
    factor_components: list[FactorComponent] = field(default_factory=list)
    factor_candidates: list[FactorCandidateDefinition] = field(default_factory=list)
    composition_spec: FactorCompositionSpec = None
    coverage_profiles: list[FeatureCoverageProfile] = field(default_factory=list)
    redundancy_profiles: list[FeatureRedundancyProfile] = field(default_factory=list)
    stability_profiles: list[FeatureStabilityProfile] = field(default_factory=list)
    selection_metadata: list[FeatureSelectionMetadata] = field(default_factory=list)
    readiness_gate: FactorReadinessGate = None
    feature_groups_ready: bool = False
    factor_candidates_ready: bool = False
    selection_metadata_ready: bool = False
    factor_readiness_gate_ready: bool = False
    ready_for_phase121: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    paid_api_enabled: bool = False
    dashboard_enabled: bool = False
    network_default_enabled: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[FactorCompositionRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FactorCompositionFullReview:
    review_id: str
    created_at_utc: str
    report_type: FactorCompositionReportType
    ingestion: FeatureEnrichmentIngestionResult
    context: FactorCompositionContext
    feature_groups: list[FeatureGroupDefinition] = field(default_factory=list)
    group_profiles: list[FeatureGroupProfile] = field(default_factory=list)
    factor_candidates: list[FactorCandidateDefinition] = field(default_factory=list)
    composition_spec: FactorCompositionSpec = None
    selection_metadata: list[FeatureSelectionMetadata] = field(default_factory=list)
    readiness_gate: FactorReadinessGate = None
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

# To Dict functions
def feature_enrichment_ingestion_result_to_dict(item: FeatureEnrichmentIngestionResult) -> dict: return asdict(item)
def feature_group_definition_to_dict(item: FeatureGroupDefinition) -> dict: return asdict(item)
def feature_group_profile_to_dict(item: FeatureGroupProfile) -> dict: return asdict(item)
def factor_component_to_dict(item: FactorComponent) -> dict: return asdict(item)
def factor_candidate_definition_to_dict(item: FactorCandidateDefinition) -> dict: return asdict(item)
def factor_composition_spec_to_dict(item: FactorCompositionSpec) -> dict: return asdict(item)
def feature_coverage_profile_to_dict(item: FeatureCoverageProfile) -> dict: return asdict(item)
def feature_redundancy_profile_to_dict(item: FeatureRedundancyProfile) -> dict: return asdict(item)
def feature_stability_profile_to_dict(item: FeatureStabilityProfile) -> dict: return asdict(item)
def feature_selection_metadata_to_dict(item: FeatureSelectionMetadata) -> dict: return asdict(item)
def factor_readiness_rule_to_dict(item: FactorReadinessRule) -> dict: return asdict(item)
def factor_readiness_gate_to_dict(item: FactorReadinessGate) -> dict: return asdict(item)
def factor_composition_context_to_dict(item: FactorCompositionContext) -> dict: return asdict(item)
def factor_composition_full_review_to_dict(item: FactorCompositionFullReview) -> dict: return asdict(item)

# Validation Functions
def validate_feature_enrichment_ingestion_result(item: FeatureEnrichmentIngestionResult) -> None:
    if not item.event_enrichment_ready: item.errors.append("event_enrichment_ready must be true")
    if not item.quality_enrichment_ready: item.errors.append("quality_enrichment_ready must be true")
    if not item.calendar_enrichment_ready: item.errors.append("calendar_enrichment_ready must be true")
    if not item.interactions_ready: item.errors.append("interactions_ready must be true")
    if not item.enriched_feature_table_ready: item.errors.append("enriched_feature_table_ready must be true")
    if not item.ready_for_phase120: item.errors.append("ready_for_phase120 must be true")
    if not item.research_data_only: item.errors.append("research_data_only must be true")
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

def validate_feature_group_definition(item: FeatureGroupDefinition) -> None:
    pass

def validate_feature_group_profile(item: FeatureGroupProfile) -> None:
    pass

def validate_factor_component(item: FactorComponent) -> None:
    if item.produces_trade_signal: item.errors.append("produces_trade_signal must be false")

def validate_factor_candidate_definition(item: FactorCandidateDefinition) -> None:
    if item.produces_trade_signal: item.errors.append("produces_trade_signal must be false")

def validate_factor_composition_spec(item: FactorCompositionSpec) -> None:
    pass

def validate_feature_coverage_profile(item: FeatureCoverageProfile) -> None:
    if not (0 <= item.average_coverage_ratio <= 1): item.errors.append("coverage ratio must be 0-1")

def validate_feature_redundancy_profile(item: FeatureRedundancyProfile) -> None:
    pass

def validate_feature_stability_profile(item: FeatureStabilityProfile) -> None:
    pass

def validate_feature_selection_metadata(item: FeatureSelectionMetadata) -> None:
    if item.produces_portfolio_weights: item.errors.append("produces_portfolio_weights must be false")

def validate_factor_readiness_gate(item: FactorReadinessGate) -> None:
    if item.activation_allowed: item.errors.append("activation_allowed must be false")
    if item.strategy_activation_allowed: item.errors.append("strategy_activation_allowed must be false")

def validate_factor_composition_context(item: FactorCompositionContext) -> None:
    pass

def validate_factor_composition_full_review(item: FactorCompositionFullReview) -> None:
    pass
