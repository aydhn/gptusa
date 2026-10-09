"""Single decision pipeline: signals -> regime weighting -> sizing -> risk limits -> exits.

Output is a ``Decision`` (target weights + trace). Nothing is sent anywhere; the caller books it
on the local paper ledger.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Mapping

from usa_signal_bot.decision.regime import DEFAULT_EXPOSURE
from usa_signal_bot.decision.rules import (
    ExitRules,
    PositionState,
    RiskLimits,
    apply_risk_limits,
    evaluate_exits,
    inverse_vol_weights,
)


@dataclass(frozen=True)
class DecisionConfig:
    top_n: int = 8
    min_score: float = 0.0
    regime_exposure: Mapping[str, float] = field(default_factory=lambda: dict(DEFAULT_EXPOSURE))
    exit_rules: ExitRules = field(default_factory=ExitRules)
    limits: RiskLimits = field(default_factory=RiskLimits)


@dataclass
class Decision:
    regime: str
    exposure: float
    target_weights: Dict[str, float]
    exits: Dict[str, str]
    trace: List[str]


def decide(
    cfg: DecisionConfig,
    signals: Mapping[str, float],
    vols: Mapping[str, float],
    regime: str,
    positions: Mapping[str, PositionState],
    prices: Mapping[str, float],
    current_weights: Mapping[str, float],
    drawdown: float,
    day_index: int,
) -> Decision:
    trace: List[str] = []
    exits = evaluate_exits(positions, prices, day_index, regime, cfg.exit_rules)
    if exits:
        trace.append(f"EXITS {sorted(exits.items())}")
    ranked = sorted((s for s, v in signals.items() if v > cfg.min_score and s not in exits), key=lambda s: -signals[s])
    picks = ranked[: cfg.top_n]
    exposure = float(cfg.regime_exposure.get(regime, 0.0))
    trace.append(f"REGIME {regime} exposure={exposure:.2f}; picks={picks}")
    sized = inverse_vol_weights({s: vols.get(s) for s in picks}, exposure, cfg.limits.max_weight)
    limited, reasons = apply_risk_limits(sized, current_weights, drawdown, cfg.limits)
    trace.extend(reasons)
    for sym in exits:
        limited.pop(sym, None)  # forced exits are never throttled by the turnover cap
    return Decision(regime, exposure, limited, exits, trace)
