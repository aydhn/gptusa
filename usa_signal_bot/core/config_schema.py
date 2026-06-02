
from dataclasses import dataclass, field

@dataclass
class PaperNoWriteAdmissionConfig:
    enabled: bool = True
    write_no_write_admission_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_no_write_contract_is_not_activation: bool = True
    warn_activation_replay_is_metadata_only: bool = True
    warn_paper_mode_preflight_is_no_write: bool = True

@dataclass
class NoWritePaperAdmissionContractConfig:
    enabled: bool = True
    require_board_review: bool = True
    require_write_block_proof: bool = True
    require_activation_firewall_events: bool = True
    require_manual_review: bool = True
    activation_denied_required: bool = True
    activation_allowed: bool = False
    all_writes_blocked_required: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class ActivationFirewallReplayConfig:
    enabled: bool = True
    deterministic_replay: bool = True
    require_all_activation_attempts_denied: bool = True
    require_activation_firewall_rules: bool = True
    require_activation_firewall_events: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class PaperModeSimulationPreflightConfig:
    enabled: bool = True
    deterministic_preflight: bool = True
    preflight_is_no_write: bool = True
    require_no_write_contract: bool = True
    require_activation_replay_passed: bool = True
    require_runtime_write_lock_assertion: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class NoWriteAdmissionSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_write_block_proof_failed: bool = True
    block_on_no_write_contract_invalid: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperNoWriteAdmissionNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_no_write_admission_report: bool = True
    notify_activation_replay_warning: bool = True
    notify_paper_mode_preflight_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

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

@dataclass
class PaperFinalHandoffConfig:
    enabled: bool = True
    write_final_handoff_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_handoff_review_is_not_activation: bool = True
    warn_sealed_archive_is_not_deployment_package: bool = True
    warn_pre_paper_checkpoint_is_not_activation: bool = True

@dataclass
class FinalHandoffReviewConfig:
    enabled: bool = True
    require_guarded_handoff_entry: bool = True
    require_final_review_lock: bool = True
    require_rehearsal_run: bool = True
    require_manual_review: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class SealedReadinessArchiveConfig:
    enabled: bool = True
    require_archive_manifest: bool = True
    require_archive_hash: bool = True
    sealed_by_default: bool = True
    immutable_by_default: bool = True
    archive_is_metadata_only: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class PrePaperGovernanceCheckpointConfig:
    enabled: bool = True
    conservative_decision_engine: bool = True
    require_archive_integrity_pass: bool = True
    require_all_safety_gates: bool = True
    pass_is_guarded_pre_paper_dry_rehearsal_only: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False

@dataclass
class FinalHandoffSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_archive_auto_enable_risk: bool = True
    block_on_checkpoint_auto_enable_risk: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperFinalHandoffNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_final_handoff_report: bool = True
    notify_sealed_archive_warning: bool = True
    notify_pre_paper_checkpoint_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

@dataclass
class PaperPreRehearsalConfig:
    enabled: bool = True
    write_pre_rehearsal_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_pre_paper_rehearsal_is_not_activation: bool = True
    warn_firewall_is_metadata_only: bool = True
    warn_activation_denied_checkpoint_is_not_activation: bool = True

@dataclass
class PrePaperDryRehearsalConfig:
    enabled: bool = True
    deterministic_rehearsal: bool = True
    require_final_handoff_checkpoint: bool = True
    require_sealed_archive: bool = True
    require_mutation_firewall: bool = True
    require_activation_denied_checkpoint: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class PaperStateMutationFirewallConfig:
    enabled: bool = True
    deny_paper_state_write: bool = True
    deny_paper_order_create: bool = True
    deny_position_mutation: bool = True
    deny_portfolio_mutation: bool = True
    deny_cash_mutation: bool = True
    deny_equity_mutation: bool = True
    deny_broker_order_send: bool = True
    deny_telegram_real_send: bool = True
    deny_config_patch: bool = True
    deny_active_paper_enable: bool = True
    deny_archive_unlock: bool = True
    deny_final_lock_unlock: bool = True
    simulate_forbidden_attempts: bool = True

@dataclass
class ActivationDeniedCheckpointConfig:
    enabled: bool = True
    activation_denied_by_default: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class PrePaperRehearsalSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_firewall_disabled_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperPreRehearsalNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_pre_paper_rehearsal_report: bool = True
    notify_mutation_firewall_warning: bool = True
    notify_activation_denied_checkpoint_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True


@dataclass
class PaperFirewallAuditConfig:
    enabled: bool = True
    write_firewall_audit_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_firewall_replay_is_metadata_only: bool = True
    warn_zero_mutation_audit_is_not_activation: bool = True
    warn_evidence_refresh_is_not_activation: bool = True

@dataclass
class PaperFirewallReplayConfig:
    enabled: bool = True
    deterministic_replay: bool = True
    require_pre_rehearsal_review: bool = True
    require_firewall_events: bool = True
    require_all_dangerous_attempts_blocked: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class ZeroMutationAuditConfig:
    enabled: bool = True
    require_before_baseline: bool = True
    require_after_baseline: bool = True
    require_hash_unchanged: bool = True
    block_on_hash_changed: bool = True
    block_on_paper_state_committed: bool = True
    block_on_paper_order_executed: bool = True
    block_on_portfolio_state_mutated: bool = True
    block_on_position_mutated: bool = True
    block_on_cash_mutated: bool = True
    block_on_equity_mutated: bool = True
    block_on_config_patched: bool = True
    block_on_broker_order_sent: bool = True
    block_on_telegram_real_sent: bool = True

@dataclass
class PrePaperReadinessEvidenceRefreshConfig:
    enabled: bool = True
    max_evidence_age_days: int = 14
    require_final_handoff_full_review: bool = True
    require_sealed_readiness_archive: bool = True
    require_pre_paper_governance_checkpoint: bool = True
    require_pre_paper_rehearsal_review: bool = True
    require_firewall_replay_result: bool = True
    require_zero_mutation_audit: bool = True
    require_activation_denied_checkpoint: bool = True
    request_followup_on_missing_evidence: bool = True
    request_followup_on_stale_evidence: bool = True

@dataclass
class ReadinessAuditCheckpointConfig:
    enabled: bool = True
    activation_denied_by_default: bool = True
    activation_allowed: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class FirewallAuditSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_firewall_bypass_risk: bool = True
    block_on_zero_mutation_failed: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperFirewallAuditNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_firewall_audit_report: bool = True
    notify_zero_mutation_audit_warning: bool = True
    notify_readiness_evidence_refresh_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True


@dataclass
class PaperReadinessConfirmationConfig:
    enabled: bool = True
    write_confirmation_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_confirmation_is_not_activation: bool = True
    warn_human_review_bundle_is_not_activation: bool = True
    warn_activation_still_denied_registry_is_not_activation: bool = True

@dataclass
class ReadinessConfirmationQueueConfig:
    enabled: bool = True
    require_firewall_audit_review: bool = True
    require_zero_mutation_audit: bool = True
    require_activation_denied_checkpoint: bool = True
    require_human_review: bool = True
    activation_denied_required: bool = True
    activation_allowed: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class HumanReviewBundleConfig:
    enabled: bool = True
    require_checklist: bool = True
    require_reviewer_notes_placeholder: bool = True
    require_evidence_refs: bool = True
    bundle_is_metadata_only: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class ActivationStillDeniedRegistryConfig:
    enabled: bool = True
    activation_denied_by_default: bool = True
    activation_allowed: bool = False
    register_is_review_only: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class ReadinessConfirmationSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperReadinessConfirmationNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_readiness_confirmation_report: bool = True
    notify_human_review_bundle_warning: bool = True
    notify_activation_still_denied_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True


@dataclass
class PaperReadinessBoardConfig:
    enabled: bool = True
    write_board_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_board_pass_is_not_activation: bool = True
    warn_write_blocked_adapter_is_metadata_only: bool = True
    warn_activation_firewall_denies_activation: bool = True

@dataclass
class HumanGatedPaperReadinessBoardConfig:
    enabled: bool = True
    require_readiness_confirmation_review: bool = True
    require_human_review_bundle: bool = True
    require_activation_still_denied_registry: bool = True
    require_manual_review: bool = True
    activation_denied_required: bool = True
    activation_allowed: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class WriteBlockedPaperRuntimeAdapterConfig:
    enabled: bool = True
    allow_reads: bool = True
    block_writes: bool = True
    prove_all_writes_blocked: bool = True
    deny_paper_state_write: bool = True
    deny_paper_order_create: bool = True
    deny_position_write: bool = True
    deny_portfolio_write: bool = True
    deny_cash_write: bool = True
    deny_equity_write: bool = True
    deny_fill_write: bool = True
    deny_config_patch: bool = True
    deny_active_paper_enable: bool = True
    deny_broker_send: bool = True
    deny_telegram_real_send: bool = True

@dataclass
class FinalActivationFirewallConfig:
    enabled: bool = True
    deny_activation_by_default: bool = True
    deny_enable_active_paper: bool = True
    deny_enable_candidate_strategy: bool = True
    deny_patch_paper_config: bool = True
    deny_commit_paper_state: bool = True
    deny_create_paper_order: bool = True
    deny_send_broker_order: bool = True
    deny_send_telegram_real: bool = True
    deny_unlock_archive: bool = True
    deny_unlock_final_lock: bool = True
    activation_allowed: bool = False

@dataclass
class PaperReadinessBoardSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_write_block_adapter_failed: bool = True
    block_on_activation_firewall_disabled: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperReadinessBoardNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_paper_readiness_board_report: bool = True
    notify_write_blocked_adapter_warning: bool = True
    notify_activation_firewall_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True



@dataclass
class PaperBoundaryCertificateConfig:
    enabled: bool = True
    write_boundary_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_blocker_replay_is_metadata_only: bool = True
    warn_evidence_freeze_is_metadata_only: bool = True
    warn_boundary_certificate_is_not_activation: bool = True

@dataclass
class PaperAdmissionBlockerReplayConfig:
    enabled: bool = True
    deterministic_replay: bool = True
    require_all_attempts_blocked: bool = True
    require_blocker_rules: bool = True
    require_blocker_events: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    paper_admission_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class NoOrderEvidenceFreezeConfig:
    enabled: bool = True
    freeze_is_metadata_only: bool = True
    require_frozen: bool = True
    require_immutable: bool = True
    require_evidence_available: bool = True
    block_on_missing_evidence: bool = True
    block_on_stale_evidence: bool = True
    block_on_freeze_failed: bool = True

@dataclass
class PaperSandboxBoundaryCertificateConfig:
    enabled: bool = True
    certificate_is_metadata_only: bool = True
    require_no_order_dossier: bool = True
    require_blocker_replay: bool = True
    require_evidence_freeze: bool = True
    require_boundary_rules: bool = True
    require_boundary_assertions: bool = True
    require_manual_review: bool = True
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    all_writes_blocked_required: bool = True
    require_order_created_false: bool = True
    require_mutation_detected_false: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class PaperBoundarySafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_admission_allowed_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_transition_allowed_risk: bool = True
    block_on_order_created_risk: bool = True
    block_on_mutation_detected_risk: bool = True
    block_on_blocker_replay_failed: bool = True
    block_on_evidence_freeze_failed: bool = True
    block_on_boundary_assertion_failed: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperBoundaryNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_boundary_certificate_report: bool = True
    notify_blocker_replay_warning: bool = True
    notify_evidence_freeze_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True


@dataclass
class PaperDryAdmissionConfig:
    enabled: bool = True
    write_dry_admission_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_dry_admission_is_not_activation: bool = True
    warn_write_lock_refresh_is_metadata_only: bool = True
    warn_human_approval_ledger_is_not_activation: bool = True

@dataclass
class PaperModeDryAdmissionRehearsalConfig:
    enabled: bool = True
    deterministic_rehearsal: bool = True
    require_no_write_admission_review: bool = True
    require_no_write_contract: bool = True
    require_write_lock_refresh: bool = True
    require_human_ledger: bool = True
    require_activation_denied: bool = True
    activation_allowed: bool = False
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class RuntimeWriteLockProofRefreshConfig:
    enabled: bool = True
    refresh_is_metadata_only: bool = True
    require_hash_unchanged: bool = True
    require_all_writes_blocked: bool = True
    require_unblocked_write_attempt_count_zero: bool = True
    block_on_hash_changed: bool = True
    block_on_mutation_detected: bool = True
    block_on_unblocked_write_attempt: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class HumanApprovalLedgerConfig:
    enabled: bool = True
    ledger_is_metadata_only: bool = True
    require_no_write_acknowledgement: bool = True
    require_not_activation_acknowledgement: bool = True
    require_manual_review: bool = True
    activation_allowed: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class DryAdmissionSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_write_lock_refresh_failed: bool = True
    block_on_human_ledger_activation_risk: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperDryAdmissionNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_dry_admission_report: bool = True
    notify_write_lock_refresh_warning: bool = True
    notify_human_approval_ledger_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

@dataclass
class PaperNoOrderDossierConfig:
    enabled: bool = True
    write_no_order_dossier_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_no_order_dossier_is_not_activation: bool = True
    warn_bridge_replay_audit_seal_is_metadata_only: bool = True
    warn_admission_blocker_denies_admission: bool = True

@dataclass
class NoOrderPaperSessionDossierConfig:
    enabled: bool = True
    deterministic_dossier: bool = True
    require_bridge_review: bool = True
    require_bridge_dry_run: bool = True
    require_no_order_session: bool = True
    require_bridge_replay_result: bool = True
    require_manual_review: bool = True
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    all_writes_blocked_required: bool = True
    require_order_created_false: bool = True
    require_mutation_detected_false: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class BridgeReplayAuditSealConfig:
    enabled: bool = True
    seal_is_metadata_only: bool = True
    require_replay_passed: bool = True
    require_all_dangerous_routes_denied: bool = True
    require_dangerous_allowed_count_zero: bool = True
    require_sealed: bool = True
    require_immutable: bool = True
    block_on_dangerous_allowed_count: bool = True
    block_on_missing_route: bool = True

@dataclass
class FinalPaperAdmissionBlockerConfig:
    enabled: bool = True
    blocker_is_metadata_only: bool = True
    deny_paper_admission_by_default: bool = True
    deny_enable_active_paper: bool = True
    deny_enable_paper_runtime: bool = True
    deny_admit_candidate_to_paper: bool = True
    deny_create_paper_session: bool = True
    deny_create_paper_order: bool = True
    deny_commit_paper_state: bool = True
    deny_patch_paper_config: bool = True
    deny_send_broker_order: bool = True
    deny_send_telegram_real: bool = True
    admission_allowed: bool = False
    active_paper_enabled: bool = False

@dataclass
class NoOrderDossierSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_admission_allowed_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_transition_allowed_risk: bool = True
    block_on_order_created_risk: bool = True
    block_on_mutation_detected_risk: bool = True
    block_on_admission_blocker_failed: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperNoOrderDossierNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_no_order_dossier_report: bool = True
    notify_bridge_replay_audit_seal_warning: bool = True
    notify_paper_admission_blocker_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True


# --- Phase 92 ---

from dataclasses import dataclass

@dataclass
class PaperSafeGateConfig:
    enabled: bool = True
    write_paper_safe_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_boundary_replay_is_metadata_only: bool = True
    warn_frozen_evidence_integrity_is_metadata_only: bool = True
    warn_final_paper_safe_gate_is_not_activation: bool = True

@dataclass
class BoundaryCertificateReplayConfig:
    enabled: bool = True
    deterministic_replay: bool = True
    require_all_rules_pass: bool = True
    require_all_assertions_pass: bool = True
    require_boundary_certificate: bool = True
    require_boundary_rules: bool = True
    require_boundary_assertions: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    paper_admission_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class FrozenEvidenceIntegrityAuditConfig:
    enabled: bool = True
    audit_is_metadata_only: bool = True
    require_frozen: bool = True
    require_immutable: bool = True
    require_hash_match: bool = True
    require_no_tamper: bool = True
    block_on_tamper: bool = True
    block_on_missing_evidence: bool = True
    block_on_stale_evidence: bool = True

@dataclass
class FinalPaperSafeGateConfig:
    enabled: bool = True
    gate_is_metadata_only: bool = True
    require_boundary_replay: bool = True
    require_frozen_evidence_integrity: bool = True
    require_paper_safe_rules: bool = True
    require_paper_safe_assertions: bool = True
    require_manual_review: bool = True
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    all_writes_blocked_required: bool = True
    require_order_created_false: bool = True
    require_mutation_detected_false: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class PaperSafeGateSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_admission_allowed_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_transition_allowed_risk: bool = True
    block_on_order_created_risk: bool = True
    block_on_mutation_detected_risk: bool = True
    block_on_boundary_replay_failed: bool = True
    block_on_frozen_evidence_tamper: bool = True
    block_on_paper_safe_assertion_failed: bool = True
    block_on_secret_risk: bool = True

@dataclass
class PaperSafeGateNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_paper_safe_gate_report: bool = True
    notify_boundary_replay_warning: bool = True
    notify_frozen_evidence_integrity_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True


@dataclass
class PaperReadinessNonExecutionBoardConfig:
    enabled: bool = True
    write_board_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_runtime_map_replay_is_metadata_only: bool = True
    warn_seal_integrity_audit_is_metadata_only: bool = True
    warn_non_execution_board_is_not_activation: bool = True

@dataclass
class PrePaperRuntimeMapReplayConfig:
    enabled: bool = True
    deterministic_replay: bool = True
    require_runtime_map: bool = True
    require_component_map: bool = True
    require_route_map: bool = True
    require_all_dangerous_routes_denied: bool = True
    allow_read_only_routes: bool = True
    allow_preview_routes: bool = True
    allow_dry_run_routes: bool = True
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    paper_admission_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class NonExecutionSealIntegrityAuditConfig:
    enabled: bool = True
    audit_is_metadata_only: bool = True
    require_seal_hash_match: bool = True
    require_confirmed_non_execution: bool = True
    require_confirmed_no_broker: bool = True
    require_confirmed_no_active_paper: bool = True
    require_confirmed_no_paper_admission: bool = True
    require_confirmed_no_order: bool = True
    require_confirmed_no_write: bool = True
    require_confirmed_no_telegram_real_send: bool = True
    require_confirmed_no_config_patch: bool = True
    block_on_hash_mismatch: bool = True
    block_on_confirmation_failed: bool = True

@dataclass
class FinalPaperReadinessNonExecutionBoardConfig:
    enabled: bool = True
    board_is_metadata_only: bool = True
    require_paper_safe_dossier: bool = True
    require_runtime_map_replay: bool = True
    require_seal_integrity_audit: bool = True
    require_board_gates: bool = True
    require_board_assertions: bool = True
    require_manual_review: bool = True
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    all_writes_blocked_required: bool = True
    require_order_created_false: bool = True
    require_mutation_detected_false: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class NonExecutionBoardSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_admission_allowed_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_transition_allowed_risk: bool = True
    block_on_order_created_risk: bool = True
    block_on_mutation_detected_risk: bool = True
    block_on_runtime_route_permission_risk: bool = True
    block_on_non_execution_seal_integrity_failed: bool = True
    block_on_board_assertion_failed: bool = True
    block_on_secret_risk: bool = True

@dataclass
class NonExecutionBoardNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_non_execution_board_report: bool = True
    notify_runtime_map_replay_warning: bool = True
    notify_seal_integrity_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
@dataclass
class PaperReadinessBoardDossierConfig:
    enabled: bool = True
    write_board_dossier_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_board_dossier_is_not_activation: bool = True
    warn_acceptance_board_seal_is_metadata_only: bool = True
    warn_shadow_launch_blocker_denies_launch: bool = True

@dataclass
class PaperReadinessNonExecutionBoardDossierConfig:
    enabled: bool = True
    deterministic_dossier: bool = True
    require_non_execution_board_review: bool = True
    require_final_non_execution_board: bool = True
    require_runtime_map_replay_result: bool = True
    require_non_execution_seal_integrity_audit: bool = True
    require_acceptance_board_seal: bool = True
    require_shadow_launch_blocker: bool = True
    require_manual_review: bool = True
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    shadow_launch_allowed: bool = False
    paper_mode_launch_allowed: bool = False
    all_writes_blocked_required: bool = True
    require_order_created_false: bool = True
    require_mutation_detected_false: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class AcceptanceBoardSealConfig:
    enabled: bool = True
    seal_is_metadata_only: bool = True
    require_board_gates_passed: bool = True
    require_board_assertions_passed: bool = True
    require_runtime_replay_passed: bool = True
    require_all_dangerous_runtime_routes_denied: bool = True
    require_non_execution_seal_integrity_valid: bool = True
    require_sealed: bool = True
    require_immutable: bool = True
    allow_shadow_launch: bool = False
    allow_paper_mode_launch: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class FinalPaperModeShadowLaunchBlockerConfig:
    enabled: bool = True
    blocker_is_metadata_only: bool = True
    deny_shadow_launch_by_default: bool = True
    deny_start_paper_mode: bool = True
    deny_start_local_paper_runtime: bool = True
    deny_shadow_launch_candidate: bool = True
    deny_admit_candidate_to_paper: bool = True
    deny_create_paper_session: bool = True
    deny_create_paper_order: bool = True
    deny_commit_paper_state: bool = True
    deny_patch_paper_config: bool = True
    deny_send_broker_order: bool = True
    deny_send_telegram_real: bool = True
    shadow_launch_allowed: bool = False
    paper_mode_launch_allowed: bool = False
    active_paper_enabled: bool = False

@dataclass
class BoardDossierSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_shadow_launch_risk: bool = True
    block_on_paper_mode_launch_risk: bool = True
    block_on_admission_allowed_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_transition_allowed_risk: bool = True
    block_on_order_created_risk: bool = True
    block_on_mutation_detected_risk: bool = True
    block_on_shadow_launch_blocker_failed: bool = True
    block_on_secret_risk: bool = True

@dataclass
class BoardDossierNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_board_dossier_report: bool = True
    notify_acceptance_board_seal_warning: bool = True
    notify_shadow_launch_blocker_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

@dataclass
class PaperModeDryAdmissionGateConfig:
    enabled: bool = True
    write_dry_admission_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_shadow_replay_is_metadata_only: bool = True
    warn_board_evidence_freeze_is_metadata_only: bool = True
    warn_dry_admission_gate_is_not_activation: bool = True

@dataclass
class ShadowLaunchBlockerReplayConfig:
    enabled: bool = True
    deterministic_replay: bool = True
    require_all_attempts_blocked: bool = True
    require_shadow_launch_blocker_events: bool = True
    execution_enabled: bool = False
    shadow_launch_enabled: bool = False
    paper_mode_launch_enabled: bool = False
    active_paper_enabled: bool = False
    paper_admission_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class BoardEvidenceFreezeConfig:
    enabled: bool = True
    freeze_is_metadata_only: bool = True
    require_frozen: bool = True
    require_immutable: bool = True
    require_evidence_available: bool = True
    block_on_missing_evidence: bool = True
    block_on_stale_evidence: bool = True
    block_on_freeze_failed: bool = True

@dataclass
class FinalPaperModeDryAdmissionGateConfig:
    enabled: bool = True
    gate_is_metadata_only: bool = True
    require_board_dossier: bool = True
    require_acceptance_board_seal: bool = True
    require_shadow_replay: bool = True
    require_board_evidence_freeze: bool = True
    require_dry_admission_rules: bool = True
    require_dry_admission_assertions: bool = True
    require_manual_review: bool = True
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    shadow_launch_allowed: bool = False
    paper_mode_launch_allowed: bool = False
    all_writes_blocked_required: bool = True
    require_order_created_false: bool = True
    require_mutation_detected_false: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class DryAdmissionGateSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_shadow_launch_risk: bool = True
    block_on_paper_mode_launch_risk: bool = True
    block_on_admission_allowed_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_transition_allowed_risk: bool = True
    block_on_order_created_risk: bool = True
    block_on_mutation_detected_risk: bool = True
    block_on_shadow_replay_failed: bool = True
    block_on_board_evidence_freeze_failed: bool = True
    block_on_dry_admission_assertion_failed: bool = True
    block_on_secret_risk: bool = True

@dataclass
class DryAdmissionGateNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_dry_admission_gate_report: bool = True
    notify_shadow_replay_warning: bool = True
    notify_board_evidence_freeze_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

@dataclass
class PrePaperHandoffFreezeGateConfig:
    enabled: bool = True
    write_handoff_freeze_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_sandbox_replay_is_metadata_only: bool = True
    warn_simulator_evidence_freeze_is_metadata_only: bool = True
    warn_handoff_freeze_gate_is_not_activation: bool = True
    warn_phase_100_is_pre_paper_freeze_only: bool = True

@dataclass
class SandboxRuntimeAdmissionBlockerReplayConfig:
    enabled: bool = True
    deterministic_replay: bool = True
    require_all_attempts_blocked: bool = True
    require_sandbox_runtime_admission_blocker_events: bool = True
    execution_enabled: bool = False
    sandbox_runtime_admission_enabled: bool = False
    paper_sandbox_runtime_enabled: bool = False
    simulator_admission_enabled: bool = False
    local_paper_simulator_enabled: bool = False
    active_paper_enabled: bool = False
    paper_admission_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    telegram_real_send_enabled: bool = False

@dataclass
class SimulatorEvidenceFreezeConfig:
    enabled: bool = True
    freeze_is_metadata_only: bool = True
    require_frozen: bool = True
    require_immutable: bool = True
    require_evidence_available: bool = True
    block_on_missing_evidence: bool = True
    block_on_stale_evidence: bool = True
    block_on_freeze_failed: bool = True

@dataclass
class FinalPrePaperHandoffFreezeGateConfig:
    enabled: bool = True
    gate_is_metadata_only: bool = True
    require_simulator_dossier: bool = True
    require_simulator_acceptance_seal: bool = True
    require_sandbox_runtime_admission_replay: bool = True
    require_simulator_evidence_freeze: bool = True
    require_handoff_freeze_rules: bool = True
    require_handoff_freeze_assertions: bool = True
    require_manual_review: bool = True
    require_frozen: bool = True
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    sandbox_runtime_admission_allowed: bool = False
    paper_sandbox_runtime_allowed: bool = False
    simulator_admission_allowed: bool = False
    local_paper_simulator_allowed: bool = False
    active_paper_enabled: bool = False
    all_writes_blocked_required: bool = True
    require_order_created_false: bool = True
    require_mutation_detected_false: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class HandoffFreezeSafetyConfig:
    enabled: bool = True
    block_on_real_order_risk: bool = True
    block_on_paper_order_risk: bool = True
    block_on_broker_order_risk: bool = True
    block_on_paper_state_mutation_risk: bool = True
    block_on_telegram_real_send_risk: bool = True
    block_on_production_config_write_risk: bool = True
    block_on_active_paper_enable_risk: bool = True
    block_on_simulator_admission_risk: bool = True
    block_on_sandbox_runtime_admission_risk: bool = True
    block_on_paper_sandbox_runtime_risk: bool = True
    block_on_admission_allowed_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_transition_allowed_risk: bool = True
    block_on_order_created_risk: bool = True
    block_on_mutation_detected_risk: bool = True
    block_on_sandbox_replay_failed: bool = True
    block_on_simulator_evidence_freeze_failed: bool = True
    block_on_handoff_freeze_assertion_failed: bool = True
    block_on_secret_risk: bool = True

@dataclass
class HandoffFreezeNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_handoff_freeze_report: bool = True
    notify_sandbox_runtime_admission_replay_warning: bool = True
    notify_simulator_evidence_freeze_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True


@dataclass
class AdvancedTransitionConfig:
    enabled: bool = True
    current_phase: int = 101
    final_phase: int = 160
    require_phase100_handoff: bool = True
    require_handoff_frozen: bool = True
    require_handoff_immutable: bool = True
    require_handoff_metadata_only: bool = True
    allow_activation: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_scraping: bool = False
    allow_dashboard: bool = False
    write_transition_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase101_is_not_activation: bool = True

@dataclass
class Phase101RuntimeBoundaryConfig:
    all_execution_blocked: bool = True
    active_paper_blocked: bool = True
    broker_execution_blocked: bool = True
    paper_state_mutation_blocked: bool = True
    telegram_real_send_blocked: bool = True
    scraping_blocked: bool = True
    dashboard_blocked: bool = True
    metadata_outputs_allowed: bool = True
    test_artifacts_allowed: bool = True
    local_read_only_allowed: bool = True

@dataclass
class Phase101NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class AdvancedRuntimeConfig:
    enabled: bool = True
    current_phase: int = 102
    final_phase: int = 160
    require_phase101_transition_review: bool = True
    normalize_runtime_registry: bool = True
    normalize_config_surface: bool = True
    provider_interfaces_ready: bool = True
    allow_activation: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_scraping: bool = False
    allow_dashboard: bool = False
    allow_paid_api: bool = False
    write_runtime_registry_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase102_is_not_activation: bool = True

@dataclass
class Phase102RuntimeModesConfig:
    default_mode: str = "PROVIDER_READY_NO_FETCH"
    offline_metadata_enabled: bool = True
    local_read_only_enabled: bool = True
    local_compute_only_enabled: bool = True
    provider_ready_no_fetch_enabled: bool = True
    provider_network_fetch_default: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False

@dataclass
class Phase102ProviderContractsConfig:
    enabled: bool = True
    metadata_only_by_default: bool = True
    network_disabled_by_default: bool = True
    cache_allowed: bool = True
    paid_api_blocked: bool = True
    scraping_blocked: bool = True
    broker_blocked: bool = True
    order_blocked: bool = True
    paper_mutation_blocked: bool = True
    telegram_real_send_blocked: bool = True

@dataclass
class Phase102ConfigSurfaceConfig:
    enabled: bool = True
    normalize_missing_safety_keys: bool = True
    block_on_conflict: bool = True
    block_on_unsafe_value: bool = True
    generate_migration_hints: bool = True

@dataclass
class Phase102NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class RuntimeServiceGraphConfig:
    enabled: bool = True
    current_phase: int = 103
    final_phase: int = 160
    require_phase102_runtime_registry: bool = True
    build_service_graph: bool = True
    validate_dependency_contracts: bool = True
    detect_cycles: bool = True
    write_service_graph_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase103_is_not_activation: bool = True

    def __post_init__(self):
        if self.current_phase != 103:
            raise ValueError("current_phase must be 103")

@dataclass
class Phase103OrchestrationConfig:
    enabled: bool = True
    dry_run_only: bool = True
    metadata_only_default: bool = True
    read_only_allowed: bool = True
    local_compute_validation_allowed: bool = True
    network_allowed: bool = False
    execution_allowed: bool = False
    broker_allowed: bool = False
    order_allowed: bool = False
    paper_mutation_allowed: bool = False
    telegram_real_send_allowed: bool = False
    scraping_allowed: bool = False
    dashboard_allowed: bool = False

    def __post_init__(self):
        if not self.dry_run_only:
            raise ValueError("dry_run_only must be true")
        if self.execution_allowed:
            raise ValueError("execution_allowed must be false")
        if self.broker_allowed:
            raise ValueError("broker_allowed must be false")

@dataclass
class Phase103DependencyPolicyConfig:
    require_no_cycles: bool = True
    require_no_missing_dependencies: bool = True
    require_no_execution_routes: bool = True
    require_no_broker_routes: bool = True
    require_no_order_routes: bool = True
    require_no_paper_mutation_routes: bool = True
    require_no_telegram_real_send_routes: bool = True
    require_no_scraping_routes: bool = True
    require_no_dashboard_routes: bool = True

    def __post_init__(self):
        if not self.require_no_cycles:
            raise ValueError("require_no_cycles must be true")

@dataclass
class Phase103NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

    def __post_init__(self):
        if self.telegram_real_send:

            raise ValueError("telegram_real_send must be false")



@dataclass
class RuntimeLifecycleConfig:
    enabled: bool = True
    current_phase: int = 104
    final_phase: int = 160
    require_phase103_service_graph: bool = True
    run_startup_checks: bool = True
    build_readiness_matrix: bool = True
    build_readiness_gate: bool = True
    lifecycle_dry_run_only: bool = True
    ready_for_phase105_metadata_only: bool = True
    allow_activation: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_scraping: bool = False
    allow_dashboard: bool = False
    write_lifecycle_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase104_is_not_activation: bool = True

@dataclass
class Phase104StartupChecksConfig:
    enabled: bool = True
    core_checks_enabled: bool = True
    provider_checks_enabled: bool = True
    observability_checks_enabled: bool = True
    notification_checks_enabled: bool = True
    no_execution_safety_check_enabled: bool = True
    external_network_allowed: bool = False
    destructive_file_ops_allowed: bool = False
    provider_fetch_allowed: bool = False

@dataclass
class Phase104ReadinessGateConfig:
    enabled: bool = True
    metadata_only: bool = True
    read_only: bool = True
    require_startup_checks_passed: bool = True
    require_service_readiness: bool = True
    require_dependency_readiness: bool = True
    require_config_readiness: bool = True
    require_provider_readiness: bool = True
    require_no_execution_readiness: bool = True
    ready_for_phase105: bool = True
    allow_activation: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_order_creation: bool = False
    allow_paper_state_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_scraping: bool = False
    allow_dashboard: bool = False

@dataclass
class Phase104NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False



@dataclass
class DataProviderAbstractionConfig:
    enabled: bool = True
    current_phase: int = 106
    final_phase: int = 160
    require_phase105_provider_kickoff_gate: bool = True
    skeleton_only: bool = True
    metadata_only: bool = True
    provider_registry_enabled: bool = True
    provider_selector_enabled: bool = True
    fallback_plan_enabled: bool = True
    write_provider_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase106_is_not_activation: bool = True
    warn_no_real_fetch_required: bool = True

    def __post_init__(self):
        if self.current_phase != 106:
            raise ValueError("current_phase must be 106")
        if self.final_phase != 160:
            raise ValueError("final_phase must be 160")
        if not self.require_phase105_provider_kickoff_gate:
            raise ValueError("require_phase105_provider_kickoff_gate must be true")
        if not self.skeleton_only:
            raise ValueError("skeleton_only must be true")
        if not self.metadata_only:
            raise ValueError("metadata_only must be true")

@dataclass
class Phase106ProviderSafetyConfig:
    metadata_only_by_default: bool = True
    network_fetch_enabled_now: bool = False
    provider_network_fetch_required: bool = False
    paid_api_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    dashboard_enabled: bool = False
    credential_required_now: bool = False

    def __post_init__(self):
        if self.network_fetch_enabled_now:
            raise ValueError("network_fetch_enabled_now must be false")
        if self.provider_network_fetch_required:
            raise ValueError("provider_network_fetch_required must be false")
        if self.paid_api_enabled:
            raise ValueError("paid_api_enabled must be false")
        if self.scraping_enabled:
            raise ValueError("scraping_enabled must be false")
        if self.html_parse_enabled:
            raise ValueError("html_parse_enabled must be false")
        if self.broker_execution_enabled:
            raise ValueError("broker_execution_enabled must be false")
        if self.order_creation_enabled:
            raise ValueError("order_creation_enabled must be false")
        if self.paper_state_mutation_enabled:
            raise ValueError("paper_state_mutation_enabled must be false")
        if self.telegram_real_send_enabled:
            raise ValueError("telegram_real_send_enabled must be false")
        if self.dashboard_enabled:
            raise ValueError("dashboard_enabled must be false")
        if self.credential_required_now:
            raise ValueError("credential_required_now must be false")

@dataclass
class Phase106ProviderRegistryConfig:
    yfinance_skeleton_enabled: bool = True
    stooq_skeleton_enabled: bool = True
    nasdaq_data_link_skeleton_enabled: bool = True
    fred_skeleton_enabled: bool = True
    sec_company_facts_skeleton_enabled: bool = True
    local_csv_skeleton_enabled: bool = True
    default_market_data_provider: str = "YFINANCE"
    default_selector_mode: str = "METADATA_ONLY"

@dataclass
class Phase106NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

    def __post_init__(self):
        if self.telegram_real_send:
            raise ValueError("telegram_real_send must be false")

@dataclass
@dataclass
class FeatureEngineFoundationConfig:
    enabled: bool = True
    current_phase: int = 116
    final_phase: int = 160
    require_phase115_feature_factor_kickoff_gate: bool = True
    indicator_registry_enabled: bool = True
    feature_registry_enabled: bool = True
    factor_registry_enabled: bool = True
    feature_input_contract_enabled: bool = True
    feature_output_schema_enabled: bool = True
    feature_computation_planner_enabled: bool = True
    feature_transform_pipeline_enabled: bool = True
    write_feature_foundation_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase116_is_not_activation: bool = True
    warn_features_are_not_trade_signals: bool = True

@dataclass
class Phase116FeaturePolicyConfig:
    metadata_only: bool = True
    research_data_only: bool = True
    dry_run_only_default: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase116FeatureScopeConfig:
    allow_indicator_input_contracts: bool = True
    allow_feature_schema_definitions: bool = True
    allow_factor_metadata_definitions: bool = True
    allow_ohlcv_feature_fixtures: bool = True
    allow_event_context_feature_metadata: bool = True
    allow_calendar_aware_feature_metadata: bool = True
    allow_quality_aware_feature_metadata: bool = True
    allow_feature_validation_rules: bool = True
    allow_feature_lineage_metadata: bool = True
    block_signal_generation: bool = True
    block_strategy_activation: bool = True
    block_order_decision: bool = True
    block_broker_execution: bool = True
    block_paper_state_mutation: bool = True

@dataclass
class Phase116NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class CoreRuntimeAcceptanceConfig:
    enabled: bool = False
    current_phase: int = 105
    final_phase: int = 160
    require_phase104_lifecycle_review: bool = True
    require_lifecycle_ready: bool = True
    require_readiness_gate_passed: bool = True
    require_startup_checks_passed: bool = True
    require_foundation_freeze: bool = True
    write_acceptance_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase105_is_not_activation: bool = True
    warn_phase105_closes_core_consolidation_band: bool = True

@dataclass
class AdvancedFoundationFreezeConfig:
    enabled: bool = False
    phase_start: int = 101
    phase_end: int = 105
    next_phase: int = 106
    final_phase: int = 160
    freeze_is_metadata_only: bool = True
    require_frozen: bool = True
    require_immutable: bool = True
    require_phase101_evidence: bool = True
    require_phase102_evidence: bool = True
    require_phase103_evidence: bool = True
    require_phase104_evidence: bool = True
    block_on_missing_evidence: bool = True
    block_on_stale_evidence: bool = True

@dataclass
class DataProviderExpansionKickoffGateConfig:
    enabled: bool = False
    ready_for_phase106: bool = True
    metadata_only: bool = True
    provider_ready: bool = True
    provider_network_fetch_required: bool = False
    allow_activation: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_order_creation: bool = False
    allow_paper_state_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_dashboard: bool = False
    allow_paid_api: bool = False

@dataclass
class Phase105NotificationsConfig:
    enabled: bool = False
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class Phase108CachePolicyConfig:
    default_ttl_seconds: int = 86400
    intraday_ttl_seconds: int = 900
    daily_ttl_seconds: int = 86400
    fundamentals_ttl_seconds: int = 604800
    macro_ttl_seconds: int = 86400
    allow_stale_read: bool = True
    stale_read_requires_warning: bool = True
    block_expired: bool = False
    destructive_compaction_allowed: bool = False

@dataclass
class Phase108FallbackPolicyConfig:
    dry_run_only: bool = True
    cache_only_default: bool = True
    network_enabled_by_default: bool = False
    paid_api_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    dashboard_enabled: bool = False

@dataclass
class Phase108SourceComparisonConfig:
    enabled: bool = True
    dry_run_only: bool = True
    default_tolerance_pct: float = 0.5
    material_difference_threshold_pct: float = 2.0
    min_rows_required: int = 1
    produce_confidence_hints: bool = True
    produce_trade_signals: bool = False

@dataclass
class Phase108NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class ProviderCacheConfig:
    enabled: bool = True
    current_phase: int = 108
    final_phase: int = 160
    require_phase107_provider_runtime: bool = True
    cache_store_enabled: bool = True
    cache_index_enabled: bool = True
    stale_fresh_policy_enabled: bool = True
    fallback_dry_run_enabled: bool = True
    source_comparison_enabled: bool = True
    write_provider_cache_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase108_is_not_activation: bool = True
    warn_no_real_network_in_tests: bool = True

@dataclass
class Phase109ScoringPolicyConfig:
    completeness_weight: float = 0.20
    freshness_weight: float = 0.15
    schema_validity_weight: float = 0.20
    continuity_weight: float = 0.15
    source_agreement_weight: float = 0.15
    outlier_profile_weight: float = 0.05
    cache_reliability_weight: float = 0.05
    safety_compliance_weight: float = 0.05
    block_on_safety_score_zero: bool = True
    block_on_schema_invalid: bool = True

    def __post_init__(self):
        total_weight = sum([
            self.completeness_weight,
            self.freshness_weight,
            self.schema_validity_weight,
            self.continuity_weight,
            self.source_agreement_weight,
            self.outlier_profile_weight,
            self.cache_reliability_weight,
            self.safety_compliance_weight
        ])
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError("Scoring policy weights must sum to approximately 1.0")

@dataclass
class Phase109SelectionPolicyConfig:
    research_data_only: bool = True
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False

    def __post_init__(self):
        if not self.research_data_only:
            raise ValueError("research_data_only must be true")
        if self.produce_trade_signals:
            raise ValueError("produce_trade_signals must be false")
        if self.produce_order_decisions:
            raise ValueError("produce_order_decisions must be false")
        if self.allow_network:
            raise ValueError("allow_network must be false")
        if self.allow_paid_api:
            raise ValueError("allow_paid_api must be false")
        if self.allow_scraping:
            raise ValueError("allow_scraping must be false")
        if self.allow_html_parsing:
            raise ValueError("allow_html_parsing must be false")
        if self.allow_broker:
            raise ValueError("allow_broker must be false")
        if self.allow_order:
            raise ValueError("allow_order must be false")
        if self.allow_paper_mutation:
            raise ValueError("allow_paper_mutation must be false")
        if self.allow_telegram_real_send:
            raise ValueError("allow_telegram_real_send must be false")
        if self.allow_dashboard:
            raise ValueError("allow_dashboard must be false")

@dataclass
class Phase109NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

    def __post_init__(self):
        if self.telegram_real_send:
            raise ValueError("telegram_real_send must be false")

@dataclass
class ProviderQualityConfig:
    enabled: bool = True
    current_phase: int = 109
    final_phase: int = 160
    require_phase108_provider_cache: bool = True
    data_quality_scoring_enabled: bool = True
    source_trust_model_enabled: bool = True
    provider_selection_scoring_enabled: bool = True
    provider_ranking_enabled: bool = True
    write_provider_quality_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase109_is_not_activation: bool = True
    warn_scores_are_not_trade_signals: bool = True

    def __post_init__(self):
        if self.current_phase != 109:
            raise ValueError("current_phase must be 109")
        if self.final_phase != 160:
            raise ValueError("final_phase must be 160")
        if not self.require_phase108_provider_cache:
            raise ValueError("require_phase108_provider_cache must be true")

@dataclass
class EventMetadataConfig:
    enabled: bool = True
    current_phase: int = 111
    final_phase: int = 160
    require_phase110_provider_orchestration: bool = True
    macro_metadata_enabled: bool = True
    economic_calendar_enabled: bool = True
    earnings_calendar_enabled: bool = True
    corporate_actions_enabled: bool = True
    news_metadata_enabled: bool = True
    event_schedule_enabled: bool = True
    write_event_metadata_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase111_is_not_activation: bool = True
    warn_events_are_not_trade_signals: bool = True

    def __post_init__(self):
        if self.current_phase != 111: raise ValueError("current_phase must be 111")
        if self.final_phase != 160: raise ValueError("final_phase must be 160")
        if not self.require_phase110_provider_orchestration: raise ValueError("require_phase110_provider_orchestration must be True")

@dataclass
class Phase111EventPolicyConfig:
    metadata_only: bool = True
    research_context_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    fetch_news_content: bool = False

    def __post_init__(self):
        if not self.metadata_only: raise ValueError()
        if not self.research_context_only: raise ValueError()
        if not self.local_fixture_only_default: raise ValueError()
        if self.allow_network: raise ValueError()
        if self.allow_paid_api: raise ValueError()
        if self.allow_scraping: raise ValueError()
        if self.allow_html_parsing: raise ValueError()
        if self.allow_broker: raise ValueError()
        if self.allow_order: raise ValueError()
        if self.allow_paper_mutation: raise ValueError()
        if self.allow_telegram_real_send: raise ValueError()
        if self.allow_dashboard: raise ValueError()
        if self.produce_trade_signals: raise ValueError()
        if self.produce_order_decisions: raise ValueError()
        if self.fetch_news_content: raise ValueError()

@dataclass
class Phase111MacroCatalogConfig:
    enabled: bool = True
    fred_compatible_metadata_only: bool = True
    network_enabled_now: bool = False
    credential_required_now: bool = False

    def __post_init__(self):
        if self.network_enabled_now: raise ValueError()

@dataclass
class Phase111NewsMetadataConfig:
    enabled: bool = True
    metadata_only: bool = True
    content_fetch_enabled: bool = False
    network_enabled_now: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    store_raw_urls: bool = False
    use_url_hash: bool = True

    def __post_init__(self):
        if self.content_fetch_enabled: raise ValueError()
        if self.network_enabled_now: raise ValueError()
        if self.store_raw_urls: raise ValueError()
        if not self.use_url_hash: raise ValueError()

@dataclass
class Phase111NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

    def __post_init__(self):
        if self.telegram_real_send: raise ValueError()


@dataclass
class EventImpactConfig:
    enabled: bool = True
    current_phase: int = 112
    final_phase: int = 160
    require_phase111_event_metadata: bool = True
    event_impact_tagging_enabled: bool = True
    macro_regime_metadata_enabled: bool = True
    calendar_aware_validation_enabled: bool = True
    write_event_impact_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase112_is_not_activation: bool = True
    warn_impact_tags_are_not_trade_signals: bool = True

@dataclass
class Phase112ImpactPolicyConfig:
    metadata_only: bool = True
    research_context_only: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False

@dataclass
class Phase112MacroRegimeConfig:
    enabled: bool = True
    metadata_only: bool = True
    research_context_only: bool = True
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False

@dataclass
class Phase112CalendarValidationConfig:
    enabled: bool = True
    metadata_only: bool = True
    research_context_only: bool = True
    price_jump_threshold_pct: float = 8.0
    volume_multiplier_threshold: float = 3.0
    explain_with_event_context: bool = True
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False

@dataclass
class Phase112NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class ProviderFreezeConfig:
    enabled: bool = True
    current_phase: int = 114
    final_phase: int = 160
    require_phase113_provider_governance: bool = True
    freeze_enabled: bool = True
    multi_provider_final_review_enabled: bool = True
    data_layer_rehearsal_enabled: bool = True
    output_contract_enabled: bool = True
    write_provider_freeze_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase114_is_not_activation: bool = True
    warn_freeze_is_not_trading_enable: bool = True

@dataclass
class Phase114FreezePolicyConfig:
    metadata_only: bool = True
    research_data_only: bool = True
    phase_start: int = 106
    phase_end: int = 114
    next_phase: int = 115
    final_phase: int = 160
    frozen: bool = True
    immutable: bool = True
    allow_activation: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_order_creation: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_paid_api: bool = False
    allow_dashboard: bool = False
    network_default_enabled: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False

@dataclass
class Phase114RehearsalConfig:
    enabled: bool = True
    metadata_only: bool = True
    dry_run_only: bool = True
    research_data_only: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False

@dataclass
class Phase114OutputContractConfig:
    enabled: bool = True
    metadata_only_required: bool = True
    research_data_only_required: bool = True
    trade_signal_blocked: bool = True
    order_decision_blocked: bool = True
    execution_blocked: bool = True
    broker_blocked: bool = True
    paper_mutation_blocked: bool = True
    telegram_real_send_blocked: bool = True
    scraping_blocked: bool = True
    html_parsing_blocked: bool = True
    paid_api_blocked: bool = True
    network_default_enabled_blocked: bool = True

@dataclass
class Phase114NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class ProviderFinalAcceptanceConfig:
    enabled: bool = False
    current_phase: int = 115
    final_phase: int = 160
    require_phase114_provider_freeze: bool = True
    final_acceptance_enabled: bool = True
    provider_layer_closure_enabled: bool = True
    feature_factor_kickoff_gate_enabled: bool = True
    write_final_acceptance_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase115_is_not_activation: bool = True
    warn_acceptance_is_not_trading_enable: bool = True

@dataclass
class Phase115FinalAcceptancePolicyConfig:
    metadata_only: bool = True
    research_data_only: bool = True
    phase_start: int = 106
    phase_end: int = 115
    next_phase: int = 116
    final_phase: int = 160
    accept_provider_layer: bool = True
    close_provider_layer: bool = True
    allow_activation: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_order_creation: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_paid_api: bool = False
    allow_dashboard: bool = False
    network_default_enabled: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False

@dataclass
class Phase115FeatureFactorKickoffConfig:
    enabled: bool = True
    ready_for_phase116: bool = True
    metadata_only: bool = True
    research_data_only: bool = True
    allow_indicator_input_contracts: bool = True
    allow_feature_schema_definitions: bool = True
    allow_factor_metadata_definitions: bool = True
    allow_feature_validation_rules: bool = True
    block_trade_signal_generation: bool = True
    block_strategy_activation: bool = True
    block_order_decision: bool = True
    block_broker_execution: bool = True
    block_paper_state_mutation: bool = True
    block_live_demo_trading: bool = True
    block_telegram_real_send: bool = True
    block_dashboard: bool = True
    block_paid_api: bool = True
    block_scraping: bool = True
    block_html_parsing: bool = True

@dataclass
class Phase115NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False




@dataclass
class Phase118FeaturePolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase118CrossSectionalConfig:
    enabled: bool = True
    min_required_symbols: int = 2
    default_benchmark_symbol: str = "SPY"
    align_on_common_timestamps: bool = True
    produce_portfolio_weights: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False

@dataclass
class Phase118FeatureTableConfig:
    preserve_core_feature_columns: bool = True
    preserve_warmup_nulls: bool = True
    block_forbidden_columns: bool = True
    allow_macd_signal_line_column: bool = True
    write_feature_tables: bool = True
    overwrite_feature_tables_default: bool = False

@dataclass
class Phase118NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class AdvancedFeaturesConfig:
    enabled: bool = True
    current_phase: int = 118
    final_phase: int = 160
    require_phase117_core_indicators: bool = True
    advanced_volatility_enabled: bool = True
    advanced_momentum_enabled: bool = True
    advanced_trend_enabled: bool = True
    normalization_enabled: bool = True
    cross_sectional_enabled: bool = True
    multi_symbol_feature_table_enabled: bool = True
    write_advanced_feature_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase118_is_not_activation: bool = True
    warn_advanced_features_are_not_trade_signals: bool = True
    policy: Phase118FeaturePolicyConfig = field(default_factory=Phase118FeaturePolicyConfig)
    cross_sectional: Phase118CrossSectionalConfig = field(default_factory=Phase118CrossSectionalConfig)
    feature_table: Phase118FeatureTableConfig = field(default_factory=Phase118FeatureTableConfig)
    notifications: Phase118NotificationsConfig = field(default_factory=Phase118NotificationsConfig)



@dataclass
class FeatureFactorIntegrationFreezeConfig:
    enabled: bool = True
    current_phase: int = 124
    final_phase: int = 160
    require_phase123_explainability: bool = True
    artifact_chain_integrity_enabled: bool = True
    schema_continuity_enabled: bool = True
    lineage_continuity_enabled: bool = True
    safety_boundary_continuity_enabled: bool = True
    integration_rehearsal_enabled: bool = True
    report_qa_acceptance_enabled: bool = True
    freeze_candidate_manifest_enabled: bool = True
    freeze_readiness_gate_enabled: bool = True
    write_freeze_preparation_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase124_is_not_activation: bool = True
    warn_freeze_preparation_is_not_deployment: bool = True

@dataclass
class Phase124FreezePolicyConfig:
    compute_metadata_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False

@dataclass
class Phase124AcceptancePolicyConfig:
    require_artifact_chain_complete: bool = True
    require_schema_continuity: bool = True
    require_lineage_continuity: bool = True
    require_safety_boundary_pass: bool = True
    require_report_qa_accepted: bool = True
    require_factor_store_hardened: bool = True
    require_freeze_manifest_valid: bool = True
    ready_for_phase125_allowed: bool = True
    ready_for_phase126_kickoff_after_phase125_allowed: bool = True

@dataclass
class Phase124NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False



@dataclass
class FeatureFactorFinalClosureConfig:
    enabled: bool = True
    current_phase: int = 125
    final_phase: int = 160
    require_phase124_freeze_preparation: bool = True
    final_artifact_chain_enabled: bool = True
    final_closure_checks_enabled: bool = True
    freeze_seal_enabled: bool = True
    engine_readiness_certificate_enabled: bool = True
    phase126_kickoff_gate_enabled: bool = True
    write_final_closure_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase125_is_not_activation: bool = True
    warn_freeze_seal_is_not_deployment: bool = True
    warn_phase126_gate_is_not_strategy_activation: bool = True

@dataclass
class Phase125FinalClosurePolicyConfig:
    compute_metadata_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase125ClosureRequirementsConfig:
    require_phase124_ready: bool = True
    require_final_artifact_chain_complete: bool = True
    require_final_checks_passed: bool = True
    require_freeze_seal_valid: bool = True
    require_engine_certificate_valid: bool = True
    require_phase126_gate_passed: bool = True
    require_safety_pass: bool = True
    ready_for_phase126_allowed: bool = True

@dataclass
class Phase125NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


from dataclasses import dataclass, field

@dataclass
class RegimeFeatureEngineeringConfig:
    enabled: bool = True
    current_phase: int = 127
    final_phase: int = 160
    require_phase126_regime_foundation: bool = True
    market_state_metrics_enabled: bool = True
    rolling_market_state_metrics_enabled: bool = True
    cross_sectional_market_state_metrics_enabled: bool = True
    regime_feature_table_enabled: bool = True
    unsupervised_candidate_preparation_enabled: bool = True
    candidate_readiness_gate_enabled: bool = True
    write_regime_feature_engineering_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase127_is_not_activation: bool = True
    warn_candidates_are_not_predictions: bool = True
    warn_candidates_are_not_trade_signals: bool = True

@dataclass
class Phase127RegimePolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_heavy_ml_dependencies: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase127MarketStateMetricsConfig:
    enabled: bool = True
    default_windows: list[int] = field(default_factory=lambda: [20, 60, 120])
    build_cross_sectional_metrics: bool = True
    preserve_warmup_nulls: bool = True
    write_feature_tables: bool = True
    overwrite_feature_tables_default: bool = False

@dataclass
class Phase127CandidatePreparationConfig:
    enabled: bool = True
    method: str = "DETERMINISTIC_RULE_TEMPLATE"
    produce_model_predictions: bool = False
    train_models: bool = False
    fit_clustering_models: bool = False
    candidate_scores_are_metadata_only: bool = True
    ready_for_phase128_allowed: bool = True

@dataclass
class Phase127NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


from dataclasses import dataclass, field

@dataclass
class RegimeFeatureEngineeringConfig:
    enabled: bool = True
    current_phase: int = 127
    final_phase: int = 160
    require_phase126_regime_foundation: bool = True
    market_state_metrics_enabled: bool = True
    rolling_market_state_metrics_enabled: bool = True
    cross_sectional_market_state_metrics_enabled: bool = True
    regime_feature_table_enabled: bool = True
    unsupervised_candidate_preparation_enabled: bool = True
    candidate_readiness_gate_enabled: bool = True
    write_regime_feature_engineering_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase127_is_not_activation: bool = True
    warn_candidates_are_not_predictions: bool = True
    warn_candidates_are_not_trade_signals: bool = True

@dataclass
class Phase127RegimePolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_heavy_ml_dependencies: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase127MarketStateMetricsConfig:
    enabled: bool = True
    default_windows: list[int] = field(default_factory=lambda: [20, 60, 120])
    build_cross_sectional_metrics: bool = True
    preserve_warmup_nulls: bool = True
    write_feature_tables: bool = True
    overwrite_feature_tables_default: bool = False

@dataclass
class Phase127CandidatePreparationConfig:
    enabled: bool = True
    method: str = "DETERMINISTIC_RULE_TEMPLATE"
    produce_model_predictions: bool = False
    train_models: bool = False
    fit_clustering_models: bool = False
    candidate_scores_are_metadata_only: bool = True
    ready_for_phase128_allowed: bool = True

@dataclass
class Phase127NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False



@dataclass
class RegimeMonitoringConfig:
    enabled: bool = True
    current_phase: int = 133
    final_phase: int = 160
    require_phase132_context_validation: bool = True
    context_validation_artifact_loader_enabled: bool = True
    baseline_builder_enabled: bool = True
    snapshot_builder_enabled: bool = True
    drift_tracking_enabled: bool = True
    degradation_diagnostics_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_regime_monitoring_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase133_is_not_activation: bool = True
    warn_monitoring_is_not_live_daemon: bool = True
    warn_drift_is_not_trade_signal: bool = True

@dataclass
class Phase133MonitoringPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase133DriftTrackingConfig:
    enabled: bool = True
    baseline_version: str = "phase133.v1"
    warning_threshold_default: float = 10.0
    blocking_threshold_default: float = 25.0
    require_baseline_hash: bool = True
    require_snapshot_hash: bool = True
    ready_for_phase134_allowed: bool = True

@dataclass
class Phase133DegradationDiagnosticsConfig:
    enabled: bool = True
    allowed_recommended_action_types: List[str] = field(default_factory=lambda: ["research_review", "data_quality_review", "documentation_review", "monitor_context", "baseline_refresh_review"])
    block_execution_action_types: bool = True

@dataclass
class Phase133NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass

@dataclass
class RegimeFinalClosureConfig:
    enabled: bool = True
    current_phase: int = 135
    final_phase: int = 160
    require_phase134_research_freeze: bool = True
    research_freeze_ingestion_enabled: bool = True
    artifact_chain_validation_enabled: bool = True
    final_closure_validation_enabled: bool = True
    freeze_seal_enabled: bool = True
    final_safety_audit_enabled: bool = True
    ml_input_contract_enabled: bool = True
    ml_kickoff_gate_enabled: bool = True
    write_final_closure_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase135_is_not_activation: bool = True
    warn_freeze_seal_is_not_deployment: bool = True
    warn_ml_kickoff_does_not_train_models: bool = True

@dataclass
class Phase135ClosurePolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase135ArtifactChainConfig:
    enabled: bool = True
    require_phase126_foundation: bool = True
    require_phase127_feature_engineering: bool = True
    require_phase128_labeling: bool = True
    require_phase129_transition_analytics: bool = True
    require_phase130_market_behavior: bool = True
    require_phase131_alignment: bool = True
    require_phase132_context_validation: bool = True
    require_phase133_monitoring: bool = True
    require_phase134_research_freeze: bool = True
    require_hashes: bool = True
    require_read_only_references: bool = True

@dataclass
class Phase135FreezeSealConfig:
    enabled: bool = True
    seal_version: str = "phase135.v1"
    sealed_phase_start: int = 126
    sealed_phase_end: int = 135
    next_phase: int = 136
    require_final_safety_audit_pass: bool = True
    require_artifact_chain_valid: bool = True

@dataclass
class Phase135MLKickoffConfig:
    enabled: bool = True
    ready_for_phase136_allowed: bool = True
    build_input_contract: bool = True
    training_started: bool = False
    prediction_started: bool = False
    allow_training_in_phase135: bool = False
    allow_prediction_in_phase135: bool = False
    require_non_activation_boundary: bool = True

@dataclass
class Phase135NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass

@dataclass
class MLDatasetAssemblyConfig:
    enabled: bool = True
    current_phase: int = 137
    final_phase: int = 160
    require_phase136_ml_foundation: bool = True
    foundation_ingestion_enabled: bool = True
    source_resolution_enabled: bool = True
    feature_matrix_assembly_enabled: bool = True
    target_matrix_assembly_enabled: bool = True
    label_matrix_assembly_enabled: bool = True
    dataset_manifest_enabled: bool = True
    split_policy_enabled: bool = True
    split_assignment_enabled: bool = True
    leakage_audit_enabled: bool = True
    dataset_quality_enabled: bool = True
    split_quality_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_dataset_assembly_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase137_does_not_train_models: bool = True
    warn_phase137_does_not_predict: bool = True
    warn_dataset_outputs_are_not_trade_signals: bool = True

@dataclass
class Phase137DatasetPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase137SplitPolicyConfig:
    default_policy_kind: str = "SYMBOL_AWARE_TIME_SPLIT"
    train_ratio: float = 0.70
    validation_ratio: float = 0.15
    test_ratio: float = 0.15
    embargo_bars: int = 5
    purge_bars: int = 5
    time_ordered: bool = True
    symbol_aware: bool = True
    random_shuffle_allowed: bool = False
    leakage_safe_required: bool = True

@dataclass
class Phase137LeakageAuditConfig:
    enabled: bool = True
    require_future_data_leakage_check: bool = True
    require_target_leakage_check: bool = True
    require_label_overlap_check: bool = True
    require_timestamp_alignment_check: bool = True
    require_train_validation_test_overlap_check: bool = True
    require_embargo_purge_check: bool = True
    require_forward_window_overlap_check: bool = True
    require_forbidden_output_field_check: bool = True
    block_on_leakage_fail: bool = True

@dataclass
class Phase137NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class MLGovernanceClosureConfig:
    enabled: bool = True
    current_phase: int = 145
    final_phase: int = 160
    require_phase144_drift_monitoring: bool = True
    drift_monitoring_ingestion_enabled: bool = True
    drift_artifact_loader_enabled: bool = True
    explainability_input_resolver_enabled: bool = True
    feature_attribution_proxy_enabled: bool = True
    factor_contribution_enabled: bool = True
    model_behavior_explanation_enabled: bool = True
    regime_aware_explanation_enabled: bool = True
    calibration_aware_explanation_enabled: bool = True
    ensemble_explanation_enabled: bool = True
    explainability_report_enabled: bool = True
    artifact_lineage_enabled: bool = True
    ml_governance_closure_enabled: bool = True
    advanced_ml_final_audit_enabled: bool = True
    non_activation_boundary_enabled: bool = True
    final_model_card_closure_enabled: bool = True
    acceptance_gate_enabled: bool = True
    write_ml_governance_closure_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_explainability_is_metadata_only: bool = True
    warn_feature_attribution_is_not_trade_signal: bool = True
    warn_governance_closure_is_not_deployment: bool = True
    warn_phase145_does_not_run_backtests: bool = True

@dataclass
class Phase145MLClosurePolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_ml_research_only: bool = True
    explainability_metadata_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_live_monitoring: bool = False
    allow_alert_sender: bool = False
    allow_live_inference: bool = False
    allow_online_inference: bool = False
    allow_scheduler: bool = False
    allow_background_daemon: bool = False
    allow_threshold_optimization: bool = False
    allow_portfolio_optimization: bool = False
    allow_backtest_execution: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_shap_lime_dependencies: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase145ExplainabilityConfig:
    enabled: bool = True
    max_feature_attributions: int = 50
    max_factor_summaries: int = 30
    use_feature_summary_proxy: bool = True
    use_factor_summary_proxy: bool = True
    use_correlation_proxy: bool = True
    use_stability_proxy: bool = True
    use_regime_aware_proxy: bool = True
    use_calibration_aware_proxy: bool = True
    use_ensemble_contribution_proxy: bool = True
    shap_enabled: bool = False
    lime_enabled: bool = False
    heavy_dependency_enabled: bool = False

@dataclass
class Phase145FinalAuditConfig:
    enabled: bool = True
    required_phase_start: int = 136
    required_phase_end: int = 145
    require_all_phase_reviews: bool = True
    require_all_readiness_gates_passed: bool = True
    require_non_activation_boundary: bool = True
    require_final_model_card_closure: bool = True
    require_phase146_handoff: bool = True

@dataclass
class Phase145NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class Config:
    realistic_backtest_run: RealisticBacktestRunConfig = field(default_factory=RealisticBacktestRunConfig)
    ml_dataset_assembly: MLDatasetAssemblyConfig = field(default_factory=MLDatasetAssemblyConfig)
    phase137_dataset_policy: Phase137DatasetPolicyConfig = field(default_factory=Phase137DatasetPolicyConfig)
    phase137_split_policy: Phase137SplitPolicyConfig = field(default_factory=Phase137SplitPolicyConfig)
    phase137_leakage_audit: Phase137LeakageAuditConfig = field(default_factory=Phase137LeakageAuditConfig)
    phase137_notifications: Phase137NotificationsConfig = field(default_factory=Phase137NotificationsConfig)
    regime_final_closure: RegimeFinalClosureConfig = field(default_factory=RegimeFinalClosureConfig)
    phase135_closure_policy: Phase135ClosurePolicyConfig = field(default_factory=Phase135ClosurePolicyConfig)
    phase135_artifact_chain: Phase135ArtifactChainConfig = field(default_factory=Phase135ArtifactChainConfig)
    phase135_freeze_seal: Phase135FreezeSealConfig = field(default_factory=Phase135FreezeSealConfig)
    phase135_ml_kickoff: Phase135MLKickoffConfig = field(default_factory=Phase135MLKickoffConfig)
    phase135_notifications: Phase135NotificationsConfig = field(default_factory=Phase135NotificationsConfig)
    advanced_features: AdvancedFeaturesConfig = field(default_factory=AdvancedFeaturesConfig)
    feature_factor_final_closure: FeatureFactorFinalClosureConfig = field(default_factory=FeatureFactorFinalClosureConfig)
    phase125_final_closure_policy: Phase125FinalClosurePolicyConfig = field(default_factory=Phase125FinalClosurePolicyConfig)
    phase125_closure_requirements: Phase125ClosureRequirementsConfig = field(default_factory=Phase125ClosureRequirementsConfig)
    phase125_notifications: Phase125NotificationsConfig = field(default_factory=Phase125NotificationsConfig)
    regime_feature_engineering: RegimeFeatureEngineeringConfig = field(default_factory=RegimeFeatureEngineeringConfig)
    phase127_regime_policy: Phase127RegimePolicyConfig = field(default_factory=Phase127RegimePolicyConfig)
    phase127_market_state_metrics: Phase127MarketStateMetricsConfig = field(default_factory=Phase127MarketStateMetricsConfig)
    phase127_candidate_preparation: Phase127CandidatePreparationConfig = field(default_factory=Phase127CandidatePreparationConfig)
    phase127_notifications: Phase127NotificationsConfig = field(default_factory=Phase127NotificationsConfig)
    regime_feature_engineering: RegimeFeatureEngineeringConfig = field(default_factory=RegimeFeatureEngineeringConfig)
    phase127_regime_policy: Phase127RegimePolicyConfig = field(default_factory=Phase127RegimePolicyConfig)
    phase127_market_state_metrics: Phase127MarketStateMetricsConfig = field(default_factory=Phase127MarketStateMetricsConfig)
    phase127_candidate_preparation: Phase127CandidatePreparationConfig = field(default_factory=Phase127CandidatePreparationConfig)
    phase127_notifications: Phase127NotificationsConfig = field(default_factory=Phase127NotificationsConfig)
    calibration_diagnostics: 'CalibrationDiagnosticsConfig' = field(default_factory=dict)




    feature_factor_integration_freeze: FeatureFactorIntegrationFreezeConfig = field(default_factory=FeatureFactorIntegrationFreezeConfig)
    phase124_freeze_policy: Phase124FreezePolicyConfig = field(default_factory=Phase124FreezePolicyConfig)
    phase124_acceptance_policy: Phase124AcceptancePolicyConfig = field(default_factory=Phase124AcceptancePolicyConfig)
    phase124_notifications: Phase124NotificationsConfig = field(default_factory=Phase124NotificationsConfig)

    provider_freeze: ProviderFreezeConfig = field(default_factory=ProviderFreezeConfig)
    phase114_freeze_policy: Phase114FreezePolicyConfig = field(default_factory=Phase114FreezePolicyConfig)
    phase114_rehearsal: Phase114RehearsalConfig = field(default_factory=Phase114RehearsalConfig)
    phase114_output_contract: Phase114OutputContractConfig = field(default_factory=Phase114OutputContractConfig)
    phase114_notifications: Phase114NotificationsConfig = field(default_factory=Phase114NotificationsConfig)


    pre_paper_handoff_freeze_gate: PrePaperHandoffFreezeGateConfig = field(default_factory=PrePaperHandoffFreezeGateConfig)
    sandbox_runtime_admission_blocker_replay: SandboxRuntimeAdmissionBlockerReplayConfig = field(default_factory=SandboxRuntimeAdmissionBlockerReplayConfig)
    simulator_evidence_freeze: SimulatorEvidenceFreezeConfig = field(default_factory=SimulatorEvidenceFreezeConfig)
    final_pre_paper_handoff_freeze_gate: FinalPrePaperHandoffFreezeGateConfig = field(default_factory=FinalPrePaperHandoffFreezeGateConfig)
    handoff_freeze_safety: HandoffFreezeSafetyConfig = field(default_factory=HandoffFreezeSafetyConfig)
    handoff_freeze_notifications: HandoffFreezeNotificationsConfig = field(default_factory=HandoffFreezeNotificationsConfig)

    paper_boundary_certificate: PaperBoundaryCertificateConfig = field(default_factory=PaperBoundaryCertificateConfig)
    paper_admission_blocker_replay: PaperAdmissionBlockerReplayConfig = field(default_factory=PaperAdmissionBlockerReplayConfig)
    no_order_evidence_freeze: NoOrderEvidenceFreezeConfig = field(default_factory=NoOrderEvidenceFreezeConfig)
    paper_sandbox_boundary_certificate: PaperSandboxBoundaryCertificateConfig = field(default_factory=PaperSandboxBoundaryCertificateConfig)
    paper_boundary_safety: PaperBoundarySafetyConfig = field(default_factory=PaperBoundarySafetyConfig)
    paper_boundary_notifications: PaperBoundaryNotificationsConfig = field(default_factory=PaperBoundaryNotificationsConfig)

    paper_no_write_admission: PaperNoWriteAdmissionConfig = field(default_factory=PaperNoWriteAdmissionConfig)
    no_write_paper_admission_contract: NoWritePaperAdmissionContractConfig = field(default_factory=NoWritePaperAdmissionContractConfig)
    activation_firewall_replay: ActivationFirewallReplayConfig = field(default_factory=ActivationFirewallReplayConfig)
    paper_mode_simulation_preflight: PaperModeSimulationPreflightConfig = field(default_factory=PaperModeSimulationPreflightConfig)
    no_write_admission_safety: NoWriteAdmissionSafetyConfig = field(default_factory=NoWriteAdmissionSafetyConfig)
    paper_no_write_admission_notifications: PaperNoWriteAdmissionNotificationsConfig = field(default_factory=PaperNoWriteAdmissionNotificationsConfig)

    data_provider_abstraction: DataProviderAbstractionConfig = field(default_factory=DataProviderAbstractionConfig)
    phase106_provider_safety: Phase106ProviderSafetyConfig = field(default_factory=Phase106ProviderSafetyConfig)
    phase106_provider_registry: Phase106ProviderRegistryConfig = field(default_factory=Phase106ProviderRegistryConfig)
    phase106_notifications: Phase106NotificationsConfig = field(default_factory=Phase106NotificationsConfig)

    phase116_notifications: Phase116NotificationsConfig = field(default_factory=Phase116NotificationsConfig)
    phase116_feature_scope: Phase116FeatureScopeConfig = field(default_factory=Phase116FeatureScopeConfig)
    phase116_feature_policy: Phase116FeaturePolicyConfig = field(default_factory=Phase116FeaturePolicyConfig)
    feature_engine_foundation: FeatureEngineFoundationConfig = field(default_factory=FeatureEngineFoundationConfig)
    def validate(self) -> None:
        pass


from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class CoreIndicatorsConfig:
    enabled: bool = True
    current_phase: int = 117
    final_phase: int = 160
    require_phase116_feature_foundation: bool = True
    local_pandas_indicators_enabled: bool = True
    rolling_window_engine_enabled: bool = True
    feature_table_builder_enabled: bool = True
    write_core_indicator_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase117_is_not_activation: bool = True
    warn_indicators_are_not_trade_signals: bool = True

@dataclass
class Phase117IndicatorPolicyConfig:
    metadata_only: bool = False
    compute_values_local_only: bool = True
    research_data_only: bool = True
    dry_run_only_default: bool = False
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase117FeatureTableConfig:
    preserve_base_ohlcv_columns: bool = True
    preserve_warmup_nulls: bool = True
    default_null_policy: str = "PRESERVE_WARMUP_NULLS"
    block_forbidden_columns: bool = True
    allow_macd_signal_line_column: bool = True
    write_feature_tables: bool = True

@dataclass
class Phase117NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class Phase119EnrichmentPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase119FeatureInteractionsConfig:
    enabled: bool = True
    allow_multiplicative: bool = True
    allow_ratio: bool = True
    allow_difference: bool = True
    allow_event_conditioned: bool = True
    allow_quality_weighted: bool = True
    allow_calendar_conditioned: bool = True
    block_signal_generation: bool = True
    block_order_decision: bool = True
    block_portfolio_weights: bool = True

@dataclass
class Phase119FeatureTableConfig:
    preserve_advanced_feature_columns: bool = True
    preserve_warmup_nulls: bool = True
    block_forbidden_columns: bool = True
    allow_macd_signal_line_column: bool = True
    write_feature_tables: bool = True
    overwrite_feature_tables_default: bool = False

@dataclass
class Phase119NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class FeatureEnrichmentConfig:
    enabled: bool = True
    current_phase: int = 119
    final_phase: int = 160
    require_phase118_advanced_features: bool = True
    event_aware_features_enabled: bool = True
    quality_aware_features_enabled: bool = True
    calendar_aware_features_enabled: bool = True
    feature_freshness_enabled: bool = True
    feature_confidence_enabled: bool = True
    feature_interactions_enabled: bool = True
    enriched_feature_table_enabled: bool = True
    write_feature_enrichment_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase119_is_not_activation: bool = True
    warn_enriched_features_are_not_trade_signals: bool = True

@dataclass
class FactorCompositionConfig:
    enabled: bool = True
    current_phase: int = 120
    final_phase: int = 160
    require_phase119_feature_enrichment: bool = True
    feature_grouping_enabled: bool = True
    factor_candidate_registry_enabled: bool = True
    feature_selection_metadata_enabled: bool = True
    factor_readiness_gate_enabled: bool = True
    write_factor_composition_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase120_is_not_activation: bool = True
    warn_factors_are_not_trade_signals: bool = True

@dataclass
class Phase120FactorPolicyConfig:
    compute_metadata_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase120FeatureSelectionConfig:
    enabled: bool = True
    min_coverage_ratio: float = 0.70
    max_missingness_ratio: float = 0.30
    min_stability_score: float = 40.0
    max_redundancy_score: float = 80.0
    research_selection_only: bool = True
    block_signal_generation: bool = True
    block_order_decision: bool = True
    block_portfolio_weights: bool = True

@dataclass
class Phase120FactorReadinessConfig:
    enabled: bool = True
    require_feature_groups: bool = True
    require_factor_candidates: bool = True
    require_selection_metadata: bool = True
    require_safety_pass: bool = True
    ready_for_phase121_allowed: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase120NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class FactorScoringConfig:
    enabled: bool = True
    current_phase: int = 121
    final_phase: int = 160
    require_phase120_factor_composition: bool = True
    factor_scoring_enabled: bool = True
    factor_normalization_enabled: bool = True
    factor_diagnostics_enabled: bool = True
    factor_table_builder_enabled: bool = True
    write_factor_scoring_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase121_is_not_activation: bool = True
    warn_factor_scores_are_not_trade_signals: bool = True

@dataclass
class Phase121FactorPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase121FactorNormalizationConfig:
    enabled: bool = True
    default_method: str = "Z_SCORE"
    winsorization_enabled: bool = True
    lower_pct: float = 0.01
    upper_pct: float = 0.99
    cross_sectional_ranks_enabled: bool = True
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False

@dataclass
class Phase121FactorTableConfig:
    preserve_enriched_feature_columns: bool = True
    preserve_warmup_nulls: bool = True
    block_forbidden_columns: bool = True
    allow_macd_signal_line_column: bool = True
    write_factor_tables: bool = True
    overwrite_factor_tables_default: bool = False

@dataclass
class Phase121NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class Phase128LabelingPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase128HeuristicLabelingConfig:
    enabled: bool = True
    minimum_score_threshold: float = 40.0
    minimum_score_gap: float = 5.0
    fallback_label: str = "unknown_regime"
    mixed_label: str = "mixed_regime"
    unknown_label: str = "unknown_regime"
    conflict_policy: str = "fallback_to_mixed_or_unknown"
    write_labeled_tables: bool = True
    overwrite_labeled_tables_default: bool = False

@dataclass
class Phase128RollingWindowsConfig:
    enabled: bool = True
    windows: list[int] = field(default_factory=lambda: [20, 60, 120])
    min_periods_ratio: float = 0.5
    preserve_warmup_nulls: bool = True
    build_stability_profiles: bool = True

@dataclass
class Phase128CandidateValidationConfig:
    enabled: bool = True
    require_candidate_definitions: bool = True
    require_candidate_scores: bool = True
    require_taxonomy_alignment: bool = True
    require_no_model_training: bool = True
    require_no_model_prediction: bool = True
    ready_for_phase129_allowed: bool = True

@dataclass
class Phase128NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class RegimeLabelingConfig:
    enabled: bool = True
    current_phase: int = 128
    final_phase: int = 160
    require_phase127_regime_feature_engineering: bool = True
    heuristic_labeling_enabled: bool = True
    rolling_regime_windows_enabled: bool = True
    candidate_validation_enabled: bool = True
    label_stability_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_regime_labeling_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase128_is_not_activation: bool = True
    warn_labels_are_not_trade_signals: bool = True
    warn_labels_are_not_model_predictions: bool = True
    policy: Phase128LabelingPolicyConfig = field(default_factory=Phase128LabelingPolicyConfig)
    heuristic_labeling: Phase128HeuristicLabelingConfig = field(default_factory=Phase128HeuristicLabelingConfig)
    rolling_windows: Phase128RollingWindowsConfig = field(default_factory=Phase128RollingWindowsConfig)
    candidate_validation: Phase128CandidateValidationConfig = field(default_factory=Phase128CandidateValidationConfig)
    notifications: Phase128NotificationsConfig = field(default_factory=Phase128NotificationsConfig)


@dataclass
class Phase129TransitionPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase129TransitionMetricsConfig:
    enabled: bool = True
    default_rolling_windows: list[int] = field(default_factory=lambda: [20, 60, 120])
    compute_cross_symbol_transitions: bool = True
    compute_transition_entropy_proxy: bool = True
    compute_transition_concentration: bool = True

@dataclass
class Phase129NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class RegimeTransitionAnalyticsConfig:
    enabled: bool = True
    current_phase: int = 129
    final_phase: int = 160
    require_phase128_regime_labeling: bool = True
    transition_matrix_enabled: bool = True
    persistence_analytics_enabled: bool = True
    duration_analytics_enabled: bool = True
    churn_diagnostics_enabled: bool = True
    stability_diagnostics_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_regime_transition_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase129_is_not_activation: bool = True
    warn_transition_matrix_is_not_trade_signal: bool = True
    policy: Phase129TransitionPolicyConfig = field(default_factory=Phase129TransitionPolicyConfig)
    metrics: Phase129TransitionMetricsConfig = field(default_factory=Phase129TransitionMetricsConfig)
    notifications: Phase129NotificationsConfig = field(default_factory=Phase129NotificationsConfig)


@dataclass
class Phase130BehaviorPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase130ReportPolicyConfig:
    formats: list[str] = field(default_factory=lambda: ["MARKDOWN", "JSON", "TEXT"])
    require_qa_pass: bool = True
    block_investment_advice_language: bool = True
    block_trade_signal_language: bool = True
    block_order_decision_language: bool = True
    block_portfolio_allocation_language: bool = True
    block_guarantee_language: bool = True
    block_broker_execution_language: bool = True
    block_deployment_language: bool = True
    overwrite_reports_default: bool = False

@dataclass
class Phase130NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class MarketBehaviorReportingConfig:
    enabled: bool = True
    current_phase: int = 130
    final_phase: int = 160
    require_phase129_regime_transition_analytics: bool = True
    behavior_profiles_enabled: bool = True
    regime_behavior_summaries_enabled: bool = True
    diagnostics_interpretation_enabled: bool = True
    report_document_enabled: bool = True
    report_qa_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_market_behavior_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase130_is_not_activation: bool = True
    warn_behavior_profiles_are_not_trade_signals: bool = True
    policy: Phase130BehaviorPolicyConfig = field(default_factory=Phase130BehaviorPolicyConfig)
    report_policy: Phase130ReportPolicyConfig = field(default_factory=Phase130ReportPolicyConfig)
    notifications: Phase130NotificationsConfig = field(default_factory=Phase130NotificationsConfig)


@dataclass
class Phase136MLPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase136DatasetContractConfig:
    enabled: bool = True
    contract_version: str = "phase136.v1"
    split_design_deferred_to_phase137: bool = True
    dataset_assembly_deferred_to_phase137: bool = True
    model_training_deferred: bool = True
    model_prediction_deferred: bool = True
    require_source_registry: bool = True
    require_feature_contracts: bool = True
    require_target_contracts: bool = True
    require_label_contracts: bool = True
    require_forbidden_output_fields: bool = True
    require_contract_hash: bool = True

@dataclass
class Phase136LeakageGuardConfig:
    enabled: bool = True
    phase137_audit_required: bool = True
    require_future_data_leakage_guard: bool = True
    require_target_leakage_guard: bool = True
    require_timestamp_alignment_guard: bool = True
    require_train_test_overlap_guard: bool = True
    require_scaler_fit_leakage_guard: bool = True
    require_feature_selection_leakage_guard: bool = True

@dataclass
class Phase136NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class MLFoundationConfig:
    enabled: bool = True
    current_phase: int = 136
    final_phase: int = 160
    require_phase135_final_closure: bool = True
    final_closure_ingestion_enabled: bool = True
    source_registry_enabled: bool = True
    feature_contract_enabled: bool = True
    target_contract_enabled: bool = True
    label_contract_enabled: bool = True
    dataset_contract_enabled: bool = True
    leakage_guard_enabled: bool = True
    non_activation_boundary_enabled: bool = True
    governance_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_ml_foundation_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase136_does_not_train_models: bool = True
    warn_phase136_does_not_predict: bool = True
    warn_ml_outputs_are_not_trade_signals: bool = True



ml_foundation: MLFoundationConfig = field(default_factory=MLFoundationConfig)
phase136_ml_policy: Phase136MLPolicyConfig = field(default_factory=Phase136MLPolicyConfig)
phase136_dataset_contract: Phase136DatasetContractConfig = field(default_factory=Phase136DatasetContractConfig)
phase136_leakage_guard: Phase136LeakageGuardConfig = field(default_factory=Phase136LeakageGuardConfig)
phase136_notifications: Phase136NotificationsConfig = field(default_factory=Phase136NotificationsConfig)


@dataclass
class Phase147BacktestRunPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    local_fixture_only_default: bool = True
    allow_offline_deterministic_backtest_run: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_real_order_creation: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_live_trading: bool = False
    allow_paper_trading: bool = False
    allow_strategy_activation: bool = False
    allow_portfolio_optimization: bool = False
    allow_walk_forward: bool = False
    allow_stress_test: bool = False
    allow_monte_carlo: bool = False
    allow_benchmark_comparison: bool = False
    allow_scheduler: bool = False
    allow_background_daemon: bool = False
    produce_live_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False

@dataclass
class Phase147RunDefaultsConfig:
    initial_cash: float = 100000.0
    currency: str = "USD"
    deterministic_seed: int = 147
    exposure_side: str = "LONG_ONLY_RESEARCH"
    max_single_symbol_exposure_fraction: float = 1.0
    allow_fractional_shares: bool = False
    allow_short_exposure: bool = False
    allow_leverage: bool = False
    default_fill_policy: str = "NEXT_BAR_OPEN"
    require_deterministic_hashes: bool = True

@dataclass
class Phase147NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class RealisticBacktestRunConfig:
    enabled: bool = True
    current_phase: int = 147
    final_phase: int = 160
    require_phase146_backtest_foundation: bool = True
    backtest_foundation_ingestion_enabled: bool = True
    artifact_loader_enabled: bool = True
    input_resolver_enabled: bool = True
    run_config_enabled: bool = True
    research_decision_stream_enabled: bool = True
    simulation_clock_enabled: bool = True
    price_event_stream_enabled: bool = True
    simulated_execution_enabled: bool = True
    cost_application_enabled: bool = True
    liquidity_partial_fill_enabled: bool = True
    exposure_timeline_enabled: bool = True
    equity_curve_enabled: bool = True
    drawdown_curve_enabled: bool = True
    ledger_enabled: bool = True
    basic_performance_enabled: bool = True
    safety_boundary_enabled: bool = True
    validation_gate_enabled: bool = True
    write_backtest_run_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_simulated_fills_are_not_orders: bool = True
    warn_backtest_run_is_offline_only: bool = True
    policy: Phase147BacktestRunPolicyConfig = field(default_factory=Phase147BacktestRunPolicyConfig)
    run_defaults: Phase147RunDefaultsConfig = field(default_factory=Phase147RunDefaultsConfig)
    notifications: Phase147NotificationsConfig = field(default_factory=Phase147NotificationsConfig)

AppConfig = Config

@dataclass
class BaselineMLScaffoldingConfig:
    enabled: bool = True
    current_phase: int = 138
    final_phase: int = 160
    require_phase137_dataset_assembly: bool = True
    dataset_assembly_ingestion_enabled: bool = True
    dataset_artifact_loader_enabled: bool = True
    experiment_specs_enabled: bool = True
    model_family_registry_enabled: bool = True
    metric_specs_enabled: bool = True
    evaluation_harness_contract_enabled: bool = True
    prediction_output_boundary_enabled: bool = True
    model_card_draft_enabled: bool = True
    experiment_registry_enabled: bool = True
    non_activation_boundary_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_baseline_scaffolding_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase138_does_not_train_models: bool = True
    warn_phase138_does_not_predict: bool = True
    warn_model_cards_are_drafts: bool = True

@dataclass
class Phase138ScaffoldingPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase138EvaluationHarnessConfig:
    enabled: bool = True
    harness_version: str = "phase138.v1"
    training_allowed_in_phase138: bool = False
    prediction_allowed_in_phase138: bool = False
    live_evaluation_allowed: bool = False
    broker_evaluation_allowed: bool = False
    paper_mutation_allowed: bool = False
    require_prediction_output_boundary: bool = True
    require_metric_specs: bool = True
    require_model_card_draft: bool = True

@dataclass
class Phase138ModelCardConfig:
    enabled: bool = True
    draft_only: bool = True
    require_training_not_started_notice: bool = True
    require_prediction_not_started_notice: bool = True
    require_non_activation_notice: bool = True
    require_not_investment_advice_notice: bool = True
    block_trade_advice_language: bool = True

@dataclass
class Phase138NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class BaselineTrainingConfig:
    enabled: bool = False
    current_phase: int = 139
    final_phase: int = 160
    require_phase138_baseline_scaffolding: bool = True
    scaffolding_ingestion_enabled: bool = True
    scaffolding_artifact_loader_enabled: bool = True
    dataset_loader_enabled: bool = True
    training_job_builder_enabled: bool = True
    baseline_trainers_enabled: bool = True
    offline_prediction_enabled: bool = True
    offline_evaluation_enabled: bool = True
    evaluation_report_enabled: bool = True
    non_activation_model_registry_enabled: bool = True
    model_card_update_enabled: bool = True
    training_boundary_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_baseline_training_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase139_training_is_offline_only: bool = True
    warn_phase139_predictions_are_offline_evaluation_only: bool = True
    warn_model_registry_is_not_deployment_registry: bool = True

@dataclass
class Phase139TrainingPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_ml_research_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_local_offline_model_training: bool = True
    allow_offline_evaluation_prediction: bool = True
    allow_live_inference: bool = False
    allow_online_inference: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase139BaselineModelsConfig:
    enabled: bool = False
    train_dummy_classification: bool = False
    train_dummy_regression: bool = False
    train_persistence_baseline: bool = False
    train_moving_average_baseline: bool = False
    train_lightweight_linear_baseline: bool = False
    require_deterministic_artifacts: bool = True
    model_registry_version: str = "phase139.v1"

@dataclass
class Phase139OfflineEvaluationConfig:
    enabled: bool = False
    evaluate_train_split: bool = True
    evaluate_validation_split: bool = True
    evaluate_test_split: bool = True
    allow_pnl_metrics: bool = False
    allow_trading_metrics: bool = False
    allow_backtest_metrics: bool = False
    require_non_trading_metrics: bool = True

@dataclass
class Phase139NotificationsConfig:
    enabled: bool = False
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class Phase141CalibrationPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_ml_research_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_live_inference: bool = False
    allow_online_inference: bool = False
    allow_calibration_fitting: bool = False
    allow_calibrated_model_creation: bool = False
    allow_threshold_optimization: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase141ReliabilityConfig:
    enabled: bool = True
    default_bin_count: int = 10
    default_bin_strategy: str = "FIXED_10_BIN"
    require_ece: bool = True
    require_mce: bool = True
    require_brier_score: bool = True
    require_brier_decomposition: bool = True
    require_score_distribution: bool = True
    require_class_balance: bool = True
    probability_missing_allowed_with_warning: bool = True

@dataclass
class Phase141PostTrainingValidationConfig:
    enabled: bool = True
    require_model_registry_consistency: bool = True
    require_candidate_shortlist_consistency: bool = True
    require_offline_predictions_available: bool = True
    require_no_forbidden_output_fields: bool = True
    require_no_live_inference: bool = True
    require_no_calibration_fitting: bool = True
    require_no_deployment: bool = True

@dataclass
class Phase141NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class CalibrationDiagnosticsConfig:
    enabled: bool = True
    current_phase: int = 141
    final_phase: int = 160
    require_phase140_model_comparison: bool = True
    model_comparison_ingestion_enabled: bool = True
    comparison_artifact_loader_enabled: bool = True
    calibration_input_resolver_enabled: bool = True
    reliability_binning_enabled: bool = True
    calibration_metric_enabled: bool = True
    brier_decomposition_enabled: bool = True
    score_distribution_enabled: bool = True
    class_balance_enabled: bool = True
    post_training_validation_enabled: bool = True
    calibration_governance_enabled: bool = True
    model_card_update_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_calibration_diagnostics_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_diagnostics_are_not_trade_signals: bool = True
    warn_phase141_does_not_fit_calibrators: bool = True
    warn_phase141_does_not_create_calibrated_models: bool = True
    phase141_calibration_policy: Phase141CalibrationPolicyConfig = field(default_factory=Phase141CalibrationPolicyConfig)
    phase141_reliability: Phase141ReliabilityConfig = field(default_factory=Phase141ReliabilityConfig)
    phase141_post_training_validation: Phase141PostTrainingValidationConfig = field(default_factory=Phase141PostTrainingValidationConfig)
    phase141_notifications: Phase141NotificationsConfig = field(default_factory=Phase141NotificationsConfig)


@dataclass
class Phase142EnsemblePolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_ml_research_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_live_inference: bool = False
    allow_online_inference: bool = False
    allow_ensemble_fitting: bool = False
    allow_final_ensemble_prediction: bool = False
    allow_calibration_fitting: bool = False
    allow_calibrated_model_creation: bool = False
    allow_threshold_optimization: bool = False
    allow_portfolio_optimization: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase142CandidateGroupingConfig:
    enabled: bool = True
    max_group_size: int = 3
    min_group_size: int = 2
    build_top_ranked_group: bool = True
    build_calibration_aware_group: bool = True
    build_diversity_placeholder_group: bool = True
    require_research_only_candidates: bool = True
    require_no_live_eligibility: bool = True

@dataclass
class Phase142BlendPolicyConfig:
    enabled: bool = True
    coefficient_sum_required: float = 1.0
    coefficient_non_negative_required: bool = True
    coefficient_cap: float = 0.8
    forbid_portfolio_weight_language: bool = True
    forbid_allocation_language: bool = True
    forbid_target_weight_language: bool = True
    fitting_performed: bool = False
    final_ensemble_prediction_created: bool = False

@dataclass
class Phase142NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class EnsembleScaffoldingConfig:
    enabled: bool = True
    current_phase: int = 142
    final_phase: int = 160
    require_phase141_calibration_diagnostics: bool = True
    calibration_diagnostics_ingestion_enabled: bool = True
    calibration_artifact_loader_enabled: bool = True
    candidate_resolver_enabled: bool = True
    family_specs_enabled: bool = True
    candidate_grouping_enabled: bool = True
    blend_policy_enabled: bool = True
    blend_coefficient_planning_enabled: bool = True
    prediction_correlation_enabled: bool = True
    diversity_diagnostics_enabled: bool = True
    complementarity_profiles_enabled: bool = True
    calibration_aware_eligibility_enabled: bool = True
    ensemble_preparation_report_enabled: bool = True
    ensemble_governance_enabled: bool = True
    non_activation_boundary_enabled: bool = True
    model_card_update_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_ensemble_scaffolding_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_blend_coefficients_are_not_portfolio_weights: bool = True
    warn_phase142_does_not_fit_ensembles: bool = True
    warn_phase142_does_not_create_final_ensemble_predictions: bool = True
    phase142_ensemble_policy: Phase142EnsemblePolicyConfig = field(default_factory=Phase142EnsemblePolicyConfig)
    phase142_candidate_grouping: Phase142CandidateGroupingConfig = field(default_factory=Phase142CandidateGroupingConfig)
    phase142_blend_policy: Phase142BlendPolicyConfig = field(default_factory=Phase142BlendPolicyConfig)
    phase142_notifications: Phase142NotificationsConfig = field(default_factory=Phase142NotificationsConfig)

@dataclass
class EnsemblePrototypeEvaluationConfig:
    enabled: bool = True
    current_phase: int = 143
    final_phase: int = 160
    require_phase142_ensemble_scaffolding: bool = True
    ensemble_scaffolding_ingestion_enabled: bool = True
    scaffolding_artifact_loader_enabled: bool = True
    ensemble_input_resolver_enabled: bool = True
    prototype_spec_builder_enabled: bool = True
    offline_ensemble_prediction_enabled: bool = True
    blend_diagnostics_enabled: bool = True
    candidate_agreement_enabled: bool = True
    ensemble_candidate_comparison_enabled: bool = True
    offline_ensemble_evaluation_enabled: bool = True
    evaluation_report_enabled: bool = True
    non_activation_ensemble_registry_enabled: bool = True
    model_card_update_enabled: bool = True
    prototype_boundary_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_ensemble_prototype_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_ensemble_predictions_are_offline_only: bool = True
    warn_blend_coefficients_are_not_portfolio_weights: bool = True
    warn_ensemble_registry_is_not_deployment_registry: bool = True

@dataclass
class Phase143EnsemblePolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_ml_research_only: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_live_inference: bool = False
    allow_online_inference: bool = False
    allow_offline_ensemble_prediction: bool = True
    allow_threshold_optimization: bool = False
    allow_portfolio_optimization: bool = False
    allow_heavy_ml_dependencies: bool = False
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase143EnsembleEvaluationConfig:
    enabled: bool = True
    evaluate_train_split: bool = True
    evaluate_validation_split: bool = True
    evaluate_test_split: bool = True
    allow_pnl_metrics: bool = False
    allow_trading_metrics: bool = False
    allow_backtest_metrics: bool = False
    require_non_trading_metrics: bool = True
    require_blend_diagnostics: bool = True
    require_candidate_agreement: bool = True
    registry_version: str = "phase143.v1"

@dataclass
class Phase143BlendDiagnosticsConfig:
    enabled: bool = True
    coefficient_sum_required: float = 1.0
    coefficient_non_negative_required: bool = True
    dominant_candidate_threshold: float = 0.80
    forbid_portfolio_weight_language: bool = True
    forbid_allocation_language: bool = True
    forbid_target_weight_language: bool = True

@dataclass
class Phase143NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class Phase144DriftPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_ml_research_only: bool = True
    metadata_only_monitoring: bool = True
    local_fixture_only_default: bool = True
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_order: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_live_monitoring: bool = False
    allow_alert_sender: bool = False
    allow_live_inference: bool = False
    allow_online_inference: bool = False
    allow_scheduler: bool = False
    allow_background_daemon: bool = False
    allow_threshold_optimization: bool = False
    allow_portfolio_optimization: bool = False
    allow_heavy_ml_dependencies: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False


@dataclass
class Phase144MonitoringWindowConfig:
    enabled: bool = True
    default_reference_splits: list[str] = field(default_factory=lambda: ["train", "validation"])
    default_monitoring_splits: list[str] = field(default_factory=lambda: ["test"])
    min_reference_rows: int = 10
    min_monitoring_rows: int = 5
    rolling_window_metadata_only: bool = True
    calendar_window_metadata_only: bool = True


@dataclass
class Phase144AlertMetadataConfig:
    enabled: bool = True
    notification_preview_only: bool = True
    alert_sender_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scheduler_enabled: bool = False
    daemon_started: bool = False


@dataclass
class Phase144NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False


@dataclass
class DriftMonitoringConfig:
    enabled: bool = True
    current_phase: int = 144
    final_phase: int = 160
    require_phase143_ensemble_prototype: bool = True
    ensemble_prototype_ingestion_enabled: bool = True
    ensemble_artifact_loader_enabled: bool = True
    drift_input_resolver_enabled: bool = True
    monitoring_window_policy_enabled: bool = True
    drift_baseline_specs_enabled: bool = True
    feature_drift_enabled: bool = True
    prediction_drift_enabled: bool = True
    score_distribution_drift_enabled: bool = True
    calibration_drift_enabled: bool = True
    residual_drift_enabled: bool = True
    label_distribution_drift_enabled: bool = True
    regime_drift_enabled: bool = True
    drift_metric_calculator_enabled: bool = True
    monitoring_snapshot_enabled: bool = True
    alert_rule_metadata_enabled: bool = True
    monitoring_metadata_package_enabled: bool = True
    post_ensemble_governance_enabled: bool = True
    non_activation_boundary_enabled: bool = True
    model_card_update_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_drift_monitoring_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_drift_scores_are_not_trade_signals: bool = True
    warn_monitoring_metadata_is_not_live_monitoring: bool = True
    warn_alert_rules_are_preview_only: bool = True
