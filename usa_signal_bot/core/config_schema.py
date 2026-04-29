"""Data classes representing the configuration schema."""

from dataclasses import dataclass, field
from typing import List

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
