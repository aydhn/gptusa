import re

with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

config_schema = '''

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

'''

if "FeatureFactorIntegrationFreezeConfig" not in content:
    content = content.replace("class Config:", config_schema + "\nclass Config:")

    # Add to config
    add_to_config = '''
    feature_factor_integration_freeze: FeatureFactorIntegrationFreezeConfig = field(default_factory=FeatureFactorIntegrationFreezeConfig)
    phase124_freeze_policy: Phase124FreezePolicyConfig = field(default_factory=Phase124FreezePolicyConfig)
    phase124_acceptance_policy: Phase124AcceptancePolicyConfig = field(default_factory=Phase124AcceptancePolicyConfig)
    phase124_notifications: Phase124NotificationsConfig = field(default_factory=Phase124NotificationsConfig)
'''
    # We replace the last line of Config which is probably `pass` or a field
    content = re.sub(r'(class Config:.*?)(?=^$|\Z)', r'\1' + add_to_config, content, flags=re.MULTILINE|re.DOTALL)

with open('usa_signal_bot/core/config_schema.py', 'w') as f:
    f.write(content)

with open('config/default.yaml', 'a') as f:
    f.write('''

feature_factor_integration_freeze:
  enabled: true
  current_phase: 124
  final_phase: 160
  require_phase123_explainability: true
  artifact_chain_integrity_enabled: true
  schema_continuity_enabled: true
  lineage_continuity_enabled: true
  safety_boundary_continuity_enabled: true
  integration_rehearsal_enabled: true
  report_qa_acceptance_enabled: true
  freeze_candidate_manifest_enabled: true
  freeze_readiness_gate_enabled: true
  write_freeze_preparation_reports: true
  warn_not_investment_advice: true
  warn_phase124_is_not_activation: true
  warn_freeze_preparation_is_not_deployment: true

phase124_freeze_policy:
  compute_metadata_local_only: true
  research_data_only: true
  local_fixture_only_default: true
  allow_network: false
  allow_paid_api: false
  allow_scraping: false
  allow_html_parsing: false
  allow_broker: false
  allow_order: false
  allow_paper_mutation: false
  allow_telegram_real_send: false
  allow_dashboard: false
  produce_trade_signals: false
  produce_order_decisions: false
  produce_portfolio_weights: false
  produce_investment_advice: false
  strategy_activation_allowed: false
  deployment_allowed: false

phase124_acceptance_policy:
  require_artifact_chain_complete: true
  require_schema_continuity: true
  require_lineage_continuity: true
  require_safety_boundary_pass: true
  require_report_qa_accepted: true
  require_factor_store_hardened: true
  require_freeze_manifest_valid: true
  ready_for_phase125_allowed: true
  ready_for_phase126_kickoff_after_phase125_allowed: true

phase124_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
''')

