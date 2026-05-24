import re
from pathlib import Path

def update_config_schema():
    path = Path("usa_signal_bot/core/config_schema.py")
    if not path.exists():
        return
    content = path.read_text()

    if "PaperModeDryAdmissionGateConfig" not in content:
        config_to_add = """
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
"""
        content += config_to_add

        # Add to AppConfig
        app_config_match = re.search(r'class AppConfig:', content)
        if app_config_match:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('class AppConfig:'):
                    lines.insert(i+1, "    paper_mode_dry_admission_gate: PaperModeDryAdmissionGateConfig = field(default_factory=PaperModeDryAdmissionGateConfig)")
                    lines.insert(i+1, "    shadow_launch_blocker_replay: ShadowLaunchBlockerReplayConfig = field(default_factory=ShadowLaunchBlockerReplayConfig)")
                    lines.insert(i+1, "    board_evidence_freeze: BoardEvidenceFreezeConfig = field(default_factory=BoardEvidenceFreezeConfig)")
                    lines.insert(i+1, "    final_paper_mode_dry_admission_gate: FinalPaperModeDryAdmissionGateConfig = field(default_factory=FinalPaperModeDryAdmissionGateConfig)")
                    lines.insert(i+1, "    dry_admission_gate_safety: DryAdmissionGateSafetyConfig = field(default_factory=DryAdmissionGateSafetyConfig)")
                    lines.insert(i+1, "    dry_admission_gate_notifications: DryAdmissionGateNotificationsConfig = field(default_factory=DryAdmissionGateNotificationsConfig)")
                    break
            content = '\n'.join(lines)

        path.write_text(content)

update_config_schema()
