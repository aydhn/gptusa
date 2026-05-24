import yaml
import sys

def update_yaml(filename):
    with open(filename, 'r') as f:
        data = yaml.safe_load(f) or {}

    if 'pre_paper_handoff_freeze_gate' not in data:
        data['pre_paper_handoff_freeze_gate'] = {
            'enabled': True,
            'write_handoff_freeze_reports': True,
            'warn_not_investment_advice': True,
            'warn_no_broker_execution': True,
            'warn_no_real_paper_mutation': True,
            'warn_sandbox_replay_is_metadata_only': True,
            'warn_simulator_evidence_freeze_is_metadata_only': True,
            'warn_handoff_freeze_gate_is_not_activation': True,
            'warn_phase_100_is_pre_paper_freeze_only': True
        }

    if 'sandbox_runtime_admission_blocker_replay' not in data:
        data['sandbox_runtime_admission_blocker_replay'] = {
            'enabled': True,
            'deterministic_replay': True,
            'require_all_attempts_blocked': True,
            'require_sandbox_runtime_admission_blocker_events': True,
            'execution_enabled': False,
            'sandbox_runtime_admission_enabled': False,
            'paper_sandbox_runtime_enabled': False,
            'simulator_admission_enabled': False,
            'local_paper_simulator_enabled': False,
            'active_paper_enabled': False,
            'paper_admission_enabled': False,
            'broker_execution_enabled': False,
            'paper_state_mutation_enabled': False,
            'config_patch_enabled': False,
            'telegram_real_send_enabled': False
        }

    if 'simulator_evidence_freeze' not in data:
        data['simulator_evidence_freeze'] = {
            'enabled': True,
            'freeze_is_metadata_only': True,
            'require_frozen': True,
            'require_immutable': True,
            'require_evidence_available': True,
            'block_on_missing_evidence': True,
            'block_on_stale_evidence': True,
            'block_on_freeze_failed': True
        }

    if 'final_pre_paper_handoff_freeze_gate' not in data:
        data['final_pre_paper_handoff_freeze_gate'] = {
            'enabled': True,
            'gate_is_metadata_only': True,
            'require_simulator_dossier': True,
            'require_simulator_acceptance_seal': True,
            'require_sandbox_runtime_admission_replay': True,
            'require_simulator_evidence_freeze': True,
            'require_handoff_freeze_rules': True,
            'require_handoff_freeze_assertions': True,
            'require_manual_review': True,
            'require_frozen': True,
            'activation_allowed': False,
            'admission_allowed': False,
            'transition_allowed': False,
            'sandbox_runtime_admission_allowed': False,
            'paper_sandbox_runtime_allowed': False,
            'simulator_admission_allowed': False,
            'local_paper_simulator_allowed': False,
            'active_paper_enabled': False,
            'all_writes_blocked_required': True,
            'require_order_created_false': True,
            'require_mutation_detected_false': True,
            'allow_active_paper': False,
            'allow_broker_execution': False,
            'allow_paper_state_mutation': False,
            'allow_config_patch': False,
            'allow_telegram_real_send': False
        }

    if 'handoff_freeze_safety' not in data:
        data['handoff_freeze_safety'] = {
            'enabled': True,
            'block_on_real_order_risk': True,
            'block_on_paper_order_risk': True,
            'block_on_broker_order_risk': True,
            'block_on_paper_state_mutation_risk': True,
            'block_on_telegram_real_send_risk': True,
            'block_on_production_config_write_risk': True,
            'block_on_active_paper_enable_risk': True,
            'block_on_simulator_admission_risk': True,
            'block_on_sandbox_runtime_admission_risk': True,
            'block_on_paper_sandbox_runtime_risk': True,
            'block_on_admission_allowed_risk': True,
            'block_on_activation_allowed_risk': True,
            'block_on_transition_allowed_risk': True,
            'block_on_order_created_risk': True,
            'block_on_mutation_detected_risk': True,
            'block_on_sandbox_replay_failed': True,
            'block_on_simulator_evidence_freeze_failed': True,
            'block_on_handoff_freeze_assertion_failed': True,
            'block_on_secret_risk': True
        }

    if 'handoff_freeze_notifications' not in data:
        data['handoff_freeze_notifications'] = {
            'enabled': True,
            'dry_run': True,
            'notify_handoff_freeze_report': True,
            'notify_sandbox_runtime_admission_replay_warning': True,
            'notify_simulator_evidence_freeze_warning': True,
            'default_channel': "dry_run",
            'warn_no_real_send_default': True
        }

    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    print(f"Updated {filename}")

if __name__ == '__main__':
    update_yaml('config/default.yaml')
    try:
        update_yaml('config/local.example.yaml')
    except FileNotFoundError:
        pass
