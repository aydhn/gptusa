from dataclasses import dataclass, field

@dataclass
class MultiTimeframeRegimeConfig:
    enabled: bool = True
    timeframes: list[str] = field(default_factory=lambda: ["daily", "weekly", "monthly"])
    min_daily_rows: int = 120
    min_weekly_rows: int = 40
    min_monthly_rows: int = 12
    require_weekly_confirmation: bool = True
    require_monthly_confirmation_for_strict_mode: bool = False
    warn_on_timeframe_conflict: bool = True
    write_regime_map_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True

@dataclass
class TrendRegimeConfirmationConfig:
    enabled: bool = True
    short_ma_window: int = 20
    long_ma_window: int = 50
    slope_window: int = 20
    strong_trend_threshold_pct: float = 10.0
    choppy_ma_distance_pct: float = 2.0

@dataclass
class VolatilityRegimeConfirmationConfig:
    enabled: bool = True
    realized_vol_lookback: int = 20
    atr_lookback: int = 60
    compressed_vol_threshold_pct: float = 1.0
    high_vol_threshold_pct: float = 4.0
    extreme_vol_threshold_pct: float = 7.0

@dataclass
class MomentumRegimeConfirmationConfig:
    enabled: bool = True
    roc_lookback: int = 20
    strong_momentum_threshold_pct: float = 10.0
    exhaustion_threshold_pct: float = 5.0

@dataclass
class LiquidityRegimeConfirmationConfig:
    enabled: bool = True
    lookback_bars: int = 60
    thin_dollar_volume_threshold: float = 5000000.0
    deep_dollar_volume_threshold: float = 100000000.0
    thinning_score_threshold: float = 50.0

@dataclass
class CrossSectionalRegimeMapConfig:
    enabled: bool = True
    min_symbol_count: int = 20
    broad_uptrend_ratio: float = 0.60
    broad_downtrend_ratio: float = 0.60
    risk_off_breadth_threshold: float = 35.0
    risk_on_breadth_threshold: float = 65.0
    high_dispersion_threshold: float = 60.0

@dataclass
class RegimeTransitionRiskConfig:
    enabled: bool = True
    high_risk_score_threshold: float = 70.0
    critical_risk_score_threshold: float = 85.0
    warn_on_breadth_deterioration: bool = True
    warn_on_momentum_exhaustion: bool = True
    warn_on_volatility_expansion: bool = True
    warn_on_liquidity_thinning: bool = True

@dataclass
class RegimeAlignmentConfig:
    enabled: bool = True
    min_alignment_score_warning: float = 50.0
    min_alignment_score_suppression: float = 30.0
    suppress_conflicted_candidates: bool = True
    rank_penalty_on_divergence: bool = True

@dataclass
class RegimeMapNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_regime_map_report: bool = True
    notify_transition_warning: bool = True
    notify_alignment_warning: bool = True
    default_channel: str = "dry_run"
    warn_no_real_send_default: bool = True
