import os
import re

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def write_file(file_path, content):
    ensure_dir(file_path)
    with open(file_path, 'w') as f:
        f.write(content)

# ---------------------------------------------------------
# STRESSED RESULTS (cost_robustness/stressed_results.py)
# ---------------------------------------------------------
stressed_results_content = """
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
    return "\\n".join(lines)

def stressed_backtest_result_to_text(result: CostStressedBacktestResult) -> str:
    lines = [
        "--- Stressed Backtest Result ---",
        f"Scenario ID: {result.scenario_id}",
        f"Status: {result.status.value}",
        f"Stressed Net PnL: {result.stressed_net_pnl_usd}",
        f"Profitable: {result.profitable_after_costs}"
    ]
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/stressed_results.py", stressed_results_content)

# ---------------------------------------------------------
# SENSITIVITY MATRIX (cost_robustness/sensitivity_matrix.py)
# ---------------------------------------------------------
sensitivity_matrix_content = """
from typing import List, Any, Dict, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import ExecutionSensitivityAxis, CostRobustnessStatus, CostStressType, CostStressSeverity, FillRealismMode, CostFragilityReason
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressScenario, ExecutionSensitivityCell, ExecutionSensitivityMatrix,
    create_cost_stress_scenario_id, create_execution_sensitivity_cell_id, create_execution_sensitivity_matrix_id
)
from usa_signal_bot.cost_robustness.stressed_results import stress_backtest_result

def build_sensitivity_axis_values() -> Dict[ExecutionSensitivityAxis, List[Any]]:
    return {
        ExecutionSensitivityAxis.SLIPPAGE_BPS: [1.0, 1.5, 2.0, 3.0],
        ExecutionSensitivityAxis.SPREAD_BPS: [1.0, 1.5, 2.0],
        ExecutionSensitivityAxis.IMPACT_BPS: [1.0, 2.0, 3.0],
        ExecutionSensitivityAxis.FILL_REALISM_MODE: [FillRealismMode.BASELINE, FillRealismMode.CONSERVATIVE, FillRealismMode.PESSIMISTIC, FillRealismMode.STRICT]
    }

def build_execution_sensitivity_scenarios(axis_values: Optional[Dict[ExecutionSensitivityAxis, List[Any]]] = None) -> List[CostStressScenario]:
    if axis_values is None:
        axis_values = build_sensitivity_axis_values()

    scenarios = []
    # To prevent combinatorial explosion, we vary one axis at a time while keeping others at baseline.

    baseline_slip = 1.0
    baseline_spread = 1.0
    baseline_impact = 1.0
    baseline_mode = FillRealismMode.BASELINE

    # Slippage axis
    for slip in axis_values.get(ExecutionSensitivityAxis.SLIPPAGE_BPS, []):
        if slip == baseline_slip: continue
        scenarios.append(CostStressScenario(
            scenario_id=create_cost_stress_scenario_id(f"mat_slip_{slip}"),
            name=f"Matrix: Slippage {slip}x",
            stress_type=CostStressType.SLIPPAGE,
            severity=CostStressSeverity.CUSTOM,
            slippage_multiplier=slip,
            spread_multiplier=baseline_spread,
            impact_multiplier=baseline_impact,
            fee_multiplier=1.0,
            participation_multiplier=1.0,
            min_dollar_volume=None,
            fill_realism_mode=baseline_mode,
            enabled=True
        ))

    # Fill realism axis
    for mode in axis_values.get(ExecutionSensitivityAxis.FILL_REALISM_MODE, []):
        if mode == baseline_mode: continue
        scenarios.append(CostStressScenario(
            scenario_id=create_cost_stress_scenario_id(f"mat_mode_{mode.value}"),
            name=f"Matrix: Mode {mode.value}",
            stress_type=CostStressType.FILL_REALISM,
            severity=CostStressSeverity.CUSTOM,
            slippage_multiplier=baseline_slip,
            spread_multiplier=baseline_spread,
            impact_multiplier=baseline_impact,
            fee_multiplier=1.0,
            participation_multiplier=1.0,
            min_dollar_volume=None,
            fill_realism_mode=mode,
            enabled=True
        ))

    return scenarios

def run_execution_sensitivity_matrix(baseline_result: Dict[str, Any], trades: List[Dict[str, Any]], scenarios: Optional[List[CostStressScenario]] = None) -> ExecutionSensitivityMatrix:
    if scenarios is None:
        scenarios = build_execution_sensitivity_scenarios()

    cells = []
    for sc in scenarios:
        stressed = stress_backtest_result(baseline_result, trades, sc)

        reasons = []
        if stressed.profitable_after_costs is False:
            reasons.append(CostFragilityReason.PROFIT_ERASED_BY_COSTS)

        cells.append(ExecutionSensitivityCell(
            cell_id=create_execution_sensitivity_cell_id(),
            axis_values={"scenario_name": sc.name},
            scenario_id=sc.scenario_id,
            status=stressed.status,
            net_return_pct=stressed.stressed_net_return_pct,
            sharpe=stressed.stressed_sharpe,
            max_drawdown_pct=stressed.stressed_max_drawdown_pct,
            total_cost_bps=None,
            cost_to_gross_profit_ratio=stressed.cost_to_gross_profit_ratio,
            fragility_reasons=reasons,
            warnings=stressed.warnings,
            errors=stressed.errors
        ))

    status = classify_matrix_robustness(cells)

    return ExecutionSensitivityMatrix(
        matrix_id=create_execution_sensitivity_matrix_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        axes=[ExecutionSensitivityAxis.SLIPPAGE_BPS, ExecutionSensitivityAxis.FILL_REALISM_MODE],
        cells=cells,
        baseline_metrics=baseline_result,
        worst_case_metrics={},
        best_case_metrics={},
        robustness_status=status,
        warnings=[],
        errors=[]
    )

def summarize_sensitivity_matrix(matrix: ExecutionSensitivityMatrix) -> Dict[str, Any]:
    return {"status": matrix.robustness_status.value, "cell_count": len(matrix.cells)}

def classify_matrix_robustness(cells: List[ExecutionSensitivityCell]) -> CostRobustnessStatus:
    if not cells:
        return CostRobustnessStatus.INSUFFICIENT_DATA

    fail_count = sum(1 for c in cells if c.status.value == 'FAIL')
    if fail_count > len(cells) * 0.5:
        return CostRobustnessStatus.VERY_FRAGILE
    if fail_count > 0:
        return CostRobustnessStatus.FRAGILE
    return CostRobustnessStatus.ROBUST

def execution_sensitivity_matrix_to_text(matrix: ExecutionSensitivityMatrix, limit: int = 100) -> str:
    lines = [f"--- Execution Sensitivity Matrix (Status: {matrix.robustness_status.value}) ---"]
    for c in matrix.cells[:limit]:
        lines.append(f"Cell: {c.axis_values.get('scenario_name')} | Status: {c.status.value}")
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/sensitivity_matrix.py", sensitivity_matrix_content)
