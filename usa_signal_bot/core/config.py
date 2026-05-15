from usa_signal_bot.core.config_schema import (
    MultiTimeframeRegimeConfig,
    TrendRegimeConfirmationConfig,
    VolatilityRegimeConfirmationConfig,
    MomentumRegimeConfirmationConfig,
    LiquidityRegimeConfirmationConfig,
    CrossSectionalRegimeMapConfig,
    RegimeTransitionRiskConfig,
    RegimeAlignmentConfig,
    RegimeMapNotificationsConfig
)

class AppConfig:
    def __init__(self):
        self.multi_timeframe_regime = MultiTimeframeRegimeConfig()
        self.trend_regime_confirmation = TrendRegimeConfirmationConfig()
        self.volatility_regime_confirmation = VolatilityRegimeConfirmationConfig()
        self.momentum_regime_confirmation = MomentumRegimeConfirmationConfig()
        self.liquidity_regime_confirmation = LiquidityRegimeConfirmationConfig()
        self.cross_sectional_regime_map = CrossSectionalRegimeMapConfig()
        self.regime_transition_risk = RegimeTransitionRiskConfig()
        self.regime_alignment = RegimeAlignmentConfig()
        self.regime_map_notifications = RegimeMapNotificationsConfig()

_config = AppConfig()

def get_config() -> AppConfig:
    return _config
