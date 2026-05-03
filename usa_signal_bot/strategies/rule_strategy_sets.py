from dataclasses import dataclass, field
from typing import List, Dict, Any
from usa_signal_bot.core.exceptions import RuleStrategySetError

@dataclass
class RuleStrategySet:
    name: str
    description: str
    strategies: List[str]
    params_by_strategy: Dict[str, Dict[str, Any]] = field(default_factory=dict)

def basic_rule_strategy_set() -> RuleStrategySet:
    return RuleStrategySet(
        name="basic_rules",
        description="Basic trend and momentum rules",
        strategies=["trend_following_rule", "momentum_continuation_rule"],
        params_by_strategy={}
    )

def trend_rule_strategy_set() -> RuleStrategySet:
    return RuleStrategySet(
        name="trend_rules",
        description="Trend following rules with volume confirmation",
        strategies=["trend_following_rule", "volume_confirmation_rule"],
        params_by_strategy={}
    )

def momentum_rule_strategy_set() -> RuleStrategySet:
    return RuleStrategySet(
        name="momentum_rules",
        description="Momentum rules with volume confirmation",
        strategies=["momentum_continuation_rule", "volume_confirmation_rule"],
        params_by_strategy={}
    )

def mean_reversion_rule_strategy_set() -> RuleStrategySet:
    return RuleStrategySet(
        name="mean_reversion_rules",
        description="Mean reversion rules",
        strategies=["mean_reversion_rule"],
        params_by_strategy={}
    )

def breakout_rule_strategy_set() -> RuleStrategySet:
    return RuleStrategySet(
        name="breakout_rules",
        description="Volatility breakout rules with volume confirmation",
        strategies=["volatility_breakout_rule", "volume_confirmation_rule"],
        params_by_strategy={}
    )

def full_rule_strategy_set() -> RuleStrategySet:
    return RuleStrategySet(
        name="full_rules",
        description="Full suite of rule-based strategies",
        strategies=[
            "trend_following_rule",
            "momentum_continuation_rule",
            "mean_reversion_rule",
            "volatility_breakout_rule",
            "volume_confirmation_rule",
            "composite_technical_rule"
        ],
        params_by_strategy={}
    )

_PRESET_SETS = {
    "basic_rules": basic_rule_strategy_set,
    "trend_rules": trend_rule_strategy_set,
    "momentum_rules": momentum_rule_strategy_set,
    "mean_reversion_rules": mean_reversion_rule_strategy_set,
    "breakout_rules": breakout_rule_strategy_set,
    "full_rules": full_rule_strategy_set,
}

def get_rule_strategy_set(name: str) -> RuleStrategySet:
    if name not in _PRESET_SETS:
        raise RuleStrategySetError(f"Unknown rule strategy set: {name}")
    return _PRESET_SETS[name]()

def list_rule_strategy_sets() -> List[RuleStrategySet]:
    return [func() for func in _PRESET_SETS.values()]

def rule_strategy_set_to_dict(strategy_set: RuleStrategySet) -> dict:
    return {
        "name": strategy_set.name,
        "description": strategy_set.description,
        "strategies": strategy_set.strategies,
        "params_by_strategy": strategy_set.params_by_strategy
    }

def rule_strategy_set_to_text(strategy_set: RuleStrategySet) -> str:
    lines = [f"Rule Strategy Set: {strategy_set.name}"]
    lines.append(f"Description: {strategy_set.description}")
    lines.append("Strategies:")
    for s in strategy_set.strategies:
        lines.append(f"  - {s}")
    return "\n".join(lines)
