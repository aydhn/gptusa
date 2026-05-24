import re
from pathlib import Path

def update_config():
    path = Path("config/default.yaml")
    if not path.exists():
        return
    content = path.read_text()

    if "paper_mode_dry_admission_gate" not in content:
        config_to_add = """
paper_mode_dry_admission_gate:
  enabled: true
  write_dry_admission_reports: true
  warn_not_investment_advice: true
  warn_no_broker_execution: true
  warn_no_real_paper_mutation: true
  warn_shadow_replay_is_metadata_only: true
  warn_board_evidence_freeze_is_metadata_only: true
  warn_dry_admission_gate_is_not_activation: true

shadow_launch_blocker_replay:
  enabled: true
  deterministic_replay: true
  require_all_attempts_blocked: true
  require_shadow_launch_blocker_events: true
  execution_enabled: false
  shadow_launch_enabled: false
  paper_mode_launch_enabled: false
  active_paper_enabled: false
  paper_admission_enabled: false
  broker_execution_enabled: false
  paper_state_mutation_enabled: false
  config_patch_enabled: false
  telegram_real_send_enabled: false

board_evidence_freeze:
  enabled: true
  freeze_is_metadata_only: true
  require_frozen: true
  require_immutable: true
  require_evidence_available: true
  block_on_missing_evidence: true
  block_on_stale_evidence: true
  block_on_freeze_failed: true

final_paper_mode_dry_admission_gate:
  enabled: true
  gate_is_metadata_only: true
  require_board_dossier: true
  require_acceptance_board_seal: true
  require_shadow_replay: true
  require_board_evidence_freeze: true
  require_dry_admission_rules: true
  require_dry_admission_assertions: true
  require_manual_review: true
  activation_allowed: false
  admission_allowed: false
  transition_allowed: false
  shadow_launch_allowed: false
  paper_mode_launch_allowed: false
  all_writes_blocked_required: true
  require_order_created_false: true
  require_mutation_detected_false: true
  allow_active_paper: false
  allow_broker_execution: false
  allow_paper_state_mutation: false
  allow_config_patch: false
  allow_telegram_real_send: false

dry_admission_gate_safety:
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
  block_on_admission_allowed_risk: true
  block_on_activation_allowed_risk: true
  block_on_transition_allowed_risk: true
  block_on_order_created_risk: true
  block_on_mutation_detected_risk: true
  block_on_shadow_replay_failed: true
  block_on_board_evidence_freeze_failed: true
  block_on_dry_admission_assertion_failed: true
  block_on_secret_risk: true

dry_admission_gate_notifications:
  enabled: true
  dry_run: true
  notify_dry_admission_gate_report: true
  notify_shadow_replay_warning: true
  notify_board_evidence_freeze_warning: true
  default_channel: "dry_run"
  warn_no_real_send_default: true
"""
        content += config_to_add
        path.write_text(content)

update_config()
