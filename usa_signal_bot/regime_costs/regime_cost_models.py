import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import (
    CostVolatilityRegime,
    CostLiquidityRegime,
    CostSpreadRegime,
    CostSessionRegime,
    CostLifecycleRegime,
    CombinedCostRegime,
    RegimeCostCurveProfile,
    AdaptiveExecutionDecision,
    RegimeCostAdjustmentStatus,
    RegimeCostReportType
)
from usa_signal_bot.core.exceptions import RegimeCostValidationError

def get_utc_now_str() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class CostRegimeSnapshot:
    snapshot_id: str
    symbol: str
    created_at_utc: str
    volatility_regime: CostVolatilityRegime
    liquidity_regime: CostLiquidityRegime
    spread_regime: CostSpreadRegime
    session_regime: CostSessionRegime
    lifecycle_regime: CostLifecycleRegime
    combined_regime: CombinedCostRegime
    evidence: Dict[str, Any]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCostMultiplier:
    multiplier_id: str
    symbol: Optional[str]
    created_at_utc: str
    volatility_multiplier: float
    liquidity_multiplier: float
    spread_multiplier: float
    session_multiplier: float
    lifecycle_multiplier: float
    combined_multiplier: float
    min_cost_bps: Optional[float]
    max_cost_bps: Optional[float]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCostCurveSelection:
    selection_id: str
    symbol: str
    created_at_utc: str
    profile: RegimeCostCurveProfile
    selected_curve_id: Optional[str]
    base_curve_id: Optional[str]
    regime_snapshot: Optional[CostRegimeSnapshot]
    multiplier: Optional[RegimeCostMultiplier]
    reason: str
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdaptiveExecutionRealismDecision:
    decision_id: str
    symbol: str
    created_at_utc: str
    decision: AdaptiveExecutionDecision
    status: RegimeCostAdjustmentStatus
    combined_regime: CombinedCostRegime
    cost_curve_profile: RegimeCostCurveProfile
    recommended_guards: List[str]
    reasons: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeAwareCostBreakdown:
    breakdown_id: str
    symbol: str
    created_at_utc: str
    base_cost_breakdown: Optional[Dict[str, Any]]
    adjusted_cost_breakdown: Optional[Dict[str, Any]]
    regime_snapshot: Optional[CostRegimeSnapshot]
    curve_selection: Optional[RegimeCostCurveSelection]
    adaptive_decision: Optional[AdaptiveExecutionRealismDecision]
    total_base_cost_bps: Optional[float]
    total_adjusted_cost_bps: Optional[float]
    adjustment_delta_bps: Optional[float]
    status: RegimeCostAdjustmentStatus
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegimeCostReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeCostReportType
    symbols: List[str]
    snapshots: List[CostRegimeSnapshot]
    multipliers: List[RegimeCostMultiplier]
    curve_selections: List[RegimeCostCurveSelection]
    adaptive_decisions: List[AdaptiveExecutionRealismDecision]
    cost_breakdowns: List[RegimeAwareCostBreakdown]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]


def cost_regime_snapshot_to_dict(item: CostRegimeSnapshot) -> Dict[str, Any]:
    return {
        "snapshot_id": item.snapshot_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "volatility_regime": item.volatility_regime.value if isinstance(item.volatility_regime, CostVolatilityRegime) else item.volatility_regime,
        "liquidity_regime": item.liquidity_regime.value if isinstance(item.liquidity_regime, CostLiquidityRegime) else item.liquidity_regime,
        "spread_regime": item.spread_regime.value if isinstance(item.spread_regime, CostSpreadRegime) else item.spread_regime,
        "session_regime": item.session_regime.value if isinstance(item.session_regime, CostSessionRegime) else item.session_regime,
        "lifecycle_regime": item.lifecycle_regime.value if isinstance(item.lifecycle_regime, CostLifecycleRegime) else item.lifecycle_regime,
        "combined_regime": item.combined_regime.value if isinstance(item.combined_regime, CombinedCostRegime) else item.combined_regime,
        "evidence": item.evidence,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def regime_cost_multiplier_to_dict(item: RegimeCostMultiplier) -> Dict[str, Any]:
    return {
        "multiplier_id": item.multiplier_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "volatility_multiplier": item.volatility_multiplier,
        "liquidity_multiplier": item.liquidity_multiplier,
        "spread_multiplier": item.spread_multiplier,
        "session_multiplier": item.session_multiplier,
        "lifecycle_multiplier": item.lifecycle_multiplier,
        "combined_multiplier": item.combined_multiplier,
        "min_cost_bps": item.min_cost_bps,
        "max_cost_bps": item.max_cost_bps,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def regime_cost_curve_selection_to_dict(item: RegimeCostCurveSelection) -> Dict[str, Any]:
    return {
        "selection_id": item.selection_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "profile": item.profile.value if isinstance(item.profile, RegimeCostCurveProfile) else item.profile,
        "selected_curve_id": item.selected_curve_id,
        "base_curve_id": item.base_curve_id,
        "regime_snapshot": cost_regime_snapshot_to_dict(item.regime_snapshot) if item.regime_snapshot else None,
        "multiplier": regime_cost_multiplier_to_dict(item.multiplier) if item.multiplier else None,
        "reason": item.reason,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def adaptive_execution_realism_decision_to_dict(item: AdaptiveExecutionRealismDecision) -> Dict[str, Any]:
    return {
        "decision_id": item.decision_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "decision": item.decision.value if isinstance(item.decision, AdaptiveExecutionDecision) else item.decision,
        "status": item.status.value if isinstance(item.status, RegimeCostAdjustmentStatus) else item.status,
        "combined_regime": item.combined_regime.value if isinstance(item.combined_regime, CombinedCostRegime) else item.combined_regime,
        "cost_curve_profile": item.cost_curve_profile.value if isinstance(item.cost_curve_profile, RegimeCostCurveProfile) else item.cost_curve_profile,
        "recommended_guards": item.recommended_guards,
        "reasons": item.reasons,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def regime_aware_cost_breakdown_to_dict(item: RegimeAwareCostBreakdown) -> Dict[str, Any]:
    return {
        "breakdown_id": item.breakdown_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "base_cost_breakdown": item.base_cost_breakdown,
        "adjusted_cost_breakdown": item.adjusted_cost_breakdown,
        "regime_snapshot": cost_regime_snapshot_to_dict(item.regime_snapshot) if item.regime_snapshot else None,
        "curve_selection": regime_cost_curve_selection_to_dict(item.curve_selection) if item.curve_selection else None,
        "adaptive_decision": adaptive_execution_realism_decision_to_dict(item.adaptive_decision) if item.adaptive_decision else None,
        "total_base_cost_bps": item.total_base_cost_bps,
        "total_adjusted_cost_bps": item.total_adjusted_cost_bps,
        "adjustment_delta_bps": item.adjustment_delta_bps,
        "status": item.status.value if isinstance(item.status, RegimeCostAdjustmentStatus) else item.status,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def regime_cost_review_to_dict(item: RegimeCostReview) -> Dict[str, Any]:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value if isinstance(item.report_type, RegimeCostReportType) else item.report_type,
        "symbols": item.symbols,
        "snapshots": [cost_regime_snapshot_to_dict(x) for x in item.snapshots],
        "multipliers": [regime_cost_multiplier_to_dict(x) for x in item.multipliers],
        "curve_selections": [regime_cost_curve_selection_to_dict(x) for x in item.curve_selections],
        "adaptive_decisions": [adaptive_execution_realism_decision_to_dict(x) for x in item.adaptive_decisions],
        "cost_breakdowns": [regime_aware_cost_breakdown_to_dict(x) for x in item.cost_breakdowns],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_cost_regime_snapshot(item: CostRegimeSnapshot) -> None:
    if not item.symbol:
        raise RegimeCostValidationError("Symbol cannot be empty.")

def validate_regime_cost_multiplier(item: RegimeCostMultiplier) -> None:
    if item.volatility_multiplier < 0 or item.liquidity_multiplier < 0 or item.spread_multiplier < 0 or item.session_multiplier < 0 or item.lifecycle_multiplier < 0 or item.combined_multiplier < 0:
        raise RegimeCostValidationError("Multipliers cannot be negative.")
    if item.min_cost_bps is not None and item.max_cost_bps is not None:
        if item.max_cost_bps < item.min_cost_bps:
            raise RegimeCostValidationError("max_cost_bps cannot be less than min_cost_bps.")

def validate_regime_cost_curve_selection(item: RegimeCostCurveSelection) -> None:
    if not item.symbol:
        raise RegimeCostValidationError("Symbol cannot be empty.")

def validate_adaptive_execution_realism_decision(item: AdaptiveExecutionRealismDecision) -> None:
    if not item.symbol:
        raise RegimeCostValidationError("Symbol cannot be empty.")

def validate_regime_aware_cost_breakdown(item: RegimeAwareCostBreakdown) -> None:
    if not item.symbol:
        raise RegimeCostValidationError("Symbol cannot be empty.")
    if item.total_base_cost_bps is not None and item.total_base_cost_bps < 0:
        raise RegimeCostValidationError("Base cost bps cannot be negative.")
    if item.total_adjusted_cost_bps is not None and item.total_adjusted_cost_bps < 0:
        raise RegimeCostValidationError("Adjusted cost bps cannot be negative.")

def create_cost_regime_snapshot_id(symbol: str) -> str:
    return f"snap_{symbol}_{uuid.uuid4().hex[:8]}"

def create_regime_cost_multiplier_id(symbol: Optional[str] = None) -> str:
    s = symbol if symbol else "generic"
    return f"mult_{s}_{uuid.uuid4().hex[:8]}"

def create_regime_cost_curve_selection_id(symbol: str) -> str:
    return f"curv_{symbol}_{uuid.uuid4().hex[:8]}"

def create_adaptive_execution_decision_id(symbol: str) -> str:
    return f"dec_{symbol}_{uuid.uuid4().hex[:8]}"

def create_regime_aware_cost_breakdown_id(symbol: str) -> str:
    return f"brk_{symbol}_{uuid.uuid4().hex[:8]}"

def create_regime_cost_review_id(prefix: str = "regime_cost_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
