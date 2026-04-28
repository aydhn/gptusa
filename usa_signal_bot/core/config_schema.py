"""Configuration schema using standard dataclasses."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.exceptions import ConfigError
from usa_signal_bot.utils.validation_utils import (
    ensure_bool,
    ensure_positive_int,
    ensure_non_negative_int,
    ensure_ratio,
    ensure_non_empty_string
)

@dataclass
class ProjectConfig:
    name: str = "USA Signal Bot"
    version: str = "0.1.0"
    timezone: str = "America/New_York"

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ProjectConfig":
        return cls(
            name=d.get("name", "USA Signal Bot"),
            version=d.get("version", "0.1.0"),
            timezone=d.get("timezone", "America/New_York")
        )

@dataclass
class RuntimeConfig:
    mode: str = "local_paper_only"
    broker_order_routing_enabled: bool = False
    web_scraping_allowed: bool = False
    dashboard_enabled: bool = False
    dry_run: bool = True
    fail_fast: bool = True

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RuntimeConfig":
        return cls(
            mode=d.get("mode", "local_paper_only"),
            broker_order_routing_enabled=ensure_bool(d.get("broker_order_routing_enabled", False), "broker_order_routing_enabled"),
            web_scraping_allowed=ensure_bool(d.get("web_scraping_allowed", False), "web_scraping_allowed"),
            dashboard_enabled=ensure_bool(d.get("dashboard_enabled", False), "dashboard_enabled"),
            dry_run=ensure_bool(d.get("dry_run", True), "dry_run"),
            fail_fast=ensure_bool(d.get("fail_fast", True), "fail_fast")
        )

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

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DataConfig":
        return cls(
            root_dir=d.get("root_dir", "data"),
            cache_dir=d.get("cache_dir", "data/cache"),
            raw_dir=d.get("raw_dir", "data/raw"),
            processed_dir=d.get("processed_dir", "data/processed"),
            universe_dir=d.get("universe_dir", "data/universe"),
            max_download_workers=ensure_positive_int(d.get("max_download_workers", 4), "max_download_workers"),
            request_timeout_seconds=ensure_positive_int(d.get("request_timeout_seconds", 30), "request_timeout_seconds"),
            retry_attempts=ensure_non_negative_int(d.get("retry_attempts", 3), "retry_attempts")
        )

@dataclass
class LoggingConfig:
    level: str = "INFO"
    log_dir: str = "data/logs"
    log_file: str = "app.log"
    enable_console: bool = True
    enable_file: bool = True

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "LoggingConfig":
        return cls(
            level=d.get("level", "INFO"),
            log_dir=d.get("log_dir", "data/logs"),
            log_file=d.get("log_file", "app.log"),
            enable_console=ensure_bool(d.get("enable_console", True), "enable_console"),
            enable_file=ensure_bool(d.get("enable_file", True), "enable_file")
        )

@dataclass
class TelegramConfig:
    enabled: bool = False
    bot_token_env: str = "TELEGRAM_BOT_TOKEN"
    chat_id_env: str = "TELEGRAM_CHAT_ID"
    parse_mode: str = "HTML"

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TelegramConfig":
        enabled = ensure_bool(d.get("enabled", False), "enabled")
        bot_token_env = d.get("bot_token_env", "TELEGRAM_BOT_TOKEN")
        chat_id_env = d.get("chat_id_env", "TELEGRAM_CHAT_ID")

        if enabled:
            if not bot_token_env.strip():
                raise ConfigError("telegram.bot_token_env cannot be empty if telegram is enabled.")
            if not chat_id_env.strip():
                raise ConfigError("telegram.chat_id_env cannot be empty if telegram is enabled.")

        return cls(
            enabled=enabled,
            bot_token_env=bot_token_env,
            chat_id_env=chat_id_env,
            parse_mode=d.get("parse_mode", "HTML")
        )

@dataclass
class UniverseConfig:
    asset_types: List[str] = field(default_factory=lambda: ["stock", "etf"])
    default_watchlist_file: str = "data/universe/watchlist.csv"
    include_etfs: bool = True
    include_stocks: bool = True
    min_price: float = 1.0
    max_symbols_per_scan: int = 500

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "UniverseConfig":
        return cls(
            asset_types=d.get("asset_types", ["stock", "etf"]),
            default_watchlist_file=d.get("default_watchlist_file", "data/universe/watchlist.csv"),
            include_etfs=ensure_bool(d.get("include_etfs", True), "include_etfs"),
            include_stocks=ensure_bool(d.get("include_stocks", True), "include_stocks"),
            min_price=float(d.get("min_price", 1.0)),
            max_symbols_per_scan=ensure_positive_int(d.get("max_symbols_per_scan", 500), "max_symbols_per_scan")
        )

@dataclass
class PaperConfig:
    initial_cash: float = 100000.0
    currency: str = "USD"
    allow_short: bool = False
    commission_per_trade: float = 0.0
    slippage_bps: float = 5.0

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PaperConfig":
        return cls(
            initial_cash=float(d.get("initial_cash", 100000.0)),
            currency=d.get("currency", "USD"),
            allow_short=ensure_bool(d.get("allow_short", False), "allow_short"),
            commission_per_trade=float(d.get("commission_per_trade", 0.0)),
            slippage_bps=float(d.get("slippage_bps", 5.0))
        )

@dataclass
class RiskConfig:
    max_position_pct: float = 0.10
    max_total_exposure_pct: float = 0.80
    max_daily_loss_pct: float = 0.03
    max_open_positions: int = 10

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RiskConfig":
        return cls(
            max_position_pct=ensure_ratio(d.get("max_position_pct", 0.10), "max_position_pct"),
            max_total_exposure_pct=ensure_ratio(d.get("max_total_exposure_pct", 0.80), "max_total_exposure_pct"),
            max_daily_loss_pct=ensure_ratio(d.get("max_daily_loss_pct", 0.03), "max_daily_loss_pct"),
            max_open_positions=ensure_positive_int(d.get("max_open_positions", 10), "max_open_positions")
        )

@dataclass
class BacktestConfig:
    default_initial_cash: float = 100000.0
    default_benchmark: str = "SPY"
    include_transaction_costs: bool = True

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "BacktestConfig":
        return cls(
            default_initial_cash=float(d.get("default_initial_cash", 100000.0)),
            default_benchmark=d.get("default_benchmark", "SPY"),
            include_transaction_costs=ensure_bool(d.get("include_transaction_costs", True), "include_transaction_costs")
        )

@dataclass
class OptimizationConfig:
    enabled: bool = False
    max_trials: int = 100
    walk_forward_enabled: bool = True

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "OptimizationConfig":
        return cls(
            enabled=ensure_bool(d.get("enabled", False), "enabled"),
            max_trials=ensure_positive_int(d.get("max_trials", 100), "max_trials"),
            walk_forward_enabled=ensure_bool(d.get("walk_forward_enabled", True), "walk_forward_enabled")
        )

@dataclass
class RegimeConfig:
    enabled: bool = False
    default_market_proxy: str = "SPY"

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RegimeConfig":
        return cls(
            enabled=ensure_bool(d.get("enabled", False), "enabled"),
            default_market_proxy=d.get("default_market_proxy", "SPY")
        )

@dataclass
class MLConfig:
    enabled: bool = False
    model_dir: str = "data/models"
    leakage_checks_enabled: bool = True

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MLConfig":
        return cls(
            enabled=ensure_bool(d.get("enabled", False), "enabled"),
            model_dir=d.get("model_dir", "data/models"),
            leakage_checks_enabled=ensure_bool(d.get("leakage_checks_enabled", True), "leakage_checks_enabled")
        )

@dataclass
class AppConfig:
    project: ProjectConfig
    runtime: RuntimeConfig
    data: DataConfig
    logging: LoggingConfig
    telegram: TelegramConfig
    universe: UniverseConfig
    paper: PaperConfig
    risk: RiskConfig
    backtest: BacktestConfig
    optimization: OptimizationConfig
    regime: RegimeConfig
    ml: MLConfig

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AppConfig":
        return cls(
            project=ProjectConfig.from_dict(d.get("project", {})),
            runtime=RuntimeConfig.from_dict(d.get("runtime", {})),
            data=DataConfig.from_dict(d.get("data", {})),
            logging=LoggingConfig.from_dict(d.get("logging", {})),
            telegram=TelegramConfig.from_dict(d.get("telegram", {})),
            universe=UniverseConfig.from_dict(d.get("universe", {})),
            paper=PaperConfig.from_dict(d.get("paper", {})),
            risk=RiskConfig.from_dict(d.get("risk", {})),
            backtest=BacktestConfig.from_dict(d.get("backtest", {})),
            optimization=OptimizationConfig.from_dict(d.get("optimization", {})),
            regime=RegimeConfig.from_dict(d.get("regime", {})),
            ml=MLConfig.from_dict(d.get("ml", {}))
        )
