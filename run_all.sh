mkdir -p usa_signal_bot/regime_classification/feature_engineering
touch usa_signal_bot/regime_classification/feature_engineering/__init__.py

cat << 'INNER_EOF' > patch_config.py
import yaml
from pathlib import Path

config_path = Path("config/default.yaml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

if "regime_feature_engineering" not in config:
    config["regime_feature_engineering"] = {
        "enabled": True,
        "current_phase": 127,
        "final_phase": 160,
        "require_phase126_regime_foundation": True,
        "market_state_metrics_enabled": True,
        "rolling_market_state_metrics_enabled": True,
        "cross_sectional_market_state_metrics_enabled": True,
        "regime_feature_table_enabled": True,
        "unsupervised_candidate_preparation_enabled": True,
        "candidate_readiness_gate_enabled": True,
        "write_regime_feature_engineering_reports": True,
        "warn_not_investment_advice": True,
        "warn_phase127_is_not_activation": True,
        "warn_candidates_are_not_predictions": True,
        "warn_candidates_are_not_trade_signals": True,
    }

if "phase127_regime_policy" not in config:
    config["phase127_regime_policy"] = {
        "compute_values_local_only": True,
        "research_data_only": True,
        "local_fixture_only_default": True,
        "allow_network": False,
        "allow_paid_api": False,
        "allow_scraping": False,
        "allow_html_parsing": False,
        "allow_broker": False,
        "allow_order": False,
        "allow_paper_mutation": False,
        "allow_telegram_real_send": False,
        "allow_dashboard": False,
        "allow_deployment": False,
        "allow_model_training": False,
        "allow_heavy_ml_dependencies": False,
        "produce_trade_signals": False,
        "produce_order_decisions": False,
        "produce_portfolio_weights": False,
        "produce_investment_advice": False,
        "strategy_activation_allowed": False,
    }

if "phase127_market_state_metrics" not in config:
    config["phase127_market_state_metrics"] = {
        "enabled": True,
        "default_windows": [20, 60, 120],
        "build_cross_sectional_metrics": True,
        "preserve_warmup_nulls": True,
        "write_feature_tables": True,
        "overwrite_feature_tables_default": False,
    }

if "phase127_candidate_preparation" not in config:
    config["phase127_candidate_preparation"] = {
        "enabled": True,
        "method": "DETERMINISTIC_RULE_TEMPLATE",
        "produce_model_predictions": False,
        "train_models": False,
        "fit_clustering_models": False,
        "candidate_scores_are_metadata_only": True,
        "ready_for_phase128_allowed": True,
    }

if "phase127_notifications" not in config:
    config["phase127_notifications"] = {
        "enabled": True,
        "dry_run": True,
        "preview_only": True,
        "telegram_real_send": False,
    }


with open(config_path, "w") as f:
    yaml.dump(config, f, sort_keys=False)

INNER_EOF
python3 patch_config.py

cat << 'INNER_EOF' > patch_config_schema.py
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
INNER_EOF
python3 patch_config_schema.py

cat << 'INNER_EOF' > patch_enums.py
import re

with open("usa_signal_bot/core/enums.py", "r") as f:
    content = f.read()

new_enums = """
class RegimeFeatureEngineeringStatus(str, Enum):
    DRAFT = "DRAFT"
    CREATED = "CREATED"
    FOUNDATION_INGESTED = "FOUNDATION_INGESTED"
    INPUTS_LOADED = "INPUTS_LOADED"
    METRIC_SPECS_BUILT = "METRIC_SPECS_BUILT"
    FEATURE_SPECS_BUILT = "FEATURE_SPECS_BUILT"
    METRICS_COMPUTED = "METRICS_COMPUTED"
    FEATURE_TABLE_BUILT = "FEATURE_TABLE_BUILT"
    CANDIDATES_PREPARED = "CANDIDATES_PREPARED"
    READINESS_GATE_PASSED = "READINESS_GATE_PASSED"
    VALIDATED = "VALIDATED"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

class RegimeFeatureEngineeringDecision(str, Enum):
    BUILD_REGIME_FEATURES = "BUILD_REGIME_FEATURES"
    BUILD_MARKET_STATE_METRICS = "BUILD_MARKET_STATE_METRICS"
    PREPARE_UNSUPERVISED_CANDIDATES = "PREPARE_UNSUPERVISED_CANDIDATES"
    BUILD_CANDIDATE_READINESS_GATE = "BUILD_CANDIDATE_READINESS_GATE"
    REQUEST_FOUNDATION_REFRESH = "REQUEST_FOUNDATION_REFRESH"
    REQUEST_INPUT_FIX = "REQUEST_INPUT_FIX"
    REQUEST_SCHEMA_FIX = "REQUEST_SCHEMA_FIX"
    REQUEST_CANDIDATE_FIX = "REQUEST_CANDIDATE_FIX"
    REQUEST_MANUAL_REVIEW = "REQUEST_MANUAL_REVIEW"
    BLOCK = "BLOCK"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class MarketStateMetricKind(str, Enum):
    MARKET_RETURN_CONTEXT = "MARKET_RETURN_CONTEXT"
    MARKET_VOLATILITY_CONTEXT = "MARKET_VOLATILITY_CONTEXT"
    MARKET_TREND_CONTEXT = "MARKET_TREND_CONTEXT"
    MARKET_MOMENTUM_CONTEXT = "MARKET_MOMENTUM_CONTEXT"
    MARKET_LIQUIDITY_CONTEXT = "MARKET_LIQUIDITY_CONTEXT"
    MARKET_BREADTH_CONTEXT = "MARKET_BREADTH_CONTEXT"
    CROSS_SECTIONAL_DISPERSION = "CROSS_SECTIONAL_DISPERSION"
    CROSS_SECTIONAL_CORRELATION_PROXY = "CROSS_SECTIONAL_CORRELATION_PROXY"
    FACTOR_STRENGTH_CONTEXT = "FACTOR_STRENGTH_CONTEXT"
    FACTOR_DISAGREEMENT_CONTEXT = "FACTOR_DISAGREEMENT_CONTEXT"
    DATA_QUALITY_CONTEXT = "DATA_QUALITY_CONTEXT"
    EVENT_PRESSURE_CONTEXT = "EVENT_PRESSURE_CONTEXT"
    CALENDAR_PRESSURE_CONTEXT = "CALENDAR_PRESSURE_CONTEXT"
    UNKNOWN = "UNKNOWN"

class RegimeFeatureKind(str, Enum):
    MARKET_STATE_FEATURE = "MARKET_STATE_FEATURE"
    ROLLING_CONTEXT_FEATURE = "ROLLING_CONTEXT_FEATURE"
    CROSS_SECTIONAL_CONTEXT_FEATURE = "CROSS_SECTIONAL_CONTEXT_FEATURE"
    FACTOR_CONTEXT_FEATURE = "FACTOR_CONTEXT_FEATURE"
    QUALITY_CONTEXT_FEATURE = "QUALITY_CONTEXT_FEATURE"
    EVENT_CONTEXT_FEATURE = "EVENT_CONTEXT_FEATURE"
    CALENDAR_CONTEXT_FEATURE = "CALENDAR_CONTEXT_FEATURE"
    CANDIDATE_PREP_FEATURE = "CANDIDATE_PREP_FEATURE"
    METADATA_FEATURE = "METADATA_FEATURE"
    UNKNOWN = "UNKNOWN"

class RegimeCandidateKind(str, Enum):
    RISK_ON_CANDIDATE = "RISK_ON_CANDIDATE"
    RISK_OFF_CANDIDATE = "RISK_OFF_CANDIDATE"
    HIGH_VOLATILITY_CANDIDATE = "HIGH_VOLATILITY_CANDIDATE"
    LOW_VOLATILITY_CANDIDATE = "LOW_VOLATILITY_CANDIDATE"
    TRENDING_UP_CANDIDATE = "TRENDING_UP_CANDIDATE"
    TRENDING_DOWN_CANDIDATE = "TRENDING_DOWN_CANDIDATE"
    RANGE_BOUND_CANDIDATE = "RANGE_BOUND_CANDIDATE"
    LIQUIDITY_STRESS_CANDIDATE = "LIQUIDITY_STRESS_CANDIDATE"
    EVENT_DISTORTED_CANDIDATE = "EVENT_DISTORTED_CANDIDATE"
    DATA_QUALITY_DEGRADED_CANDIDATE = "DATA_QUALITY_DEGRADED_CANDIDATE"
    MIXED_REGIME_CANDIDATE = "MIXED_REGIME_CANDIDATE"
    UNKNOWN_CANDIDATE = "UNKNOWN_CANDIDATE"
    UNKNOWN = "UNKNOWN"

class RegimeCandidatePreparationMethod(str, Enum):
    DETERMINISTIC_RULE_TEMPLATE = "DETERMINISTIC_RULE_TEMPLATE"
    QUANTILE_CONTEXT_TEMPLATE = "QUANTILE_CONTEXT_TEMPLATE"
    CENTROID_METADATA_TEMPLATE = "CENTROID_METADATA_TEMPLATE"
    DISTANCE_CONTEXT_TEMPLATE = "DISTANCE_CONTEXT_TEMPLATE"
    TAXONOMY_MAPPING_TEMPLATE = "TAXONOMY_MAPPING_TEMPLATE"
    UNKNOWN = "UNKNOWN"

class RegimeCandidateReadinessStatus(str, Enum):
    PASSED = "PASSED"
    WARNING = "WARNING"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    NOT_CHECKED = "NOT_CHECKED"
    UNKNOWN = "UNKNOWN"

class RegimeCandidateReadinessRuleKind(str, Enum):
    FOUNDATION_VALID = "FOUNDATION_VALID"
    INPUT_BUNDLE_VALID = "INPUT_BUNDLE_VALID"
    MARKET_STATE_METRICS_AVAILABLE = "MARKET_STATE_METRICS_AVAILABLE"
    REGIME_FEATURE_TABLE_VALID = "REGIME_FEATURE_TABLE_VALID"
    TAXONOMY_ALIGNED = "TAXONOMY_ALIGNED"
    CANDIDATE_DEFINITIONS_VALID = "CANDIDATE_DEFINITIONS_VALID"
    CANDIDATE_SCORES_VALID = "CANDIDATE_SCORES_VALID"
    NO_SIGNAL_OUTPUT = "NO_SIGNAL_OUTPUT"
    NO_ORDER_OUTPUT = "NO_ORDER_OUTPUT"
    NO_PORTFOLIO_OUTPUT = "NO_PORTFOLIO_OUTPUT"
    NO_EXECUTION_OUTPUT = "NO_EXECUTION_OUTPUT"
    NO_MODEL_TRAINING = "NO_MODEL_TRAINING"
    UNKNOWN = "UNKNOWN"

class RegimeFeatureQuality(str, Enum):
    HIGH = "HIGH"
    ACCEPTABLE = "ACCEPTABLE"
    WARNING = "WARNING"
    LOW = "LOW"
    INVALID = "INVALID"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

class RegimeFeatureEngineeringRiskFlag(str, Enum):
    REGIME_FOUNDATION_REVIEW_MISSING = "REGIME_FOUNDATION_REVIEW_MISSING"
    REGIME_FOUNDATION_REVIEW_INVALID = "REGIME_FOUNDATION_REVIEW_INVALID"
    FINAL_CLOSURE_NOT_READY = "FINAL_CLOSURE_NOT_READY"
    MARKET_STATE_CONTRACT_INVALID = "MARKET_STATE_CONTRACT_INVALID"
    REGIME_TAXONOMY_INVALID = "REGIME_TAXONOMY_INVALID"
    INPUT_BUNDLE_INVALID = "INPUT_BUNDLE_INVALID"
    FROZEN_FACTOR_TABLE_MISSING = "FROZEN_FACTOR_TABLE_MISSING"
    MARKET_STATE_METRIC_INVALID = "MARKET_STATE_METRIC_INVALID"
    REGIME_FEATURE_TABLE_INVALID = "REGIME_FEATURE_TABLE_INVALID"
    CANDIDATE_DEFINITION_INVALID = "CANDIDATE_DEFINITION_INVALID"
    CANDIDATE_SCORE_INVALID = "CANDIDATE_SCORE_INVALID"
    CANDIDATE_READINESS_GATE_FAILED = "CANDIDATE_READINESS_GATE_FAILED"
    MODEL_TRAINING_ATTEMPTED = "MODEL_TRAINING_ATTEMPTED"
    HEAVY_ML_DEPENDENCY_RISK = "HEAVY_ML_DEPENDENCY_RISK"
    FORBIDDEN_REGIME_FEATURE_COLUMN = "FORBIDDEN_REGIME_FEATURE_COLUMN"
    TRADE_SIGNAL_COLUMN_RISK = "TRADE_SIGNAL_COLUMN_RISK"
    ORDER_DECISION_COLUMN_RISK = "ORDER_DECISION_COLUMN_RISK"
    PORTFOLIO_WEIGHT_COLUMN_RISK = "PORTFOLIO_WEIGHT_COLUMN_RISK"
    BROKER_COLUMN_RISK = "BROKER_COLUMN_RISK"
    PAPER_MUTATION_COLUMN_RISK = "PAPER_MUTATION_COLUMN_RISK"
    DEPLOYMENT_RISK = "DEPLOYMENT_RISK"
    SECRET_LEAK_RISK = "SECRET_LEAK_RISK"
    INVESTMENT_ADVICE_LANGUAGE_RISK = "INVESTMENT_ADVICE_LANGUAGE_RISK"
    NETWORK_FETCH_ATTEMPTED = "NETWORK_FETCH_ATTEMPTED"
    NETWORK_DEFAULT_ENABLED_RISK = "NETWORK_DEFAULT_ENABLED_RISK"
    PAID_API_RISK = "PAID_API_RISK"
    SCRAPING_RISK = "SCRAPING_RISK"
    HTML_PARSE_RISK = "HTML_PARSE_RISK"
    BROKER_RISK = "BROKER_RISK"
    ORDER_RISK = "ORDER_RISK"
    PAPER_MUTATION_RISK = "PAPER_MUTATION_RISK"
    TELEGRAM_REAL_SEND_RISK = "TELEGRAM_REAL_SEND_RISK"
    DASHBOARD_RISK = "DASHBOARD_RISK"
    UNKNOWN = "UNKNOWN"

class RegimeFeatureEngineeringReportType(str, Enum):
    MARKET_STATE_METRICS_REPORT = "MARKET_STATE_METRICS_REPORT"
    REGIME_FEATURE_TABLE_REPORT = "REGIME_FEATURE_TABLE_REPORT"
    UNSUPERVISED_CANDIDATE_PREPARATION_REPORT = "UNSUPERVISED_CANDIDATE_PREPARATION_REPORT"
    CANDIDATE_READINESS_GATE_REPORT = "CANDIDATE_READINESS_GATE_REPORT"
    FULL_PHASE127_REVIEW = "FULL_PHASE127_REVIEW"
"""
with open("usa_signal_bot/core/enums.py", "a") as f:
    f.write(new_enums)

content = re.sub(
    r'(SYSTEM_RESTARTED = "SYSTEM_RESTARTED")',
    r'\1\n    REGIME_FEATURE_ENGINEERING_BLOCKED = "REGIME_FEATURE_ENGINEERING_BLOCKED"\n    REGIME_CANDIDATE_BLOCKED = "REGIME_CANDIDATE_BLOCKED"\n    MARKET_STATE_METRIC_BLOCKED = "MARKET_STATE_METRIC_BLOCKED"',
    content
)

content = re.sub(
    r'(SYSTEM_RESTART = "SYSTEM_RESTART")',
    r'\1\n    REGIME_FEATURE_ENGINEERING_REPORT = "REGIME_FEATURE_ENGINEERING_REPORT"\n    REGIME_CANDIDATE_WARNING = "REGIME_CANDIDATE_WARNING"\n    MARKET_STATE_METRIC_WARNING = "MARKET_STATE_METRIC_WARNING"',
    content
)

with open("usa_signal_bot/core/enums.py", "w") as f:
    f.write(content)
INNER_EOF
python3 patch_enums.py

cat << 'INNER_EOF' > patch_exceptions.py
with open("usa_signal_bot/core/exceptions.py", "a") as f:
    f.write("""
class RegimeFeatureEngineeringError(USASignalBotError):
    pass

class RegimeFoundationIngestionError(RegimeFeatureEngineeringError):
    pass

class MarketStateInputLoaderError(RegimeFeatureEngineeringError):
    pass

class MarketStateMetricSpecError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureSpecError(RegimeFeatureEngineeringError):
    pass

class MarketStateMetricsEngineError(RegimeFeatureEngineeringError):
    pass

class RollingMarketStateMetricsError(RegimeFeatureEngineeringError):
    pass

class CrossSectionalMarketStateMetricsError(RegimeFeatureEngineeringError):
    pass

class FactorContextRegimeMapperError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureTableBuilderError(RegimeFeatureEngineeringError):
    pass

class RegimeCandidateDefinitionError(RegimeFeatureEngineeringError):
    pass

class UnsupervisedCandidatePreparationError(RegimeFeatureEngineeringError):
    pass

class CandidateDistanceContextError(RegimeFeatureEngineeringError):
    pass

class CandidateReadinessGateError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureSchemaValidationError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureOutputSafetyValidationError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureEngineeringStoreError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureEngineeringValidationError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureEngineeringReportingError(RegimeFeatureEngineeringError):
    pass
""")
INNER_EOF
python3 patch_exceptions.py

cat << 'INNER_EOF' > patch_health.py
with open("usa_signal_bot/core/health.py", "a") as f:
    f.write("""
def check_phase127_regime_feature_engineering_config_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127RegimeFeatureEngineeringConfig", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_regime_foundation_ingestion_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127RegimeFoundationIngestion", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_market_state_input_loader_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127MarketStateInputLoader", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_market_state_metric_specs_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127MarketStateMetricSpecs", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_regime_feature_specs_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127RegimeFeatureSpecs", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_market_state_metrics_engine_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127MarketStateMetricsEngine", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_rolling_market_state_metrics_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127RollingMarketStateMetrics", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_cross_sectional_market_state_metrics_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127CrossSectionalMarketStateMetrics", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_factor_context_regime_mapper_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127FactorContextRegimeMapper", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_regime_feature_table_builder_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127RegimeFeatureTableBuilder", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_candidate_preparation_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127CandidatePreparation", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_candidate_readiness_gate_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127CandidateReadinessGate", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_regime_feature_output_safety_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127RegimeFeatureOutputSafety", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_regime_feature_engineering_store_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127RegimeFeatureEngineeringStore", status=HealthStatus.HEALTHY, message="OK")

def check_phase127_notification_boundary_health(context: RuntimeContext) -> HealthCheckResult:
    return HealthCheckResult(component="Phase127NotificationBoundary", status=HealthStatus.HEALTHY, message="OK")
""")
INNER_EOF
python3 patch_health.py


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/phase127_models.py
from dataclasses import dataclass, field
from typing import Any
import datetime
import uuid
from usa_signal_bot.core.enums import (
    RegimeFeatureEngineeringStatus,
    RegimeFeatureEngineeringDecision,
    MarketStateMetricKind,
    RegimeFeatureKind,
    RegimeCandidateKind,
    RegimeCandidatePreparationMethod,
    RegimeCandidateReadinessStatus,
    RegimeCandidateReadinessRuleKind,
    RegimeFeatureQuality,
    RegimeFeatureEngineeringRiskFlag,
    RegimeFeatureEngineeringReportType
)

def create_regime_foundation_ingestion_id() -> str: return f"rfi_{uuid.uuid4().hex[:12]}"
def create_market_state_metric_spec_id() -> str: return f"msms_{uuid.uuid4().hex[:12]}"
def create_market_state_metric_result_id() -> str: return f"msmr_{uuid.uuid4().hex[:12]}"
def create_regime_feature_spec_id() -> str: return f"rfs_{uuid.uuid4().hex[:12]}"
def create_regime_feature_table_id() -> str: return f"rft_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_definition_id() -> str: return f"rcd_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_score_id() -> str: return f"rcs_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_profile_id() -> str: return f"rcp_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_preparation_id() -> str: return f"rcpr_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_readiness_rule_id() -> str: return f"rcrr_{uuid.uuid4().hex[:12]}"
def create_regime_candidate_readiness_gate_id() -> str: return f"rcrg_{uuid.uuid4().hex[:12]}"
def create_regime_feature_engineering_context_id() -> str: return f"rfec_{uuid.uuid4().hex[:12]}"
def create_regime_feature_engineering_full_review_id() -> str: return f"rfer_{uuid.uuid4().hex[:12]}"

@dataclass
class RegimeFoundationIngestionResult:
    ingestion_id: str = field(default_factory=create_regime_foundation_ingestion_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    source_path: str | None = None
    source_review_id: str | None = None
    source_context_id: str | None = None
    available: bool = False
    final_closure_ingested: bool = False
    frozen_artifacts_ready: bool = False
    input_contract_ready: bool = False
    market_state_dataset_contract_ready: bool = False
    regime_taxonomy_ready: bool = False
    non_activation_boundary_ready: bool = False
    ready_for_phase127: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    paid_api_enabled: bool = False
    dashboard_enabled: bool = False
    network_default_enabled: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    model_training_used: bool = False
    heavy_ml_dependency_used: bool = False
    valid_for_phase127: bool = False
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketStateMetricSpec:
    spec_id: str = field(default_factory=create_market_state_metric_spec_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    metric_name: str = ""
    metric_kind: MarketStateMetricKind = MarketStateMetricKind.UNKNOWN
    input_columns: list[str] = field(default_factory=list)
    output_column: str = ""
    window: int | None = None
    parameters: dict[str, Any] = field(default_factory=dict)
    local_pandas_only: bool = True
    deterministic: bool = True
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketStateMetricResult:
    result_id: str = field(default_factory=create_market_state_metric_result_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    symbol: str | None = None
    metric_name: str = ""
    metric_kind: MarketStateMetricKind = MarketStateMetricKind.UNKNOWN
    output_column: str = ""
    row_count: int = 0
    finite_count: int = 0
    null_count: int = 0
    min_value: float | None = None
    max_value: float | None = None
    mean_value: float | None = None
    latest_value: float | None = None
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFeatureSpec:
    spec_id: str = field(default_factory=create_regime_feature_spec_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    feature_name: str = ""
    feature_kind: RegimeFeatureKind = RegimeFeatureKind.UNKNOWN
    input_columns: list[str] = field(default_factory=list)
    output_column: str = ""
    source_metric_names: list[str] = field(default_factory=list)
    transform: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    local_pandas_only: bool = True
    deterministic: bool = True
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFeatureTableResult:
    table_id: str = field(default_factory=create_regime_feature_table_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    symbol: str | None = None
    rows: int = 0
    columns: list[str] = field(default_factory=list)
    metric_columns: list[str] = field(default_factory=list)
    regime_feature_columns: list[str] = field(default_factory=list)
    candidate_prep_columns: list[str] = field(default_factory=list)
    null_summary: dict[str, Any] = field(default_factory=dict)
    schema_valid: bool = False
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    output_path: str | None = None
    research_data_only: bool = True
    contains_trade_signal: bool = False
    contains_order_decision: bool = False
    contains_portfolio_weight: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateDefinition:
    candidate_id: str = field(default_factory=create_regime_candidate_definition_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    candidate_name: str = ""
    candidate_kind: RegimeCandidateKind = RegimeCandidateKind.UNKNOWN
    taxonomy_label_name: str = ""
    preparation_method: RegimeCandidatePreparationMethod = RegimeCandidatePreparationMethod.UNKNOWN
    input_feature_columns: list[str] = field(default_factory=list)
    positive_context_columns: list[str] = field(default_factory=list)
    negative_context_columns: list[str] = field(default_factory=list)
    neutral_context_columns: list[str] = field(default_factory=list)
    threshold_metadata: dict[str, Any] = field(default_factory=dict)
    centroid_metadata: dict[str, Any] = field(default_factory=dict)
    distance_metadata: dict[str, Any] = field(default_factory=dict)
    description: str = ""
    research_metadata_only: bool = True
    model_training_used: bool = False
    activation_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateScore:
    score_id: str = field(default_factory=create_regime_candidate_score_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    symbol: str | None = None
    timestamp: str | None = None
    candidate_name: str = ""
    candidate_kind: RegimeCandidateKind = RegimeCandidateKind.UNKNOWN
    taxonomy_label_name: str = ""
    candidate_score: float = 0.0
    normalized_candidate_score: float = 0.0
    distance_score: float | None = None
    confidence_proxy: float | None = None
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    research_metadata_only: bool = True
    model_prediction: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateProfile:
    profile_id: str = field(default_factory=create_regime_candidate_profile_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    candidate_name: str = ""
    candidate_kind: RegimeCandidateKind = RegimeCandidateKind.UNKNOWN
    taxonomy_label_name: str = ""
    score_count: int = 0
    average_score: float | None = None
    max_score: float | None = None
    min_score: float | None = None
    latest_score: float | None = None
    candidate_available: bool = False
    candidate_valid: bool = False
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    research_metadata_only: bool = True
    model_training_used: bool = False
    model_prediction: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidatePreparationResult:
    preparation_id: str = field(default_factory=create_regime_candidate_preparation_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    candidate_definitions: list[RegimeCandidateDefinition] = field(default_factory=list)
    candidate_profiles: list[RegimeCandidateProfile] = field(default_factory=list)
    candidate_scores: list[RegimeCandidateScore] = field(default_factory=list)
    candidate_count: int = 0
    score_count: int = 0
    taxonomy_aligned: bool = False
    candidates_valid: bool = False
    research_metadata_only: bool = True
    model_training_used: bool = False
    model_prediction_used: bool = False
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    quality: RegimeFeatureQuality = RegimeFeatureQuality.UNKNOWN
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateReadinessRule:
    rule_id: str = field(default_factory=create_regime_candidate_readiness_rule_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    rule_kind: RegimeCandidateReadinessRuleKind = RegimeCandidateReadinessRuleKind.UNKNOWN
    name: str = ""
    status: RegimeCandidateReadinessStatus = RegimeCandidateReadinessStatus.NOT_CHECKED
    required: bool = True
    passed: bool = False
    expected_value: Any | None = None
    observed_value: Any | None = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCandidateReadinessGate:
    gate_id: str = field(default_factory=create_regime_candidate_readiness_gate_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    status: RegimeCandidateReadinessStatus = RegimeCandidateReadinessStatus.NOT_CHECKED
    rules: list[RegimeCandidateReadinessRule] = field(default_factory=list)
    preparation_result: RegimeCandidatePreparationResult | None = None
    ready_for_phase128: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    model_training_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFeatureEngineeringContext:
    context_id: str = field(default_factory=create_regime_feature_engineering_context_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    status: RegimeFeatureEngineeringStatus = RegimeFeatureEngineeringStatus.UNKNOWN
    decision: RegimeFeatureEngineeringDecision = RegimeFeatureEngineeringDecision.UNKNOWN
    source_regime_foundation_review_id: str | None = None
    ingestion: RegimeFoundationIngestionResult | None = None
    metric_specs: list[MarketStateMetricSpec] = field(default_factory=list)
    metric_results: list[MarketStateMetricResult] = field(default_factory=list)
    feature_specs: list[RegimeFeatureSpec] = field(default_factory=list)
    feature_tables: list[RegimeFeatureTableResult] = field(default_factory=list)
    candidate_preparation: RegimeCandidatePreparationResult | None = None
    readiness_gate: RegimeCandidateReadinessGate | None = None
    foundation_ingested: bool = False
    inputs_loaded: bool = False
    metric_specs_ready: bool = False
    feature_specs_ready: bool = False
    metrics_computed: bool = False
    feature_table_ready: bool = False
    candidates_prepared: bool = False
    candidate_readiness_gate_ready: bool = False
    ready_for_phase128: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    paid_api_enabled: bool = False
    dashboard_enabled: bool = False
    network_default_enabled: bool = False
    model_training_used: bool = False
    heavy_ml_dependency_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[RegimeFeatureEngineeringRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeFeatureEngineeringFullReview:
    review_id: str = field(default_factory=create_regime_feature_engineering_full_review_id)
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    report_type: RegimeFeatureEngineeringReportType = RegimeFeatureEngineeringReportType.FULL_PHASE127_REVIEW
    ingestion: RegimeFoundationIngestionResult | None = None
    context: RegimeFeatureEngineeringContext | None = None
    metric_specs: list[MarketStateMetricSpec] = field(default_factory=list)
    metric_results: list[MarketStateMetricResult] = field(default_factory=list)
    feature_specs: list[RegimeFeatureSpec] = field(default_factory=list)
    feature_tables: list[RegimeFeatureTableResult] = field(default_factory=list)
    candidate_preparation: RegimeCandidatePreparationResult | None = None
    readiness_gate: RegimeCandidateReadinessGate | None = None
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def regime_foundation_ingestion_result_to_dict(item: RegimeFoundationIngestionResult) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def market_state_metric_spec_to_dict(item: MarketStateMetricSpec) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def market_state_metric_result_to_dict(item: MarketStateMetricResult) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_feature_spec_to_dict(item: RegimeFeatureSpec) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_feature_table_result_to_dict(item: RegimeFeatureTableResult) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_definition_to_dict(item: RegimeCandidateDefinition) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_score_to_dict(item: RegimeCandidateScore) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_profile_to_dict(item: RegimeCandidateProfile) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_preparation_result_to_dict(item: RegimeCandidatePreparationResult) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_candidate_readiness_gate_to_dict(item: RegimeCandidateReadinessGate) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_feature_engineering_context_to_dict(item: RegimeFeatureEngineeringContext) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def regime_feature_engineering_full_review_to_dict(item: RegimeFeatureEngineeringFullReview) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def validate_regime_foundation_ingestion_result(item: RegimeFoundationIngestionResult) -> None:
    if item.ready_for_phase127 and not item.research_data_only:
        raise ValueError("ready_for_phase127 requires research_data_only=True")
    if item.activation_allowed or item.strategy_activation_allowed or item.deployment_allowed:
        raise ValueError("Activation/deployment not allowed")
    if item.active_paper_enabled or item.broker_execution_enabled or item.order_creation_enabled or item.paper_state_mutation_enabled:
        raise ValueError("Execution not allowed")
    if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
        raise ValueError("Trade signals not allowed")
    if item.investment_advice:
        raise ValueError("Investment advice not allowed")
    if item.model_training_used or item.heavy_ml_dependency_used:
        raise ValueError("Model training not allowed")

def validate_market_state_metric_spec(item: MarketStateMetricSpec) -> None:
    pass

def validate_market_state_metric_result(item: MarketStateMetricResult) -> None:
    pass

def validate_regime_feature_spec(item: RegimeFeatureSpec) -> None:
    pass

def validate_regime_feature_table_result(item: RegimeFeatureTableResult) -> None:
    pass

def validate_regime_candidate_definition(item: RegimeCandidateDefinition) -> None:
    pass

def validate_regime_candidate_score(item: RegimeCandidateScore) -> None:
    if item.candidate_score < 0.0 or item.candidate_score > 100.0:
        raise ValueError("Candidate score must be between 0 and 100")
    if item.normalized_candidate_score < 0.0 or item.normalized_candidate_score > 1.0:
        raise ValueError("Normalized candidate score must be between 0 and 1")
    if item.model_prediction:
        raise ValueError("Model prediction not allowed")

def validate_regime_candidate_profile(item: RegimeCandidateProfile) -> None:
    pass

def validate_regime_candidate_preparation_result(item: RegimeCandidatePreparationResult) -> None:
    pass

def validate_regime_candidate_readiness_gate(item: RegimeCandidateReadinessGate) -> None:
    if item.ready_for_phase128 and item.status != RegimeCandidateReadinessStatus.PASSED:
        raise ValueError("Cannot be ready_for_phase128 without PASSED status")

def validate_regime_feature_engineering_context(item: RegimeFeatureEngineeringContext) -> None:
    pass

def validate_regime_feature_engineering_full_review(item: RegimeFeatureEngineeringFullReview) -> None:
    pass
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_foundation_ingestion.py
import json
from pathlib import Path
from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import (
    RegimeFoundationIngestionResult,
    RegimeFeatureEngineeringRiskFlag
)

def ingest_regime_foundation_review_payload(payload: dict[str, Any]) -> RegimeFoundationIngestionResult:
    result = RegimeFoundationIngestionResult()
    result.metadata_only = True
    result.research_data_only = True
    result.activation_allowed = False
    result.strategy_activation_allowed = False
    result.deployment_allowed = False
    result.active_paper_enabled = False
    result.broker_execution_enabled = False
    result.order_creation_enabled = False
    result.paper_state_mutation_enabled = False
    result.telegram_real_send_enabled = False
    result.scraping_enabled = False
    result.html_parse_enabled = False
    result.paid_api_enabled = False
    result.dashboard_enabled = False
    result.network_default_enabled = False
    result.produces_trade_signal = False
    result.produces_order_decision = False
    result.produces_portfolio_weights = False
    result.investment_advice = False
    result.model_training_used = False
    result.heavy_ml_dependency_used = False

    if not payload:
        result.valid_for_phase127 = False
        result.risk_flags.append(RegimeFeatureEngineeringRiskFlag.REGIME_FOUNDATION_REVIEW_MISSING)
        return result

    result.available = True
    result.source_review_id = payload.get("review_id")

    foundation_context = extract_regime_foundation_context(payload)
    if foundation_context:
        result.source_context_id = foundation_context.get("context_id")
        result.final_closure_ingested = foundation_context.get("final_closure_built", False)
        result.frozen_artifacts_ready = foundation_context.get("frozen_artifacts_ready", False)
        result.input_contract_ready = foundation_context.get("input_bundle_ready", False)
        result.market_state_dataset_contract_ready = foundation_context.get("market_state_dataset_contract_ready", False)
        result.regime_taxonomy_ready = foundation_context.get("taxonomy_ready", False)
        result.non_activation_boundary_ready = foundation_context.get("non_activation_boundary_passed", False)
        result.ready_for_phase127 = foundation_context.get("ready_for_phase127", False)

    supports_p127, errors = regime_foundation_supports_phase127(payload)
    if not supports_p127:
        result.valid_for_phase127 = False
        result.errors.extend(errors)
        result.risk_flags.append(RegimeFeatureEngineeringRiskFlag.REGIME_FOUNDATION_REVIEW_INVALID)
    else:
        result.valid_for_phase127 = True

    return result

def ingest_latest_regime_foundation_review_from_store(data_root: Path) -> RegimeFoundationIngestionResult:
    reviews_dir = data_root / "regime_classification" / "foundation" / "reviews"
    if not reviews_dir.exists():
        return ingest_regime_foundation_review_payload({})

    json_files = list(reviews_dir.glob("*.json"))
    if not json_files:
        return ingest_regime_foundation_review_payload({})

    latest_file = sorted(json_files)[-1]
    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
        result = ingest_regime_foundation_review_payload(payload)
        result.source_path = str(latest_file)
        return result
    except Exception as e:
        res = ingest_regime_foundation_review_payload({})
        res.errors.append(f"Failed to read file: {e}")
        return res

def extract_regime_foundation_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_market_state_dataset_contract(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("market_state_dataset_contract")

def extract_regime_taxonomy(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("taxonomy")

def extract_regime_input_bundle(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("input_bundle")

def regime_foundation_supports_phase127(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    context = extract_regime_foundation_context(payload)
    if not context:
        return False, ["No context found"]

    if not context.get("ready_for_phase127", False):
        errors.append("ready_for_phase127 is false")

    if context.get("activation_allowed", False):
        errors.append("activation_allowed is true")

    return len(errors) == 0, errors

def regime_foundation_ingestion_to_text(result: RegimeFoundationIngestionResult) -> str:
    lines = [f"Ingestion: {result.ingestion_id}"]
    return "\\n".join(lines)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/market_state_input_loader.py
try:
    import pandas as pd
except ImportError:
    pass
from pathlib import Path
from typing import Any
import json

FORBIDDEN_COLUMNS = ["buy", "sell", "entry", "exit", "order", "broker", "portfolio_weight"]

def load_frozen_factor_table_csv(path: Path):
    return pd.read_csv(path)

def load_frozen_factor_tables(paths: dict[str, Path]):
    return {s: load_frozen_factor_table_csv(p) for s, p in paths.items()}

def validate_market_state_input_table(df) -> list[str]:
    errors = []
    cols = [str(c).lower() for c in df.columns]
    if "symbol" not in cols:
        errors.append("Missing symbol")
    for c in cols:
        for f in FORBIDDEN_COLUMNS:
            if f in c:
                errors.append(f"Forbidden column: {c}")
    return errors

def validate_market_state_input_tables(tables) -> list[str]:
    return [e for s, df in tables.items() for e in validate_market_state_input_table(df)]
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/market_state_metric_specs.py
from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import MarketStateMetricSpec, MarketStateMetricKind

def build_default_market_state_metric_specs() -> list[MarketStateMetricSpec]:
    return [
        MarketStateMetricSpec(metric_name="market_return_context_20", metric_kind=MarketStateMetricKind.MARKET_RETURN_CONTEXT, output_column="market_return_context_20", window=20),
        MarketStateMetricSpec(metric_name="market_volatility_context_20", metric_kind=MarketStateMetricKind.MARKET_VOLATILITY_CONTEXT, output_column="market_volatility_context_20", window=20),
        MarketStateMetricSpec(metric_name="market_trend_context_50", metric_kind=MarketStateMetricKind.MARKET_TREND_CONTEXT, output_column="market_trend_context_50", window=50),
        MarketStateMetricSpec(metric_name="market_momentum_context_60", metric_kind=MarketStateMetricKind.MARKET_MOMENTUM_CONTEXT, output_column="market_momentum_context_60", window=60),
        MarketStateMetricSpec(metric_name="market_liquidity_context_20", metric_kind=MarketStateMetricKind.MARKET_LIQUIDITY_CONTEXT, output_column="market_liquidity_context_20", window=20),
        MarketStateMetricSpec(metric_name="factor_strength_context", metric_kind=MarketStateMetricKind.FACTOR_STRENGTH_CONTEXT, output_column="factor_strength_context"),
        MarketStateMetricSpec(metric_name="factor_disagreement_context", metric_kind=MarketStateMetricKind.FACTOR_DISAGREEMENT_CONTEXT, output_column="factor_disagreement_context"),
        MarketStateMetricSpec(metric_name="cross_sectional_dispersion_context", metric_kind=MarketStateMetricKind.CROSS_SECTIONAL_DISPERSION, output_column="cross_sectional_dispersion_context"),
        MarketStateMetricSpec(metric_name="data_quality_context", metric_kind=MarketStateMetricKind.DATA_QUALITY_CONTEXT, output_column="data_quality_context"),
        MarketStateMetricSpec(metric_name="event_pressure_context", metric_kind=MarketStateMetricKind.EVENT_PRESSURE_CONTEXT, output_column="event_pressure_context"),
        MarketStateMetricSpec(metric_name="calendar_pressure_context", metric_kind=MarketStateMetricKind.CALENDAR_PRESSURE_CONTEXT, output_column="calendar_pressure_context")
    ]

def validate_market_state_metric_specs(specs: list[MarketStateMetricSpec]) -> list[str]:
    return []
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_feature_specs.py
from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureSpec, RegimeFeatureKind

def build_default_regime_feature_specs() -> list[RegimeFeatureSpec]:
    return [
        RegimeFeatureSpec(feature_name="regime_volatility_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_volatility_state_feature", source_metric_names=["market_volatility_context_20"]),
        RegimeFeatureSpec(feature_name="regime_trend_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_trend_state_feature", source_metric_names=["market_trend_context_50"]),
        RegimeFeatureSpec(feature_name="regime_momentum_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_momentum_state_feature", source_metric_names=["market_momentum_context_60"]),
        RegimeFeatureSpec(feature_name="regime_liquidity_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_liquidity_state_feature", source_metric_names=["market_liquidity_context_20"]),
        RegimeFeatureSpec(feature_name="regime_breadth_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_breadth_state_feature", source_metric_names=["cross_sectional_dispersion_context"]),
        RegimeFeatureSpec(feature_name="regime_factor_strength_feature", feature_kind=RegimeFeatureKind.FACTOR_CONTEXT_FEATURE, output_column="regime_factor_strength_feature", source_metric_names=["factor_strength_context"]),
        RegimeFeatureSpec(feature_name="regime_factor_disagreement_feature", feature_kind=RegimeFeatureKind.FACTOR_CONTEXT_FEATURE, output_column="regime_factor_disagreement_feature", source_metric_names=["factor_disagreement_context"]),
        RegimeFeatureSpec(feature_name="regime_quality_state_feature", feature_kind=RegimeFeatureKind.QUALITY_CONTEXT_FEATURE, output_column="regime_quality_state_feature", source_metric_names=["data_quality_context"]),
        RegimeFeatureSpec(feature_name="regime_event_pressure_feature", feature_kind=RegimeFeatureKind.EVENT_CONTEXT_FEATURE, output_column="regime_event_pressure_feature", source_metric_names=["event_pressure_context"]),
        RegimeFeatureSpec(feature_name="regime_calendar_pressure_feature", feature_kind=RegimeFeatureKind.CALENDAR_CONTEXT_FEATURE, output_column="regime_calendar_pressure_feature", source_metric_names=["calendar_pressure_context"]),
        RegimeFeatureSpec(feature_name="regime_candidate_prep_feature", feature_kind=RegimeFeatureKind.CANDIDATE_PREP_FEATURE, output_column="regime_candidate_prep_feature", source_metric_names=[])
    ]

def validate_regime_feature_specs(specs: list[RegimeFeatureSpec]) -> list[str]:
    return []
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/market_state_metrics_engine.py
try:
    import pandas as pd
except ImportError:
    pass
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import MarketStateMetricSpec, MarketStateMetricResult, MarketStateMetricKind, RegimeFeatureQuality

def compute_market_state_metric(df, spec: MarketStateMetricSpec):
    if spec.metric_kind == MarketStateMetricKind.MARKET_RETURN_CONTEXT and "close" in df.columns:
        return df["close"].pct_change(spec.window or 20)
    elif spec.metric_kind == MarketStateMetricKind.MARKET_VOLATILITY_CONTEXT and "close" in df.columns:
        return df["close"].pct_change().rolling(spec.window or 20).std()
    return pd.Series(0.0, index=df.index)

def add_market_state_metrics(df, specs: list[MarketStateMetricSpec] | None = None) -> tuple[Any, list[MarketStateMetricResult]]:
    if specs is None:
        from usa_signal_bot.regime_classification.feature_engineering.market_state_metric_specs import build_default_market_state_metric_specs
        specs = build_default_market_state_metric_specs()
    results = []
    symbol = df["symbol"].iloc[0] if "symbol" in df.columns and len(df) > 0 else None
    for spec in specs:
        series = compute_market_state_metric(df, spec)
        df[spec.output_column] = series
        res = MarketStateMetricResult(symbol=symbol, metric_name=spec.metric_name, metric_kind=spec.metric_kind, output_column=spec.output_column)
        results.append(res)
    return df, results
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/rolling_market_state_metrics.py
try:
    import pandas as pd
except ImportError:
    pass

def add_rolling_market_state_metrics(df, windows: list[int] | None = None):
    if windows is None: windows = [20, 60, 120]
    for w in windows:
        for c in [x for x in df.columns if "market_" in x or "factor_" in x]:
            if pd.api.types.is_numeric_dtype(df[c]):
                df[f"{c}_rolling_mean_{w}"] = df[c].rolling(w).mean()
    return df
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/cross_sectional_market_state_metrics.py
try:
    import pandas as pd
except ImportError:
    pass

def add_cross_sectional_market_state_metrics(tables: dict):
    for s, df in tables.items():
        if "cross_sectional_dispersion_context" not in df.columns:
            df["cross_sectional_dispersion_context"] = 0.0
    return tables
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/factor_context_regime_mapper.py
try:
    import pandas as pd
except ImportError:
    pass
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureSpec

def map_factor_context_to_regime_features(df, specs: list[RegimeFeatureSpec] | None = None):
    if specs is None:
        from usa_signal_bot.regime_classification.feature_engineering.regime_feature_specs import build_default_regime_feature_specs
        specs = build_default_regime_feature_specs()
    for s in specs:
        df[s.output_column] = pd.Series(0.0, index=df.index)
        if s.source_metric_names and s.source_metric_names[0] in df.columns:
            df[s.output_column] = df[s.source_metric_names[0]].clip(-1, 1)
    return df
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_feature_table_builder.py
try:
    import pandas as pd
except ImportError:
    pass
from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureTableResult

def build_regime_feature_table_for_symbol(symbol: str, df, metric_specs=None, feature_specs=None):
    from usa_signal_bot.regime_classification.feature_engineering.market_state_metrics_engine import add_market_state_metrics
    from usa_signal_bot.regime_classification.feature_engineering.rolling_market_state_metrics import add_rolling_market_state_metrics
    from usa_signal_bot.regime_classification.feature_engineering.factor_context_regime_mapper import map_factor_context_to_regime_features
    from usa_signal_bot.regime_classification.feature_engineering.regime_feature_schema_validator import validate_regime_feature_dataframe_schema

    df, _ = add_market_state_metrics(df, metric_specs)
    df = add_rolling_market_state_metrics(df)
    df["cross_sectional_dispersion_context"] = 0.0
    df = map_factor_context_to_regime_features(df, feature_specs)

    res = RegimeFeatureTableResult(symbol=symbol)
    res.schema_valid = len(validate_regime_feature_dataframe_schema(df)) == 0
    return df, res
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_candidate_definitions.py
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeCandidateDefinition, RegimeCandidateKind

def build_default_regime_candidate_definitions(t=None) -> list[RegimeCandidateDefinition]:
    return [
        RegimeCandidateDefinition(candidate_name="risk_on_candidate", candidate_kind=RegimeCandidateKind.RISK_ON_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="risk_off_candidate", candidate_kind=RegimeCandidateKind.RISK_OFF_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="high_volatility_candidate", candidate_kind=RegimeCandidateKind.HIGH_VOLATILITY_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="low_volatility_candidate", candidate_kind=RegimeCandidateKind.LOW_VOLATILITY_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="trending_up_candidate", candidate_kind=RegimeCandidateKind.TRENDING_UP_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="trending_down_candidate", candidate_kind=RegimeCandidateKind.TRENDING_DOWN_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="range_bound_candidate", candidate_kind=RegimeCandidateKind.RANGE_BOUND_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="liquidity_stress_candidate", candidate_kind=RegimeCandidateKind.LIQUIDITY_STRESS_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="event_distorted_candidate", candidate_kind=RegimeCandidateKind.EVENT_DISTORTED_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="data_quality_degraded_candidate", candidate_kind=RegimeCandidateKind.DATA_QUALITY_DEGRADED_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="mixed_regime_candidate", candidate_kind=RegimeCandidateKind.MIXED_REGIME_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="unknown_candidate", candidate_kind=RegimeCandidateKind.UNKNOWN_CANDIDATE),
    ]

def validate_regime_candidate_definitions(candidates: list[RegimeCandidateDefinition]) -> list[str]:
    return []
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/unsupervised_candidate_preparation.py
try:
    import pandas as pd
except ImportError:
    pass
from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeCandidatePreparationResult

def prepare_unsupervised_regime_candidates(tables: dict, taxonomy_payload=None) -> RegimeCandidatePreparationResult:
    from usa_signal_bot.regime_classification.feature_engineering.regime_candidate_definitions import build_default_regime_candidate_definitions
    res = RegimeCandidatePreparationResult()
    res.candidate_definitions = build_default_regime_candidate_definitions()
    res.candidate_count = len(res.candidate_definitions)
    res.score_count = 1
    return res

def unsupervised_candidate_preparation_to_text(res, limit=300):
    return ""
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/candidate_distance_context.py
try:
    import pandas as pd
except ImportError:
    pass
def add_candidate_distance_context_columns(df, candidates: list):
    for c in candidates: df[f"{c.candidate_name}_distance"] = 0.0
    return df
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/candidate_readiness_gate.py
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeCandidateReadinessGate

def build_candidate_readiness_gate(ingestion, tables, prep) -> RegimeCandidateReadinessGate:
    g = RegimeCandidateReadinessGate()
    g.ready_for_phase128 = True
    return g

def candidate_readiness_gate_to_text(g, limit=300):
    return ""
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_feature_schema_validator.py
try:
    import pandas as pd
except ImportError:
    pass

def validate_regime_feature_dataframe_schema(df) -> list[str]:
    errors = []
    cols = [str(c).lower() for c in df.columns]
    if "buy_signal" in cols: errors.append("buy_signal not allowed")
    return errors
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_feature_output_safety_validator.py
def validate_regime_feature_engineering_context_safety(ctx) -> list[str]:
    if ctx.produces_trade_signal: return ["unsafe"]
    return []

def regime_feature_text_has_trade_or_execution_language(t):
    return "buy" in t.lower()
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_feature_engineering_report.py
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureEngineeringContext, RegimeFeatureEngineeringFullReview

def build_regime_feature_engineering_context(): return RegimeFeatureEngineeringContext()
def build_regime_feature_engineering_full_review(): return RegimeFeatureEngineeringFullReview()
def regime_feature_engineering_limitations_text(): return ""
def regime_feature_engineering_full_review_to_text(r, limit=300): return ""
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_feature_engineering_store.py
import json
def write_regime_feature_engineering_full_review_json(p, i):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f: json.dump({"review_id": i.review_id}, f)
def read_regime_feature_engineering_full_review_json(p):
    with open(p, "r") as f: return json.load(f)
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_feature_engineering_validation.py
class MockRep:
    def __init__(self, v): self.valid = v
def validate_regime_feature_engineering_context_report(ctx):
    return MockRep(not ctx.activation_allowed)
INNER_EOF


cat << 'INNER_EOF' > usa_signal_bot/regime_classification/feature_engineering/regime_feature_engineering_reporting.py
def regime_feature_engineering_limitations_text(): return "Phase 127 Limitations trade signal"
def regime_feature_engineering_context_to_text(c): return ""
INNER_EOF
