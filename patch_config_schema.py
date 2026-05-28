import re

with open("usa_signal_bot/core/config_schema.py", "r") as f:
    content = f.read()

new_configs = """
@dataclass
class FeatureFactorFinalClosureConfig:
    enabled: bool = True
    current_phase: int = 125
    final_phase: int = 160
    require_phase124_freeze_preparation: bool = True
    final_artifact_chain_enabled: bool = True
    final_closure_checks_enabled: bool = True
    freeze_seal_enabled: bool = True
    engine_readiness_certificate_enabled: bool = True
    phase126_kickoff_gate_enabled: bool = True
    write_final_closure_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase125_is_not_activation: bool = True
    warn_freeze_seal_is_not_deployment: bool = True
    warn_phase126_gate_is_not_strategy_activation: bool = True

@dataclass
class Phase125FinalClosurePolicyConfig:
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
    allow_deployment: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase125ClosureRequirementsConfig:
    require_phase124_ready: bool = True
    require_final_artifact_chain_complete: bool = True
    require_final_checks_passed: bool = True
    require_freeze_seal_valid: bool = True
    require_engine_certificate_valid: bool = True
    require_phase126_gate_passed: bool = True
    require_safety_pass: bool = True
    ready_for_phase126_allowed: bool = True

@dataclass
class Phase125NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

"""

# Insert before `class Config:`
content = re.sub(
    r'(class Config:)',
    new_configs + r'\1',
    content
)

# Append to Config class
content = re.sub(
    r'(class Config:.*?)(?=\n\n|\Z)',
    r'\1\n    feature_factor_final_closure: FeatureFactorFinalClosureConfig = field(default_factory=FeatureFactorFinalClosureConfig)\n'
    r'    phase125_final_closure_policy: Phase125FinalClosurePolicyConfig = field(default_factory=Phase125FinalClosurePolicyConfig)\n'
    r'    phase125_closure_requirements: Phase125ClosureRequirementsConfig = field(default_factory=Phase125ClosureRequirementsConfig)\n'
    r'    phase125_notifications: Phase125NotificationsConfig = field(default_factory=Phase125NotificationsConfig)\n',
    content,
    flags=re.DOTALL
)

with open("usa_signal_bot/core/config_schema.py", "w") as f:
    f.write(content)
