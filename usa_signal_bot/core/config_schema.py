"""Data classes representing the configuration schema."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ProjectConfig:
    name: str = "USA Signal Bot"
    version: str = "0.2.0"
    timezone: str = "America/New_York"

@dataclass
class RuntimeConfig:
    mode: str = "local_paper_only"
    broker_order_routing_enabled: bool = False
    web_scraping_allowed: bool = False
    dashboard_enabled: bool = False
    dry_run: bool = True
    fail_fast: bool = True

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
class LoggingConfig:
    level: str = "INFO"
    log_dir: str = "data/logs"
    log_file: str = "app.log"
    enable_console: bool = True
    enable_file: bool = True
    max_bytes: int = 5000000
    backup_count: int = 5

@dataclass
class TelegramConfig:
    enabled: bool = False
    bot_token_env: str = "TELEGRAM_BOT_TOKEN"
    chat_id_env: str = "TELEGRAM_CHAT_ID"
    parse_mode: str = "HTML"

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
class PaperConfig:
    initial_cash: float = 100000.0
    currency: str = "USD"
    allow_short: bool = False
    commission_per_trade: float = 0.0
    slippage_bps: float = 5.0

@dataclass
class RiskConfig:
    max_position_pct: float = 0.10
    max_total_exposure_pct: float = 0.80
    max_daily_loss_pct: float = 0.03
    max_open_positions: int = 10

@dataclass
class BacktestConfig:
    default_initial_cash: float = 100000.0
    default_benchmark: str = "SPY"
    include_transaction_costs: bool = True

@dataclass
class OptimizationConfig:
    enabled: bool = False
    max_trials: int = 100
    walk_forward_enabled: bool = True

@dataclass
class RegimeConfig:
    enabled: bool = False
    default_market_proxy: str = "SPY"

@dataclass
class MLConfig:
    enabled: bool = False
    model_dir: str = "data/models"
    leakage_checks_enabled: bool = True


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
class ActiveUniverseConfig:
    enabled: bool = True
    prefer_active_snapshot: bool = True
    fallback_to_latest_snapshot: bool = True
    fallback_to_watchlist: bool = True
    max_symbols_per_run: int = 200
    default_asset_type_filter: Optional[str] = None
    write_resolution_report: bool = True

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
class UniverseRunsConfig:
    enabled: bool = True
    runs_dir: str = "data/universe/runs"
    readiness_dir: str = "data/universe/readiness"
    keep_last_n_runs: int = 50


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
class AppConfig:

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
    universe_readiness_gate: UniverseReadinessGateConfig = field(default_factory=UniverseReadinessGateConfig)
    universe_runs: UniverseRunsConfig = field(default_factory=UniverseRunsConfig)
    trend_features: TrendFeatureConfig = field(default_factory=TrendFeatureConfig)
