import re

with open("usa_signal_bot/core/config_schema.py", "r") as f:
    content = f.read()

new_classes = """
@dataclass
class Phase128LabelingPolicyConfig:
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
class Phase128HeuristicLabelingConfig:
    enabled: bool = True
    minimum_score_threshold: float = 40.0
    minimum_score_gap: float = 5.0
    fallback_label: str = "unknown_regime"
    mixed_label: str = "mixed_regime"
    unknown_label: str = "unknown_regime"
    conflict_policy: str = "fallback_to_mixed_or_unknown"
    write_labeled_tables: bool = True
    overwrite_labeled_tables_default: bool = False

@dataclass
class Phase128RollingWindowsConfig:
    enabled: bool = True
    windows: list[int] = field(default_factory=lambda: [20, 60, 120])
    min_periods_ratio: float = 0.5
    preserve_warmup_nulls: bool = True
    build_stability_profiles: bool = True

@dataclass
class Phase128CandidateValidationConfig:
    enabled: bool = True
    require_candidate_definitions: bool = True
    require_candidate_scores: bool = True
    require_taxonomy_alignment: bool = True
    require_no_model_training: bool = True
    require_no_model_prediction: bool = True
    ready_for_phase129_allowed: bool = True

@dataclass
class Phase128NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class RegimeLabelingConfig:
    enabled: bool = True
    current_phase: int = 128
    final_phase: int = 160
    require_phase127_regime_feature_engineering: bool = True
    heuristic_labeling_enabled: bool = True
    rolling_regime_windows_enabled: bool = True
    candidate_validation_enabled: bool = True
    label_stability_enabled: bool = True
    readiness_gate_enabled: bool = True
    write_regime_labeling_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase128_is_not_activation: bool = True
    warn_labels_are_not_trade_signals: bool = True
    warn_labels_are_not_model_predictions: bool = True
    policy: Phase128LabelingPolicyConfig = field(default_factory=Phase128LabelingPolicyConfig)
    heuristic_labeling: Phase128HeuristicLabelingConfig = field(default_factory=Phase128HeuristicLabelingConfig)
    rolling_windows: Phase128RollingWindowsConfig = field(default_factory=Phase128RollingWindowsConfig)
    candidate_validation: Phase128CandidateValidationConfig = field(default_factory=Phase128CandidateValidationConfig)
    notifications: Phase128NotificationsConfig = field(default_factory=Phase128NotificationsConfig)
"""

if "RegimeLabelingConfig" not in content:
    content += "\n" + new_classes

# Add to AppConfig
if "regime_labeling: RegimeLabelingConfig" not in content:
    content = re.sub(
        r'(class AppConfig:\n(?:.*\n)*?)(\s*def )',
        r'\1    regime_labeling: RegimeLabelingConfig = field(default_factory=RegimeLabelingConfig)\n\2',
        content
    )

with open("usa_signal_bot/core/config_schema.py", "w") as f:
    f.write(content)

