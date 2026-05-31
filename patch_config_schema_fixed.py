import sys

file_path = "usa_signal_bot/core/config_schema.py"
with open(file_path, "r") as f:
    content = f.read()

new_dataclasses = """
@dataclass
class RegimeFinalClosureConfig:
    enabled: bool = True
    current_phase: int = 135
    final_phase: int = 160
    require_phase134_research_freeze: bool = True
    research_freeze_ingestion_enabled: bool = True
    artifact_chain_validation_enabled: bool = True
    final_closure_validation_enabled: bool = True
    freeze_seal_enabled: bool = True
    final_safety_audit_enabled: bool = True
    ml_input_contract_enabled: bool = True
    ml_kickoff_gate_enabled: bool = True
    write_final_closure_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase135_is_not_activation: bool = True
    warn_freeze_seal_is_not_deployment: bool = True
    warn_ml_kickoff_does_not_train_models: bool = True

@dataclass
class Phase135ClosurePolicyConfig:
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
    allow_background_daemon: bool = False
    allow_scheduler: bool = False
    produce_trade_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False
    strategy_activation_allowed: bool = False

@dataclass
class Phase135ArtifactChainConfig:
    enabled: bool = True
    require_phase126_foundation: bool = True
    require_phase127_feature_engineering: bool = True
    require_phase128_labeling: bool = True
    require_phase129_transition_analytics: bool = True
    require_phase130_market_behavior: bool = True
    require_phase131_alignment: bool = True
    require_phase132_context_validation: bool = True
    require_phase133_monitoring: bool = True
    require_phase134_research_freeze: bool = True
    require_hashes: bool = True
    require_read_only_references: bool = True

@dataclass
class Phase135FreezeSealConfig:
    enabled: bool = True
    seal_version: str = "phase135.v1"
    sealed_phase_start: int = 126
    sealed_phase_end: int = 135
    next_phase: int = 136
    require_final_safety_audit_pass: bool = True
    require_artifact_chain_valid: bool = True

@dataclass
class Phase135MLKickoffConfig:
    enabled: bool = True
    ready_for_phase136_allowed: bool = True
    build_input_contract: bool = True
    training_started: bool = False
    prediction_started: bool = False
    allow_training_in_phase135: bool = False
    allow_prediction_in_phase135: bool = False
    require_non_activation_boundary: bool = True

@dataclass
class Phase135NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False
"""

if "RegimeFinalClosureConfig" not in content:
    parts = content.split("class AppConfig:")
    content = parts[0] + new_dataclasses + "\n@dataclass\nclass AppConfig:" + parts[1]

app_config_additions = """    regime_final_closure: RegimeFinalClosureConfig = field(default_factory=RegimeFinalClosureConfig)
    phase135_closure_policy: Phase135ClosurePolicyConfig = field(default_factory=Phase135ClosurePolicyConfig)
    phase135_artifact_chain: Phase135ArtifactChainConfig = field(default_factory=Phase135ArtifactChainConfig)
    phase135_freeze_seal: Phase135FreezeSealConfig = field(default_factory=Phase135FreezeSealConfig)
    phase135_ml_kickoff: Phase135MLKickoffConfig = field(default_factory=Phase135MLKickoffConfig)
    phase135_notifications: Phase135NotificationsConfig = field(default_factory=Phase135NotificationsConfig)
"""
if "regime_final_closure:" not in content:
    content = content + "\n" + app_config_additions

with open(file_path, "w") as f:
    f.write(content)
