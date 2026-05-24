
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
class Config:

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

    def validate(self) -> None:
        pass

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
