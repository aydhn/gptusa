from typing import Optional
from .workflow_models import RepairQueueItem
from ..core.enums import ExperimentScope, ExperimentType, RepairItemType, RepairPriority, ResearchRiskLevel

def classify_experiment_scope_from_repair_item(item: RepairQueueItem) -> ExperimentScope:
    if item.item_type == RepairItemType.STRATEGY_RULE:
        return ExperimentScope.SINGLE_STRATEGY
    elif item.item_type == RepairItemType.SIGNAL_FILTER:
        return ExperimentScope.SINGLE_SIGNAL_FAMILY
    elif item.item_type == RepairItemType.REGIME_GATE:
        return ExperimentScope.REGIME_BUCKET
    elif item.item_type == RepairItemType.COST_FILTER:
        return ExperimentScope.BACKTEST_ONLY
    elif item.item_type == RepairItemType.SIZING_RULE:
        return ExperimentScope.PORTFOLIO_LEVEL
    elif item.item_type == RepairItemType.REBALANCE_RULE:
        return ExperimentScope.PORTFOLIO_LEVEL
    elif item.item_type == RepairItemType.DATA_QUALITY_RULE:
        return ExperimentScope.BACKTEST_ONLY
    elif item.item_type == RepairItemType.FEATURE_ENGINEERING:
        return ExperimentScope.BACKTEST_ONLY
    return ExperimentScope.UNKNOWN

def classify_experiment_type_from_repair_item(item: RepairQueueItem) -> ExperimentType:
    mapping = {
        RepairItemType.STRATEGY_RULE: ExperimentType.PARAMETER_CHANGE,
        RepairItemType.SIGNAL_FILTER: ExperimentType.FILTER_CHANGE,
        RepairItemType.REGIME_GATE: ExperimentType.REGIME_GATE_CHANGE,
        RepairItemType.COST_FILTER: ExperimentType.COST_FILTER_CHANGE,
        RepairItemType.LIQUIDITY_FILTER: ExperimentType.LIQUIDITY_FILTER_CHANGE,
        RepairItemType.SIZING_RULE: ExperimentType.SIZING_RULE_CHANGE,
        RepairItemType.REBALANCE_RULE: ExperimentType.REBALANCE_RULE_CHANGE,
        RepairItemType.DATA_QUALITY_RULE: ExperimentType.SIGNAL_QUALITY_CHANGE,
        RepairItemType.FEATURE_ENGINEERING: ExperimentType.FEATURE_CHANGE,
        RepairItemType.DIAGNOSTIC_TAGGING: ExperimentType.DIAGNOSTIC_TAGGING_CHANGE
    }
    return mapping.get(item.item_type, ExperimentType.UNKNOWN)

def scope_supported_for_local_planning(scope: ExperimentScope) -> bool:
    return scope != ExperimentScope.UNKNOWN

def experiment_scope_risk_level(scope: ExperimentScope, item_priority: Optional[RepairPriority] = None) -> ResearchRiskLevel:
    if scope in [ExperimentScope.PORTFOLIO_LEVEL, ExperimentScope.REGIME_BUCKET]:
        return ResearchRiskLevel.HIGH
    elif scope in [ExperimentScope.SINGLE_STRATEGY, ExperimentScope.SINGLE_SIGNAL_FAMILY]:
        return ResearchRiskLevel.MODERATE
    elif scope in [ExperimentScope.BACKTEST_ONLY, ExperimentScope.PAPER_ONLY]:
        return ResearchRiskLevel.LOW
    return ResearchRiskLevel.UNKNOWN

def experiment_scope_to_text(scope: ExperimentScope) -> str:
    return f"Scope: {scope.value}"
