from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestMetricInventoryItem, BacktestBandPhase, BacktestMetricInventoryKind,
    BacktestClosureRiskFlag
)

def extract_metric_items_from_payload(phase: BacktestBandPhase, payload: dict[str, Any]) -> list[BacktestMetricInventoryItem]:
    items = []
    # simplified mock extraction for inventory
    if phase == BacktestBandPhase.PHASE147_BACKTEST_RUN:
        metrics = payload.get("metrics", {})
        if "total_return" in metrics:
            item = BacktestMetricInventoryItem(
                metric_kind=BacktestMetricInventoryKind.RETURN_METRIC,
                metric_name="Total Return",
                source_phase=phase,
                source_artifact="BACKTEST_RUN_REVIEW",
                value=metrics["total_return"],
                non_trading_metric=True,
                not_investment_advice=True,
                suitable_for_phase153_research_input=True
            )
            items.append(item)
    elif phase == BacktestBandPhase.PHASE151_STRESS_MONTE_CARLO:
        stress = payload.get("stress_validation_report", {})
        if "max_stress_drawdown" in stress:
            item = BacktestMetricInventoryItem(
                metric_kind=BacktestMetricInventoryKind.STRESS_METRIC,
                metric_name="Max Stress Drawdown",
                source_phase=phase,
                source_artifact="STRESS_VALIDATION_REPORT",
                value=stress["max_stress_drawdown"],
                non_trading_metric=True,
                not_investment_advice=True,
                suitable_for_phase153_research_input=True
            )
            items.append(item)
    return items

def build_backtest_metric_inventory(payloads: dict[str, dict[str, Any]]) -> list[BacktestMetricInventoryItem]:
    inventory = []
    for phase_name, payload in payloads.items():
        try:
            phase = BacktestBandPhase(phase_name)
        except ValueError:
            phase = BacktestBandPhase.UNKNOWN
        inventory.extend(extract_metric_items_from_payload(phase, payload))
    return inventory

def validate_backtest_metric_inventory(items: list[BacktestMetricInventoryItem]) -> list[str]:
    errors = []
    for item in items:
        if not item.non_trading_metric:
            errors.append(f"Metric {item.metric_name} is not marked as non-trading")
        if not item.not_investment_advice:
            errors.append(f"Metric {item.metric_name} flagged as investment advice")
    return errors

def metric_inventory_summary(items: list[BacktestMetricInventoryItem]) -> dict[str, Any]:
    return {"count": len(items)}

def metric_inventory_to_text(items: list[BacktestMetricInventoryItem], limit: int = 300) -> str:
    return f"Metric Inventory: {len(items)} items"
