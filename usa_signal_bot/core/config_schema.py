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

@dataclass
class PaperObserverGovernanceConfig:
    enabled: bool = True
    write_observer_governance_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_governance_is_non_executing: bool = True
    warn_governance_is_not_activation: bool = True

@dataclass
class ObserverPaperComparisonConfig:
    enabled: bool = True
    require_paper_baseline: bool = True
    require_observer_output: bool = True
    max_acceptable_drift_event_count: int = 10
    block_on_unsafe_drift: bool = True
    block_on_missing_locked_runtime: bool = True

@dataclass
class PromotionEvidenceRefreshConfig:
    enabled: bool = True
    max_evidence_age_days: int = 14
    require_observer_review: bool = True
    require_observer_comparison: bool = True
    require_controlled_planning_ticket: bool = True
    require_observation_exit_review: bool = True
    request_followup_on_missing_evidence: bool = True
    request_followup_on_stale_evidence: bool = True

@dataclass
class ObserverGovernanceConfig:
    enabled: bool = True
    conservative_decision_board: bool = True
    eligible_decision_is_dossier_only: bool = True
    require_manual_review: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class ObserverGovernanceSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_observer_unlock_risk: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperObserverGovernanceNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_observer_governance_report: bool = True
    notify_observer_evidence_warning: bool = True
    notify_observer_comparison_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

@dataclass
class PaperPromotionDossierConfig:
    enabled: bool = True
    write_dossier_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_dossier_is_not_activation: bool = True
    warn_safety_board_is_not_deployment_approval: bool = True
    warn_readiness_package_is_metadata_only: bool = True

@dataclass
class PromotionDossierConfig:
    enabled: bool = True
    require_observer_governance_eligible: bool = True
    require_evidence_index: bool = True
    require_manual_review: bool = True
    require_final_safety_board: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class FinalSafetyBoardConfig:
    enabled: bool = True
    conservative_decision_engine: bool = True
    require_all_safety_gates: bool = True
    require_evidence_complete: bool = True
    require_non_execution_compliance: bool = True
    pass_is_non_executing_readiness_only: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class StagedPaperReadinessPackageConfig:
    enabled: bool = True
    package_is_metadata_only: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    include_stage_0_dossier_only: bool = True
    include_stage_1_non_executing_readiness_rehearsal: bool = True
    include_stage_2_guarded_handoff_review: bool = True
    include_stage_3_final_locked_review: bool = True

@dataclass
class PromotionDossierSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_dossier_auto_enable_risk: bool = True
    block_on_readiness_package_activation_risk: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperPromotionDossierNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_promotion_dossier_report: bool = True
    notify_final_safety_board_warning: bool = True
    notify_readiness_package_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True


@dataclass
class PaperReadinessRehearsalConfig:
    enabled: bool = True
    write_rehearsal_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_rehearsal_is_not_activation: bool = True
    warn_final_lock_is_not_deployment_approval: bool = True
    warn_handoff_registry_is_not_activation: bool = True

@dataclass
class ReadinessStageRehearsalConfig:
    enabled: bool = True
    deterministic_rehearsal: bool = True
    require_readiness_package: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False

@dataclass
class FinalReviewLockConfig:
    enabled: bool = True
    require_rehearsal_completed: bool = True
    lock_is_metadata_only: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class GuardedHandoffRegistryConfig:
    enabled: bool = True
    require_final_review_lock: bool = True
    require_handoff_evidence_index: bool = True
    register_is_next_review_only: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class ReadinessRehearsalSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_package_activation_risk: bool = True
    block_on_final_lock_auto_enable_risk: bool = True
    block_on_handoff_auto_enable_risk: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperReadinessRehearsalNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_readiness_rehearsal_report: bool = True
    notify_final_review_lock_warning: bool = True
    notify_guarded_handoff_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
