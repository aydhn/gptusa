
from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    CostStressType, CostStressSeverity, CostRobustnessStatus, ExecutionSensitivityAxis,
    FillRealismMode, CostStressResultStatus, CostFragilityReason, CostRobustnessReportType
)

@dataclass
class CostStressScenario:
    scenario_id: str
    name: str
    stress_type: CostStressType
    severity: CostStressSeverity
    slippage_multiplier: float
    spread_multiplier: float
    impact_multiplier: float
    fee_multiplier: float
    participation_multiplier: float
    min_dollar_volume: Optional[float]
    fill_realism_mode: FillRealismMode
    enabled: bool
    metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

@dataclass
class CostStressInput:
    input_id: str
    symbol: Optional[str]
    baseline_result: Dict[str, Any]
    trades: List[Dict[str, Any]]
    scenarios: List[CostStressScenario]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CostStressedTradeResult:
    result_id: str
    symbol: str
    scenario_id: str
    created_at_utc: str
    gross_pnl_usd: Optional[float]
    stressed_cost_usd: Optional[float]
    stressed_cost_bps: Optional[float]
    stressed_net_pnl_usd: Optional[float]
    stressed_return_pct: Optional[float]
    fill_status: Optional[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CostStressedBacktestResult:
    result_id: str
    scenario_id: str
    created_at_utc: str
    status: CostStressResultStatus
    trade_count: int
    gross_total_pnl_usd: Optional[float]
    stressed_total_cost_usd: Optional[float]
    stressed_net_pnl_usd: Optional[float]
    gross_return_pct: Optional[float]
    stressed_net_return_pct: Optional[float]
    gross_sharpe: Optional[float]
    stressed_sharpe: Optional[float]
    max_drawdown_pct: Optional[float]
    stressed_max_drawdown_pct: Optional[float]
    cost_to_gross_profit_ratio: Optional[float]
    profitable_after_costs: Optional[bool]
    stressed_trades: List[CostStressedTradeResult]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExecutionSensitivityCell:
    cell_id: str
    axis_values: Dict[str, Any]
    scenario_id: str
    status: CostStressResultStatus
    net_return_pct: Optional[float]
    sharpe: Optional[float]
    max_drawdown_pct: Optional[float]
    total_cost_bps: Optional[float]
    cost_to_gross_profit_ratio: Optional[float]
    fragility_reasons: List[CostFragilityReason]
    warnings: List[str]
    errors: List[str]

@dataclass
class ExecutionSensitivityMatrix:
    matrix_id: str
    created_at_utc: str
    axes: List[ExecutionSensitivityAxis]
    cells: List[ExecutionSensitivityCell]
    baseline_metrics: Dict[str, Any]
    worst_case_metrics: Dict[str, Any]
    best_case_metrics: Dict[str, Any]
    robustness_status: CostRobustnessStatus
    warnings: List[str]
    errors: List[str]

@dataclass
class WalkForwardCostRobustnessResult:
    result_id: str
    created_at_utc: str
    window_count: int
    scenario_count: int
    status: CostRobustnessStatus
    window_results: List[Dict[str, Any]]
    scenario_results: List[CostStressedBacktestResult]
    robustness_score: Optional[float]
    fragile_window_count: int
    failed_scenario_count: int
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CostFragilityAssessment:
    assessment_id: str
    created_at_utc: str
    status: CostRobustnessStatus
    fragility_score: Optional[float]
    reasons: List[CostFragilityReason]
    breakeven_cost_bps: Optional[float]
    breakeven_slippage_bps: Optional[float]
    breakeven_impact_bps: Optional[float]
    evidence: Dict[str, Any]
    warnings: List[str]
    errors: List[str]

@dataclass
class CostRobustnessReview:
    review_id: str
    created_at_utc: str
    report_type: CostRobustnessReportType
    scenarios: List[CostStressScenario]
    stressed_results: List[CostStressedBacktestResult]
    sensitivity_matrix: Optional[ExecutionSensitivityMatrix]
    walk_forward_result: Optional[WalkForwardCostRobustnessResult]
    fragility_assessment: Optional[CostFragilityAssessment]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# Implement simple to_dict functions
def cost_stress_scenario_to_dict(item: CostStressScenario) -> dict: return item.__dict__
def cost_stress_input_to_dict(item: CostStressInput) -> dict: return item.__dict__
def cost_stressed_trade_result_to_dict(item: CostStressedTradeResult) -> dict: return item.__dict__
def cost_stressed_backtest_result_to_dict(item: CostStressedBacktestResult) -> dict: return item.__dict__
def execution_sensitivity_cell_to_dict(item: ExecutionSensitivityCell) -> dict: return item.__dict__
def execution_sensitivity_matrix_to_dict(item: ExecutionSensitivityMatrix) -> dict: return item.__dict__
def walk_forward_cost_robustness_result_to_dict(item: WalkForwardCostRobustnessResult) -> dict: return item.__dict__
def cost_fragility_assessment_to_dict(item: CostFragilityAssessment) -> dict: return item.__dict__
def cost_robustness_review_to_dict(item: CostRobustnessReview) -> dict: return item.__dict__

def validate_cost_stress_scenario(item: CostStressScenario) -> None:
    if item.slippage_multiplier < 0 or item.spread_multiplier < 0 or item.impact_multiplier < 0 or item.fee_multiplier < 0 or item.participation_multiplier < 0:
        raise ValueError("Multipliers cannot be negative.")
    if item.min_dollar_volume is not None and item.min_dollar_volume < 0:
        raise ValueError("min_dollar_volume cannot be negative.")

def validate_cost_stressed_backtest_result(item: CostStressedBacktestResult) -> None: pass
def validate_execution_sensitivity_matrix(item: ExecutionSensitivityMatrix) -> None: pass
def validate_cost_fragility_assessment(item: CostFragilityAssessment) -> None:
    if item.fragility_score is not None and not (0 <= item.fragility_score <= 100):
        raise ValueError("Score must be 0-100.")
    if item.breakeven_cost_bps is not None and item.breakeven_cost_bps < 0:
        raise ValueError("Breakeven bps cannot be negative.")

def create_cost_stress_scenario_id(name: str) -> str: return f"scene_{uuid.uuid4().hex[:8]}"
def create_cost_stress_input_id(prefix: str = "cost_stress_input") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_cost_stressed_trade_result_id(symbol: str) -> str: return f"tr_{symbol}_{uuid.uuid4().hex[:8]}"
def create_cost_stressed_backtest_result_id(prefix: str = "cost_stressed_bt") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_execution_sensitivity_cell_id(prefix: str = "sensitivity_cell") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_execution_sensitivity_matrix_id(prefix: str = "sensitivity_matrix") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_walk_forward_cost_robustness_result_id(prefix: str = "wf_cost_robust") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_cost_fragility_assessment_id(prefix: str = "cost_fragility") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_cost_robustness_review_id(prefix: str = "cost_robustness_review") -> str: return f"{prefix}_{uuid.uuid4().hex[:8]}"
