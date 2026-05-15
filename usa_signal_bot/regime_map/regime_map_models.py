import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from usa_signal_bot.core.enums import (
    RegimeTimeframe,
    RegimeConfirmationStatus,
    TrendRegime,
    VolatilityMapRegime,
    MomentumRegime,
    LiquidityMapRegime,
    BreadthRegime,
    CrossSectionalRegime,
    RegimeAlignmentStatus,
    RegimeTransitionType,
    RegimeTransitionRisk,
    RegimeMapGuardStatus,
    RegimeMapReportType
)


@dataclass
class TimeframeRegimeSnapshot:
    snapshot_id: str
    symbol: str
    timeframe: RegimeTimeframe
    created_at_utc: str
    trend_regime: TrendRegime
    volatility_regime: VolatilityMapRegime
    momentum_regime: MomentumRegime
    liquidity_regime: LiquidityMapRegime
    confidence: Optional[float]
    evidence: dict[str, Any]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MultiTimeframeRegimeConfirmation:
    confirmation_id: str
    symbol: str
    created_at_utc: str
    snapshots: list[TimeframeRegimeSnapshot]
    status: RegimeConfirmationStatus
    dominant_trend_regime: TrendRegime
    dominant_volatility_regime: VolatilityMapRegime
    dominant_momentum_regime: MomentumRegime
    dominant_liquidity_regime: LiquidityMapRegime
    confidence: Optional[float]
    conflicts: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CrossSectionalRegimeMap:
    map_id: str
    universe_name: str
    created_at_utc: str
    symbol_count: int
    cross_sectional_regime: CrossSectionalRegime
    breadth_regime: BreadthRegime
    uptrend_count: int
    downtrend_count: int
    range_count: int
    high_vol_count: int
    thin_liquidity_count: int
    momentum_positive_count: int
    momentum_negative_count: int
    dispersion_score: Optional[float]
    breadth_score: Optional[float]
    symbol_snapshots: list[MultiTimeframeRegimeConfirmation]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SymbolRegimeAlignment:
    alignment_id: str
    symbol: str
    universe_name: str
    created_at_utc: str
    status: RegimeAlignmentStatus
    symbol_confirmation: Optional[MultiTimeframeRegimeConfirmation]
    universe_regime_map: Optional[CrossSectionalRegimeMap]
    alignment_score: Optional[float]
    conflict_reasons: list[str]
    recommended_guards: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RegimeTransitionSignal:
    transition_id: str
    symbol: Optional[str]
    universe_name: Optional[str]
    created_at_utc: str
    transition_type: RegimeTransitionType
    risk: RegimeTransitionRisk
    score: Optional[float]
    evidence: dict[str, Any]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RegimeMapReview:
    review_id: str
    created_at_utc: str
    report_type: RegimeMapReportType
    universe_name: str
    timeframe_confirmations: list[MultiTimeframeRegimeConfirmation]
    cross_sectional_map: Optional[CrossSectionalRegimeMap]
    alignments: list[SymbolRegimeAlignment]
    transition_signals: list[RegimeTransitionSignal]
    guard_status: RegimeMapGuardStatus
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]


def timeframe_regime_snapshot_to_dict(item: TimeframeRegimeSnapshot) -> dict:
    return {
        "snapshot_id": item.snapshot_id,
        "symbol": item.symbol,
        "timeframe": item.timeframe.value,
        "created_at_utc": item.created_at_utc,
        "trend_regime": item.trend_regime.value,
        "volatility_regime": item.volatility_regime.value,
        "momentum_regime": item.momentum_regime.value,
        "liquidity_regime": item.liquidity_regime.value,
        "confidence": item.confidence,
        "evidence": item.evidence,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def multi_timeframe_regime_confirmation_to_dict(item: MultiTimeframeRegimeConfirmation) -> dict:
    return {
        "confirmation_id": item.confirmation_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "snapshots": [timeframe_regime_snapshot_to_dict(s) for s in item.snapshots],
        "status": item.status.value,
        "dominant_trend_regime": item.dominant_trend_regime.value,
        "dominant_volatility_regime": item.dominant_volatility_regime.value,
        "dominant_momentum_regime": item.dominant_momentum_regime.value,
        "dominant_liquidity_regime": item.dominant_liquidity_regime.value,
        "confidence": item.confidence,
        "conflicts": item.conflicts,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def cross_sectional_regime_map_to_dict(item: CrossSectionalRegimeMap) -> dict:
    return {
        "map_id": item.map_id,
        "universe_name": item.universe_name,
        "created_at_utc": item.created_at_utc,
        "symbol_count": item.symbol_count,
        "cross_sectional_regime": item.cross_sectional_regime.value,
        "breadth_regime": item.breadth_regime.value,
        "uptrend_count": item.uptrend_count,
        "downtrend_count": item.downtrend_count,
        "range_count": item.range_count,
        "high_vol_count": item.high_vol_count,
        "thin_liquidity_count": item.thin_liquidity_count,
        "momentum_positive_count": item.momentum_positive_count,
        "momentum_negative_count": item.momentum_negative_count,
        "dispersion_score": item.dispersion_score,
        "breadth_score": item.breadth_score,
        "symbol_snapshots": [multi_timeframe_regime_confirmation_to_dict(s) for s in item.symbol_snapshots],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def symbol_regime_alignment_to_dict(item: SymbolRegimeAlignment) -> dict:
    return {
        "alignment_id": item.alignment_id,
        "symbol": item.symbol,
        "universe_name": item.universe_name,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "symbol_confirmation": multi_timeframe_regime_confirmation_to_dict(item.symbol_confirmation) if item.symbol_confirmation else None,
        "universe_regime_map": cross_sectional_regime_map_to_dict(item.universe_regime_map) if item.universe_regime_map else None,
        "alignment_score": item.alignment_score,
        "conflict_reasons": item.conflict_reasons,
        "recommended_guards": item.recommended_guards,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def regime_transition_signal_to_dict(item: RegimeTransitionSignal) -> dict:
    return {
        "transition_id": item.transition_id,
        "symbol": item.symbol,
        "universe_name": item.universe_name,
        "created_at_utc": item.created_at_utc,
        "transition_type": item.transition_type.value,
        "risk": item.risk.value,
        "score": item.score,
        "evidence": item.evidence,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def regime_map_review_to_dict(item: RegimeMapReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "universe_name": item.universe_name,
        "timeframe_confirmations": [multi_timeframe_regime_confirmation_to_dict(c) for c in item.timeframe_confirmations],
        "cross_sectional_map": cross_sectional_regime_map_to_dict(item.cross_sectional_map) if item.cross_sectional_map else None,
        "alignments": [symbol_regime_alignment_to_dict(a) for a in item.alignments],
        "transition_signals": [regime_transition_signal_to_dict(t) for t in item.transition_signals],
        "guard_status": item.guard_status.value,
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def _validate_score(score: Optional[float], field_name: str) -> None:
    if score is not None:
        if not ((0.0 <= score <= 1.0) or (0.0 <= score <= 100.0)):
            raise ValueError(f"{field_name} must be between 0-1 or 0-100")

def validate_timeframe_regime_snapshot(item: TimeframeRegimeSnapshot) -> None:
    if not item.symbol:
        raise ValueError("Symbol cannot be empty")
    _validate_score(item.confidence, "confidence")

def validate_multi_timeframe_regime_confirmation(item: MultiTimeframeRegimeConfirmation) -> None:
    if not item.symbol:
        raise ValueError("Symbol cannot be empty")
    _validate_score(item.confidence, "confidence")

def validate_cross_sectional_regime_map(item: CrossSectionalRegimeMap) -> None:
    if not item.universe_name:
        raise ValueError("Universe name cannot be empty")
    if item.symbol_count < 0:
        raise ValueError("Symbol count cannot be negative")
    for count_attr in ["uptrend_count", "downtrend_count", "range_count", "high_vol_count", "thin_liquidity_count", "momentum_positive_count", "momentum_negative_count"]:
        if getattr(item, count_attr) < 0:
            raise ValueError(f"{count_attr} cannot be negative")
    _validate_score(item.dispersion_score, "dispersion_score")
    _validate_score(item.breadth_score, "breadth_score")

def validate_symbol_regime_alignment(item: SymbolRegimeAlignment) -> None:
    if not item.symbol:
        raise ValueError("Symbol cannot be empty")
    _validate_score(item.alignment_score, "alignment_score")

def validate_regime_transition_signal(item: RegimeTransitionSignal) -> None:
    if not item.symbol and not item.universe_name:
        raise ValueError("Transition signal must have either symbol or universe_name")
    _validate_score(item.score, "score")

def create_timeframe_regime_snapshot_id(symbol: str, timeframe: RegimeTimeframe) -> str:
    return f"trsnap_{symbol}_{timeframe.value}_{uuid.uuid4().hex[:8]}"

def create_multi_timeframe_confirmation_id(symbol: str) -> str:
    return f"mtconf_{symbol}_{uuid.uuid4().hex[:8]}"

def create_cross_sectional_regime_map_id(universe_name: str) -> str:
    return f"xsrmap_{universe_name}_{uuid.uuid4().hex[:8]}"

def create_symbol_regime_alignment_id(symbol: str) -> str:
    return f"sralign_{symbol}_{uuid.uuid4().hex[:8]}"

def create_regime_transition_signal_id(symbol: Optional[str] = None) -> str:
    prefix = f"rtrans_{symbol}" if symbol else "rtrans_univ"
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_regime_map_review_id(prefix: str = "regime_map_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
