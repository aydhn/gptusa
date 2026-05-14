import os
import re
from pathlib import Path

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def append_if_not_exists(file_path, content, search_str):
    if not os.path.exists(file_path):
        ensure_dir(file_path)
        with open(file_path, 'w') as f:
            f.write(content)
        return

    with open(file_path, 'r') as f:
        existing = f.read()
    if search_str not in existing:
        with open(file_path, 'a') as f:
            f.write("\n" + content)

def write_file(file_path, content):
    ensure_dir(file_path)
    with open(file_path, 'w') as f:
        f.write(content)

# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------
enums_ext = """
class CostStressType(str, Enum):
    SLIPPAGE = "SLIPPAGE"
    SPREAD = "SPREAD"
    MARKET_IMPACT = "MARKET_IMPACT"
    FEE = "FEE"
    PARTICIPATION = "PARTICIPATION"
    LIQUIDITY_FILTER = "LIQUIDITY_FILTER"
    FILL_REALISM = "FILL_REALISM"
    COMBINED = "COMBINED"
    UNKNOWN = "UNKNOWN"

class CostStressSeverity(str, Enum):
    BASELINE = "BASELINE"
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"
    EXTREME = "EXTREME"
    CUSTOM = "CUSTOM"
    UNKNOWN = "UNKNOWN"

class CostRobustnessStatus(str, Enum):
    ROBUST = "ROBUST"
    ACCEPTABLE = "ACCEPTABLE"
    FRAGILE = "FRAGILE"
    VERY_FRAGILE = "VERY_FRAGILE"
    FAILED = "FAILED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNKNOWN = "UNKNOWN"

class ExecutionSensitivityAxis(str, Enum):
    SLIPPAGE_BPS = "SLIPPAGE_BPS"
    SPREAD_BPS = "SPREAD_BPS"
    IMPACT_BPS = "IMPACT_BPS"
    COMMISSION_BPS = "COMMISSION_BPS"
    PARTICIPATION_PCT = "PARTICIPATION_PCT"
    MIN_DOLLAR_VOLUME = "MIN_DOLLAR_VOLUME"
    FILL_REALISM_MODE = "FILL_REALISM_MODE"
    LIQUIDITY_STATUS = "LIQUIDITY_STATUS"
    UNKNOWN = "UNKNOWN"

class FillRealismMode(str, Enum):
    OPTIMISTIC = "OPTIMISTIC"
    BASELINE = "BASELINE"
    CONSERVATIVE = "CONSERVATIVE"
    PESSIMISTIC = "PESSIMISTIC"
    STRICT = "STRICT"
    UNKNOWN = "UNKNOWN"

class CostStressResultStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNKNOWN = "UNKNOWN"

class CostFragilityReason(str, Enum):
    PROFIT_ERASED_BY_COSTS = "PROFIT_ERASED_BY_COSTS"
    SHARPE_COLLAPSE = "SHARPE_COLLAPSE"
    DRAWDOWN_EXPANSION = "DRAWDOWN_EXPANSION"
    LOW_MARGIN_PER_TRADE = "LOW_MARGIN_PER_TRADE"
    HIGH_TURNOVER = "HIGH_TURNOVER"
    HIGH_IMPACT_SENSITIVITY = "HIGH_IMPACT_SENSITIVITY"
    HIGH_SLIPPAGE_SENSITIVITY = "HIGH_SLIPPAGE_SENSITIVITY"
    LOW_LIQUIDITY_DEPENDENCE = "LOW_LIQUIDITY_DEPENDENCE"
    STRICT_FILL_FAILURE = "STRICT_FILL_FAILURE"
    UNKNOWN = "UNKNOWN"

class CostRobustnessReportType(str, Enum):
    STRESS_SCENARIO_SUMMARY = "STRESS_SCENARIO_SUMMARY"
    SENSITIVITY_MATRIX = "SENSITIVITY_MATRIX"
    WALK_FORWARD_COST_ROBUSTNESS = "WALK_FORWARD_COST_ROBUSTNESS"
    FRAGILITY_REVIEW = "FRAGILITY_REVIEW"
    FULL_COST_ROBUSTNESS_REVIEW = "FULL_COST_ROBUSTNESS_REVIEW"
"""
append_if_not_exists("usa_signal_bot/core/enums.py", enums_ext, "CostStressType")

# In core/enums.py, we might also need to append to NotificationType and AlertType if they exist.
# Let's do a sed replacement directly via python if needed.
enum_file = "usa_signal_bot/core/enums.py"
if os.path.exists(enum_file):
    with open(enum_file, 'r') as f:
        content = f.read()
    if 'NotificationType' in content and 'COST_ROBUSTNESS_REPORT' not in content:
        content = re.sub(r'(class NotificationType.*?):', r'\1:\n    COST_ROBUSTNESS_REPORT = "COST_ROBUSTNESS_REPORT"\n    COST_FRAGILITY_WARNING = "COST_FRAGILITY_WARNING"\n    EXECUTION_SENSITIVITY_WARNING = "EXECUTION_SENSITIVITY_WARNING"', content, count=1, flags=re.DOTALL)
    if 'AlertType' in content and 'COST_ROBUSTNESS_FAILED' not in content:
        content = re.sub(r'(class AlertType.*?):', r'\1:\n    COST_ROBUSTNESS_FAILED = "COST_ROBUSTNESS_FAILED"\n    COST_FRAGILITY_DETECTED = "COST_FRAGILITY_DETECTED"\n    EXECUTION_SENSITIVITY_HIGH = "EXECUTION_SENSITIVITY_HIGH"', content, count=1, flags=re.DOTALL)
    with open(enum_file, 'w') as f:
        f.write(content)

# ---------------------------------------------------------
# EXCEPTIONS
# ---------------------------------------------------------
exceptions_ext = """
class CostRobustnessError(Exception): pass
class CostStressScenarioError(CostRobustnessError): pass
class SlippageStressError(CostRobustnessError): pass
class SpreadStressError(CostRobustnessError): pass
class ImpactStressError(CostRobustnessError): pass
class FeeStressError(CostRobustnessError): pass
class ParticipationStressError(CostRobustnessError): pass
class LiquidityFilterStressError(CostRobustnessError): pass
class FillRealismStressError(CostRobustnessError): pass
class ExecutionSensitivityMatrixError(CostRobustnessError): pass
class WalkForwardCostRobustnessError(CostRobustnessError): pass
class CostFragilityError(CostRobustnessError): pass
class BreakevenCostError(CostRobustnessError): pass
class CostRobustnessStorageError(CostRobustnessError): pass
class CostRobustnessValidationError(CostRobustnessError): pass
class CostRobustnessReportingError(CostRobustnessError): pass
"""
append_if_not_exists("usa_signal_bot/core/exceptions.py", exceptions_ext, "CostRobustnessError")

# ---------------------------------------------------------
# MODELS (cost_robustness/robustness_models.py)
# ---------------------------------------------------------
models_content = """
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

"""
write_file("usa_signal_bot/cost_robustness/robustness_models.py", models_content)
