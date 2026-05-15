from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    StrategyFamily,
    StrategyRegimeCompatibility,
    StrategyGateDecision,
    StrategyConflictType,
    StrategyEnsembleDecision,
    AdaptiveWeightStatus,
    StrategyAdaptationRisk,
    StrategyAdaptationReportType
)
from usa_signal_bot.core.exceptions import StrategyAdaptationValidationError

@dataclass
class StrategyRegimeProfile:
    profile_id: str
    strategy_name: str
    strategy_family: StrategyFamily
    preferred_trend_regimes: List[str]
    preferred_volatility_regimes: List[str]
    preferred_momentum_regimes: List[str]
    preferred_liquidity_regimes: List[str]
    preferred_cross_sectional_regimes: List[str]
    avoided_regimes: List[str]
    blocked_regimes: List[str]
    base_weight: float
    min_required_confidence: float
    notes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyCompatibilityScore:
    score_id: str
    strategy_name: str
    created_at_utc: str
    compatibility: StrategyRegimeCompatibility
    score: Optional[float]
    matched_regimes: List[str]
    conflicted_regimes: List[str]
    evidence: Dict[str, Any]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyGateResult:
    gate_id: str
    strategy_name: str
    symbol: Optional[str]
    created_at_utc: str
    decision: StrategyGateDecision
    risk: StrategyAdaptationRisk
    compatibility_score: Optional[StrategyCompatibilityScore]
    confidence_multiplier: float
    rank_penalty: float
    suppress_reason: Optional[str]
    recommended_actions: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyConflictResult:
    conflict_id: str
    created_at_utc: str
    conflict_type: StrategyConflictType
    involved_strategies: List[str]
    severity: StrategyAdaptationRisk
    description: str
    recommended_resolution: str
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyEnsembleMember:
    member_id: str
    strategy_name: str
    strategy_family: StrategyFamily
    raw_score: Optional[float]
    adjusted_score: Optional[float]
    base_weight: float
    adaptive_weight: float
    weight_status: AdaptiveWeightStatus
    gate_result: Optional[StrategyGateResult]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyEnsembleResult:
    ensemble_id: str
    symbol: Optional[str]
    created_at_utc: str
    decision: StrategyEnsembleDecision
    consensus_score: Optional[float]
    long_score: Optional[float]
    short_score: Optional[float]
    neutral_score: Optional[float]
    members: List[StrategyEnsembleMember]
    conflicts: List[StrategyConflictResult]
    selected_strategy_names: List[str]
    suppressed_strategy_names: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyAdaptationReview:
    review_id: str
    created_at_utc: str
    report_type: StrategyAdaptationReportType
    symbol: Optional[str]
    profiles: List[StrategyRegimeProfile]
    compatibility_scores: List[StrategyCompatibilityScore]
    gate_results: List[StrategyGateResult]
    ensemble_result: Optional[StrategyEnsembleResult]
    conflicts: List[StrategyConflictResult]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def strategy_regime_profile_to_dict(item: StrategyRegimeProfile) -> Dict[str, Any]:
    return {
        "profile_id": item.profile_id,
        "strategy_name": item.strategy_name,
        "strategy_family": item.strategy_family.value,
        "preferred_trend_regimes": item.preferred_trend_regimes,
        "preferred_volatility_regimes": item.preferred_volatility_regimes,
        "preferred_momentum_regimes": item.preferred_momentum_regimes,
        "preferred_liquidity_regimes": item.preferred_liquidity_regimes,
        "preferred_cross_sectional_regimes": item.preferred_cross_sectional_regimes,
        "avoided_regimes": item.avoided_regimes,
        "blocked_regimes": item.blocked_regimes,
        "base_weight": item.base_weight,
        "min_required_confidence": item.min_required_confidence,
        "notes": item.notes,
        "metadata": item.metadata,
    }

def strategy_compatibility_score_to_dict(item: StrategyCompatibilityScore) -> Dict[str, Any]:
    return {
        "score_id": item.score_id,
        "strategy_name": item.strategy_name,
        "created_at_utc": item.created_at_utc,
        "compatibility": item.compatibility.value,
        "score": item.score,
        "matched_regimes": item.matched_regimes,
        "conflicted_regimes": item.conflicted_regimes,
        "evidence": item.evidence,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def strategy_gate_result_to_dict(item: StrategyGateResult) -> Dict[str, Any]:
    return {
        "gate_id": item.gate_id,
        "strategy_name": item.strategy_name,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "decision": item.decision.value,
        "risk": item.risk.value,
        "compatibility_score": strategy_compatibility_score_to_dict(item.compatibility_score) if item.compatibility_score else None,
        "confidence_multiplier": item.confidence_multiplier,
        "rank_penalty": item.rank_penalty,
        "suppress_reason": item.suppress_reason,
        "recommended_actions": item.recommended_actions,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def strategy_conflict_result_to_dict(item: StrategyConflictResult) -> Dict[str, Any]:
    return {
        "conflict_id": item.conflict_id,
        "created_at_utc": item.created_at_utc,
        "conflict_type": item.conflict_type.value,
        "involved_strategies": item.involved_strategies,
        "severity": item.severity.value,
        "description": item.description,
        "recommended_resolution": item.recommended_resolution,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def strategy_ensemble_member_to_dict(item: StrategyEnsembleMember) -> Dict[str, Any]:
    return {
        "member_id": item.member_id,
        "strategy_name": item.strategy_name,
        "strategy_family": item.strategy_family.value,
        "raw_score": item.raw_score,
        "adjusted_score": item.adjusted_score,
        "base_weight": item.base_weight,
        "adaptive_weight": item.adaptive_weight,
        "weight_status": item.weight_status.value,
        "gate_result": strategy_gate_result_to_dict(item.gate_result) if item.gate_result else None,
        "metadata": item.metadata,
    }

def strategy_ensemble_result_to_dict(item: StrategyEnsembleResult) -> Dict[str, Any]:
    return {
        "ensemble_id": item.ensemble_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "decision": item.decision.value,
        "consensus_score": item.consensus_score,
        "long_score": item.long_score,
        "short_score": item.short_score,
        "neutral_score": item.neutral_score,
        "members": [strategy_ensemble_member_to_dict(m) for m in item.members],
        "conflicts": [strategy_conflict_result_to_dict(c) for c in item.conflicts],
        "selected_strategy_names": item.selected_strategy_names,
        "suppressed_strategy_names": item.suppressed_strategy_names,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def strategy_adaptation_review_to_dict(item: StrategyAdaptationReview) -> Dict[str, Any]:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "symbol": item.symbol,
        "profiles": [strategy_regime_profile_to_dict(p) for p in item.profiles],
        "compatibility_scores": [strategy_compatibility_score_to_dict(s) for s in item.compatibility_scores],
        "gate_results": [strategy_gate_result_to_dict(g) for g in item.gate_results],
        "ensemble_result": strategy_ensemble_result_to_dict(item.ensemble_result) if item.ensemble_result else None,
        "conflicts": [strategy_conflict_result_to_dict(c) for c in item.conflicts],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_strategy_regime_profile(item: StrategyRegimeProfile) -> None:
    if not item.strategy_name:
        raise StrategyAdaptationValidationError("strategy_name cannot be empty")
    if item.base_weight < 0:
        raise StrategyAdaptationValidationError("base_weight cannot be negative")
    if not (0 <= item.min_required_confidence <= 100):
        raise StrategyAdaptationValidationError("min_required_confidence must be between 0 and 100")

def validate_strategy_compatibility_score(item: StrategyCompatibilityScore) -> None:
    if not item.strategy_name:
        raise StrategyAdaptationValidationError("strategy_name cannot be empty")
    if item.score is not None and not (0 <= item.score <= 100):
        raise StrategyAdaptationValidationError("score must be between 0 and 100 or None")

def validate_strategy_gate_result(item: StrategyGateResult) -> None:
    if not item.strategy_name:
        raise StrategyAdaptationValidationError("strategy_name cannot be empty")
    if item.confidence_multiplier < 0:
        raise StrategyAdaptationValidationError("confidence_multiplier cannot be negative")
    if item.rank_penalty < 0:
        raise StrategyAdaptationValidationError("rank_penalty cannot be negative")

def validate_strategy_ensemble_result(item: StrategyEnsembleResult) -> None:
    for m in item.members:
        if m.base_weight < 0:
            raise StrategyAdaptationValidationError("base_weight cannot be negative")
        if m.adaptive_weight < 0:
            raise StrategyAdaptationValidationError("adaptive_weight cannot be negative")

def create_strategy_regime_profile_id(strategy_name: str) -> str:
    return f"prof_{strategy_name}_{uuid.uuid4().hex[:8]}"

def create_strategy_compatibility_score_id(strategy_name: str) -> str:
    return f"comp_{strategy_name}_{uuid.uuid4().hex[:8]}"

def create_strategy_gate_result_id(strategy_name: str, symbol: Optional[str] = None) -> str:
    sym = symbol or "BASKET"
    return f"gate_{strategy_name}_{sym}_{uuid.uuid4().hex[:8]}"

def create_strategy_conflict_result_id(prefix: str = "strategy_conflict") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_strategy_ensemble_member_id(strategy_name: str) -> str:
    return f"ens_mem_{strategy_name}_{uuid.uuid4().hex[:8]}"

def create_strategy_ensemble_result_id(symbol: Optional[str] = None) -> str:
    sym = symbol or "BASKET"
    return f"ens_res_{sym}_{uuid.uuid4().hex[:8]}"

def create_strategy_adaptation_review_id(prefix: str = "strategy_adaptation_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
