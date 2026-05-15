from typing import List, Optional
from usa_signal_bot.core.enums import StrategyFamily
from usa_signal_bot.strategy_adaptation.adaptation_models import StrategyRegimeProfile, create_strategy_regime_profile_id

def trend_following_profile(strategy_name: str = "trend_following") -> StrategyRegimeProfile:
    return StrategyRegimeProfile(
        profile_id=create_strategy_regime_profile_id(strategy_name),
        strategy_name=strategy_name, strategy_family=StrategyFamily.TREND_FOLLOWING,
        preferred_trend_regimes=["UPTREND"], preferred_volatility_regimes=[], preferred_momentum_regimes=[],
        preferred_liquidity_regimes=[], preferred_cross_sectional_regimes=[], avoided_regimes=["CHOPPY"],
        blocked_regimes=[], base_weight=1.0, min_required_confidence=60.0
    )

def default_strategy_regime_profiles() -> List[StrategyRegimeProfile]:
    return [trend_following_profile()]

def profile_for_strategy(strategy_name: str, profiles: Optional[List[StrategyRegimeProfile]] = None) -> Optional[StrategyRegimeProfile]:
    for p in (profiles or default_strategy_regime_profiles()):
        if p.strategy_name == strategy_name: return p
    return None

def strategy_regime_profiles_to_text(profiles: List[StrategyRegimeProfile]) -> str:
    return "Profiles ready"
