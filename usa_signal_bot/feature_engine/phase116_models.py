from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from usa_signal_bot.core.enums import (
    FeatureFoundationStatus,
    FeatureFoundationDecision,
    FeatureFoundationRiskFlag,
    FeatureFoundationReportType,
)

class FeatureFactorKickoffIngestionResult:
    pass

@dataclass
class FeatureFoundationFullReview:
    review_id: str
    created_at_utc: str
    report_type: FeatureFoundationReportType
    feature_foundation_ready: bool
    indicator_registry_ready: bool
    feature_registry_ready: bool
    factor_registry_ready: bool
    input_contract_ready: bool
    output_schema_ready: bool
    ready_for_phase117: bool
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
    valid_for_phase117: bool
    risk_flags: List[FeatureFoundationRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

def feature_foundation_full_review_to_dict(item: FeatureFoundationFullReview) -> dict:
    return {}
