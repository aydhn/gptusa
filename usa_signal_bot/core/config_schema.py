from dataclasses import dataclass

@dataclass
class PaperShadowConfig:
    enabled: bool
    default_runtime_mode: str
    write_shadow_reports: bool
    warn_not_investment_advice: bool
    warn_no_broker_execution: bool
    warn_no_real_paper_mutation: bool
    warn_shadow_orders_are_not_orders: bool
    warn_shadow_fills_are_simulated: bool

@dataclass
class ShadowSimulationConfig:
    enabled: bool
    starting_equity_usd: float
    deterministic_simulation: bool
    use_mock_signals_by_default: bool
    allow_real_orders: bool
    allow_broker_calls: bool
    allow_paper_state_mutation: bool
    allow_telegram_real_send: bool
    allow_production_config_write: bool

@dataclass
class ShadowOrderIntentsConfig:
    enabled: bool
    default_notional_usd: float
    max_notional_pct_equity_warning: float
    block_real_order_like_fields: bool
    broker_destination_must_be_null: bool

@dataclass
class ShadowFillSimulationConfig:
    enabled: bool
    default_fill_price: float
    default_slippage_bps: float
    default_cost_bps: float
    deterministic_fills: bool
    real_fill_forbidden: bool

@dataclass
class ShadowLedgerConfig:
    enabled: bool
    write_ledger_events: bool
    require_session_started_event: bool
    require_session_completed_event: bool
    record_blocked_operations: bool

@dataclass
class ShadowSafetyConfig:
    enabled: bool
    block_on_real_order_risk: bool
    block_on_broker_field_risk: bool
    block_on_paper_state_mutation_risk: bool
    block_on_telegram_real_send_risk: bool
    block_on_production_config_write_risk: bool
    block_on_secret_risk: bool

@dataclass
class PaperShadowNotificationsConfig:
    enabled: bool
    dry_run: bool
    notify_shadow_report: bool
    notify_shadow_safety_warning: bool
    notify_shadow_rehearsal_warning: bool
    default_channel: str
    warn_no_real_send_default: bool

from dataclasses import dataclass, field
from typing import List

@dataclass
class PaperShadowGovernanceConfig:
    enabled: bool = True
    write_shadow_governance_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_shadow_acceptance_is_not_approval: bool = True
    warn_shadow_pnl_is_simulated: bool = True

@dataclass
class ShadowComparisonConfig:
    enabled: bool = True
    require_baseline_session: bool = True
    require_candidate_session: bool = True
    required_metrics: List[str] = field(default_factory=lambda: [
        "signal_count", "candidate_count", "intent_count",
        "risk_approved_intent_count", "blocked_intent_count",
        "simulated_fill_count", "simulated_total_cost_usd",
        "simulated_slippage_usd", "simulated_pnl_usd",
        "return_pct", "max_drawdown_pct", "safety_flag_count",
        "ledger_event_count", "notification_warning_count"
    ])

@dataclass
class ShadowAcceptanceConfig:
    enabled: bool = True
    min_acceptance_score: float = 70.0
    block_on_real_order_risk: bool = True
    block_on_paper_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    request_retest_on_incomplete_ledger: bool = True
    warn_on_cost_regression: bool = True
    warn_on_risk_regression: bool = True
    warn_on_safety_flags_increased: bool = True

@dataclass
class ShadowRehearsalGovernanceConfig:
    enabled: bool = True
    conservative_decision_board: bool = True
    allow_real_orders: bool = False
    allow_paper_state_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_production_config_write: bool = False
    accepted_status_means_sandboxed_candidate_only: bool = True
    require_manual_review: bool = True

@dataclass
class ShadowEvidencePackConfig:
    enabled: bool = True
    required_items: List[str] = field(default_factory=lambda: [
        "baseline_shadow_session", "candidate_shadow_session",
        "metric_comparisons", "acceptance_gates", "safety_delta",
        "risk_delta", "ledger_completeness", "notification_review",
        "shadow_pnl_snapshot"
    ])
    request_more_data_on_missing_evidence: bool = True

@dataclass
class PaperShadowGovernanceNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_shadow_governance_report: bool = True
    notify_shadow_acceptance_warning: bool = True
    notify_shadow_decision_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
