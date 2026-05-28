import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from usa_signal_bot.core.enums import (
    RegimeFoundationStatus,
    RegimeFoundationDecision,
    MarketStateDatasetStatus,
    MarketStateColumnKind,
    RegimeLabelKind,
    RegimeTaxonomyStatus,
    RegimeBoundaryRuleKind,
    RegimeBoundaryStatus,
    RegimeFoundationQuality,
    RegimeFoundationRiskFlag,
    RegimeFoundationReportType
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def _uuid() -> str:
    return str(uuid.uuid4())

def create_final_closure_ingestion_id() -> str:
    return f"ingest_final_closure_{_uuid()[:8]}"

def create_frozen_artifact_reference_id() -> str:
    return f"frozen_ref_{_uuid()[:8]}"

def create_regime_research_input_bundle_id() -> str:
    return f"regime_input_{_uuid()[:8]}"

def create_market_state_column_contract_id() -> str:
    return f"col_contract_{_uuid()[:8]}"

def create_market_state_dataset_contract_id() -> str:
    return f"dataset_contract_{_uuid()[:8]}"

def create_market_state_dataset_skeleton_id() -> str:
    return f"skeleton_{_uuid()[:8]}"

def create_regime_label_definition_id() -> str:
    return f"label_def_{_uuid()[:8]}"

def create_regime_label_taxonomy_id() -> str:
    return f"taxonomy_{_uuid()[:8]}"

def create_regime_boundary_rule_id() -> str:
    return f"rule_{_uuid()[:8]}"

def create_regime_non_activation_boundary_id() -> str:
    return f"boundary_{_uuid()[:8]}"

def create_regime_foundation_context_id() -> str:
    return f"ctx_{_uuid()[:8]}"

def create_regime_foundation_full_review_id() -> str:
    return f"review_{_uuid()[:8]}"

@dataclass
class FinalClosureIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    final_artifacts_ready: bool
    final_checks_passed: bool
    freeze_seal_ready: bool
    engine_certificate_ready: bool
    phase126_kickoff_gate_ready: bool
    feature_factor_engine_final_closed: bool
    ready_for_phase126: bool
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
    valid_for_phase126: bool
    risk_flags: List[RegimeFoundationRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class FrozenArtifactReference:
    reference_id: str
    created_at_utc: str
    artifact_name: str
    artifact_kind: str
    source_phase: Optional[int]
    path: Optional[str]
    artifact_hash: Optional[str]
    schema_signature: Optional[str]
    lineage_reference: Optional[str]
    safety_reference: Optional[str]
    required_for_regime_foundation: bool
    available: bool
    immutable: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeResearchInputBundle:
    bundle_id: str
    created_at_utc: str
    source_final_closure_review_id: Optional[str]
    frozen_artifacts: List[FrozenArtifactReference]
    factor_table_refs: List[str]
    factor_diagnostics_refs: List[str]
    schema_contract_refs: List[str]
    lineage_contract_refs: List[str]
    safety_contract_refs: List[str]
    research_report_refs: List[str]
    bundle_valid: bool
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class MarketStateColumnContract:
    column_id: str
    created_at_utc: str
    column_name: str
    column_kind: MarketStateColumnKind
    dtype: str
    required: bool
    nullable: bool
    description: str
    source_artifact_kind: Optional[str]
    research_metadata_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class MarketStateDatasetContract:
    contract_id: str
    created_at_utc: str
    status: MarketStateDatasetStatus
    dataset_name: str
    version: str
    columns: List[MarketStateColumnContract]
    required_columns: List[str]
    optional_columns: List[str]
    primary_key_columns: List[str]
    timestamp_column: str
    symbol_column: str
    label_placeholder_columns: List[str]
    schema_hash: Optional[str]
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class MarketStateDatasetSkeleton:
    skeleton_id: str
    created_at_utc: str
    contract_id: Optional[str]
    status: MarketStateDatasetStatus
    columns: List[str]
    example_rows: List[Dict[str, Any]]
    row_count: int
    schema_valid: bool
    research_data_only: bool
    contains_trade_signal: bool
    contains_order_decision: bool
    contains_portfolio_weight: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeLabelDefinition:
    label_id: str
    created_at_utc: str
    label_name: str
    label_kind: RegimeLabelKind
    description: str
    intended_use: str
    allowed_inputs: List[str]
    disallowed_outputs: List[str]
    mutually_exclusive_group: Optional[str]
    hierarchy_level: int
    research_metadata_only: bool
    activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeLabelTaxonomy:
    taxonomy_id: str
    created_at_utc: str
    status: RegimeTaxonomyStatus
    taxonomy_name: str
    version: str
    labels: List[RegimeLabelDefinition]
    default_label: str
    unknown_label: str
    label_count: int
    taxonomy_hash: Optional[str]
    research_data_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: RegimeBoundaryRuleKind
    name: str
    status: RegimeBoundaryStatus
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeNonActivationBoundaryResult:
    boundary_id: str
    created_at_utc: str
    status: RegimeBoundaryStatus
    rules: List[RegimeBoundaryRule]
    total_rules: int
    passed_rules: int
    failed_rules: int
    blocked_rules: int
    boundary_passed: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeFoundationContext:
    context_id: str
    created_at_utc: str
    status: RegimeFoundationStatus
    decision: RegimeFoundationDecision
    source_final_closure_review_id: Optional[str]
    ingestion: FinalClosureIngestionResult
    input_bundle: RegimeResearchInputBundle
    dataset_contract: MarketStateDatasetContract
    dataset_skeleton: MarketStateDatasetSkeleton
    taxonomy: RegimeLabelTaxonomy
    boundary: RegimeNonActivationBoundaryResult
    final_closure_ingested: bool
    frozen_artifacts_ready: bool
    input_contract_ready: bool
    market_state_dataset_contract_ready: bool
    regime_taxonomy_ready: bool
    non_activation_boundary_ready: bool
    ready_for_phase127: bool
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
    warnings: List[str]
    errors: List[str]
    risk_flags: List[RegimeFoundationRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class RegimeFoundationFullReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeFoundationReportType
    ingestion: FinalClosureIngestionResult
    context: RegimeFoundationContext
    input_bundle: RegimeResearchInputBundle
    dataset_contract: MarketStateDatasetContract
    dataset_skeleton: MarketStateDatasetSkeleton
    taxonomy: RegimeLabelTaxonomy
    boundary: RegimeNonActivationBoundaryResult
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# Conversion to dict functions
def final_closure_ingestion_result_to_dict(item: FinalClosureIngestionResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def frozen_artifact_reference_to_dict(item: FrozenArtifactReference) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_research_input_bundle_to_dict(item: RegimeResearchInputBundle) -> dict:
    from dataclasses import asdict
    return asdict(item)

def market_state_column_contract_to_dict(item: MarketStateColumnContract) -> dict:
    from dataclasses import asdict
    return asdict(item)

def market_state_dataset_contract_to_dict(item: MarketStateDatasetContract) -> dict:
    from dataclasses import asdict
    return asdict(item)

def market_state_dataset_skeleton_to_dict(item: MarketStateDatasetSkeleton) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_label_definition_to_dict(item: RegimeLabelDefinition) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_label_taxonomy_to_dict(item: RegimeLabelTaxonomy) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_boundary_rule_to_dict(item: RegimeBoundaryRule) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_non_activation_boundary_result_to_dict(item: RegimeNonActivationBoundaryResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_foundation_context_to_dict(item: RegimeFoundationContext) -> dict:
    from dataclasses import asdict
    return asdict(item)

def regime_foundation_full_review_to_dict(item: RegimeFoundationFullReview) -> dict:
    from dataclasses import asdict
    return asdict(item)

# Validation functions
def validate_final_closure_ingestion_result(item: FinalClosureIngestionResult) -> None:
    assert item.final_artifacts_ready, "final_artifacts_ready must be True"
    assert item.final_checks_passed, "final_checks_passed must be True"
    assert item.freeze_seal_ready, "freeze_seal_ready must be True"
    assert item.engine_certificate_ready, "engine_certificate_ready must be True"
    assert item.phase126_kickoff_gate_ready, "phase126_kickoff_gate_ready must be True"
    assert item.feature_factor_engine_final_closed, "feature_factor_engine_final_closed must be True"
    assert item.ready_for_phase126, "ready_for_phase126 must be True"
    assert item.research_data_only, "research_data_only must be True"
    assert not item.activation_allowed, "activation_allowed must be False"
    assert not item.strategy_activation_allowed, "strategy_activation_allowed must be False"
    assert not item.deployment_allowed, "deployment_allowed must be False"
    assert not item.active_paper_enabled, "active_paper_enabled must be False"
    assert not item.broker_execution_enabled, "broker_execution_enabled must be False"
    assert not item.order_creation_enabled, "order_creation_enabled must be False"
    assert not item.paper_state_mutation_enabled, "paper_state_mutation_enabled must be False"
    assert not item.telegram_real_send_enabled, "telegram_real_send_enabled must be False"
    assert not item.scraping_enabled, "scraping_enabled must be False"
    assert not item.html_parse_enabled, "html_parse_enabled must be False"
    assert not item.paid_api_enabled, "paid_api_enabled must be False"
    assert not item.dashboard_enabled, "dashboard_enabled must be False"
    assert not item.network_default_enabled, "network_default_enabled must be False"
    assert not item.produces_trade_signal, "produces_trade_signal must be False"
    assert not item.produces_order_decision, "produces_order_decision must be False"
    assert not item.produces_portfolio_weights, "produces_portfolio_weights must be False"
    assert not item.investment_advice, "investment_advice must be False"
    assert not item.network_used, "network_used must be False"
    assert not item.paid_api_used, "paid_api_used must be False"
    assert not item.scraping_used, "scraping_used must be False"
    assert not item.html_parsing_used, "html_parsing_used must be False"
    assert not item.broker_used, "broker_used must be False"
    assert not item.order_created, "order_created must be False"
    assert not item.paper_state_mutated, "paper_state_mutated must be False"
    assert not item.telegram_real_sent, "telegram_real_sent must be False"
    assert not item.dashboard_started, "dashboard_started must be False"

def validate_regime_research_input_bundle(item: RegimeResearchInputBundle) -> None:
    pass

def validate_market_state_dataset_contract(item: MarketStateDatasetContract) -> None:
    pass

def validate_market_state_dataset_skeleton(item: MarketStateDatasetSkeleton) -> None:
    pass

def validate_regime_label_taxonomy(item: RegimeLabelTaxonomy) -> None:
    assert not item.activation_allowed, "Taxonomy activation_allowed must be False"

def validate_regime_non_activation_boundary_result(item: RegimeNonActivationBoundaryResult) -> None:
    pass

def validate_regime_foundation_context(item: RegimeFoundationContext) -> None:
    if item.ready_for_phase127:
        assert item.boundary.boundary_passed, "Boundary boundary_passed=True required for ready_for_phase127"

def validate_regime_foundation_full_review(item: RegimeFoundationFullReview) -> None:
    pass
