"""Data classes representing the configuration schema."""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class ProjectConfig:
    name: str = "USA Signal Bot"
    version: str = "0.2.0"
    timezone: str = "America/New_York"

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class RuntimeConfig:
    notification_step_enabled: bool = False
    mode: str = "local_paper_only"
    broker_order_routing_enabled: bool = False
    web_scraping_allowed: bool = False
    dashboard_enabled: bool = False
    dry_run: bool = True
    fail_fast: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class DataConfig:
    root_dir: str = "data"
    cache_dir: str = "data/cache"
    raw_dir: str = "data/raw"
    processed_dir: str = "data/processed"
    universe_dir: str = "data/universe"
    max_download_workers: int = 4
    request_timeout_seconds: int = 30
    retry_attempts: int = 3

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class LoggingConfig:
    level: str = "INFO"
    log_dir: str = "data/logs"
    log_file: str = "app.log"
    enable_console: bool = True
    enable_file: bool = True
    max_bytes: int = 5000000
    backup_count: int = 5

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class UniverseConfig:
    asset_types: List[str] = field(default_factory=lambda: ["stock", "etf"])
    default_watchlist_file: str = "data/universe/watchlist.csv"
    include_etfs: bool = True
    include_stocks: bool = True
    min_price: float = 1.0
    max_symbols_per_scan: int = 500
    allow_inactive_symbols: bool = False
    symbol_max_length: int = 15
    default_currency: str = "USD"
    snapshot_file: str = "data/universe/default_universe.csv"
    imports_dir: str = "data/universe/imports"
    snapshots_dir: str = "data/universe/snapshots"
    catalog_dir: str = "data/universe/catalog"
    presets_dir: str = "data/universe/presets"
    exports_dir: str = "data/universe/exports"
    active_snapshot_file: str = "data/universe/catalog/active_snapshot.json"
    default_conflict_resolution: str = "prefer_complete_metadata"
    max_import_file_size_mb: int = 25
    allow_reserved_external_sources: bool = False

    def __post_init__(self):
        if not self.imports_dir:
            raise ValueError("imports_dir cannot be empty")
        if not self.snapshots_dir:
            raise ValueError("snapshots_dir cannot be empty")
        if not self.catalog_dir:
            raise ValueError("catalog_dir cannot be empty")
        if not self.presets_dir:
            raise ValueError("presets_dir cannot be empty")
        if not self.exports_dir:
            raise ValueError("exports_dir cannot be empty")
        if not self.active_snapshot_file:
            raise ValueError("active_snapshot_file cannot be empty")

        valid_resolutions = ["first_wins", "last_wins", "prefer_active", "prefer_complete_metadata", "error_on_conflict"]
        if self.default_conflict_resolution.lower() not in valid_resolutions:
            raise ValueError(f"default_conflict_resolution must be one of {valid_resolutions}")

        if self.max_import_file_size_mb <= 0:
            raise ValueError("max_import_file_size_mb must be positive")

        if self.allow_reserved_external_sources:
             raise ValueError("allow_reserved_external_sources must be False in this phase")

        if not self.include_stocks and not self.include_etfs:
            raise ValueError("Both include_stocks and include_etfs cannot be False")

        if self.symbol_max_length <= 1:
            raise ValueError("symbol_max_length must be greater than 1")

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class PaperConfig:
    initial_cash: float = 100000.0
    currency: str = "USD"
    allow_short: bool = False
    commission_per_trade: float = 0.0
    slippage_bps: float = 5.0

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class RiskConfig:
    max_position_pct: float = 0.10
    max_total_exposure_pct: float = 0.80
    max_daily_loss_pct: float = 0.03
    max_open_positions: int = 10

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class BacktestConfig:
    default_initial_cash: float = 100000.0
    default_benchmark: str = "SPY"
    include_transaction_costs: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class OptimizationConfig:
    enabled: bool = False
    max_trials: int = 100
    walk_forward_enabled: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class RegimeConfig:
    enabled: bool = False
    default_market_proxy: str = "SPY"

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class MLConfig:
    enabled: bool = False
    model_dir: str = "data/models"
    leakage_checks_enabled: bool = True


@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class StorageConfig:
    enabled: bool = True
    manifests_dir: str = "data/manifests"
    features_dir: str = "data/features"
    models_dir: str = "data/models"
    atomic_writes: bool = True
    default_json_indent: int = 2
    parquet_enabled: bool = False


@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class ProviderConfig:
    default_provider: str = "yfinance"
    enabled_providers: List[str] = field(default_factory=lambda: ["mock", "yfinance"])
    allow_paid_providers: bool = False
    allow_scraping_providers: bool = False
    allow_broker_data_providers: bool = False
    request_timeout_seconds: int = 30
    max_symbols_per_batch: int = 25
    min_seconds_between_requests: float = 1.0
    cache_enabled: bool = True
    cache_ttl_seconds: int = 86400
    yfinance_enabled: bool = True
    yfinance_threads: bool = True
    yfinance_auto_adjust: bool = False
    yfinance_progress: bool = False


@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class DataQualityConfig:
    enabled: bool = True
    allow_zero_volume: bool = True
    allow_warnings: bool = True
    repair_enabled: bool = True
    drop_invalid_price_bars: bool = True
    drop_duplicate_bars: bool = True
    fill_missing_volume_with_zero: bool = True
    max_allowed_warning_ratio: float = 0.20
    block_on_errors: bool = True

    def __post_init__(self):
        if not (0 <= self.max_allowed_warning_ratio <= 1):
            raise ValueError("max_allowed_warning_ratio must be between 0 and 1")
        if not self.enabled:
            raise ValueError("data_quality.enabled must be True")

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class CacheRefreshConfig:
    enabled: bool = True
    default_ttl_seconds: int = 86400
    force_refresh_default: bool = False
    validate_cache_before_use: bool = True
    repair_cache_before_use: bool = True
    max_cache_age_days_daily: int = 3
    max_cache_age_days_intraday: int = 1

    def __post_init__(self):
        if self.default_ttl_seconds < 0:
            raise ValueError("default_ttl_seconds cannot be negative")
        if self.max_cache_age_days_daily <= 0:
            raise ValueError("max_cache_age_days_daily must be positive")
        if self.max_cache_age_days_intraday <= 0:
            raise ValueError("max_cache_age_days_intraday must be positive")
        if not self.enabled:
            raise ValueError("cache_refresh.enabled must be True")


@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class MultiTimeframeConfig:
    enabled: bool = True
    default_timeframes: List[str] = field(default_factory=lambda: ["1d", "1h", "15m"])
    primary_timeframe: str = "1d"
    confirmation_timeframes: List[str] = field(default_factory=lambda: ["1h"])
    intraday_timeframes: List[str] = field(default_factory=lambda: ["15m"])
    max_timeframes_per_run: int = 4
    max_symbols_per_multitimeframe_run: int = 50

    def __post_init__(self):
        if not self.default_timeframes:
            raise ValueError("default_timeframes cannot be empty")
        if self.primary_timeframe not in self.default_timeframes:
            raise ValueError("primary_timeframe must be in default_timeframes")
        if self.max_timeframes_per_run <= 0:
            raise ValueError("max_timeframes_per_run must be positive")
        if self.max_symbols_per_multitimeframe_run <= 0:
            raise ValueError("max_symbols_per_multitimeframe_run must be positive")

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class DataReadinessConfig:
    enabled: bool = True
    min_ready_pair_ratio: float = 0.70
    min_symbol_coverage_ratio: float = 0.70
    require_primary_timeframe: bool = True
    allow_partial_intraday: bool = True
    max_error_count: int = 0
    max_warning_ratio: float = 0.30
    write_reports: bool = True

    def __post_init__(self):
        if not (0 <= self.min_ready_pair_ratio <= 1):
            raise ValueError("min_ready_pair_ratio must be between 0 and 1")
        if not (0 <= self.min_symbol_coverage_ratio <= 1):
            raise ValueError("min_symbol_coverage_ratio must be between 0 and 1")
        if self.max_error_count < 0:
            raise ValueError("max_error_count cannot be negative")
        if not (0 <= self.max_warning_ratio <= 1):
            raise ValueError("max_warning_ratio must be between 0 and 1")

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class ActiveUniverseConfig:
    enabled: bool = True
    prefer_active_snapshot: bool = True
    fallback_to_latest_snapshot: bool = True
    fallback_to_watchlist: bool = True
    max_symbols_per_run: int = 200
    default_asset_type_filter: Optional[str] = None
    write_resolution_report: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class UniverseReadinessGateConfig:
    enabled: bool = True
    min_symbol_score: float = 70.0
    min_required_timeframes: int = 1
    required_primary_timeframe: str = "1d"
    allow_partial_symbols: bool = True
    min_eligible_symbol_ratio: float = 0.60
    max_failed_symbol_ratio: float = 0.30
    write_eligible_outputs: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class UniverseRunsConfig:
    enabled: bool = True
    runs_dir: str = "data/universe/runs"
    readiness_dir: str = "data/universe/readiness"
    keep_last_n_runs: int = 50


@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class TrendFeatureConfig:
    enabled: bool = True
    default_indicator_set: str = "basic_trend"
    available_indicator_sets: List[str] = field(default_factory=lambda: ["basic_trend", "moving_average_trend", "macd_trend", "full_trend"])
    default_ma_windows: List[int] = field(default_factory=lambda: [20, 50, 200])
    default_macd_fast: int = 12
    default_macd_slow: int = 26
    default_macd_signal: int = 9
    max_window: int = 500
    allow_partial_trend_features: bool = True

    def __post_init__(self):
        if not self.available_indicator_sets:
            raise ValueError("available_indicator_sets cannot be empty")
        if self.default_indicator_set not in self.available_indicator_sets:
            raise ValueError("default_indicator_set must be in available_indicator_sets")
        if not self.default_ma_windows or not all(isinstance(x, int) and x > 0 for x in self.default_ma_windows):
            raise ValueError("default_ma_windows must be a list of positive integers")
        if self.max_window <= 0:
            raise ValueError("max_window must be positive")
        if any(w > self.max_window for w in self.default_ma_windows):
            raise ValueError("Values in default_ma_windows cannot exceed max_window")
        if self.default_macd_fast >= self.default_macd_slow:
            raise ValueError("MACD fast must be less than slow")
        if self.default_macd_signal <= 0:
            raise ValueError("MACD signal must be positive")


@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class MomentumFeatureConfig:
    enabled: bool = True
    default_indicator_set: str = "basic_momentum"
    available_indicator_sets: List[str] = field(default_factory=lambda: ["basic_momentum", "oscillator_momentum", "rate_of_change_momentum", "full_momentum"])
    default_rsi_window: int = 14
    default_stochastic_k_window: int = 14
    default_stochastic_d_window: int = 3
    default_roc_window: int = 12
    default_momentum_window: int = 10
    default_cci_window: int = 20
    max_window: int = 500
    allow_partial_momentum_features: bool = True
    oscillator_min_value: float = 0.0
    oscillator_max_value: float = 100.0

    def __post_init__(self):
        if not self.enabled:
            raise ValueError("momentum_features.enabled must be True")
        if not self.available_indicator_sets:
            raise ValueError("available_indicator_sets cannot be empty")
        if self.default_indicator_set not in self.available_indicator_sets:
            raise ValueError("default_indicator_set must be in available_indicator_sets")
        if self.default_rsi_window <= 0:
            raise ValueError("default_rsi_window must be positive")
        if self.default_stochastic_k_window <= 0:
            raise ValueError("default_stochastic_k_window must be positive")
        if self.default_stochastic_d_window <= 0:
            raise ValueError("default_stochastic_d_window must be positive")
        if self.default_roc_window <= 0:
            raise ValueError("default_roc_window must be positive")
        if self.default_momentum_window <= 0:
            raise ValueError("default_momentum_window must be positive")
        if self.default_cci_window <= 0:
            raise ValueError("default_cci_window must be positive")
        if self.max_window <= 0:
            raise ValueError("max_window must be positive")
        if self.oscillator_min_value >= self.oscillator_max_value:
            raise ValueError("oscillator_min_value must be less than oscillator_max_value")
        windows = [self.default_rsi_window, self.default_stochastic_k_window,
                   self.default_stochastic_d_window, self.default_roc_window,
                   self.default_momentum_window, self.default_cci_window]
        if any(w > self.max_window for w in windows):
            raise ValueError("Values in default windows cannot exceed max_window")


@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class VolatilityFeatureConfig:
    enabled: bool = True
    default_indicator_set: str = "basic_volatility"
    available_indicator_sets: list[str] = field(default_factory=lambda: [
        "basic_volatility",
        "band_volatility",
        "channel_volatility",
        "compression_volatility",
        "full_volatility"
    ])
    default_atr_window: int = 14
    default_bollinger_window: int = 20
    default_bollinger_std: float = 2.0
    default_keltner_ema_window: int = 20
    default_keltner_atr_window: int = 10
    default_keltner_multiplier: float = 2.0
    default_donchian_window: int = 20
    default_rolling_volatility_window: int = 20
    default_reference_window: int = 100
    max_window: int = 1000
    allow_partial_volatility_features: bool = True
    fail_on_negative_volatility: bool = True


@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class StrategiesConfig:
    enabled: bool = True
    default_strategies: list[str] = field(default_factory=lambda: [
        "trend_following_skeleton",
        "mean_reversion_skeleton",
        "momentum_skeleton",
        "volatility_breakout_skeleton"
    ])
    allow_experimental_strategies: bool = True
    default_action_mode: str = "watch_only"
    allow_long_candidates: bool = True
    allow_short_candidates: bool = False
    max_signals_per_strategy_run: int = 200
    min_confidence: float = 0.0
    max_confidence_allowed_without_backtest: float = 0.70
    write_signal_outputs: bool = True
    write_strategy_reports: bool = True

    def __post_init__(self):
        if not self.default_strategies:
            raise ValueError("default_strategies cannot be empty")
        if self.default_action_mode != "watch_only":
            raise ValueError("default_action_mode must be 'watch_only'")
        if self.max_signals_per_strategy_run <= 0:
            raise ValueError("max_signals_per_strategy_run must be positive")
        if not (0.0 <= self.min_confidence <= 1.0):
            raise ValueError("min_confidence must be between 0.0 and 1.0")
        if not (0.0 <= self.max_confidence_allowed_without_backtest <= 1.0):
            raise ValueError("max_confidence_allowed_without_backtest must be between 0.0 and 1.0")

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class SignalsConfig:
    enabled: bool = True
    store_dir: str = "data/signals"
    default_format: str = "jsonl"
    expire_after_hours: int = 24
    require_reasons: bool = True
    reject_duplicate_signal_ids: bool = True
    overconfidence_warning_threshold: float = 0.80

    def __post_init__(self):
        if not self.store_dir:
            raise ValueError("store_dir cannot be empty")
        if self.default_format != "jsonl":
            raise ValueError("default_format must be 'jsonl'")
        if self.expire_after_hours <= 0:
            raise ValueError("expire_after_hours must be positive")
        if not (0.0 <= self.overconfidence_warning_threshold <= 1.0):
            raise ValueError("overconfidence_warning_threshold must be between 0.0 and 1.0")



@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class SignalScoringConfigSchema:
    enabled: bool = True
    min_score: float = 0.0
    max_score: float = 100.0
    base_score: float = 50.0
    confidence_weight: float = 25.0
    reason_quality_weight: float = 15.0
    feature_snapshot_weight: float = 10.0
    risk_penalty_weight: float = 20.0
    max_allowed_score_without_backtest: float = 70.0
    overconfidence_penalty: float = 15.0
    min_score_for_review: float = 40.0

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class SignalQualityConfig:
    enabled: bool = True
    min_confidence_for_review: float = 0.25
    min_score_for_review: float = 40.0
    reject_missing_reasons: bool = True
    reject_missing_feature_snapshot: bool = True
    reject_expired_signals: bool = True
    overconfidence_warning_threshold: float = 0.70
    max_rejected_ratio_warning: float = 0.80
    allow_empty_signal_list: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class ConfluenceConfig:
    enabled: bool = True
    default_aggregation_mode: str = "by_symbol_timeframe"
    min_signals_for_confluence: int = 2
    conflict_penalty: float = 25.0
    strong_threshold: float = 70.0
    moderate_threshold: float = 50.0
    weak_threshold: float = 25.0
    write_confluence_reports: bool = True


@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class SignalRankingConfigSchema:
    enabled: bool = True
    min_rank_score: float = 0.0
    max_rank_score: float = 100.0
    signal_score_weight: float = 35.0
    confidence_weight: float = 15.0
    confluence_weight: float = 20.0
    quality_weight: float = 15.0
    recency_weight: float = 5.0
    risk_penalty_weight: float = 20.0
    action_priority_weight: float = 10.0
    max_rank_score_without_backtest: float = 75.0
    default_min_rank_score_for_candidates: float = 45.0

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class CandidateSelectionConfigSchema:
    enabled: bool = True
    max_candidates: int = 20
    max_candidates_per_symbol: int = 1
    max_candidates_per_strategy: int = 10
    min_rank_score: float = 45.0
    min_confidence: float = 0.25
    min_confluence_score: Optional[float] = None
    allow_watch_action: bool = True
    allow_long_action: bool = True
    allow_short_action: bool = False
    reject_high_risk_flags: bool = True
    collapse_mode: str = "best_per_symbol_timeframe"
    write_selected_candidates: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class StrategyPortfolioConfigSchema:
    enabled: bool = True
    default_mode: str = "research_pool"
    default_rule_set: str = "basic_rules"
    max_candidates: int = 20
    max_per_strategy: int = 10
    max_per_symbol: int = 1
    require_confluence: bool = False
    min_confluence_score: Optional[float] = None
    diversify_by_strategy: bool = True
    write_portfolio_reports: bool = True



@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class BacktestingConfig:
    enabled: bool = True
    store_dir: str = "data/backtests"
    default_starting_cash: float = 100000.0
    default_fee_rate: float = 0.0
    default_slippage_bps: float = 0.0
    default_order_type: str = "next_open"
    default_signal_mode: str = "watch_as_long_candidate"
    default_exit_mode: str = "hold_n_bars"
    default_hold_bars: int = 5
    max_positions: int = 10
    max_position_notional: float = 10000.0
    allow_fractional_quantity: bool = True
    allow_short: bool = False
    write_events: bool = True
    write_fills: bool = True
    write_equity_curve: bool = True
    warn_on_backtest_limitations: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class HistoricalReplayConfig:
    enabled: bool = True
    require_cached_market_data: bool = True
    require_signal_file: bool = True
    prevent_same_bar_fill: bool = True
    default_timeframe: str = "1d"
    max_symbols_per_backtest: int = 50
    max_events_per_run: int = 100000

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class TransactionCostsConfig:
    enabled: bool = True
    model_type: str = "bps"
    flat_fee: float = 0.0
    fee_bps: float = 0.0
    per_share_fee: float = 0.0
    min_fee: float = 0.0
    max_fee: Optional[float] = None

    def __post_init__(self):
        valid_models = ["none", "flat_fee", "bps", "per_share", "combined"]
        if self.model_type.lower() not in valid_models:
            raise ValueError(f"model_type must be one of {valid_models}")
        if self.flat_fee < 0 or self.fee_bps < 0 or self.per_share_fee < 0 or self.min_fee < 0:
            raise ValueError("fee values cannot be negative")
        if self.max_fee is not None and self.max_fee < self.min_fee:
            raise ValueError("max_fee must be greater than or equal to min_fee")

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class SlippageConfigSchema:
    enabled: bool = True
    model_type: str = "fixed_bps"
    fixed_bps: float = 0.0
    spread_bps: float = 0.0
    volume_participation_rate: float = 0.01
    volume_impact_factor: float = 10.0
    volatility_multiplier: float = 1.0
    max_slippage_bps: float = 100.0

    def __post_init__(self):
        valid_models = ["none", "fixed_bps", "volume_participation", "spread_proxy", "volatility_adjusted"]
        if self.model_type.lower() not in valid_models:
            raise ValueError(f"model_type must be one of {valid_models}")
        if self.fixed_bps < 0 or self.spread_bps < 0:
            raise ValueError("fixed_bps and spread_bps cannot be negative")
        if not (0.0 <= self.volume_participation_rate <= 1.0):
            raise ValueError("volume_participation_rate must be between 0.0 and 1.0")
        if self.volume_impact_factor < 0:
            raise ValueError("volume_impact_factor cannot be negative")
        if self.max_slippage_bps <= 0:
            raise ValueError("max_slippage_bps must be positive")

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class TradeLedgerConfig:
    enabled: bool = True
    build_trade_ledger: bool = True
    include_open_trades: bool = True
    fifo_pairing: bool = True
    write_trade_ledger: bool = True
    write_trade_breakdowns: bool = True

    def __post_init__(self):
        if not self.build_trade_ledger:
            raise ValueError("build_trade_ledger must be true")
        if not self.fifo_pairing:
            raise ValueError("fifo_pairing must be true")

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class AdvancedBacktestMetricsConfig:
    enabled: bool = True
    periods_per_year: int = 252
    calculate_sharpe_like: bool = True
    calculate_sortino_like: bool = True
    calculate_calmar_like: bool = True
    calculate_drawdown_periods: bool = True
    calculate_strategy_breakdown: bool = True
    calculate_symbol_breakdown: bool = True
    warn_metrics_are_not_guarantees: bool = True

    def __post_init__(self):
        if self.periods_per_year <= 0:
            raise ValueError("periods_per_year must be positive")

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class WalkForwardConfigSchema:
    enabled: bool = True
    default_mode: str = "rolling"
    train_window_days: int = 365
    test_window_days: int = 90
    step_days: int = 90
    min_train_days: int = 180
    max_windows: int = 20
    include_partial_last_window: bool = False
    anchored_start: bool = False
    run_in_sample: bool = True
    run_out_of_sample: bool = True
    continue_on_window_error: bool = True
    write_window_backtests: bool = True
    write_walk_forward_reports: bool = True
    warn_no_optimization_performed: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class OutOfSampleEvaluationConfig:
    enabled: bool = True
    min_completed_windows: int = 2
    min_oos_positive_window_ratio: float = 0.50
    max_average_degradation_pct: float = 0.0
    min_stability_score: float = 50.0
    classify_results: bool = True
    warn_if_insufficient_windows: bool = True



@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class ParameterSensitivityConfigSchema:
    enabled: bool = True
    max_cells: int = 100
    hard_max_cells: int = 1000
    continue_on_cell_error: bool = True
    run_backtest: bool = True
    include_benchmark: bool = False
    include_monte_carlo: bool = False
    include_walk_forward: bool = False
    primary_metric: str = "RETURN_PCT"
    stability_metric: str = "STABILITY_SCORE"
    min_completed_cells: int = 5
    write_sensitivity_reports: bool = True
    warn_not_optimizer: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class RobustnessGridConfig:
    enabled: bool = True
    default_grid_type: str = "SINGLE_PARAMETER"
    max_single_parameter_values: int = 20
    max_two_parameter_cells: int = 100
    max_multi_parameter_cells: int = 250
    local_neighborhood_radius: int = 2
    detect_robust_regions: bool = True
    detect_fragile_regions: bool = True
    min_robust_region_size: int = 2

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass
class StabilityMapConfig:
    enabled: bool = True
    local_stability_neighbors: int = 2
    robust_zone_min_stability_score: float = 65.0
    fragile_zone_max_stability_score: float = 35.0
    overfit_risk_high_range_ratio: float = 2.0
    write_stability_map: bool = True

@dataclass
class PortfolioConstructionConfig:
    enabled: bool
    default_method: str
    available_methods: list[str]
    max_total_allocation_pct: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool
    write_portfolio_reports: bool
    warn_not_optimizer: bool
    warn_not_investment_advice: bool

@dataclass
class AllocationLimitsConfig:
    enabled: bool
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_total_candidates: int
    reject_missing_price: bool

@dataclass
class RiskBudgetingConfig:
    enabled: bool
    max_total_budget_pct: float
    max_symbol_budget_pct: float
    max_strategy_budget_pct: float
    max_timeframe_budget_pct: float
    max_single_candidate_budget_pct: float
    min_cash_buffer_pct: float
    enforce_budget: bool
    write_budget_reports: bool

@dataclass
class ConcentrationGuardsConfig:
    enabled: bool
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool
    cap_breaches: bool
    write_concentration_reports: bool

@dataclass

@dataclass
class BasketSimulationConfigSchema:
    enabled: bool = True
    store_dir: str = "data/backtests/baskets"
    default_starting_cash: float = 100000.0
    default_entry_mode: str = "enter_all_at_start"
    default_exit_mode: str = "hold_n_bars"
    default_allocation_replay_mode: str = "target_notional"
    default_hold_bars: int = 5
    prevent_same_bar_fill: bool = True
    allow_fractional_quantity: bool = True
    max_positions: int = 20
    max_total_allocation_pct: float = 0.80
    enable_transaction_costs: bool = True
    enable_slippage: bool = True
    enable_benchmark_comparison: bool = False
    benchmark_set_name: str = "default"
    write_basket_reports: bool = True
    warn_not_live_execution: bool = True

@dataclass
class AllocationReplayConfig:
    enabled: bool = True
    default_quantity: float = 1.0
    default_notional: float = 5000.0
    min_notional: float = 0.0
    max_notional: float = 10000.0
    allow_short: bool = False
    order_type: str = "next_open"
    reject_missing_price: bool = True
    reject_zero_quantity: bool = True

@dataclass
class AllocationDriftConfigSchema:
    enabled: bool = True
    drift_warning_threshold: float = 0.03
    drift_breach_threshold: float = 0.05
    evaluate_by_symbol: bool = True
    evaluate_total_weight: bool = True
    write_drift_reports: bool = True


@dataclass
@dataclass
class NotificationsConfig:
    enabled: bool = True
    default_channel: str = "dry_run"
    dry_run: bool = True
    log_only: bool = True
    max_message_length: int = 3500
    max_queue_size: int = 1000
    suppress_duplicates: bool = True
    duplicate_window_seconds: int = 3600
    rate_limit_per_minute: int = 20
    include_disclaimer: bool = True
    disclaimer_text: str = "Research-only notification. Not investment advice. No live, broker, or paper order was created."
    write_notification_reports: bool = True

@dataclass
class TelegramConfig:
    enabled: bool = False
    dry_run: bool = True
    allow_real_send: bool = False
    bot_token_env_var: str = "USA_SIGNAL_BOT_TELEGRAM_TOKEN"
    chat_id_env_var: str = "USA_SIGNAL_BOT_TELEGRAM_CHAT_ID"
    parse_mode: str = "none"
    timeout_seconds: int = 10
    disable_web_page_preview: bool = True
    redact_token_in_logs: bool = True

@dataclass
class NotificationTemplatesConfig:
    enabled: bool = True
    include_scan_summary: bool = True
    include_selected_candidates: bool = True
    include_risk_summary: bool = True
    include_portfolio_summary: bool = True
    include_runtime_warnings: bool = True
    include_runtime_errors: bool = True
    max_candidates_in_message: int = 10
    max_risk_decisions_in_message: int = 10
    max_allocations_in_message: int = 10

def validate_notifications_config(config: NotificationsConfig) -> None:
    if config.max_message_length <= 0:
        raise ValueError("max_message_length must be positive")
    if config.max_queue_size <= 0:
        raise ValueError("max_queue_size must be positive")
    if config.duplicate_window_seconds <= 0:
        raise ValueError("duplicate_window_seconds must be positive")
    if config.rate_limit_per_minute <= 0:
        raise ValueError("rate_limit_per_minute must be positive")
    if config.include_disclaimer and not config.disclaimer_text:
        raise ValueError("disclaimer_text must be provided if include_disclaimer is True")

def validate_telegram_config(config: TelegramConfig) -> None:
    if not config.bot_token_env_var:
        raise ValueError("bot_token_env_var cannot be empty")
    if not config.chat_id_env_var:
        raise ValueError("chat_id_env_var cannot be empty")
    if config.timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")

def validate_notification_templates_config(config: NotificationTemplatesConfig) -> None:
    if config.max_candidates_in_message <= 0:
        raise ValueError("max_candidates_in_message must be positive")
    if config.max_risk_decisions_in_message <= 0:
        raise ValueError("max_risk_decisions_in_message must be positive")
    if config.max_allocations_in_message <= 0:
        raise ValueError("max_allocations_in_message must be positive")


@dataclass

@dataclass
class ComparisonConfig:
    enabled: bool = True
    store_dir: str = "data/comparison"
    default_report_type: str = "full_comparison"
    matching_tolerance_bars: int = 1
    price_gap_warning_pct: float = 1.0
    timing_gap_warning_bars: int = 1
    min_matched_trades_for_realism_score: int = 3
    write_comparison_reports: bool = True
    warn_not_execution_validation: bool = True
    warn_not_investment_advice: bool = True

@dataclass
class PerformanceGapConfig:
    enabled: bool = True
    return_gap_warning_pct: float = 5.0
    drawdown_gap_warning_pct: float = 5.0
    win_rate_gap_warning: float = 0.10
    profit_factor_gap_warning: float = 0.50
    trade_count_gap_warning: int = 3

@dataclass
class ExecutionGapConfig:
    enabled: bool = True
    price_gap_warning_pct: float = 1.0
    price_gap_critical_pct: float = 5.0
    timing_gap_warning_bars: int = 1
    timing_gap_critical_bars: int = 5
    pnl_gap_warning: float = 100.0
    unmatched_trade_warning_ratio: float = 0.25
    realism_score_warning_threshold: float = 60.0

@dataclass
class SignalDriftConfig:
    enabled: bool = True
    score_gap_warning: float = 10.0
    confidence_gap_warning: float = 0.10
    rank_gap_warning: float = 10.0
    feature_gap_warning: float = 0.20
    changed_action_is_high_drift: bool = True
    write_signal_drift_reports: bool = True

@dataclass
class ComparisonNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_comparison_report: bool = True
    notify_execution_gap_warning: bool = True
    notify_signal_drift_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

def validate_comparison_config(config: ComparisonConfig) -> None:
    if config.matching_tolerance_bars < 0:
        raise ValueError("matching_tolerance_bars cannot be negative")
    if config.price_gap_warning_pct < 0:
        raise ValueError("price_gap_warning_pct cannot be negative")
    if config.timing_gap_warning_bars < 0:
        raise ValueError("timing_gap_warning_bars cannot be negative")
    if config.min_matched_trades_for_realism_score <= 0:
        raise ValueError("min_matched_trades_for_realism_score must be positive")
    if not config.warn_not_execution_validation:
        raise ValueError("warn_not_execution_validation must be True")
    if not config.warn_not_investment_advice:
        raise ValueError("warn_not_investment_advice must be True")

def validate_performance_gap_config(config: PerformanceGapConfig) -> None:
    if not (0 <= config.win_rate_gap_warning <= 1):
        raise ValueError("win_rate_gap_warning must be between 0 and 1")

def validate_execution_gap_config(config: ExecutionGapConfig) -> None:
    if not (0 <= config.unmatched_trade_warning_ratio <= 1):
        raise ValueError("unmatched_trade_warning_ratio must be between 0 and 1")
    if not (0 <= config.realism_score_warning_threshold <= 100):
        raise ValueError("realism_score_warning_threshold must be between 0 and 100")

def validate_signal_drift_config(config: SignalDriftConfig) -> None:
    if not (0 <= config.confidence_gap_warning <= 1):
        raise ValueError("confidence_gap_warning must be between 0 and 1")
    if not (0 <= config.feature_gap_warning <= 1):
        raise ValueError("feature_gap_warning must be between 0 and 1")

def validate_comparison_notifications_config(config: ComparisonNotificationsConfig) -> None:
    if not config.warn_no_real_send_default:
        raise ValueError("warn_no_real_send_default must be True")




@dataclass
class QualityScorecardConfig:
    enabled: bool = True
    overall_pass_score: float = 75.0
    overall_warn_score: float = 60.0
    fail_on_critical_issue: bool = True
    insufficient_data_threshold: float = 0.40
    write_scorecard_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_not_live_approval: bool = True

@dataclass
class QualityWeightsConfig:
    data: float = 0.10
    feature: float = 0.08
    signal: float = 0.10
    backtest: float = 0.12
    robustness: float = 0.10
    risk: float = 0.10
    portfolio: float = 0.08
    paper: float = 0.10
    comparison: float = 0.10
    runtime: float = 0.07
    notification: float = 0.03
    documentation: float = 0.02

@dataclass
class ReadinessGateConfig:
    enabled: bool = True
    scope: str = "full_local_stack"
    min_overall_score: float = 70.0
    min_data_score: float = 50.0
    min_backtest_score: float = 50.0
    min_risk_score: float = 50.0
    min_runtime_score: float = 60.0
    require_no_critical_safety_issue: bool = True
    require_broker_flags_disabled: bool = True
    require_telegram_real_send_disabled: bool = True
    write_gate_reports: bool = True

@dataclass
class SystemAcceptanceConfig:
    enabled: bool = True
    default_scope: str = "full_local_stack"
    accept_with_warnings_allowed: bool = True
    block_on_live_or_broker_flags: bool = True
    block_on_investment_advice_language: bool = True
    write_acceptance_reports: bool = True
    warn_local_research_only: bool = True

@dataclass
class QualityNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_scorecard: bool = True
    notify_gate_result: bool = True
    notify_acceptance_result: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True


@dataclass
class ReleaseConfig:
    enabled: bool = True
    release_name: str = "usa_signal_bot_local"
    output_dir: str = "data/release/builds"
    include_docs: bool = True
    include_tests: bool = True
    include_reports: bool = True
    include_data_cache: bool = False
    include_backups: bool = False
    include_secrets: bool = False
    validate_after_build: bool = True
    write_release_reports: bool = True
    warn_not_live_approval: bool = True
    warn_not_investment_advice: bool = True

@dataclass
class ReleaseArtifactsConfig:
    enabled: bool = True
    include_source: bool = True
    include_config_examples: bool = True
    include_docs: bool = True
    include_tests: bool = True
    include_requirements: bool = True
    include_latest_regression_report: bool = True
    include_latest_quality_report: bool = True
    exclude_git: bool = True
    exclude_pycache: bool = True
    exclude_env_files: bool = True
    exclude_secret_like_paths: bool = True

@dataclass
class OperatorRunbookConfig:
    enabled: bool = True
    write_runbook: bool = True
    include_command_reference: bool = True
    include_safety_limitations: bool = True
    include_troubleshooting: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass
class MaintenanceConfig:
    enabled: bool = True
    daily_enabled: bool = True
    weekly_enabled: bool = True
    monthly_enabled: bool = True
    pre_release_enabled: bool = True
    execute_commands: bool = False
    command_timeout_seconds: int = 60
    write_maintenance_reports: bool = True

@dataclass
class BackupConfig:
    enabled: bool = True
    output_dir: str = "data/release/backups"
    default_scope: str = "reports_only"
    include_configs: bool = True
    include_reports: bool = True
    include_data_cache: bool = False
    include_secrets: bool = False
    validate_after_backup: bool = True
    restore_dry_run_only: bool = True

@dataclass
class ConfigProfilesConfig:
    enabled: bool = True
    write_default_profiles: bool = True
    profiles_dir: str = "config/profiles"
    require_broker_flags_false: bool = True
    require_telegram_real_send_false: bool = True
    require_no_dashboard: bool = True

@dataclass
class UpgradePrecheckConfig:
    enabled: bool = True
    check_python_version: bool = True
    check_requirements: bool = True
    check_config_files: bool = True
    check_data_directories: bool = True
    check_secret_like_files: bool = True
    check_regression_smoke: bool = True
    write_precheck_reports: bool = True

def validate_release_config(config: ReleaseConfig) -> None:
    if not config.release_name:
        raise ValueError("release_name must not be empty")
    if not config.output_dir:
        raise ValueError("output_dir must not be empty")
    if config.include_secrets:
        raise ValueError("include_secrets must be False")
    if not config.warn_not_live_approval:
        raise ValueError("warn_not_live_approval must be True")
    if not config.warn_not_investment_advice:
        raise ValueError("warn_not_investment_advice must be True")

def validate_release_artifacts_config(config: ReleaseArtifactsConfig) -> None:
    if not config.exclude_secret_like_paths:
        raise ValueError("exclude_secret_like_paths must be True")

def validate_operator_runbook_config(config: OperatorRunbookConfig) -> None:
    if not config.warn_no_broker_execution:
        raise ValueError("warn_no_broker_execution must be True")

def validate_maintenance_config(config: MaintenanceConfig) -> None:
    if config.execute_commands is not False:
        raise ValueError("execute_commands must be False by default")
    if config.command_timeout_seconds <= 0:
        raise ValueError("command_timeout_seconds must be positive")

def validate_backup_config(config: BackupConfig) -> None:
    if config.include_secrets:
        raise ValueError("include_secrets must be False")
    if not config.restore_dry_run_only:
        raise ValueError("restore_dry_run_only must be True")
    from usa_signal_bot.core.enums import BackupScope
    if config.default_scope.upper() not in [s.value for s in BackupScope]:
        raise ValueError(f"default_scope must be a valid BackupScope, got {config.default_scope}")

def validate_config_profiles_config(config: ConfigProfilesConfig) -> None:
    if not config.require_broker_flags_false:
        raise ValueError("require_broker_flags_false must be True")
    if not config.require_telegram_real_send_false:
        raise ValueError("require_telegram_real_send_false must be True")
    if not config.require_no_dashboard:
        raise ValueError("require_no_dashboard must be True")


@dataclass
class ObservabilityConfig:
    enabled: bool = True
    store_dir: str = "data/observability"
    logs_dir: str = "data/observability/logs"
    metrics_dir: str = "data/observability/metrics"
    reports_dir: str = "data/observability/reports"
    write_jsonl_events: bool = True
    write_text_log: bool = True
    sanitize_payloads: bool = True
    external_telemetry_enabled: bool = False
    dashboard_enabled: bool = False
    warn_local_only: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass
class LogRotationConfigSchema:
    enabled: bool = True
    max_file_size_bytes: int = 5242880
    max_rotated_files: int = 5
    compress_rotated: bool = False
    dry_run_default: bool = False
    write_rotation_reports: bool = True

@dataclass
class OperationalMetricsConfig:
    enabled: bool = True
    collect_runtime_metrics: bool = True
    collect_scan_metrics: bool = True
    collect_backtest_metrics: bool = True
    collect_paper_metrics: bool = True
    collect_comparison_metrics: bool = True
    collect_quality_metrics: bool = True
    collect_regression_metrics: bool = True
    collect_release_metrics: bool = True
    collect_notification_metrics: bool = True
    collect_disk_usage: bool = True
    write_metric_snapshots: bool = True

@dataclass
class OperationalHealthConfig:
    enabled: bool = True
    disk_warning_threshold_pct: float = 80.0
    disk_critical_threshold_pct: float = 90.0
    error_warning_threshold_24h: int = 5
    error_critical_threshold_24h: int = 20
    stale_artifact_warning_hours: int = 72
    write_health_reports: bool = True

@dataclass
class SafetyMonitorConfig:
    enabled: bool = True
    require_broker_flags_disabled: bool = True
    require_live_demo_flags_disabled: bool = True
    require_telegram_real_send_disabled: bool = True
    require_dashboard_disabled: bool = True
    require_external_telemetry_disabled: bool = True
    block_on_safety_violation: bool = True

@dataclass
class ObservabilityNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_operational_health: bool = True
    notify_log_rotation: bool = True
    notify_safety_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True



@dataclass
class IncidentResponseConfig:
    enabled: bool = True
    store_dir: str = "data/incident"
    auto_collect_from_latest_artifacts: bool = True
    minimum_severity_to_report: str = "medium"
    write_incident_reports: bool = True
    redact_sensitive_data: bool = True
    warn_local_only: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass
class RecoveryConfig:
    enabled: bool = True
    dry_run_default: bool = True
    execute_commands_default: bool = False
    allow_destructive_actions: bool = False
    require_manual_review_for_critical: bool = True
    write_recovery_plans: bool = True
    write_recovery_results: bool = True
    block_on_safety_violation: bool = True

@dataclass
class RollbackConfig:
    enabled: bool = True
    dry_run_default: bool = True
    execute_enabled: bool = False
    allow_overwrite_default: bool = False
    require_force: bool = True
    protect_source_code: bool = True
    protect_config: bool = True
    protect_docs: bool = True
    protect_tests: bool = True
    protect_secrets: bool = True
    inspect_zip_only_by_default: bool = True
    write_rollback_plans: bool = True
    write_rollback_results: bool = True
    write_rollback_prechecks: bool = True

@dataclass
class RollbackSourcesConfig:
    enabled: bool = True
    include_release_bundles: bool = True
    include_backup_archives: bool = True
    include_config_profiles: bool = True
    include_regression_baselines: bool = True
    prefer_latest_valid_source: bool = True

@dataclass
class IncidentAuditConfig:
    enabled: bool = True
    audit_path: str = "data/incident/audit/incident_audit.jsonl"
    redact_sensitive_paths: bool = True
    append_only: bool = True

@dataclass
class IncidentNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_incident_report: bool = True
    notify_recovery_plan: bool = True
    notify_rollback_dry_run: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True




@dataclass
class SchedulerConfig:
    enabled: bool = True
    store_dir: str = "data/scheduler"
    dry_run_default: bool = True
    execute_commands_default: bool = False
    install_daemon: bool = False
    install_cron: bool = False
    install_service: bool = False
    allow_destructive_jobs: bool = False
    write_scheduler_reports: bool = True
    warn_local_only: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass
class RunLocksConfig:
    enabled: bool = True
    locks_dir: str = "data/scheduler/locks"
    stale_after_seconds_default: int = 3600
    global_stale_after_seconds: int = 7200
    acquisition_mode_default: str = "FAIL_FAST"
    allow_steal_if_stale: bool = True
    cleanup_stale_locks_dry_run_default: bool = True
    write_lock_audit: bool = True

@dataclass
class ConcurrencyConfig:
    enabled: bool = True
    global_max_concurrent_runs: int = 1
    scan_max_concurrent_runs: int = 1
    backtest_max_concurrent_runs: int = 1
    paper_max_concurrent_runs: int = 1
    regression_max_concurrent_runs: int = 1
    retention_max_concurrent_runs: int = 1
    observability_max_concurrent_runs: int = 2
    notification_max_concurrent_runs: int = 1
    block_on_conflict: bool = True
    allow_overlap_default: bool = False

@dataclass
class IdempotencyConfig:
    enabled: bool = True
    store_path: str = "data/scheduler/idempotency.jsonl"
    duplicate_policy: str = "SKIP"
    record_completed_runs: bool = True
    prune_after_days: int = 30
    prune_dry_run_default: bool = True

@dataclass
class AtomicIOConfig:
    enabled: bool = True
    use_atomic_writes: bool = True
    temp_suffix: str = ".tmp"
    verify_checksum_after_write: bool = True
    block_protected_target_write: bool = False

@dataclass
class SchedulerJobsConfig:
    enabled: bool = True
    default_dry_run: bool = True
    execute_commands: bool = False
    safe_allowlist_only: bool = True
    blocked_commands: List[str] = field(default_factory=lambda: [
        "cleanup-execute",
        "rollback-execute",
        "send-broker-order",
        "live-order",
        "demo-order"
    ])

@dataclass
class SchedulerNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_scheduler_report: bool = True
    notify_stale_lock_warning: bool = True
    notify_concurrency_blocked: bool = True
    default_channel: str = "DRY_RUN"
    warn_no_real_send_default: bool = True

def validate_scheduler_config(config: SchedulerConfig) -> None:
    if not config.dry_run_default:
        pass # warning maybe, but schema says dry_run_default is true
    if config.execute_commands_default:
        raise ValueError("execute_commands_default must be False")
    if config.install_daemon:
        raise ValueError("install_daemon must be False")
    if config.install_cron:
        raise ValueError("install_cron must be False")
    if config.install_service:
        raise ValueError("install_service must be False")
    if config.allow_destructive_jobs:
        raise ValueError("allow_destructive_jobs must be False")

def validate_run_locks_config(config: RunLocksConfig) -> None:
    if config.stale_after_seconds_default <= 0:
        raise ValueError("stale_after_seconds_default must be positive")

def validate_concurrency_config(config: ConcurrencyConfig) -> None:
    for f in [config.global_max_concurrent_runs, config.scan_max_concurrent_runs,
              config.backtest_max_concurrent_runs, config.paper_max_concurrent_runs,
              config.regression_max_concurrent_runs, config.retention_max_concurrent_runs,
              config.observability_max_concurrent_runs, config.notification_max_concurrent_runs]:
        if f <= 0:
            raise ValueError("max_concurrent_runs must be positive")

def validate_idempotency_config(config: IdempotencyConfig) -> None:
    if config.duplicate_policy.upper() not in ["SKIP", "REVIEW", "BLOCK"]:
        raise ValueError("duplicate_policy must be SKIP, REVIEW, or BLOCK")
    if config.prune_after_days <= 0:
        raise ValueError("prune_after_days must be positive")

def validate_scheduler_jobs_config(config: SchedulerJobsConfig) -> None:
    if config.execute_commands:
        raise ValueError("execute_commands must be False in scheduler_jobs")
    if not config.safe_allowlist_only:
        raise ValueError("safe_allowlist_only must be True")
    if not all(cmd in config.blocked_commands for cmd in ["cleanup-execute", "rollback-execute", "send-broker-order", "live-order", "demo-order"]):
        raise ValueError("blocked_commands must include destructive commands")

def validate_scheduler_notifications_config(config: SchedulerNotificationsConfig) -> None:
    if not config.dry_run:
        raise ValueError("scheduler_notifications.dry_run must be True")

@dataclass
@dataclass
class TaskQueueConfig:
    enabled: bool = True
    store_dir: str = "data/taskqueue"
    dry_run_default: bool = True
    real_worker_enabled: bool = False
    daemon_enabled: bool = False
    execute_commands: bool = False
    allow_destructive_tasks: bool = False
    write_taskqueue_reports: bool = True
    warn_local_simulation_only: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass
class TaskPriorityConfig:
    enabled: bool = True
    incident_priority_boost: float = 30.0
    safety_priority_boost: float = 25.0
    regression_priority_boost: float = 10.0
    cleanup_priority_boost_on_quota_warning: float = 15.0
    workload_penalty_enabled: bool = True

@dataclass
class WorkloadBudgetConfig:
    enabled: bool = True
    profile: str = "average_local_pc"
    max_cpu_pct: float = 85.0
    max_gpu_pct: float = 70.0
    max_ram_mb: float = 8192.0
    max_disk_mb: float = 2048.0
    max_network_mb_per_run: float = 1024.0
    max_duration_seconds: float = 7200.0
    max_parallel_tasks: int = 1
    block_on_budget_exceeded: bool = True

@dataclass
class RunWindowsConfig:
    enabled: bool = True
    enforce_windows: bool = False
    warn_outside_window: bool = True
    local_timezone: str = "Europe/Istanbul"
    heavy_research_start_hour: int = 22
    heavy_research_end_hour: int = 7

@dataclass
class TaskConflictsConfig:
    enabled: bool = True
    block_destructive_tasks: bool = True
    block_duplicate_tasks: bool = False
    block_lock_scope_conflicts: bool = True
    block_resource_budget_conflicts: bool = True
    warn_dependency_conflicts: bool = True

@dataclass
class QueueExecutorConfig:
    enabled: bool = True
    dry_run_only: bool = True
    execute_commands: bool = False
    safe_allowlist_only: bool = True
    write_queue_run_results: bool = True

@dataclass
class TaskQueueNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_taskqueue_report: bool = True
    notify_workload_budget_warning: bool = True
    notify_priority_plan_report: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

@dataclass
class PerformanceBaselinesConfig:
    enabled: bool = True
    store_dir: str = "data/performance"
    min_samples_per_baseline: int = 3
    preferred_percentile: int = 90
    active_baseline_version: str = "latest"
    mark_stale_after_days: int = 30
    write_baselines: bool = True
    external_telemetry_enabled: bool = False
    warn_local_only: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass
class SLAThresholdsConfig:
    enabled: bool = True
    scan_wall_time_warning_seconds: float = 1800.0
    scan_wall_time_critical_seconds: float = 3600.0
    scan_wall_time_blocker_seconds: float = 7200.0
    backtest_wall_time_warning_seconds: float = 7200.0
    backtest_wall_time_critical_seconds: float = 14400.0
    backtest_wall_time_blocker_seconds: float = 21600.0
    regression_wall_time_warning_seconds: float = 3600.0
    regression_wall_time_critical_seconds: float = 7200.0
    regression_wall_time_blocker_seconds: float = 10800.0
    memory_peak_warning_mb: float = 4096.0
    memory_peak_critical_mb: float = 6144.0
    memory_peak_blocker_mb: float = 8192.0
    output_growth_warning_mb: float = 512.0
    output_growth_critical_mb: float = 2048.0
    output_growth_blocker_mb: float = 4096.0
    error_count_warning: int = 1
    error_count_critical: int = 5
    error_count_blocker: int = 10

@dataclass
class RuntimeRegressionConfig:
    enabled: bool = True
    compare_against_p90: bool = True
    warning_delta_pct: float = 25.0
    fail_delta_pct: float = 50.0
    blocker_delta_pct: float = 100.0
    suppress_insufficient_data_alerts: bool = True
    write_regression_reports: bool = True

@dataclass
class PerformanceAcceptanceConfig:
    enabled: bool = True
    block_on_blocker_threshold: bool = True
    fail_on_critical_regression: bool = True
    warn_on_moderate_regression: bool = True
    pass_with_minor_regression_allowed: bool = True
    pass_is_not_live_approval: bool = True

@dataclass
class PerformanceAlertingConfig:
    enabled: bool = True
    dry_run: bool = True
    alert_on_sla_warning: bool = True
    alert_on_runtime_regression: bool = True
    alert_on_stale_baseline: bool = True
    suppress_duplicate_alerts: bool = True
    write_alert_reports: bool = True

@dataclass
class PerformanceNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_baseline_report: bool = True
    notify_sla_threshold_warning: bool = True
    notify_runtime_regression_alert: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

def validate_performance_baselines_config(config: PerformanceBaselinesConfig) -> None:
    if config.min_samples_per_baseline <= 0:
        raise ValueError("min_samples_per_baseline must be positive")
    if not (50 <= config.preferred_percentile <= 99):
        raise ValueError("preferred_percentile must be between 50 and 99")
    if config.mark_stale_after_days <= 0:
        raise ValueError("mark_stale_after_days must be positive")
    if config.external_telemetry_enabled:
        raise ValueError("external_telemetry_enabled must be False")
    if not config.warn_local_only:
        raise ValueError("warn_local_only must be True")
    if not config.warn_not_investment_advice:
        raise ValueError("warn_not_investment_advice must be True")
    if not config.warn_no_broker_execution:
        raise ValueError("warn_no_broker_execution must be True")

def validate_sla_thresholds_config(config: SLAThresholdsConfig) -> None:
    pass

def validate_runtime_regression_config(config: RuntimeRegressionConfig) -> None:
    if not (config.warning_delta_pct < config.fail_delta_pct < config.blocker_delta_pct):
        raise ValueError("delta percentages must strictly increase: warning < fail < blocker")

def validate_performance_acceptance_config(config: PerformanceAcceptanceConfig) -> None:
    if not config.pass_is_not_live_approval:
        raise ValueError("pass_is_not_live_approval must be True")

def validate_performance_alerting_config(config: PerformanceAlertingConfig) -> None:
    if not config.dry_run:
        raise ValueError("performance_alerting.dry_run must be True")

def validate_performance_notifications_config(config: PerformanceNotificationsConfig) -> None:
    if not config.dry_run:
        raise ValueError("performance_notifications.dry_run must be True")



@dataclass
class YFinanceProviderConfig:
    enabled: bool = True
    allow_network: bool = True
    timeout_seconds: int = 30
    max_symbols_per_batch: int = 25
    default_interval: str = "1d"
    default_period: str = "6mo"
    validate_ohlcv: bool = True
    cache_successful_responses: bool = True

@dataclass
class LocalCacheProviderConfig:
    enabled: bool = True
    cache_root: str = "data/cache"
    max_staleness_days: int = 7
    allow_stale_with_warning: bool = True

@dataclass
class LocalFixtureProviderConfig:
    enabled: bool = True
    fixture_root: str = "data/regression/golden"
    test_only: bool = True
    allow_for_regression: bool = True

@dataclass
class ManualFileProviderConfig:
    enabled: bool = True
    manual_data_root: str = "data/manual"
    allowed_extensions: list[str] = field(default_factory=lambda: [".csv", ".jsonl"])
    require_ohlcv_columns: bool = True

@dataclass
class ProviderQualityConfig:
    enabled: bool = True
    freshness_weight: float = 0.20
    completeness_weight: float = 0.20
    schema_weight: float = 0.20
    ohlcv_weight: float = 0.20
    latency_weight: float = 0.10
    error_weight: float = 0.10
    excellent_score: float = 90.0
    good_score: float = 75.0
    acceptable_score: float = 60.0
    degraded_score: float = 40.0

@dataclass
class ProviderNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_provider_health: bool = True
    notify_provider_quality_warning: bool = True
    notify_provider_fallback: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True

@dataclass
class DataProvidersConfig:
    enabled: bool = True
    default_provider_order: list[str] = field(default_factory=lambda: ["local_cache", "yfinance", "manual_file", "local_fixture"])
    prefer_cache: bool = True
    fallback_enabled: bool = True
    min_quality_score: float = 60.0
    allow_network_providers: bool = True
    no_paid_providers: bool = True
    no_html_scraping: bool = True
    write_provider_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass

@dataclass
class ExecutionRealismConfig:
    enabled: bool = True
    write_execution_reports: bool = True
    warn_no_broker_execution: bool = True
    warn_not_investment_advice: bool = True
    warn_proxies_are_heuristic: bool = True
    no_real_borrow_feed: bool = True

@dataclass
class LiquidityGuardConfig:
    enabled: bool = True
    lookback_bars: int = 60
    min_price: float = 2.0
    penny_stock_price_threshold: float = 5.0
    min_avg_daily_volume: float = 500000.0
    min_avg_dollar_volume: float = 5000000.0
    thin_avg_daily_volume: float = 1000000.0
    thin_avg_dollar_volume: float = 10000000.0
    max_stale_days: int = 5
    block_signal_on_illiquid: bool = True
    warn_on_thin_liquidity: bool = True

@dataclass
class SpreadSlippageProxyConfig:
    enabled: bool = True
    max_spread_proxy_bps: float = 100.0
    max_slippage_proxy_bps: float = 150.0
    high_spread_proxy_bps: float = 200.0
    high_slippage_proxy_bps: float = 300.0
    use_atr_penalty: bool = True
    use_gap_penalty: bool = True
    use_low_price_penalty: bool = True

@dataclass
class VolumeParticipationConfig:
    enabled: bool = True
    default_notional_usd: float = 1000.0
    max_participation_pct: float = 1.0
    high_participation_pct: float = 5.0
    critical_participation_pct: float = 10.0
    block_backtest_fill_on_critical_participation: bool = True

@dataclass
class BorrowabilityProxyConfig:
    enabled: bool = True
    no_real_borrow_feed: bool = True
    low_price_penalty: bool = True
    low_liquidity_penalty: bool = True
    high_volatility_penalty: bool = True
    lifecycle_risk_penalty: bool = True
    corporate_action_risk_penalty: bool = True
    block_short_on_likely_unavailable: bool = True
    require_review_on_hard_to_borrow_proxy: bool = True

@dataclass
class ExecutionQualityConfig:
    enabled: bool = True
    liquidity_quality_weight: float = 0.30
    tradability_weight: float = 0.25
    slippage_realism_weight: float = 0.20
    borrowability_proxy_weight: float = 0.10
    participation_weight: float = 0.15

@dataclass
class ExecutionNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_liquidity_warning: bool = True
    notify_tradability_guard: bool = True
    notify_execution_realism_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
@dataclass
class AppConfig:

    execution_realism: ExecutionRealismConfig = field(default_factory=ExecutionRealismConfig)
    liquidity_guard: LiquidityGuardConfig = field(default_factory=LiquidityGuardConfig)
    spread_slippage_proxy: SpreadSlippageProxyConfig = field(default_factory=SpreadSlippageProxyConfig)
    volume_participation: VolumeParticipationConfig = field(default_factory=VolumeParticipationConfig)
    borrowability_proxy: BorrowabilityProxyConfig = field(default_factory=BorrowabilityProxyConfig)
    execution_quality: ExecutionQualityConfig = field(default_factory=ExecutionQualityConfig)
    execution_notifications: ExecutionNotificationsConfig = field(default_factory=ExecutionNotificationsConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    data_providers: DataProvidersConfig = field(default_factory=DataProvidersConfig)
    yfinance_provider: YFinanceProviderConfig = field(default_factory=YFinanceProviderConfig)
    local_cache_provider: LocalCacheProviderConfig = field(default_factory=LocalCacheProviderConfig)
    local_fixture_provider: LocalFixtureProviderConfig = field(default_factory=LocalFixtureProviderConfig)
    manual_file_provider: ManualFileProviderConfig = field(default_factory=ManualFileProviderConfig)
    provider_quality: ProviderQualityConfig = field(default_factory=ProviderQualityConfig)
    provider_notifications: ProviderNotificationsConfig = field(default_factory=ProviderNotificationsConfig)
    run_locks: RunLocksConfig = field(default_factory=RunLocksConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    idempotency: IdempotencyConfig = field(default_factory=IdempotencyConfig)
    atomic_io: AtomicIOConfig = field(default_factory=AtomicIOConfig)
    scheduler_jobs: SchedulerJobsConfig = field(default_factory=SchedulerJobsConfig)
    scheduler_notifications: SchedulerNotificationsConfig = field(default_factory=SchedulerNotificationsConfig)


    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    run_locks: RunLocksConfig = field(default_factory=RunLocksConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    idempotency: IdempotencyConfig = field(default_factory=IdempotencyConfig)
    atomic_io: AtomicIOConfig = field(default_factory=AtomicIOConfig)
    scheduler_jobs: SchedulerJobsConfig = field(default_factory=SchedulerJobsConfig)
    scheduler_notifications: SchedulerNotificationsConfig = field(default_factory=SchedulerNotificationsConfig)

    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    run_locks: RunLocksConfig = field(default_factory=RunLocksConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    idempotency: IdempotencyConfig = field(default_factory=IdempotencyConfig)
    atomic_io: AtomicIOConfig = field(default_factory=AtomicIOConfig)
    scheduler_jobs: SchedulerJobsConfig = field(default_factory=SchedulerJobsConfig)
    scheduler_notifications: SchedulerNotificationsConfig = field(default_factory=SchedulerNotificationsConfig)
    incident_response: IncidentResponseConfig = field(default_factory=IncidentResponseConfig)
    recovery: RecoveryConfig = field(default_factory=RecoveryConfig)
    rollback: RollbackConfig = field(default_factory=RollbackConfig)
    rollback_sources: RollbackSourcesConfig = field(default_factory=RollbackSourcesConfig)
    incident_audit: IncidentAuditConfig = field(default_factory=IncidentAuditConfig)
    incident_notifications: IncidentNotificationsConfig = field(default_factory=IncidentNotificationsConfig)


    observability: ObservabilityConfig = field(default_factory=ObservabilityConfig)
    log_rotation: LogRotationConfigSchema = field(default_factory=LogRotationConfigSchema)
    operational_metrics: OperationalMetricsConfig = field(default_factory=OperationalMetricsConfig)
    operational_health: OperationalHealthConfig = field(default_factory=OperationalHealthConfig)
    safety_monitor: SafetyMonitorConfig = field(default_factory=SafetyMonitorConfig)
    observability_notifications: ObservabilityNotificationsConfig = field(default_factory=ObservabilityNotificationsConfig)


    comparison: ComparisonConfig = field(default_factory=ComparisonConfig)
    release: ReleaseConfig = field(default_factory=ReleaseConfig)
    release_artifacts: ReleaseArtifactsConfig = field(default_factory=ReleaseArtifactsConfig)
    operator_runbook: OperatorRunbookConfig = field(default_factory=OperatorRunbookConfig)
    maintenance: MaintenanceConfig = field(default_factory=MaintenanceConfig)
    backup: BackupConfig = field(default_factory=BackupConfig)
    config_profiles: ConfigProfilesConfig = field(default_factory=ConfigProfilesConfig)
    upgrade_precheck: UpgradePrecheckConfig = field(default_factory=UpgradePrecheckConfig)

    performance_gap: PerformanceGapConfig = field(default_factory=PerformanceGapConfig)
    execution_gap: ExecutionGapConfig = field(default_factory=ExecutionGapConfig)
    signal_drift: SignalDriftConfig = field(default_factory=SignalDriftConfig)
    comparison_notifications: ComparisonNotificationsConfig = field(default_factory=ComparisonNotificationsConfig)
    notifications: NotificationsConfig = field(default_factory=NotificationsConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    notification_templates: NotificationTemplatesConfig = field(default_factory=NotificationTemplatesConfig)
    basket_simulation: BasketSimulationConfigSchema = None
    allocation_replay: AllocationReplayConfig = None
    allocation_drift: AllocationDriftConfigSchema = None
    portfolio_construction: 'PortfolioConstructionConfig' = None
    allocation_limits: 'AllocationLimitsConfig' = None
    risk_budgeting: 'RiskBudgetingConfig' = None
    concentration_guards: 'ConcentrationGuardsConfig' = None
    parameter_sensitivity: ParameterSensitivityConfigSchema = field(default_factory=ParameterSensitivityConfigSchema)
    robustness_grid: RobustnessGridConfig = field(default_factory=RobustnessGridConfig)
    stability_map: StabilityMapConfig = field(default_factory=StabilityMapConfig)
    transaction_costs: TransactionCostsConfig = field(default_factory=TransactionCostsConfig)
    slippage: SlippageConfigSchema = field(default_factory=SlippageConfigSchema)
    trade_ledger: TradeLedgerConfig = field(default_factory=TradeLedgerConfig)
    advanced_backtest_metrics: AdvancedBacktestMetricsConfig = field(default_factory=AdvancedBacktestMetricsConfig)

    taskqueue: TaskQueueConfig = field(default_factory=TaskQueueConfig)
    task_priority: TaskPriorityConfig = field(default_factory=TaskPriorityConfig)
    workload_budget: WorkloadBudgetConfig = field(default_factory=WorkloadBudgetConfig)
    run_windows: RunWindowsConfig = field(default_factory=RunWindowsConfig)
    task_conflicts: TaskConflictsConfig = field(default_factory=TaskConflictsConfig)
    queue_executor: QueueExecutorConfig = field(default_factory=QueueExecutorConfig)
    taskqueue_notifications: TaskQueueNotificationsConfig = field(default_factory=TaskQueueNotificationsConfig)
    performance_baselines: PerformanceBaselinesConfig = field(default_factory=PerformanceBaselinesConfig)
    sla_thresholds: SLAThresholdsConfig = field(default_factory=SLAThresholdsConfig)
    runtime_regression: RuntimeRegressionConfig = field(default_factory=RuntimeRegressionConfig)
    performance_acceptance: PerformanceAcceptanceConfig = field(default_factory=PerformanceAcceptanceConfig)
    performance_alerting: PerformanceAlertingConfig = field(default_factory=PerformanceAlertingConfig)
    performance_notifications: PerformanceNotificationsConfig = field(default_factory=PerformanceNotificationsConfig)
    project: ProjectConfig = field(default_factory=ProjectConfig)
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
    data: DataConfig = field(default_factory=DataConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    universe: UniverseConfig = field(default_factory=UniverseConfig)
    paper: PaperConfig = field(default_factory=PaperConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    backtest: BacktestConfig = field(default_factory=BacktestConfig)
    optimization: OptimizationConfig = field(default_factory=OptimizationConfig)
    regime: RegimeConfig = field(default_factory=RegimeConfig)
    ml: MLConfig = field(default_factory=MLConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    providers: ProviderConfig = field(default_factory=ProviderConfig)
    data_quality: DataQualityConfig = field(default_factory=DataQualityConfig)
    cache_refresh: CacheRefreshConfig = field(default_factory=CacheRefreshConfig)
    multi_timeframe: MultiTimeframeConfig = field(default_factory=MultiTimeframeConfig)
    data_readiness: DataReadinessConfig = field(default_factory=DataReadinessConfig)
    active_universe: ActiveUniverseConfig = field(default_factory=ActiveUniverseConfig)
    backtesting: BacktestingConfig = field(default_factory=BacktestingConfig)
    walk_forward: WalkForwardConfigSchema = field(default_factory=WalkForwardConfigSchema)
    out_of_sample_evaluation: OutOfSampleEvaluationConfig = field(default_factory=OutOfSampleEvaluationConfig)
    historical_replay: HistoricalReplayConfig = field(default_factory=HistoricalReplayConfig)
    signal_ranking: SignalRankingConfigSchema = field(default_factory=SignalRankingConfigSchema)
    candidate_selection: CandidateSelectionConfigSchema = field(default_factory=CandidateSelectionConfigSchema)
    strategy_portfolio: StrategyPortfolioConfigSchema = field(default_factory=StrategyPortfolioConfigSchema)
    universe_readiness_gate: UniverseReadinessGateConfig = field(default_factory=UniverseReadinessGateConfig)
    universe_runs: UniverseRunsConfig = field(default_factory=UniverseRunsConfig)
    trend_features: TrendFeatureConfig = field(default_factory=TrendFeatureConfig)
    momentum_features: MomentumFeatureConfig = field(default_factory=MomentumFeatureConfig)
    volatility_features: VolatilityFeatureConfig = field(default_factory=VolatilityFeatureConfig)

    strategies: StrategiesConfig = field(default_factory=StrategiesConfig)
    signals: SignalsConfig = field(default_factory=SignalsConfig)
    signal_scoring: SignalScoringConfigSchema = field(default_factory=SignalScoringConfigSchema)
    signal_quality: SignalQualityConfig = field(default_factory=SignalQualityConfig)
    confluence: ConfluenceConfig = field(default_factory=ConfluenceConfig)

@dataclass
class RuntimeConfig:
    notification_step_enabled: bool = False
    enabled: bool = True
    default_mode: str = "manual_once"
    data_root: str = "data"
    lock_dir: str = "data/runtime/locks"
    stop_file: str = "data/runtime/stop.json"
    stale_lock_after_seconds: int = 7200
    max_run_duration_seconds: int = 3600
    continue_on_optional_step_failure: bool = True
    fail_on_required_step_failure: bool = True
    write_runtime_events: bool = True
    write_scan_reports: bool = True
    warn_no_live_execution: bool = True

@dataclass
class MarketScanConfig:
    notify_default: bool = False
    notification_channel_default: str = "dry_run"
    enabled: bool = True
    default_scope: str = "latest_eligible_universe"
    default_timeframes: List[str] = field(default_factory=lambda: ["1d"])
    default_composite_set: str = "core"
    default_rule_strategy_set: str = "basic_rules"
    max_symbols_per_scan: int = 100
    refresh_data_default: bool = False
    write_outputs_default: bool = True
    dry_run_default: bool = False
    output_level: str = "normal"
    small_test_symbols: List[str] = field(default_factory=lambda: ["SPY", "QQQ", "AAPL"])

@dataclass
class PipelineStepsConfig:
    enabled: bool = True
    preflight_required: bool = True
    universe_resolve_required: bool = True
    data_refresh_required: bool = False
    data_readiness_required: bool = False
    feature_pipeline_required: bool = True
    strategy_run_required: bool = True
    signal_ranking_required: bool = True
    candidate_selection_required: bool = True
    risk_evaluation_required: bool = False
    portfolio_construction_required: bool = False
    cleanup_required: bool = False

@dataclass
class ScheduledScanConfig:
    enabled: bool = True
    plan_only: bool = True
    interval_minutes: int = 60
    max_runs_per_day: int = 8
    market_hours_only: bool = False
    timezone: str = "Europe/Istanbul"
    allow_background_daemon: bool = False
    allow_os_cron_install: bool = False
    write_plan_file: bool = True

def validate_observability_config(config: ObservabilityConfig) -> None:
    if config.external_telemetry_enabled:
        raise ValueError("external_telemetry_enabled must be False")
    if config.dashboard_enabled:
        raise ValueError("dashboard_enabled must be False")
    if not config.warn_local_only:
        raise ValueError("warn_local_only must be True")
    if not config.warn_not_investment_advice:
        raise ValueError("warn_not_investment_advice must be True")
    if not config.warn_no_broker_execution:
        raise ValueError("warn_no_broker_execution must be True")

def validate_log_rotation_config(config: LogRotationConfigSchema) -> None:
    if config.max_file_size_bytes <= 0:
        raise ValueError("max_file_size_bytes must be positive")
    if config.max_rotated_files <= 0:
        raise ValueError("max_rotated_files must be positive")

def validate_operational_health_config(config: OperationalHealthConfig) -> None:
    if config.disk_warning_threshold_pct < 0 or config.disk_warning_threshold_pct > 100:
        raise ValueError("disk_warning_threshold_pct must be between 0 and 100")
    if config.disk_critical_threshold_pct < 0 or config.disk_critical_threshold_pct > 100:
        raise ValueError("disk_critical_threshold_pct must be between 0 and 100")
    if config.disk_warning_threshold_pct >= config.disk_critical_threshold_pct:
        raise ValueError("disk_warning_threshold_pct must be less than disk_critical_threshold_pct")
    if config.error_warning_threshold_24h < 0:
        raise ValueError("error_warning_threshold_24h cannot be negative")
    if config.error_critical_threshold_24h < 0:
        raise ValueError("error_critical_threshold_24h cannot be negative")

def validate_safety_monitor_config(config: SafetyMonitorConfig) -> None:
    if not config.require_broker_flags_disabled:
        raise ValueError("require_broker_flags_disabled must be True")
    if not config.require_live_demo_flags_disabled:
        raise ValueError("require_live_demo_flags_disabled must be True")
    if not config.require_telegram_real_send_disabled:
        raise ValueError("require_telegram_real_send_disabled must be True")
    if not config.require_dashboard_disabled:
        raise ValueError("require_dashboard_disabled must be True")
    if not config.require_external_telemetry_disabled:
        raise ValueError("require_external_telemetry_disabled must be True")

def validate_observability_notifications_config(config: ObservabilityNotificationsConfig) -> None:
    # dry_run default can be verified in usage, but enforcing it's valid:
    if not config.dry_run and not config.warn_no_real_send_default:
        raise ValueError("If dry_run is false, warn_no_real_send_default must be True.")

@dataclass
class SchedulerConfig:
    enabled: bool = True
    store_dir: str = "data/scheduler"
    dry_run_default: bool = True
    execute_commands_default: bool = False
    install_daemon: bool = False
    install_cron: bool = False
    install_service: bool = False
    allow_destructive_jobs: bool = False
    write_scheduler_reports: bool = True
    warn_local_only: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass
class RunLocksConfig:
    enabled: bool = True
    locks_dir: str = "data/scheduler/locks"
    stale_after_seconds_default: int = 3600
    global_stale_after_seconds: int = 7200
    acquisition_mode_default: str = "FAIL_FAST"
    allow_steal_if_stale: bool = True
    cleanup_stale_locks_dry_run_default: bool = True
    write_lock_audit: bool = True

@dataclass
class ConcurrencyConfig:
    enabled: bool = True
    global_max_concurrent_runs: int = 1
    scan_max_concurrent_runs: int = 1
    backtest_max_concurrent_runs: int = 1
    paper_max_concurrent_runs: int = 1
    regression_max_concurrent_runs: int = 1
    retention_max_concurrent_runs: int = 1
    observability_max_concurrent_runs: int = 2
    notification_max_concurrent_runs: int = 1
    block_on_conflict: bool = True
    allow_overlap_default: bool = False

@dataclass
class IdempotencyConfig:
    enabled: bool = True
    store_path: str = "data/scheduler/idempotency.jsonl"
    duplicate_policy: str = "SKIP"
    record_completed_runs: bool = True
    prune_after_days: int = 30
    prune_dry_run_default: bool = True

@dataclass
class AtomicIOConfig:
    enabled: bool = True
    use_atomic_writes: bool = True
    temp_suffix: str = ".tmp"
    verify_checksum_after_write: bool = True
    block_protected_target_write: bool = False

@dataclass
class SchedulerJobsConfig:
    enabled: bool = True
    default_dry_run: bool = True
    execute_commands: bool = False
    safe_allowlist_only: bool = True
    blocked_commands: List[str] = field(default_factory=lambda: [
        "cleanup-execute",
        "rollback-execute",
        "send-broker-order",
        "live-order",
        "demo-order"
    ])

@dataclass
class SchedulerNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_scheduler_report: bool = True
    notify_stale_lock_warning: bool = True
    notify_concurrency_blocked: bool = True
    default_channel: str = "DRY_RUN"
    warn_no_real_send_default: bool = True

def validate_scheduler_config(config: SchedulerConfig) -> None:
    if not config.dry_run_default:
        pass # warning maybe, but schema says dry_run_default is true
    if config.execute_commands_default:
        raise ValueError("execute_commands_default must be False")
    if config.install_daemon:
        raise ValueError("install_daemon must be False")
    if config.install_cron:
        raise ValueError("install_cron must be False")
    if config.install_service:
        raise ValueError("install_service must be False")
    if config.allow_destructive_jobs:
        raise ValueError("allow_destructive_jobs must be False")

def validate_run_locks_config(config: RunLocksConfig) -> None:
    if config.stale_after_seconds_default <= 0:
        raise ValueError("stale_after_seconds_default must be positive")

def validate_concurrency_config(config: ConcurrencyConfig) -> None:
    for f in [config.global_max_concurrent_runs, config.scan_max_concurrent_runs,
              config.backtest_max_concurrent_runs, config.paper_max_concurrent_runs,
              config.regression_max_concurrent_runs, config.retention_max_concurrent_runs,
              config.observability_max_concurrent_runs, config.notification_max_concurrent_runs]:
        if f <= 0:
            raise ValueError("max_concurrent_runs must be positive")

def validate_idempotency_config(config: IdempotencyConfig) -> None:
    if config.duplicate_policy.upper() not in ["SKIP", "REVIEW", "BLOCK"]:
        raise ValueError("duplicate_policy must be SKIP, REVIEW, or BLOCK")
    if config.prune_after_days <= 0:
        raise ValueError("prune_after_days must be positive")

def validate_scheduler_jobs_config(config: SchedulerJobsConfig) -> None:
    if config.execute_commands:
        raise ValueError("execute_commands must be False in scheduler_jobs")
    if not config.safe_allowlist_only:
        raise ValueError("safe_allowlist_only must be True")
    if not all(cmd in config.blocked_commands for cmd in ["cleanup-execute", "rollback-execute", "send-broker-order", "live-order", "demo-order"]):
        raise ValueError("blocked_commands must include destructive commands")

def validate_scheduler_notifications_config(config: SchedulerNotificationsConfig) -> None:
    if not config.dry_run:
        raise ValueError("scheduler_notifications.dry_run must be True")


@dataclass
class SchedulerConfig:
    enabled: bool = True
    store_dir: str = "data/scheduler"
    dry_run_default: bool = True
    execute_commands_default: bool = False
    install_daemon: bool = False
    install_cron: bool = False
    install_service: bool = False
    allow_destructive_jobs: bool = False
    write_scheduler_reports: bool = True
    warn_local_only: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass
class RunLocksConfig:
    enabled: bool = True
    locks_dir: str = "data/scheduler/locks"
    stale_after_seconds_default: int = 3600
    global_stale_after_seconds: int = 7200
    acquisition_mode_default: str = "FAIL_FAST"
    allow_steal_if_stale: bool = True
    cleanup_stale_locks_dry_run_default: bool = True
    write_lock_audit: bool = True

@dataclass
class ConcurrencyConfig:
    enabled: bool = True
    global_max_concurrent_runs: int = 1
    scan_max_concurrent_runs: int = 1
    backtest_max_concurrent_runs: int = 1
    paper_max_concurrent_runs: int = 1
    regression_max_concurrent_runs: int = 1
    retention_max_concurrent_runs: int = 1
    observability_max_concurrent_runs: int = 2
    notification_max_concurrent_runs: int = 1
    block_on_conflict: bool = True
    allow_overlap_default: bool = False

@dataclass
class IdempotencyConfig:
    enabled: bool = True
    store_path: str = "data/scheduler/idempotency.jsonl"
    duplicate_policy: str = "SKIP"
    record_completed_runs: bool = True
    prune_after_days: int = 30
    prune_dry_run_default: bool = True

@dataclass
class AtomicIOConfig:
    enabled: bool = True
    use_atomic_writes: bool = True
    temp_suffix: str = ".tmp"
    verify_checksum_after_write: bool = True
    block_protected_target_write: bool = False

@dataclass
class SchedulerJobsConfig:
    enabled: bool = True
    default_dry_run: bool = True
    execute_commands: bool = False
    safe_allowlist_only: bool = True
    blocked_commands: List[str] = field(default_factory=lambda: [
        "cleanup-execute",
        "rollback-execute",
        "send-broker-order",
        "live-order",
        "demo-order"
    ])

@dataclass
class SchedulerNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_scheduler_report: bool = True
    notify_stale_lock_warning: bool = True
    notify_concurrency_blocked: bool = True
    default_channel: str = "DRY_RUN"
    warn_no_real_send_default: bool = True

def validate_scheduler_config(config: SchedulerConfig) -> None:
    if not config.dry_run_default:
        pass # warning maybe, but schema says dry_run_default is true
    if config.execute_commands_default:
        raise ValueError("execute_commands_default must be False")
    if config.install_daemon:
        raise ValueError("install_daemon must be False")
    if config.install_cron:
        raise ValueError("install_cron must be False")
    if config.install_service:
        raise ValueError("install_service must be False")
    if config.allow_destructive_jobs:
        raise ValueError("allow_destructive_jobs must be False")

def validate_run_locks_config(config: RunLocksConfig) -> None:
    if config.stale_after_seconds_default <= 0:
        raise ValueError("stale_after_seconds_default must be positive")

def validate_concurrency_config(config: ConcurrencyConfig) -> None:
    for f in [config.global_max_concurrent_runs, config.scan_max_concurrent_runs,
              config.backtest_max_concurrent_runs, config.paper_max_concurrent_runs,
              config.regression_max_concurrent_runs, config.retention_max_concurrent_runs,
              config.observability_max_concurrent_runs, config.notification_max_concurrent_runs]:
        if f <= 0:
            raise ValueError("max_concurrent_runs must be positive")

def validate_idempotency_config(config: IdempotencyConfig) -> None:
    if config.duplicate_policy.upper() not in ["SKIP", "REVIEW", "BLOCK"]:
        raise ValueError("duplicate_policy must be SKIP, REVIEW, or BLOCK")
    if config.prune_after_days <= 0:
        raise ValueError("prune_after_days must be positive")

def validate_scheduler_jobs_config(config: SchedulerJobsConfig) -> None:
    if config.execute_commands:
        raise ValueError("execute_commands must be False in scheduler_jobs")
    if not config.safe_allowlist_only:
        raise ValueError("safe_allowlist_only must be True")
    if not all(cmd in config.blocked_commands for cmd in ["cleanup-execute", "rollback-execute", "send-broker-order", "live-order", "demo-order"]):
        raise ValueError("blocked_commands must include destructive commands")

def validate_scheduler_notifications_config(config: SchedulerNotificationsConfig) -> None:
    if not config.dry_run:
        raise ValueError("scheduler_notifications.dry_run must be True")

@dataclass
class MarketCalendarConfig:
    enabled: bool = True
    calendar_name: str = "US_EQUITIES"
    timezone: str = "America/New_York"
    regular_open_time_local: str = "09:30"
    regular_close_time_local: str = "16:00"
    use_manual_holiday_file: bool = True
    holiday_file: str = "config/calendars/us_equities_holidays.example.json"
    early_close_file: str = "config/calendars/us_equities_early_closes.example.json"
    warn_calendar_not_official: bool = True
    write_calendar_reports: bool = True

@dataclass
class SessionAwarenessConfig:
    enabled: bool = True
    validate_provider_rows: bool = True
    validate_runtime_rows: bool = True
    allow_premarket_with_warning: bool = True
    allow_after_hours_with_warning: bool = True
    block_closed_session_signals: bool = True
    warn_missing_trading_days: bool = True
    max_missing_trading_days_warning: int = 3

@dataclass
class CorporateActionsConfig:
    enabled: bool = True
    manual_actions_file: str = "config/corporate_actions/manual_corporate_actions.example.json"
    load_provider_metadata_actions: bool = True
    detect_possible_splits: bool = True
    detect_possible_dividends: bool = True
    validate_adjusted_close: bool = True
    adjusted_close_tolerance_pct: float = 0.5
    split_gap_threshold_pct: float = 35.0
    price_gap_anomaly_threshold_pct: float = 15.0
    volume_anomaly_multiplier: float = 10.0
    skip_signal_on_action_date: bool = True
    skip_days_after_split: int = 3
    block_signal_on_adjusted_inconsistency: bool = True
    write_corporate_action_reports: bool = True

@dataclass
class CalendarQualityConfig:
    enabled: bool = True
    calendar_alignment_weight: float = 0.25
    session_validation_weight: float = 0.25
    corporate_action_weight: float = 0.25
    adjusted_price_weight: float = 0.25
    fail_on_non_trading_day_rows: bool = False
    warn_on_missing_trading_days: bool = True

@dataclass
class CalendarNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_calendar_session_report: bool = True
    notify_corporate_action_warning: bool = True
    notify_adjusted_price_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
