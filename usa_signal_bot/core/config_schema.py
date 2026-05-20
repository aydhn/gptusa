from dataclasses import dataclass, field
from typing import List

@dataclass
class PaperDryRunBridgeConfig:
    enabled: bool = True
    default_mode: str = "full_supervised_dry_run"
    write_dry_run_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_dry_run_proposals_are_not_orders: bool = True
    warn_human_checkpoint_is_not_deployment_approval: bool = True

@dataclass
class DryRunBridgeContextConfig:
    enabled: bool = True
    require_quarantine_candidate: bool = True
    require_promotion_ticket: bool = True
    require_bridge_plan: bool = True
    require_read_only_paper_snapshot: bool = True
    allow_paper_state_mutation: bool = False
    allow_paper_orders: bool = False
    allow_broker_orders: bool = False
    allow_telegram_real_send: bool = False
    allow_production_config_write: bool = False
    allow_active_paper_enable: bool = False

@dataclass
class DryRunProposalsConfig:
    enabled: bool = True
    deterministic_proposals: bool = True
    default_symbols: List[str] = field(default_factory=lambda: ["SPY", "QQQ", "AAPL"])
    default_notional_usd: float = 1000.0
    real_order_forbidden: bool = True
    paper_mutation_forbidden: bool = True
    broker_send_forbidden: bool = True

@dataclass
class BridgeTelemetryConfig:
    enabled: bool = True
    local_only: bool = True
    record_session_events: bool = True
    record_blocked_operations: bool = True
    record_checkpoint_events: bool = True
    external_telemetry_enabled: bool = False

@dataclass
class HumanReviewCheckpointConfig:
    enabled: bool = True
    required: bool = True
    reviewer_notes_required_for_reviewed_status: bool = True
    allows_active_paper: bool = False
    allows_broker_execution: bool = False
    allows_config_patch: bool = False
    max_checkpoint_age_days: int = 7

@dataclass
class DryRunBridgeSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperDryRunBridgeNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_dry_run_report: bool = True
    notify_dry_run_safety_warning: bool = True
    notify_human_checkpoint_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
