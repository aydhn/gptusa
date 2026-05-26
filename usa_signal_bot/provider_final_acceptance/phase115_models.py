from dataclasses import dataclass, field
from typing import Any, Optional
from usa_signal_bot.core.enums import (
    ProviderFinalAcceptanceStatus,
    ProviderFinalAcceptanceDecision,
    ProviderLayerClosureStatus,
    ProviderLayerClosureDecision,
    ProviderFinalAcceptanceCriterionKind,
    ProviderFinalAcceptanceCriterionStatus,
    FeatureFactorKickoffGateStatus,
    FeatureFactorKickoffGateDecision,
    FeatureFactorAllowedScope,
    FeatureFactorBlockedScope,
    FeatureFactorKickoffRuleStatus,
    FeatureFactorKickoffAssertionStatus,
    ProviderFinalAcceptanceRiskFlag,
    ProviderFinalAcceptanceReportType
)

@dataclass
class ProviderFreezeIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    provider_expansion_frozen: bool
    multi_provider_review_passed: bool
    data_layer_rehearsal_passed: bool
    output_contracts_passed: bool
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
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    ready_for_phase115: bool
    valid_for_phase115: bool
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class ProviderFinalAcceptanceCriterion:
    criterion_id: str
    created_at_utc: str
    criterion_kind: ProviderFinalAcceptanceCriterionKind
    name: str
    status: ProviderFinalAcceptanceCriterionStatus
    required: bool
    passed: bool
    rationale: str
    evidence_refs: list[str]
    warnings: list[str]
    errors: list[str]
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    metadata: dict[str, Any]

@dataclass
class DataProviderFinalAcceptanceReport:
    report_id: str
    created_at_utc: str
    status: ProviderFinalAcceptanceStatus
    decision: ProviderFinalAcceptanceDecision
    criteria: list[ProviderFinalAcceptanceCriterion]
    total_criteria: int
    passed_criteria: int
    warning_criteria: int
    failed_criteria: int
    blocked_criteria: int
    data_provider_layer_accepted: bool
    metadata_only_acceptance: bool
    research_data_only_acceptance: bool
    no_execution_confirmed: bool
    no_scraping_confirmed: bool
    no_paid_api_confirmed: bool
    no_broker_order_confirmed: bool
    no_secret_leak_confirmed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ProviderLayerClosureItem:
    closure_item_id: str
    created_at_utc: str
    source_phase: int
    closure_name: str
    source_ref_id: Optional[str]
    source_path: Optional[str]
    status: ProviderLayerClosureStatus
    closed: bool
    frozen: bool
    immutable: bool
    metadata_only: bool
    research_data_only: bool
    artifact_hash: Optional[str]
    warnings: list[str]
    errors: list[str]
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ProviderLayerClosureBundle:
    closure_id: str
    created_at_utc: str
    status: ProviderLayerClosureStatus
    decision: ProviderLayerClosureDecision
    phase_start: int
    phase_end: int
    next_phase: int
    final_phase: int
    items: list[ProviderLayerClosureItem]
    closure_hash: Optional[str]
    closed: bool
    frozen: bool
    immutable: bool
    metadata_only: bool
    research_data_only: bool
    total_items: int
    closed_items: int
    warning_items: int
    failed_items: int
    blocked_items: int
    closure_valid: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureFactorDataContract:
    contract_id: str
    created_at_utc: str
    status: FeatureFactorKickoffGateStatus
    allowed_input_kinds: list[str]
    blocked_output_kinds: list[str]
    ohlcv_input_allowed: bool
    event_context_input_allowed: bool
    quality_metadata_input_allowed: bool
    lineage_metadata_required: bool
    metadata_only_required: bool
    research_data_only_required: bool
    trade_signal_blocked: bool
    order_decision_blocked: bool
    broker_blocked: bool
    paper_mutation_blocked: bool
    telegram_real_send_blocked: bool
    scraping_blocked: bool
    html_parsing_blocked: bool
    paid_api_blocked: bool
    dashboard_blocked: bool
    network_default_enabled_blocked: bool
    contract_valid: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    metadata: dict[str, Any]

@dataclass
class FeatureFactorKickoffRule:
    rule_id: str
    created_at_utc: str
    rule_name: str
    status: FeatureFactorKickoffRuleStatus
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    required: bool
    description: str
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class FeatureFactorKickoffAssertion:
    assertion_id: str
    created_at_utc: str
    assertion_name: str
    status: FeatureFactorKickoffAssertionStatus
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    description: str
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class FeatureFactorEngineKickoffGate:
    gate_id: str
    created_at_utc: str
    status: FeatureFactorKickoffGateStatus
    decision: FeatureFactorKickoffGateDecision
    source_acceptance_report_id: Optional[str]
    source_closure_id: Optional[str]
    data_contract: FeatureFactorDataContract
    allowed_scopes: list[FeatureFactorAllowedScope]
    blocked_scopes: list[FeatureFactorBlockedScope]
    rules: list[FeatureFactorKickoffRule]
    assertions: list[FeatureFactorKickoffAssertion]
    gate_hash: Optional[str]
    sealed: bool
    immutable: bool
    frozen: bool
    metadata_only: bool
    research_data_only: bool
    ready_for_phase116: bool
    phase116_scope_allowed: bool
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
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ProviderFinalAcceptanceContext:
    context_id: str
    created_at_utc: str
    status: ProviderFinalAcceptanceStatus
    decision: ProviderFinalAcceptanceDecision
    source_provider_freeze_review_id: Optional[str]
    ingestion: ProviderFreezeIngestionResult
    final_acceptance_report: DataProviderFinalAcceptanceReport
    closure_bundle: ProviderLayerClosureBundle
    feature_factor_data_contract: FeatureFactorDataContract
    kickoff_gate: FeatureFactorEngineKickoffGate
    data_provider_layer_accepted: bool
    provider_layer_closed: bool
    feature_factor_kickoff_ready: bool
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
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    ready_for_phase116: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[ProviderFinalAcceptanceRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ProviderFinalAcceptanceFullReview:
    review_id: str
    created_at_utc: str
    report_type: ProviderFinalAcceptanceReportType
    ingestion: ProviderFreezeIngestionResult
    context: ProviderFinalAcceptanceContext
    final_acceptance_report: DataProviderFinalAcceptanceReport
    closure_bundle: ProviderLayerClosureBundle
    feature_factor_data_contract: FeatureFactorDataContract
    kickoff_gate: FeatureFactorEngineKickoffGate
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

import uuid
from datetime import datetime, timezone

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def create_provider_freeze_ingestion_id() -> str:
    return f"ingest_phase115_{uuid.uuid4().hex[:8]}"

def create_provider_final_acceptance_criterion_id() -> str:
    return f"crit_final_{uuid.uuid4().hex[:8]}"

def create_data_provider_final_acceptance_report_id() -> str:
    return f"report_final_acc_{uuid.uuid4().hex[:8]}"

def create_provider_layer_closure_item_id() -> str:
    return f"cls_item_{uuid.uuid4().hex[:8]}"

def create_provider_layer_closure_id() -> str:
    return f"cls_bundle_{uuid.uuid4().hex[:8]}"

def create_feature_factor_data_contract_id() -> str:
    return f"ff_contract_{uuid.uuid4().hex[:8]}"

def create_feature_factor_kickoff_rule_id() -> str:
    return f"ff_rule_{uuid.uuid4().hex[:8]}"

def create_feature_factor_kickoff_assertion_id() -> str:
    return f"ff_assert_{uuid.uuid4().hex[:8]}"

def create_feature_factor_kickoff_gate_id() -> str:
    return f"ff_gate_{uuid.uuid4().hex[:8]}"

def create_provider_final_acceptance_context_id() -> str:
    return f"ctx_final_acc_{uuid.uuid4().hex[:8]}"

def create_provider_final_acceptance_full_review_id() -> str:
    return f"rev_final_acc_{uuid.uuid4().hex[:8]}"

def provider_freeze_ingestion_result_to_dict(item: ProviderFreezeIngestionResult) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def provider_final_acceptance_criterion_to_dict(item: ProviderFinalAcceptanceCriterion) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def data_provider_final_acceptance_report_to_dict(item: DataProviderFinalAcceptanceReport) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def provider_layer_closure_item_to_dict(item: ProviderLayerClosureItem) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def provider_layer_closure_bundle_to_dict(item: ProviderLayerClosureBundle) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def feature_factor_data_contract_to_dict(item: FeatureFactorDataContract) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def feature_factor_kickoff_rule_to_dict(item: FeatureFactorKickoffRule) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def feature_factor_kickoff_assertion_to_dict(item: FeatureFactorKickoffAssertion) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def feature_factor_engine_kickoff_gate_to_dict(item: FeatureFactorEngineKickoffGate) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def provider_final_acceptance_context_to_dict(item: ProviderFinalAcceptanceContext) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def provider_final_acceptance_full_review_to_dict(item: ProviderFinalAcceptanceFullReview) -> dict:
    import dataclasses
    return dataclasses.asdict(item)

def validate_provider_freeze_ingestion_result(item: ProviderFreezeIngestionResult) -> None:
    if not item.provider_expansion_frozen:
        item.valid_for_phase115 = False
        item.errors.append("provider_expansion_frozen is false")
    if not item.multi_provider_review_passed:
        item.valid_for_phase115 = False
        item.errors.append("multi_provider_review_passed is false")
    if not item.data_layer_rehearsal_passed:
        item.valid_for_phase115 = False
        item.errors.append("data_layer_rehearsal_passed is false")
    if not item.output_contracts_passed:
        item.valid_for_phase115 = False
        item.errors.append("output_contracts_passed is false")
    if not item.ready_for_phase115:
        item.valid_for_phase115 = False
        item.errors.append("ready_for_phase115 is false")
    if not item.metadata_only:
        item.valid_for_phase115 = False
        item.errors.append("metadata_only is false")
    if not item.research_data_only:
        item.valid_for_phase115 = False
        item.errors.append("research_data_only is false")

    if item.activation_allowed:
        item.valid_for_phase115 = False
        item.errors.append("activation_allowed is true")
    if item.active_paper_enabled:
        item.valid_for_phase115 = False
        item.errors.append("active_paper_enabled is true")
    if item.broker_execution_enabled:
        item.valid_for_phase115 = False
        item.errors.append("broker_execution_enabled is true")
    if item.order_creation_enabled:
        item.valid_for_phase115 = False
        item.errors.append("order_creation_enabled is true")
    if item.paper_state_mutation_enabled:
        item.valid_for_phase115 = False
        item.errors.append("paper_state_mutation_enabled is true")
    if item.telegram_real_send_enabled:
        item.valid_for_phase115 = False
        item.errors.append("telegram_real_send_enabled is true")
    if item.scraping_enabled:
        item.valid_for_phase115 = False
        item.errors.append("scraping_enabled is true")
    if item.html_parse_enabled:
        item.valid_for_phase115 = False
        item.errors.append("html_parse_enabled is true")
    if item.paid_api_enabled:
        item.valid_for_phase115 = False
        item.errors.append("paid_api_enabled is true")
    if item.dashboard_enabled:
        item.valid_for_phase115 = False
        item.errors.append("dashboard_enabled is true")
    if item.network_default_enabled:
        item.valid_for_phase115 = False
        item.errors.append("network_default_enabled is true")
    if item.produces_trade_signal:
        item.valid_for_phase115 = False
        item.errors.append("produces_trade_signal is true")
    if item.produces_order_decision:
        item.valid_for_phase115 = False
        item.errors.append("produces_order_decision is true")

def validate_data_provider_final_acceptance_report(item: DataProviderFinalAcceptanceReport) -> None:
    pass

def validate_provider_layer_closure_bundle(item: ProviderLayerClosureBundle) -> None:
    pass

def validate_feature_factor_data_contract(item: FeatureFactorDataContract) -> None:
    pass

def validate_feature_factor_engine_kickoff_gate(item: FeatureFactorEngineKickoffGate) -> None:
    pass

def validate_provider_final_acceptance_context(item: ProviderFinalAcceptanceContext) -> None:
    pass

def validate_provider_final_acceptance_full_review(item: ProviderFinalAcceptanceFullReview) -> None:
    pass
