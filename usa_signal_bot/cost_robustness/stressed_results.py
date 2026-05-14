
from typing import List, Any, Dict, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import CostStressResultStatus
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressScenario, CostStressedTradeResult, CostStressedBacktestResult,
    create_cost_stressed_trade_result_id, create_cost_stressed_backtest_result_id
)
from usa_signal_bot.cost_robustness.fill_realism_stress import apply_fill_realism_mode_to_trade

def stress_trade_result(trade: Dict[str, Any], scenario: CostStressScenario) -> CostStressedTradeResult:
    # 1. Apply liquidity filter (if fails, return immediately?)
    # For now, we process it and rely on the backtest builder to filter them out or mark as failed.

    # 2. Apply fill realism
    modified_trade = apply_fill_realism_mode_to_trade(trade, scenario)

    symbol = modified_trade.get('symbol', 'UNKNOWN')
    gross_pnl = modified_trade.get('gross_pnl_usd')

    # Calculate stressed costs
    # Fallback to estimated costs in trade, then apply multipliers
    # Simplified logic here:
    base_cost_usd = modified_trade.get('estimated_cost_usd', 0.0)

    # A robust model would decompose and apply individual multipliers.
    # We will use a generic combo multiplier for demonstration if component level isn't available
    combo_multiplier = max(scenario.slippage_multiplier, scenario.spread_multiplier, scenario.impact_multiplier, scenario.fee_multiplier)

    penalty_bps = modified_trade.get('metadata', {}).get('fill_realism_penalty_bps', 0.0)
    notional = modified_trade.get('notional_value_usd', 0.0)
    penalty_usd = notional * (penalty_bps / 10000.0)

    stressed_cost_usd = (base_cost_usd * combo_multiplier) + penalty_usd

    stressed_net_pnl_usd = None
    if gross_pnl is not None:
        stressed_net_pnl_usd = gross_pnl - stressed_cost_usd

    warnings = list(modified_trade.get('warnings', []))
    if modified_trade.get('metadata', {}).get('fill_realism_blocked'):
        warnings.append("Trade blocked by fill realism")

    return CostStressedTradeResult(
        result_id=create_cost_stressed_trade_result_id(symbol),
        symbol=symbol,
        scenario_id=scenario.scenario_id,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gross_pnl_usd=gross_pnl,
        stressed_cost_usd=stressed_cost_usd,
        stressed_cost_bps=None, # Needs explicit calculation
        stressed_net_pnl_usd=stressed_net_pnl_usd,
        stressed_return_pct=None,
        fill_status="BLOCKED" if modified_trade.get('metadata', {}).get('fill_realism_blocked') else "FILLED",
        warnings=warnings,
        errors=[],
        metadata=modified_trade.get('metadata', {})
    )

def stress_backtest_result(baseline_result: Dict[str, Any], trades: List[Dict[str, Any]], scenario: CostStressScenario) -> CostStressedBacktestResult:
    stressed_trades = []
    from usa_signal_bot.cost_robustness.liquidity_filter_stress import symbol_passes_liquidity_filter

    warnings = []
    for trade in trades:
        # Apply Liquidity Filter
        adv = trade.get('avg_dollar_volume')
        if not symbol_passes_liquidity_filter(adv, scenario):
            warnings.append(f"Trade {trade.get('symbol')} skipped due to liquidity filter")
            continue

        str_trade = stress_trade_result(trade, scenario)
        stressed_trades.append(str_trade)

    gross_total_pnl = baseline_result.get('gross_total_pnl_usd', 0.0)
    stressed_total_cost = sum(t.stressed_cost_usd for t in stressed_trades if t.stressed_cost_usd is not None)
    stressed_net_pnl = sum(t.stressed_net_pnl_usd for t in stressed_trades if t.stressed_net_pnl_usd is not None)

    profitable = stressed_net_pnl > 0 if stressed_net_pnl is not None else None

    result = CostStressedBacktestResult(
        result_id=create_cost_stressed_backtest_result_id(),
        scenario_id=scenario.scenario_id,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=CostStressResultStatus.UNKNOWN,
        trade_count=len(stressed_trades),
        gross_total_pnl_usd=gross_total_pnl,
        stressed_total_cost_usd=stressed_total_cost,
        stressed_net_pnl_usd=stressed_net_pnl,
        gross_return_pct=baseline_result.get('gross_return_pct'),
        stressed_net_return_pct=None, # Approximate or recompute
        gross_sharpe=baseline_result.get('gross_sharpe'),
        stressed_sharpe=None, # Recompute required
        max_drawdown_pct=baseline_result.get('max_drawdown_pct'),
        stressed_max_drawdown_pct=None,
        cost_to_gross_profit_ratio=(stressed_total_cost / gross_total_pnl) if gross_total_pnl and gross_total_pnl > 0 else None,
        profitable_after_costs=profitable,
        stressed_trades=stressed_trades,
        warnings=warnings,
        errors=[],
        metadata={}
    )

    result.status = calculate_stressed_result_status(result)
    return result

def calculate_stressed_result_status(result: CostStressedBacktestResult) -> CostStressResultStatus:
    if result.stressed_net_pnl_usd is None:
        return CostStressResultStatus.INSUFFICIENT_DATA
    if result.stressed_net_pnl_usd < 0:
        return CostStressResultStatus.FAIL
    if result.cost_to_gross_profit_ratio is not None and result.cost_to_gross_profit_ratio > 0.8:
        return CostStressResultStatus.WARN
    return CostStressResultStatus.PASS

def stressed_trade_results_to_text(results: List[CostStressedTradeResult], limit: int = 50) -> str:
    lines = [f"--- Stressed Trade Results (showing {min(len(results), limit)}) ---"]
    for r in results[:limit]:
        lines.append(f"{r.symbol} | Net PnL: {r.stressed_net_pnl_usd} | Status: {r.fill_status}")
    return "\n".join(lines)

def stressed_backtest_result_to_text(result: CostStressedBacktestResult) -> str:
    lines = [
        "--- Stressed Backtest Result ---",
        f"Scenario ID: {result.scenario_id}",
        f"Status: {result.status.value}",
        f"Stressed Net PnL: {result.stressed_net_pnl_usd}",
        f"Profitable: {result.profitable_after_costs}"
    ]
    return "\n".join(lines)
