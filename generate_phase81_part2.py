import re
from pathlib import Path

# Add Exceptions
with open('usa_signal_bot/core/exceptions.py', 'a') as f:
    f.write("""
class PaperPreRehearsalError(USASignalBotError):
    \"\"\"Base exception for pre-paper dry rehearsal errors.\"\"\"
    pass

class PreRehearsalFinalHandoffIngestionError(PaperPreRehearsalError):
    pass

class PrePaperEligibilityError(PaperPreRehearsalError):
    pass

class PrePaperDryRehearsalPlanError(PaperPreRehearsalError):
    pass

class PaperBaselineLoaderError(PaperPreRehearsalError):
    pass

class MutationFirewallRuleError(PaperPreRehearsalError):
    pass

class PaperStateMutationFirewallError(PaperPreRehearsalError):
    pass

class MutationAttemptDetectorError(PaperPreRehearsalError):
    pass

class ForbiddenOperationSimulatorError(PaperPreRehearsalError):
    pass

class PrePaperDryRehearsalRunnerError(PaperPreRehearsalError):
    pass

class RehearsalOutputAnalyzerError(PaperPreRehearsalError):
    pass

class ActivationDeniedCheckpointError(PaperPreRehearsalError):
    pass

class ActivationCheckpointValidationError(PaperPreRehearsalError):
    pass

class ZeroMutationAssertionError(PaperPreRehearsalError):
    pass

class PrePaperAuditError(PaperPreRehearsalError):
    pass

class PrePaperStorageError(PaperPreRehearsalError):
    pass

class PrePaperValidationError(PaperPreRehearsalError):
    pass

class PrePaperReportingError(PaperPreRehearsalError):
    pass
""")

# config/default.yaml update
import yaml
with open('config/default.yaml', 'r') as f:
    config_yaml = yaml.safe_load(f)

config_yaml['paper_pre_rehearsal'] = {
  'enabled': True,
  'write_pre_rehearsal_reports': True,
  'warn_not_investment_advice': True,
  'warn_no_broker_execution': True,
  'warn_no_real_paper_mutation': True,
  'warn_pre_paper_rehearsal_is_not_activation': True,
  'warn_firewall_is_metadata_only': True,
  'warn_activation_denied_checkpoint_is_not_activation': True
}
config_yaml['pre_paper_dry_rehearsal'] = {
  'enabled': True,
  'deterministic_rehearsal': True,
  'require_final_handoff_checkpoint': True,
  'require_sealed_archive': True,
  'require_mutation_firewall': True,
  'require_activation_denied_checkpoint': True,
  'execution_enabled': False,
  'active_paper_enabled': False,
  'broker_execution_enabled': False,
  'paper_state_mutation_enabled': False,
  'config_patch_enabled': False,
  'telegram_real_send_enabled': False
}
config_yaml['paper_state_mutation_firewall'] = {
  'enabled': True,
  'deny_paper_state_write': True,
  'deny_paper_order_create': True,
  'deny_position_mutation': True,
  'deny_portfolio_mutation': True,
  'deny_cash_mutation': True,
  'deny_equity_mutation': True,
  'deny_broker_order_send': True,
  'deny_telegram_real_send': True,
  'deny_config_patch': True,
  'deny_active_paper_enable': True,
  'deny_archive_unlock': True,
  'deny_final_lock_unlock': True,
  'simulate_forbidden_attempts': True
}
config_yaml['activation_denied_checkpoint'] = {
  'enabled': True,
  'activation_denied_by_default': True,
  'allow_active_paper': False,
  'allow_broker_execution': False,
  'allow_paper_state_mutation': False,
  'allow_config_patch': False,
  'allow_telegram_real_send': False
}
config_yaml['pre_paper_rehearsal_safety'] = {
  'enabled': True,
  'block_on_real_order_risk': True,
  'block_on_paper_order_risk': True,
  'block_on_broker_order_risk': True,
  'block_on_paper_state_mutation_risk': True,
  'block_on_telegram_real_send_risk': True,
  'block_on_production_config_write_risk': True,
  'block_on_active_paper_enable_risk': True,
  'block_on_firewall_disabled_risk': True,
  'block_on_activation_allowed_risk': True,
  'block_on_secret_risk': True
}
config_yaml['paper_pre_rehearsal_notifications'] = {
  'enabled': True,
  'dry_run': True,
  'notify_pre_paper_rehearsal_report': True,
  'notify_mutation_firewall_warning': True,
  'notify_activation_denied_checkpoint_warning': True,
  'default_channel': "dry_run",
  'warn_no_real_send_default': True
}

with open('config/default.yaml', 'w') as f:
    yaml.dump(config_yaml, f, default_flow_style=False)

try:
    with open('config/local.example.yaml', 'r') as f:
        local_yaml = yaml.safe_load(f)
    if local_yaml is None: local_yaml = {}
    local_yaml['paper_pre_rehearsal'] = config_yaml['paper_pre_rehearsal']
    with open('config/local.example.yaml', 'w') as f:
        yaml.dump(local_yaml, f, default_flow_style=False)
except FileNotFoundError:
    pass

# config_schema.py addition
with open('usa_signal_bot/core/config_schema.py', 'a') as f:
    f.write("""
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
""")

with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    schema_content = f.read()

# Make sure we add them to RootConfig
root_config_updates = """    paper_pre_rehearsal: PaperPreRehearsalConfig = field(default_factory=PaperPreRehearsalConfig)
    pre_paper_dry_rehearsal: PrePaperDryRehearsalConfig = field(default_factory=PrePaperDryRehearsalConfig)
    paper_state_mutation_firewall: PaperStateMutationFirewallConfig = field(default_factory=PaperStateMutationFirewallConfig)
    activation_denied_checkpoint: ActivationDeniedCheckpointConfig = field(default_factory=ActivationDeniedCheckpointConfig)
    pre_paper_rehearsal_safety: PrePaperRehearsalSafetyConfig = field(default_factory=PrePaperRehearsalSafetyConfig)
    paper_pre_rehearsal_notifications: PaperPreRehearsalNotificationsConfig = field(default_factory=PaperPreRehearsalNotificationsConfig)"""

if "paper_pre_rehearsal:" not in schema_content:
    schema_content = re.sub(
        r'(class RootConfig:.*?)(?=\s+def |\Z)',
        lambda m: m.group(1) + "\n" + root_config_updates + "\n",
        schema_content,
        flags=re.DOTALL
    )
    with open('usa_signal_bot/core/config_schema.py', 'w') as f:
        f.write(schema_content)
