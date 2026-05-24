import re
from pathlib import Path

def update_config():
    path = Path("usa_signal_bot/core/config.py")
    if not path.exists():
        return
    content = path.read_text()

    if "load_paper_mode_dry_admission_gate_config" not in content:
        config_to_add = """
def load_paper_mode_dry_admission_gate_config(data: dict) -> PaperModeDryAdmissionGateConfig:
    d = data.get("paper_mode_dry_admission_gate", {})
    return PaperModeDryAdmissionGateConfig(
        enabled=d.get("enabled", True),
        write_dry_admission_reports=d.get("write_dry_admission_reports", True),
        warn_not_investment_advice=d.get("warn_not_investment_advice", True),
        warn_no_broker_execution=d.get("warn_no_broker_execution", True),
        warn_no_real_paper_mutation=d.get("warn_no_real_paper_mutation", True),
        warn_shadow_replay_is_metadata_only=d.get("warn_shadow_replay_is_metadata_only", True),
        warn_board_evidence_freeze_is_metadata_only=d.get("warn_board_evidence_freeze_is_metadata_only", True),
        warn_dry_admission_gate_is_not_activation=d.get("warn_dry_admission_gate_is_not_activation", True)
    )

def load_shadow_launch_blocker_replay_config(data: dict) -> ShadowLaunchBlockerReplayConfig:
    d = data.get("shadow_launch_blocker_replay", {})
    return ShadowLaunchBlockerReplayConfig(
        enabled=d.get("enabled", True),
        deterministic_replay=d.get("deterministic_replay", True),
        require_all_attempts_blocked=d.get("require_all_attempts_blocked", True),
        require_shadow_launch_blocker_events=d.get("require_shadow_launch_blocker_events", True),
        execution_enabled=d.get("execution_enabled", False),
        shadow_launch_enabled=d.get("shadow_launch_enabled", False),
        paper_mode_launch_enabled=d.get("paper_mode_launch_enabled", False),
        active_paper_enabled=d.get("active_paper_enabled", False),
        paper_admission_enabled=d.get("paper_admission_enabled", False),
        broker_execution_enabled=d.get("broker_execution_enabled", False),
        paper_state_mutation_enabled=d.get("paper_state_mutation_enabled", False),
        config_patch_enabled=d.get("config_patch_enabled", False),
        telegram_real_send_enabled=d.get("telegram_real_send_enabled", False)
    )

def load_board_evidence_freeze_config(data: dict) -> BoardEvidenceFreezeConfig:
    d = data.get("board_evidence_freeze", {})
    return BoardEvidenceFreezeConfig(
        enabled=d.get("enabled", True),
        freeze_is_metadata_only=d.get("freeze_is_metadata_only", True),
        require_frozen=d.get("require_frozen", True),
        require_immutable=d.get("require_immutable", True),
        require_evidence_available=d.get("require_evidence_available", True),
        block_on_missing_evidence=d.get("block_on_missing_evidence", True),
        block_on_stale_evidence=d.get("block_on_stale_evidence", True),
        block_on_freeze_failed=d.get("block_on_freeze_failed", True)
    )

def load_final_paper_mode_dry_admission_gate_config(data: dict) -> FinalPaperModeDryAdmissionGateConfig:
    d = data.get("final_paper_mode_dry_admission_gate", {})
    return FinalPaperModeDryAdmissionGateConfig(
        enabled=d.get("enabled", True),
        gate_is_metadata_only=d.get("gate_is_metadata_only", True),
        require_board_dossier=d.get("require_board_dossier", True),
        require_acceptance_board_seal=d.get("require_acceptance_board_seal", True),
        require_shadow_replay=d.get("require_shadow_replay", True),
        require_board_evidence_freeze=d.get("require_board_evidence_freeze", True),
        require_dry_admission_rules=d.get("require_dry_admission_rules", True),
        require_dry_admission_assertions=d.get("require_dry_admission_assertions", True),
        require_manual_review=d.get("require_manual_review", True),
        activation_allowed=d.get("activation_allowed", False),
        admission_allowed=d.get("admission_allowed", False),
        transition_allowed=d.get("transition_allowed", False),
        shadow_launch_allowed=d.get("shadow_launch_allowed", False),
        paper_mode_launch_allowed=d.get("paper_mode_launch_allowed", False),
        all_writes_blocked_required=d.get("all_writes_blocked_required", True),
        require_order_created_false=d.get("require_order_created_false", True),
        require_mutation_detected_false=d.get("require_mutation_detected_false", True),
        allow_active_paper=d.get("allow_active_paper", False),
        allow_broker_execution=d.get("allow_broker_execution", False),
        allow_paper_state_mutation=d.get("allow_paper_state_mutation", False),
        allow_config_patch=d.get("allow_config_patch", False),
        allow_telegram_real_send=d.get("allow_telegram_real_send", False)
    )

def load_dry_admission_gate_safety_config(data: dict) -> DryAdmissionGateSafetyConfig:
    d = data.get("dry_admission_gate_safety", {})
    return DryAdmissionGateSafetyConfig(
        enabled=d.get("enabled", True),
        block_on_real_order_risk=d.get("block_on_real_order_risk", True),
        block_on_paper_order_risk=d.get("block_on_paper_order_risk", True),
        block_on_broker_order_risk=d.get("block_on_broker_order_risk", True),
        block_on_paper_state_mutation_risk=d.get("block_on_paper_state_mutation_risk", True),
        block_on_telegram_real_send_risk=d.get("block_on_telegram_real_send_risk", True),
        block_on_production_config_write_risk=d.get("block_on_production_config_write_risk", True),
        block_on_active_paper_enable_risk=d.get("block_on_active_paper_enable_risk", True),
        block_on_shadow_launch_risk=d.get("block_on_shadow_launch_risk", True),
        block_on_paper_mode_launch_risk=d.get("block_on_paper_mode_launch_risk", True),
        block_on_admission_allowed_risk=d.get("block_on_admission_allowed_risk", True),
        block_on_activation_allowed_risk=d.get("block_on_activation_allowed_risk", True),
        block_on_transition_allowed_risk=d.get("block_on_transition_allowed_risk", True),
        block_on_order_created_risk=d.get("block_on_order_created_risk", True),
        block_on_mutation_detected_risk=d.get("block_on_mutation_detected_risk", True),
        block_on_shadow_replay_failed=d.get("block_on_shadow_replay_failed", True),
        block_on_board_evidence_freeze_failed=d.get("block_on_board_evidence_freeze_failed", True),
        block_on_dry_admission_assertion_failed=d.get("block_on_dry_admission_assertion_failed", True),
        block_on_secret_risk=d.get("block_on_secret_risk", True)
    )

def load_dry_admission_gate_notifications_config(data: dict) -> DryAdmissionGateNotificationsConfig:
    d = data.get("dry_admission_gate_notifications", {})
    return DryAdmissionGateNotificationsConfig(
        enabled=d.get("enabled", True),
        dry_run=d.get("dry_run", True),
        notify_dry_admission_gate_report=d.get("notify_dry_admission_gate_report", True),
        notify_shadow_replay_warning=d.get("notify_shadow_replay_warning", True),
        notify_board_evidence_freeze_warning=d.get("notify_board_evidence_freeze_warning", True),
        default_channel=d.get("default_channel", "dry_run"),
        warn_no_real_send_default=d.get("warn_no_real_send_default", True)
    )
"""
        # Find imports to add config schema types
        imports_match = re.search(r'from usa_signal_bot\.core\.config_schema import \((.*?)\)', content, re.DOTALL)
        if imports_match:
            new_imports = ",\n    PaperModeDryAdmissionGateConfig,\n    ShadowLaunchBlockerReplayConfig,\n    BoardEvidenceFreezeConfig,\n    FinalPaperModeDryAdmissionGateConfig,\n    DryAdmissionGateSafetyConfig,\n    DryAdmissionGateNotificationsConfig"
            content = content[:imports_match.end(1)] + new_imports + content[imports_match.end(1):]

        # Add loading functions
        content += "\n" + config_to_add

        # Update AppConfig load
        app_config_match = re.search(r'def load_config.*?AppConfig:.*?return AppConfig\(.*?\)', content, re.DOTALL)
        if app_config_match:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() == 'return AppConfig(':
                    lines.insert(i+1, "        paper_mode_dry_admission_gate=load_paper_mode_dry_admission_gate_config(data),")
                    lines.insert(i+1, "        shadow_launch_blocker_replay=load_shadow_launch_blocker_replay_config(data),")
                    lines.insert(i+1, "        board_evidence_freeze=load_board_evidence_freeze_config(data),")
                    lines.insert(i+1, "        final_paper_mode_dry_admission_gate=load_final_paper_mode_dry_admission_gate_config(data),")
                    lines.insert(i+1, "        dry_admission_gate_safety=load_dry_admission_gate_safety_config(data),")
                    lines.insert(i+1, "        dry_admission_gate_notifications=load_dry_admission_gate_notifications_config(data),")
                    break
            content = '\n'.join(lines)

        path.write_text(content)

update_config()
