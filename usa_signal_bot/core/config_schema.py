"""Data classes representing the configuration schema."""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

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
class HistoricalReplayConfig:
    enabled: bool = True
    require_cached_market_data: bool = True
    require_signal_file: bool = True
    prevent_same_bar_fill: bool = True
    default_timeframe: str = "1d"
    max_symbols_per_backtest: int = 50
    max_events_per_run: int = 100000

@dataclass
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
class OutOfSampleEvaluationConfig:
    enabled: bool = True
    min_completed_windows: int = 2
    min_oos_positive_window_ratio: float = 0.50
    max_average_degradation_pct: float = 0.0
    min_stability_score: float = 50.0
    classify_results: bool = True
    warn_if_insufficient_windows: bool = True



@dataclass
class AppConfig:
    transaction_costs: TransactionCostsConfig = field(default_factory=TransactionCostsConfig)
    slippage: SlippageConfigSchema = field(default_factory=SlippageConfigSchema)
    trade_ledger: TradeLedgerConfig = field(default_factory=TradeLedgerConfig)
    advanced_backtest_metrics: AdvancedBacktestMetricsConfig = field(default_factory=AdvancedBacktestMetricsConfig)

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
