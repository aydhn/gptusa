"""Strategy evidence pipeline: point-in-time universe, adjusted-price validation,
cost-aware walk-forward backtest and an honest out-of-sample report.

Research only: no orders, no broker, no live or paper execution. Deterministic
(all randomness is seeded and injected).
"""

from usa_signal_bot.evidence.corporate_actions import PriceIssue, validate_adjusted_prices
from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.metrics import PerformanceSummary, summarize
from usa_signal_bot.evidence.universe import PointInTimeUniverse
from usa_signal_bot.evidence.walk_forward import WalkForwardConfig, WalkForwardResult, run_walk_forward

__all__ = [
    "CostModel",
    "PerformanceSummary",
    "PointInTimeUniverse",
    "PriceIssue",
    "WalkForwardConfig",
    "WalkForwardResult",
    "run_walk_forward",
    "summarize",
    "validate_adjusted_prices",
]
