from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from usa_signal_bot.core.enums import RuleConditionOperator, RuleConditionStatus, RuleStrategyFamily, RuleSignalBias, SignalAction
from usa_signal_bot.core.exceptions import RuleConditionError, RuleStrategyError

@dataclass
class RuleCondition:
    name: str
    feature_name: str
    operator: RuleConditionOperator
    threshold: Optional[Any] = None
    lower: Optional[float] = None
    upper: Optional[float] = None
    weight: float = 1.0
    required: bool = True
    description: Optional[str] = None

@dataclass
class RuleConditionResult:
    condition: RuleCondition
    status: RuleConditionStatus
    passed: bool
    observed_value: Any
    message: str
    score_contribution: float

@dataclass
class RuleEvaluation:
    symbol: str
    timeframe: str
    timestamp_utc: str
    strategy_name: str
    family: RuleStrategyFamily
    condition_results: List[RuleConditionResult]
    passed_count: int
    failed_count: int
    missing_count: int
    raw_score: float
    normalized_score: float
    bias: RuleSignalBias
    reasons: List[str]
    warnings: List[str]

@dataclass
class RuleStrategyDefinition:
    name: str
    family: RuleStrategyFamily
    description: str
    conditions: List[RuleCondition]
    required_features: List[str]
    default_action: SignalAction
    min_passed_conditions: int
    min_normalized_score: float
    experimental: bool = True

def validate_rule_condition(condition: RuleCondition) -> None:
    if not condition.name:
        raise RuleConditionError("name cannot be empty")
    if not condition.feature_name:
        raise RuleConditionError("feature_name cannot be empty")
    if not isinstance(condition.operator, RuleConditionOperator):
        raise RuleConditionError("operator must be a valid RuleConditionOperator")

    if condition.operator in [RuleConditionOperator.BETWEEN, RuleConditionOperator.OUTSIDE]:
        if condition.lower is None or condition.upper is None:
            raise RuleConditionError("lower and upper bounds required for BETWEEN/OUTSIDE")
        if condition.lower >= condition.upper:
            raise RuleConditionError("lower bound must be less than upper bound")

def validate_rule_strategy_definition(definition: RuleStrategyDefinition) -> None:
    if not definition.name:
        raise RuleStrategyError("name cannot be empty")
    if not isinstance(definition.family, RuleStrategyFamily):
        raise RuleStrategyError("family must be a valid RuleStrategyFamily")
    if not definition.conditions:
        raise RuleStrategyError("conditions cannot be empty")
    if not isinstance(definition.required_features, list):
        raise RuleStrategyError("required_features must be a list")
    if not isinstance(definition.default_action, SignalAction):
        raise RuleStrategyError("default_action must be a valid SignalAction")
    if definition.min_passed_conditions < 0:
        raise RuleStrategyError("min_passed_conditions cannot be negative")
    if not (0.0 <= definition.min_normalized_score <= 100.0):
        raise RuleStrategyError("min_normalized_score must be between 0.0 and 100.0")

    for cond in definition.conditions:
        validate_rule_condition(cond)

def rule_condition_to_dict(condition: RuleCondition) -> dict:
    return {
        "name": condition.name,
        "feature_name": condition.feature_name,
        "operator": condition.operator.value if hasattr(condition.operator, 'value') else condition.operator,
        "threshold": condition.threshold,
        "lower": condition.lower,
        "upper": condition.upper,
        "weight": condition.weight,
        "required": condition.required,
        "description": condition.description
    }

def rule_condition_result_to_dict(result: RuleConditionResult) -> dict:
    return {
        "condition": rule_condition_to_dict(result.condition),
        "status": result.status.value if hasattr(result.status, 'value') else result.status,
        "passed": result.passed,
        "observed_value": result.observed_value,
        "message": result.message,
        "score_contribution": result.score_contribution
    }

def rule_evaluation_to_dict(evaluation: RuleEvaluation) -> dict:
    return {
        "symbol": evaluation.symbol,
        "timeframe": evaluation.timeframe,
        "timestamp_utc": evaluation.timestamp_utc,
        "strategy_name": evaluation.strategy_name,
        "family": evaluation.family.value if hasattr(evaluation.family, 'value') else evaluation.family,
        "condition_results": [rule_condition_result_to_dict(r) for r in evaluation.condition_results],
        "passed_count": evaluation.passed_count,
        "failed_count": evaluation.failed_count,
        "missing_count": evaluation.missing_count,
        "raw_score": evaluation.raw_score,
        "normalized_score": evaluation.normalized_score,
        "bias": evaluation.bias.value if hasattr(evaluation.bias, 'value') else evaluation.bias,
        "reasons": evaluation.reasons,
        "warnings": evaluation.warnings
    }

def rule_strategy_definition_to_dict(definition: RuleStrategyDefinition) -> dict:
    return {
        "name": definition.name,
        "family": definition.family.value if hasattr(definition.family, 'value') else definition.family,
        "description": definition.description,
        "conditions": [rule_condition_to_dict(c) for c in definition.conditions],
        "required_features": definition.required_features,
        "default_action": definition.default_action.value if hasattr(definition.default_action, 'value') else definition.default_action,
        "min_passed_conditions": definition.min_passed_conditions,
        "min_normalized_score": definition.min_normalized_score,
        "experimental": definition.experimental
    }
