from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import StrategyGateDecision, StrategyAdaptationRisk
from usa_signal_bot.strategy_adaptation.adaptation_models import StrategyRegimeProfile, StrategyCompatibilityScore, StrategyGateResult, create_strategy_gate_result_id

class StrategyGateEngine:
    def evaluate_strategy(self, profile: StrategyRegimeProfile, regime_payload: Dict[str, Any], symbol: Optional[str] = None) -> StrategyGateResult:
        return StrategyGateResult("g1", profile.strategy_name, symbol, datetime.now(timezone.utc).isoformat(), StrategyGateDecision.ALLOW, StrategyAdaptationRisk.LOW, None, 1.0, 0.0, None, [], [], [])
