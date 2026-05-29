import re

with open("usa_signal_bot/core/config_schema.py", "r") as f:
    content = f.read()

new_configs = """
from dataclasses import dataclass, field

@dataclass
class RegimeFeatureEngineeringConfig:
    enabled: bool = True
    current_phase: int = 127
    final_phase: int = 160
    require_phase126_regime_foundation: bool = True
    market_state_metrics_enabled: bool = True
    rolling_market_state_metrics_enabled: bool = True
    cross_sectional_market_state_metrics_enabled: bool = True
    regime_feature_table_enabled: bool = True
    unsupervised_candidate_preparation_enabled: bool = True
    candidate_readiness_gate_enabled: bool = True
    write_regime_feature_engineering_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase127_is_not_activation: bool = True
    warn_candidates_are_not_predictions: bool = True
    warn_candidates_are_not_trade_signals: bool = True

@dataclass
class Phase127RegimePolicyConfig:
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
    allow_heavy_ml_dependencies: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase127MarketStateMetricsConfig:
    enabled: bool = True
    default_windows: list[int] = field(default_factory=lambda: [20, 60, 120])
    build_cross_sectional_metrics: bool = True
    preserve_warmup_nulls: bool = True
    write_feature_tables: bool = True
    overwrite_feature_tables_default: bool = False

@dataclass
class Phase127CandidatePreparationConfig:
    enabled: bool = True
    method: str = "DETERMINISTIC_RULE_TEMPLATE"
    produce_model_predictions: bool = False
    train_models: bool = False
    fit_clustering_models: bool = False
    candidate_scores_are_metadata_only: bool = True
    ready_for_phase128_allowed: bool = True

@dataclass
class Phase127NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False
"""

# Insert before class Config:
content = re.sub(
    r'(class Config:)',
    new_configs + r'\n\1',
    content
)

content = re.sub(
    r'(class Config:.*?)(?=\n\n|\Z)',
    r'\1\n    regime_feature_engineering: RegimeFeatureEngineeringConfig = field(default_factory=RegimeFeatureEngineeringConfig)\n'
    r'    phase127_regime_policy: Phase127RegimePolicyConfig = field(default_factory=Phase127RegimePolicyConfig)\n'
    r'    phase127_market_state_metrics: Phase127MarketStateMetricsConfig = field(default_factory=Phase127MarketStateMetricsConfig)\n'
    r'    phase127_candidate_preparation: Phase127CandidatePreparationConfig = field(default_factory=Phase127CandidatePreparationConfig)\n'
    r'    phase127_notifications: Phase127NotificationsConfig = field(default_factory=Phase127NotificationsConfig)\n',
    content,
    flags=re.DOTALL
)

with open("usa_signal_bot/core/config_schema.py", "w") as f:
    f.write(content)
