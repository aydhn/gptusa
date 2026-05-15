from typing import Any, Dict, List, Tuple, Optional
from usa_signal_bot.core.enums import StrategyRegimeCompatibility
from usa_signal_bot.strategy_adaptation.adaptation_models import StrategyRegimeProfile, StrategyCompatibilityScore, create_strategy_compatibility_score_id
from datetime import datetime, timezone

def score_strategy_regime_compatibility(profile: StrategyRegimeProfile, regime_payload: Dict[str, Any]) -> StrategyCompatibilityScore:
    return StrategyCompatibilityScore("comp1", profile.strategy_name, datetime.now(timezone.utc).isoformat(), StrategyRegimeCompatibility.COMPATIBLE, 80.0, [], [], {}, [], [])

def compatibility_score_to_text(score: StrategyCompatibilityScore) -> str:
    return "Score"
