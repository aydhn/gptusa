with open("usa_signal_bot/core/config_schema.py", "r") as f:
    content = f.read()

schema_add = """
@dataclass
class Phase130BehaviorPolicyConfig:
    compute_values_local_only: bool = True
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
    allow_model_training: bool = False
    allow_model_prediction: bool = False
    allow_heavy_ml_dependencies: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase130ReportPolicyConfig:
    formats: list[str] = field(default_factory=lambda: ["MARKDOWN", "JSON", "TEXT"])
    require_qa_pass: bool = True
    block_investment_advice_language: bool = True
    block_trade_signal_language: bool = True
    block_order_decision_language: bool = True
    block_portfolio_allocation_language: bool = True
    block_guarantee_language: bool = True
    block_broker_execution_language: bool = True
    block_deployment_language: bool = True
    overwrite_reports_default: bool = False

@dataclass
class Phase130NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class MarketBehaviorReportingConfig:
    enabled: bool = True
    current_phase: int = 130
    final_phase: int = 160
    require_phase129_regime_transition_analytics: bool = True
    behavior_profiles_enabled: bool = True
    regime_behavior_summaries_enabled: bool = True
    diagnostics_interpretation_enabled: bool = True
    report_document_enabled: bool = True
    report_qa_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_market_behavior_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase130_is_not_activation: bool = True
    warn_behavior_profiles_are_not_trade_signals: bool = True
    policy: Phase130BehaviorPolicyConfig = field(default_factory=Phase130BehaviorPolicyConfig)
    report_policy: Phase130ReportPolicyConfig = field(default_factory=Phase130ReportPolicyConfig)
    notifications: Phase130NotificationsConfig = field(default_factory=Phase130NotificationsConfig)
"""
if "MarketBehaviorReportingConfig" not in content:
    with open("usa_signal_bot/core/config_schema.py", "a") as f:
        f.write("\n" + schema_add)

# Make sure MarketBehaviorReportingConfig is added to the MainConfig dataclass
with open("usa_signal_bot/core/config_schema.py", "r") as f:
    content = f.read()

import re
if "market_behavior_reporting: MarketBehaviorReportingConfig" not in content:
    content = re.sub(
        r'(class MainConfig:\n(?:    [^\n]+\n)*)',
        r'\1    market_behavior_reporting: MarketBehaviorReportingConfig = field(default_factory=MarketBehaviorReportingConfig)\n',
        content
    )
    with open("usa_signal_bot/core/config_schema.py", "w") as f:
        f.write(content)
print("Updated schema.")
