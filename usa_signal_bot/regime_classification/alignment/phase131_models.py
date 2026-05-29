from dataclasses import dataclass, field
from typing import Any, Optional
import uuid
import datetime
from usa_signal_bot.core.enums import (
    RegimeAlignmentRiskFlag, RegimeAlignmentKind, MarketBehaviorOverlayKind,
    RegimeCompatibilityKind, RegimeCompatibilityMetricKind, RegimeAlignmentQuality,
    RegimeAlignmentReadinessRuleKind, RegimeAlignmentReadinessStatus,
    RegimeAlignmentStatus, RegimeAlignmentDecision, RegimeAlignmentReportType
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class MarketBehaviorIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    transition_analytics_ingested: bool
    diagnostics_loaded: bool
    profile_specs_ready: bool
    behavior_profiles_ready: bool
    regime_summaries_ready: bool
    diagnostics_interpreted: bool
    report_built: bool
    report_qa_passed: bool
    readiness_gate_ready: bool
    ready_for_phase131: bool
    metadata_only: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
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
    model_training_used: bool
    model_prediction_used: bool
    heavy_ml_dependency_used: bool
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
    valid_for_phase131: bool
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FrozenFactorAlignmentReference:
    reference_id: str
    created_at_utc: str
    symbol: Optional[str]
    artifact_name: str
    artifact_path: Optional[str]
    artifact_hash: Optional[str]
    factor_columns: list[str] = field(default_factory=list)
    feature_columns: list[str] = field(default_factory=list)
    schema_signature: Optional[str] = None
    lineage_reference: Optional[str] = None
    safety_reference: Optional[str] = None
    available: bool = False
    immutable: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeAwareAlignmentSpec:
    spec_id: str
    created_at_utc: str
    spec_name: str
    alignment_kind: RegimeAlignmentKind
    source_columns: list[str] = field(default_factory=list)
    regime_context_fields: list[str] = field(default_factory=list)
    behavior_profile_fields: list[str] = field(default_factory=list)
    diagnostic_fields: list[str] = field(default_factory=list)
    compatibility_metric_kind: RegimeCompatibilityMetricKind = RegimeCompatibilityMetricKind.UNKNOWN
    deterministic: bool = True
    research_metadata_only: bool = True
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketBehaviorOverlaySpec:
    spec_id: str
    created_at_utc: str
    overlay_name: str
    overlay_kind: MarketBehaviorOverlayKind
    behavior_fields: list[str] = field(default_factory=list)
    target_factor_columns: list[str] = field(default_factory=list)
    target_feature_columns: list[str] = field(default_factory=list)
    deterministic: bool = True
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketBehaviorOverlayResult:
    overlay_id: str
    created_at_utc: str
    symbol: Optional[str]
    overlay_name: str
    overlay_kind: MarketBehaviorOverlayKind
    source_behavior_profile_id: Optional[str]
    target_column: Optional[str]
    overlay_score: float
    normalized_overlay_score: float
    overlay_notes: list[str] = field(default_factory=list)
    quality: RegimeAlignmentQuality = RegimeAlignmentQuality.UNKNOWN
    research_metadata_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeContextCompatibilityResult:
    compatibility_id: str
    created_at_utc: str
    symbol: Optional[str]
    source_column: str
    source_kind: str
    regime_label: Optional[str]
    behavior_profile_name: Optional[str]
    compatibility_kind: RegimeCompatibilityKind
    compatibility_metric_kind: RegimeCompatibilityMetricKind
    compatibility_score: float
    normalized_compatibility_score: float
    confidence_proxy: Optional[float]
    diagnostic_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)
    quality: RegimeAlignmentQuality = RegimeAlignmentQuality.UNKNOWN
    research_metadata_only: bool = True
    investment_advice: bool = False
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AlignmentDiagnosticsProfile:
    diagnostics_id: str
    created_at_utc: str
    symbol: Optional[str]
    profile_name: str
    compatibility_count: int
    high_compatibility_count: int
    low_compatibility_count: int
    uncertain_count: int
    data_quality_limited_count: int
    average_compatibility_score: Optional[float]
    average_confidence_proxy: Optional[float]
    diagnostic_summary: str
    quality: RegimeAlignmentQuality = RegimeAlignmentQuality.UNKNOWN
    research_metadata_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeAlignmentReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: RegimeAlignmentReadinessRuleKind
    name: str
    status: RegimeAlignmentReadinessStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeAlignmentReadinessGate:
    gate_id: str
    created_at_utc: str
    status: RegimeAlignmentReadinessStatus
    rules: list[RegimeAlignmentReadinessRule] = field(default_factory=list)
    ready_for_phase132: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeAlignmentContext:
    context_id: str
    created_at_utc: str
    status: RegimeAlignmentStatus
    decision: RegimeAlignmentDecision
    source_market_behavior_review_id: Optional[str]
    ingestion: Optional[MarketBehaviorIngestionResult] = None
    frozen_factor_refs: list[FrozenFactorAlignmentReference] = field(default_factory=list)
    alignment_specs: list[RegimeAwareAlignmentSpec] = field(default_factory=list)
    overlay_specs: list[MarketBehaviorOverlaySpec] = field(default_factory=list)
    overlay_results: list[MarketBehaviorOverlayResult] = field(default_factory=list)
    compatibility_results: list[RegimeContextCompatibilityResult] = field(default_factory=list)
    diagnostics_profiles: list[AlignmentDiagnosticsProfile] = field(default_factory=list)
    readiness_gate: Optional[RegimeAlignmentReadinessGate] = None
    market_behavior_ingested: bool = False
    frozen_factors_loaded: bool = False
    behavior_artifacts_loaded: bool = False
    alignment_specs_ready: bool = False
    overlays_built: bool = False
    compatibility_computed: bool = False
    diagnostics_built: bool = False
    readiness_gate_ready: bool = False
    ready_for_phase132: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
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
    model_training_used: bool = False
    model_prediction_used: bool = False
    heavy_ml_dependency_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
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
    risk_flags: list[RegimeAlignmentRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeAlignmentFullReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeAlignmentReportType
    ingestion: Optional[MarketBehaviorIngestionResult] = None
    context: Optional[RegimeAlignmentContext] = None
    frozen_factor_refs: list[FrozenFactorAlignmentReference] = field(default_factory=list)
    overlay_results: list[MarketBehaviorOverlayResult] = field(default_factory=list)
    compatibility_results: list[RegimeContextCompatibilityResult] = field(default_factory=list)
    diagnostics_profiles: list[AlignmentDiagnosticsProfile] = field(default_factory=list)
    readiness_gate: Optional[RegimeAlignmentReadinessGate] = None
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def create_market_behavior_ingestion_id() -> str:
    return f"ingest_{uuid.uuid4().hex}"
def create_frozen_factor_alignment_reference_id() -> str:
    return f"ref_{uuid.uuid4().hex}"
def create_regime_aware_alignment_spec_id() -> str:
    return f"alignspec_{uuid.uuid4().hex}"
def create_market_behavior_overlay_spec_id() -> str:
    return f"overspec_{uuid.uuid4().hex}"
def create_market_behavior_overlay_result_id() -> str:
    return f"overlay_{uuid.uuid4().hex}"
def create_regime_context_compatibility_result_id() -> str:
    return f"compat_{uuid.uuid4().hex}"
def create_alignment_diagnostics_profile_id() -> str:
    return f"diag_{uuid.uuid4().hex}"
def create_regime_alignment_readiness_rule_id() -> str:
    return f"rule_{uuid.uuid4().hex}"
def create_regime_alignment_readiness_gate_id() -> str:
    return f"gate_{uuid.uuid4().hex}"
def create_regime_alignment_context_id() -> str:
    return f"ctx_{uuid.uuid4().hex}"
def create_regime_alignment_full_review_id() -> str:
    return f"rev_{uuid.uuid4().hex}"
