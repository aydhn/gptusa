from typing import Any, Dict, List, Optional
from usa_signal_bot.strategy_adaptation.adaptation_models import StrategyRegimeProfile
def transition_penalty_for_strategy(profile: StrategyRegimeProfile, transition_signals: Optional[List[Dict[str, Any]]] = None) -> float:
    return 0.0
