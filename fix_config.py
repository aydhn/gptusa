import re

with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

new_classes = """

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
"""

# Append to file
with open('usa_signal_bot/core/config_schema.py', 'w') as f:
    f.write(content + new_classes)

# Also append instances to Config class
with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

# Make sure we add fields to Config dataclass. We find 'class Config:' and inject inside.
config_injection = """
    feature_engine_foundation: FeatureEngineFoundationConfig = field(default_factory=FeatureEngineFoundationConfig)
    phase116_feature_policy: Phase116FeaturePolicyConfig = field(default_factory=Phase116FeaturePolicyConfig)
    phase116_feature_scope: Phase116FeatureScopeConfig = field(default_factory=Phase116FeatureScopeConfig)
    phase116_notifications: Phase116NotificationsConfig = field(default_factory=Phase116NotificationsConfig)
"""
# Assuming the file ends with the Config class or we find where it is defined. Let's just find the last block of attributes in Config
# Actually, the file has @dataclass class Config:. We can add right at the end of class Config:
import re

lines = content.split('\n')
config_start = -1
for i, line in enumerate(lines):
    if line.startswith('class Config:'):
        config_start = i
        break

if config_start != -1:
    # insert at the end of the class
    last_line_of_config = len(lines)
    for i in range(config_start + 1, len(lines)):
        if lines[i].startswith('class '):
            last_line_of_config = i
            break

    lines.insert(last_line_of_config, "    feature_engine_foundation: FeatureEngineFoundationConfig = field(default_factory=FeatureEngineFoundationConfig)")
    lines.insert(last_line_of_config, "    phase116_feature_policy: Phase116FeaturePolicyConfig = field(default_factory=Phase116FeaturePolicyConfig)")
    lines.insert(last_line_of_config, "    phase116_feature_scope: Phase116FeatureScopeConfig = field(default_factory=Phase116FeatureScopeConfig)")
    lines.insert(last_line_of_config, "    phase116_notifications: Phase116NotificationsConfig = field(default_factory=Phase116NotificationsConfig)")

    with open('usa_signal_bot/core/config_schema.py', 'w') as f:
        f.write('\n'.join(lines))
else:
    print("Could not find Config class!")
