import os
import re

def append_to_config_schema():
    path = "usa_signal_bot/core/config_schema.py"
    with open(path, "r") as f:
        content = f.read()

    classes_to_add = """
@dataclass
class PaperModeDryAdmissionDossierConfig:
    enabled: bool = True
    write_dry_admission_dossier_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_no_real_paper_mutation: bool = True
    warn_dry_admission_dossier_is_not_activation: bool = True
    warn_dry_admission_acceptance_seal_is_metadata_only: bool = True
    warn_rehearsal_blocker_denies_rehearsal: bool = True

@dataclass
class DryAdmissionGateDossierConfig:
    enabled: bool = True
    deterministic_dossier: bool = True
    require_dry_admission_gate_review: bool = True
    require_final_dry_admission_gate: bool = True
    require_shadow_replay_result: bool = True
    require_board_evidence_freeze: bool = True
    require_dry_admission_acceptance_seal: bool = True
    require_rehearsal_blocker: bool = True
    require_manual_review: bool = True
    activation_allowed: bool = False
    admission_allowed: bool = False
    transition_allowed: bool = False
    shadow_launch_allowed: bool = False
    paper_mode_launch_allowed: bool = False
    rehearsal_allowed: bool = False
    paper_mode_rehearsal_allowed: bool = False
    all_writes_blocked_required: bool = True
    require_order_created_false: bool = True
    require_mutation_detected_false: bool = True
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class DryAdmissionAcceptanceSealConfig:
    enabled: bool = True
    seal_is_metadata_only: bool = True
    require_dry_admission_gate_passed: bool = True
    require_shadow_replay_passed: bool = True
    require_board_evidence_freeze_valid: bool = True
    require_no_shadow_launch_confirmed: bool = True
    require_no_paper_mode_launch_confirmed: bool = True
    require_no_rehearsal_confirmed: bool = True
    require_no_admission_confirmed: bool = True
    require_no_order_confirmed: bool = True
    require_no_write_confirmed: bool = True
    require_no_broker_confirmed: bool = True
    require_no_config_patch_confirmed: bool = True
    require_no_telegram_real_send_confirmed: bool = True
    require_sealed: bool = True
    require_immutable: bool = True
    allow_rehearsal: bool = False
    allow_paper_mode_rehearsal: bool = False
    allow_shadow_launch: bool = False
    allow_paper_mode_launch: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_config_patch: bool = False
    allow_telegram_real_send: bool = False

@dataclass
class FinalPaperModeRehearsalBlockerConfig:
    enabled: bool = True
    blocker_is_metadata_only: bool = True
    deny_rehearsal_by_default: bool = True
    deny_start_paper_mode_rehearsal: bool = True
    deny_start_local_paper_rehearsal_runtime: bool = True
    deny_rehearse_candidate: bool = True
    deny_admit_candidate_to_rehearsal: bool = True
    deny_create_rehearsal_session: bool = True
    deny_create_paper_session: bool = True
    deny_create_paper_order: bool = True
    deny_commit_paper_state: bool = True
    deny_patch_paper_config: bool = True
    deny_send_broker_order: bool = True
    deny_send_telegram_real: bool = True
    rehearsal_allowed: bool = False
    paper_mode_rehearsal_allowed: bool = False
    active_paper_enabled: bool = False

@dataclass
class DryAdmissionDossierSafetyConfig:
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
    block_on_rehearsal_risk: bool = True
    block_on_admission_allowed_risk: bool = True
    block_on_activation_allowed_risk: bool = True
    block_on_transition_allowed_risk: bool = True
    block_on_order_created_risk: bool = True
    block_on_mutation_detected_risk: bool = True
    block_on_rehearsal_blocker_failed: bool = True
    block_on_secret_risk: bool = True

@dataclass
class DryAdmissionDossierNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_dry_admission_dossier_report: bool = True
    notify_dry_admission_acceptance_seal_warning: bool = True
    notify_rehearsal_blocker_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

"""
    if "PaperModeDryAdmissionDossierConfig" not in content:
        # Add to the AppConfig class
        content = content.replace("class AppConfig:", classes_to_add + "\nclass AppConfig:")

        # Add attributes to AppConfig
        app_config_attrs = """
    paper_mode_dry_admission_dossier: PaperModeDryAdmissionDossierConfig = field(default_factory=PaperModeDryAdmissionDossierConfig)
    dry_admission_gate_dossier: DryAdmissionGateDossierConfig = field(default_factory=DryAdmissionGateDossierConfig)
    dry_admission_acceptance_seal: DryAdmissionAcceptanceSealConfig = field(default_factory=DryAdmissionAcceptanceSealConfig)
    final_paper_mode_rehearsal_blocker: FinalPaperModeRehearsalBlockerConfig = field(default_factory=FinalPaperModeRehearsalBlockerConfig)
    dry_admission_dossier_safety: DryAdmissionDossierSafetyConfig = field(default_factory=DryAdmissionDossierSafetyConfig)
    dry_admission_dossier_notifications: DryAdmissionDossierNotificationsConfig = field(default_factory=DryAdmissionDossierNotificationsConfig)
"""
        content = content.replace("    metadata: dict[str, Any] = field(default_factory=dict)", app_config_attrs + "    metadata: dict[str, Any] = field(default_factory=dict)")

        with open(path, "w") as f:
            f.write(content)

def append_to_yaml():
    path = "config/default.yaml"
    with open(path, "r") as f:
        content = f.read()

    yaml_to_add = """
paper_mode_dry_admission_dossier:
  enabled: true
  write_dry_admission_dossier_reports: true
  warn_not_investment_advice: true
  warn_no_broker_execution: true
  warn_no_real_paper_mutation: true
  warn_dry_admission_dossier_is_not_activation: true
  warn_dry_admission_acceptance_seal_is_metadata_only: true
  warn_rehearsal_blocker_denies_rehearsal: true

dry_admission_gate_dossier:
  enabled: true
  deterministic_dossier: true
  require_dry_admission_gate_review: true
  require_final_dry_admission_gate: true
  require_shadow_replay_result: true
  require_board_evidence_freeze: true
  require_dry_admission_acceptance_seal: true
  require_rehearsal_blocker: true
  require_manual_review: true
  activation_allowed: false
  admission_allowed: false
  transition_allowed: false
  shadow_launch_allowed: false
  paper_mode_launch_allowed: false
  rehearsal_allowed: false
  paper_mode_rehearsal_allowed: false
  all_writes_blocked_required: true
  require_order_created_false: true
  require_mutation_detected_false: true
  allow_active_paper: false
  allow_broker_execution: false
  allow_paper_state_mutation: false
  allow_config_patch: false
  allow_telegram_real_send: false

dry_admission_acceptance_seal:
  enabled: true
  seal_is_metadata_only: true
  require_dry_admission_gate_passed: true
  require_shadow_replay_passed: true
  require_board_evidence_freeze_valid: true
  require_no_shadow_launch_confirmed: true
  require_no_paper_mode_launch_confirmed: true
  require_no_rehearsal_confirmed: true
  require_no_admission_confirmed: true
  require_no_order_confirmed: true
  require_no_write_confirmed: true
  require_no_broker_confirmed: true
  require_no_config_patch_confirmed: true
  require_no_telegram_real_send_confirmed: true
  require_sealed: true
  require_immutable: true
  allow_rehearsal: false
  allow_paper_mode_rehearsal: false
  allow_shadow_launch: false
  allow_paper_mode_launch: false
  allow_active_paper: false
  allow_broker_execution: false
  allow_paper_state_mutation: false
  allow_config_patch: false
  allow_telegram_real_send: false

final_paper_mode_rehearsal_blocker:
  enabled: true
  blocker_is_metadata_only: true
  deny_rehearsal_by_default: true
  deny_start_paper_mode_rehearsal: true
  deny_start_local_paper_rehearsal_runtime: true
  deny_rehearse_candidate: true
  deny_admit_candidate_to_rehearsal: true
  deny_create_rehearsal_session: true
  deny_create_paper_session: true
  deny_create_paper_order: true
  deny_commit_paper_state: true
  deny_patch_paper_config: true
  deny_send_broker_order: true
  deny_send_telegram_real: true
  rehearsal_allowed: false
  paper_mode_rehearsal_allowed: false
  active_paper_enabled: false

dry_admission_dossier_safety:
  enabled: true
  block_on_real_order_risk: true
  block_on_paper_order_risk: true
  block_on_broker_order_risk: true
  block_on_paper_state_mutation_risk: true
  block_on_telegram_real_send_risk: true
  block_on_production_config_write_risk: true
  block_on_active_paper_enable_risk: true
  block_on_shadow_launch_risk: true
  block_on_paper_mode_launch_risk: true
  block_on_rehearsal_risk: true
  block_on_admission_allowed_risk: true
  block_on_activation_allowed_risk: true
  block_on_transition_allowed_risk: true
  block_on_order_created_risk: true
  block_on_mutation_detected_risk: true
  block_on_rehearsal_blocker_failed: true
  block_on_secret_risk: true

dry_admission_dossier_notifications:
  enabled: true
  dry_run: true
  notify_dry_admission_dossier_report: true
  notify_dry_admission_acceptance_seal_warning: true
  notify_rehearsal_blocker_warning: true
  default_channel: "dry_run"
  warn_no_real_send_default: true
"""
    if "paper_mode_dry_admission_dossier:" not in content:
        with open(path, "a") as f:
            f.write(yaml_to_add)

if __name__ == "__main__":
    append_to_config_schema()
    append_to_yaml()
    print("Config schema and yaml updated.")
