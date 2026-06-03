from typing import Any
from usa_signal_bot.backtesting.stress_robustness.phase151_models import *

def stress_robustness_limitations_text() -> str:
    return """
LIMITATIONS:
Phase 151 is strictly an offline stress testing, scenario analysis and Monte Carlo robustness phase.
It does NOT perform live trading, paper trading, broker execution, deployment, or portfolio optimization.
The outputs of this phase are research diagnostics only and do NOT constitute investment advice.
"""

def stress_robustness_full_review_to_text(item: StressRobustnessFullReview, limit: int = 300) -> str:
    s = f"Review ID: {item.review_id}\n"
    s += f"Status: {item.context.status.value}\n"
    s += f"Ready for Phase 152: {item.phase152_readiness_gate.ready_for_phase152 if item.phase152_readiness_gate else False}\n"
    s += stress_robustness_limitations_text()
    return s
