"""Decision pipeline (signals -> regime weighting -> sizing -> risk limits -> exits) and a local
simulated paper ledger. Research only: no orders, no broker, no live connection.
"""

from usa_signal_bot.decision.ledger import EXECUTION_MODE, ORDER_ROUTING_ENABLED, PaperLedger
from usa_signal_bot.decision.pipeline import Decision, DecisionConfig, decide
from usa_signal_bot.decision.rules import ExitRules, RiskLimits

__all__ = [
    "Decision",
    "DecisionConfig",
    "EXECUTION_MODE",
    "ExitRules",
    "ORDER_ROUTING_ENABLED",
    "PaperLedger",
    "RiskLimits",
    "decide",
]
