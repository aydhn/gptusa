
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
    return "\n".join(lines)
