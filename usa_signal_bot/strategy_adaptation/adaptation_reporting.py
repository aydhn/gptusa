from typing import Any, Dict
from usa_signal_bot.strategy_adaptation.adaptation_models import StrategyGateResult, StrategyEnsembleResult

def strategy_gate_result_to_text(item: StrategyGateResult) -> str:
    return "Gate Text"
def strategy_ensemble_result_to_text(item: StrategyEnsembleResult, limit: int = 100) -> str:
    return "Ensemble Text"
