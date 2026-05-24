import re

def update_config_schema():
    with open('usa_signal_bot/core/config_schema.py', 'r') as f:
        content = f.read()

    new_dataclasses = """
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

"""
    if "PrePaperHandoffFreezeGateConfig" not in content:
        content += new_dataclasses

    # Update Config class
    config_injection = """
    pre_paper_handoff_freeze_gate: PrePaperHandoffFreezeGateConfig = field(default_factory=PrePaperHandoffFreezeGateConfig)
    sandbox_runtime_admission_blocker_replay: SandboxRuntimeAdmissionBlockerReplayConfig = field(default_factory=SandboxRuntimeAdmissionBlockerReplayConfig)
    simulator_evidence_freeze: SimulatorEvidenceFreezeConfig = field(default_factory=SimulatorEvidenceFreezeConfig)
    final_pre_paper_handoff_freeze_gate: FinalPrePaperHandoffFreezeGateConfig = field(default_factory=FinalPrePaperHandoffFreezeGateConfig)
    handoff_freeze_safety: HandoffFreezeSafetyConfig = field(default_factory=HandoffFreezeSafetyConfig)
    handoff_freeze_notifications: HandoffFreezeNotificationsConfig = field(default_factory=HandoffFreezeNotificationsConfig)
"""
    if "pre_paper_handoff_freeze_gate:" not in content:
        content = re.sub(r'(class Config:.*?)(?=^$)', r'\1' + config_injection, content, flags=re.MULTILINE | re.DOTALL)

    with open('usa_signal_bot/core/config_schema.py', 'w') as f:
        f.write(content)
    print("Config schema updated.")

if __name__ == '__main__':
    update_config_schema()
