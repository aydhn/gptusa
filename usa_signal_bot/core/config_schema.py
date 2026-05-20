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
