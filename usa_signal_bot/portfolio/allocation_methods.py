from dataclasses import dataclass
from typing import List, Dict, Optional
from usa_signal_bot.portfolio.portfolio_models import (
    AllocationRequest,
    AllocationResult,
    PortfolioCandidate,
    AllocationMethod,
    AllocationStatus
)
from usa_signal_bot.core.enums import PortfolioCandidateStatus
from usa_signal_bot.portfolio.portfolio_candidates import sort_candidates_for_allocation, infer_candidate_price

@dataclass
class AllocationConfig:
    method: AllocationMethod
    max_total_allocation_pct: float
    max_candidate_weight: float
    min_candidate_weight: float
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    cash_buffer_pct: float
    allow_fractional_quantity: bool
    normalize_weights: bool

def default_allocation_config() -> AllocationConfig:
    return AllocationConfig(
        method=AllocationMethod.NOTIONAL_FROM_RISK_DECISION,
        max_total_allocation_pct=0.80,
        max_candidate_weight=0.10,
        min_candidate_weight=0.0,
        max_symbol_weight=0.15,
        max_strategy_weight=0.30,
        max_timeframe_weight=0.50,
        cash_buffer_pct=0.05,
        allow_fractional_quantity=True,
        normalize_weights=True
    )

def validate_allocation_config(config: AllocationConfig) -> None:
    from usa_signal_bot.core.exceptions import AllocationMethodError
    if not (0 <= config.max_total_allocation_pct <= 1):
        raise AllocationMethodError("max_total_allocation_pct must be between 0 and 1.")
    if not (0 <= config.max_candidate_weight <= 1):
        raise AllocationMethodError("max_candidate_weight must be between 0 and 1.")
    if not (0 <= config.min_candidate_weight <= 1):
        raise AllocationMethodError("min_candidate_weight must be between 0 and 1.")
    if not (0 <= config.cash_buffer_pct <= 1):
        raise AllocationMethodError("cash_buffer_pct must be between 0 and 1.")
    if config.min_candidate_weight > config.max_candidate_weight:
        raise AllocationMethodError("min_candidate_weight cannot be greater than max_candidate_weight.")

def normalize_allocation_weights(raw_weights: Dict[str, float], max_total_weight: float) -> Dict[str, float]:
    total_raw = sum(raw_weights.values())
    if total_raw <= 0:
        return {k: 0.0 for k in raw_weights.keys()}

    scale_factor = min(1.0, max_total_weight / total_raw)
    normalized = {}
    for k, v in raw_weights.items():
        normalized[k] = (v / total_raw) * scale_factor * total_raw # equals v * scale_factor
    return normalized

def convert_weight_to_notional(weight: float, portfolio_equity: float) -> float:
    return weight * portfolio_equity

def convert_notional_to_quantity(notional: float, price: Optional[float], allow_fractional: bool = True) -> float:
    if not price or price <= 0:
        return 0.0
    qty = notional / price
    if not allow_fractional:
        qty = float(int(qty))
    return qty

def apply_allocation_caps(results: List[AllocationResult], config: AllocationConfig) -> List[AllocationResult]:
    for result in results:
        if result.status in [AllocationStatus.REJECTED, AllocationStatus.ZERO]:
            continue

        if result.target_weight > config.max_candidate_weight:
            result.target_weight = config.max_candidate_weight
            result.status = AllocationStatus.CAPPED
            result.capped = True
            if f"Capped at max_candidate_weight {config.max_candidate_weight}" not in result.cap_reasons:
                result.cap_reasons.append(f"Capped at max_candidate_weight {config.max_candidate_weight}")
        elif result.target_weight < config.min_candidate_weight and result.target_weight > 0:
            result.target_weight = 0.0
            result.status = AllocationStatus.REJECTED
            result.capped = True
            if f"Rejected: below min_candidate_weight {config.min_candidate_weight}" not in result.cap_reasons:
                result.cap_reasons.append(f"Rejected: below min_candidate_weight {config.min_candidate_weight}")
    return results

def _base_allocate(request: AllocationRequest, raw_weights: Dict[str, float], config: Optional[AllocationConfig] = None) -> List[AllocationResult]:
    cfg = config or default_allocation_config()

    weights = raw_weights
    if cfg.normalize_weights:
        weights = normalize_allocation_weights(raw_weights, request.max_total_allocation_pct)

    results = []
    for candidate in request.candidates:
        if candidate.status != PortfolioCandidateStatus.ELIGIBLE:
            results.append(AllocationResult(
                candidate_id=candidate.candidate_id,
                symbol=candidate.symbol,
                timeframe=candidate.timeframe,
                method=request.method,
                status=AllocationStatus.REJECTED,
                target_weight=0.0,
                target_notional=0.0,
                target_quantity=0.0,
                raw_weight=raw_weights.get(candidate.candidate_id, 0.0),
                raw_notional=convert_weight_to_notional(raw_weights.get(candidate.candidate_id, 0.0), request.portfolio_equity),
                capped=False,
                cap_reasons=[],
                warnings=[],
                errors=["Candidate is not eligible."],
                strategy_name=candidate.strategy_name
            ))
            continue

        price = infer_candidate_price(candidate)
        if not price or price <= 0:
            results.append(AllocationResult(
                candidate_id=candidate.candidate_id,
                symbol=candidate.symbol,
                timeframe=candidate.timeframe,
                method=request.method,
                status=AllocationStatus.REJECTED,
                target_weight=0.0,
                target_notional=0.0,
                target_quantity=0.0,
                raw_weight=raw_weights.get(candidate.candidate_id, 0.0),
                raw_notional=convert_weight_to_notional(raw_weights.get(candidate.candidate_id, 0.0), request.portfolio_equity),
                capped=False,
                cap_reasons=[],
                warnings=["Missing or invalid price. Cannot allocate."],
                errors=[],
                strategy_name=candidate.strategy_name
            ))
            continue

        weight = weights.get(candidate.candidate_id, 0.0)
        notional = convert_weight_to_notional(weight, request.portfolio_equity)
        qty = convert_notional_to_quantity(notional, price, cfg.allow_fractional_quantity)

        status = AllocationStatus.ALLOCATED if weight > 0 else AllocationStatus.ZERO

        results.append(AllocationResult(
            candidate_id=candidate.candidate_id,
            symbol=candidate.symbol,
            timeframe=candidate.timeframe,
            method=request.method,
            status=status,
            target_weight=weight,
            target_notional=notional,
            target_quantity=qty,
            raw_weight=raw_weights.get(candidate.candidate_id, 0.0),
            raw_notional=convert_weight_to_notional(raw_weights.get(candidate.candidate_id, 0.0), request.portfolio_equity),
            capped=False,
            cap_reasons=[],
            warnings=[],
            errors=[],
            strategy_name=candidate.strategy_name
        ))

    return apply_allocation_caps(results, cfg)

def allocate_equal_weight(request: AllocationRequest, config: Optional[AllocationConfig] = None) -> List[AllocationResult]:
    eligible = [c for c in request.candidates if c.status == PortfolioCandidateStatus.ELIGIBLE]
    raw_weights = {}
    if eligible:
        weight_per_candidate = request.max_total_allocation_pct / len(eligible)
        for c in eligible:
            raw_weights[c.candidate_id] = weight_per_candidate
    return _base_allocate(request, raw_weights, config)

def allocate_rank_weighted(request: AllocationRequest, config: Optional[AllocationConfig] = None) -> List[AllocationResult]:
    eligible = [c for c in request.candidates if c.status == PortfolioCandidateStatus.ELIGIBLE]
    raw_weights = {}
    if eligible:
        total_rank = sum(c.rank_score if c.rank_score is not None else 1.0 for c in eligible)
        if total_rank > 0:
            for c in eligible:
                rank = c.rank_score if c.rank_score is not None else 1.0
                raw_weights[c.candidate_id] = (rank / total_rank) * request.max_total_allocation_pct
        else:
            weight_per = request.max_total_allocation_pct / len(eligible)
            for c in eligible:
                raw_weights[c.candidate_id] = weight_per
    return _base_allocate(request, raw_weights, config)

def allocate_risk_score_weighted(request: AllocationRequest, config: Optional[AllocationConfig] = None) -> List[AllocationResult]:
    eligible = [c for c in request.candidates if c.status == PortfolioCandidateStatus.ELIGIBLE]
    raw_weights = {}
    if eligible:
        inverse_risks = []
        for c in eligible:
            risk = c.risk_score if c.risk_score is not None else 50.0
            inverse_risks.append(max(0.1, 100.0 - risk))

        total_inverse_risk = sum(inverse_risks)
        if total_inverse_risk > 0:
            for c, inv_risk in zip(eligible, inverse_risks):
                raw_weights[c.candidate_id] = (inv_risk / total_inverse_risk) * request.max_total_allocation_pct
        else:
             weight_per = request.max_total_allocation_pct / len(eligible)
             for c in eligible:
                 raw_weights[c.candidate_id] = weight_per
    return _base_allocate(request, raw_weights, config)

def allocate_volatility_adjusted(request: AllocationRequest, config: Optional[AllocationConfig] = None) -> List[AllocationResult]:
    eligible = [c for c in request.candidates if c.status == PortfolioCandidateStatus.ELIGIBLE]
    raw_weights = {}
    if eligible:
        inverse_vols = []
        for c in eligible:
            vol = c.volatility_value if c.volatility_value is not None and c.volatility_value > 0 else 1.0
            inverse_vols.append(1.0 / vol)

        total_inverse_vol = sum(inverse_vols)
        if total_inverse_vol > 0:
            for c, inv_vol in zip(eligible, inverse_vols):
                raw_weights[c.candidate_id] = (inv_vol / total_inverse_vol) * request.max_total_allocation_pct
        else:
             weight_per = request.max_total_allocation_pct / len(eligible)
             for c in eligible:
                 raw_weights[c.candidate_id] = weight_per
    return _base_allocate(request, raw_weights, config)

def allocate_from_risk_decision_notional(request: AllocationRequest, config: Optional[AllocationConfig] = None) -> List[AllocationResult]:
    raw_weights = {}
    for c in request.candidates:
        if c.status == PortfolioCandidateStatus.ELIGIBLE:
            weight = c.approved_notional / request.portfolio_equity if request.portfolio_equity > 0 else 0.0
            raw_weights[c.candidate_id] = weight
    return _base_allocate(request, raw_weights, config)

def allocate_hybrid_baseline(request: AllocationRequest, config: Optional[AllocationConfig] = None) -> List[AllocationResult]:
    eligible = [c for c in request.candidates if c.status == PortfolioCandidateStatus.ELIGIBLE]
    raw_weights = {}
    if eligible:
        scores = []
        for c in eligible:
            rank = c.rank_score if c.rank_score is not None else 50.0
            risk = c.risk_score if c.risk_score is not None else 50.0
            conf = c.confidence if c.confidence is not None else 0.5
            vol = c.volatility_value if c.volatility_value is not None and c.volatility_value > 0 else 1.0

            score = (rank * conf) / (risk * vol)
            scores.append(score)

        total_score = sum(scores)
        if total_score > 0:
            for c, score in zip(eligible, scores):
                raw_weights[c.candidate_id] = (score / total_score) * request.max_total_allocation_pct
        else:
             weight_per = request.max_total_allocation_pct / len(eligible)
             for c in eligible:
                 raw_weights[c.candidate_id] = weight_per
    return _base_allocate(request, raw_weights, config)

def zero_allocation(request: AllocationRequest, reason: str) -> List[AllocationResult]:
    results = []
    for c in request.candidates:
        results.append(AllocationResult(
            candidate_id=c.candidate_id,
            symbol=c.symbol,
            timeframe=c.timeframe,
            method=request.method,
            status=AllocationStatus.ZERO,
            target_weight=0.0,
            target_notional=0.0,
            target_quantity=0.0,
            raw_weight=0.0,
            raw_notional=0.0,
            capped=False,
            cap_reasons=[],
            warnings=[],
            errors=[reason],
            strategy_name=c.strategy_name
        ))
    return results

def allocate_candidates(request: AllocationRequest, config: Optional[AllocationConfig] = None) -> List[AllocationResult]:
    if request.method == AllocationMethod.EQUAL_WEIGHT:
        return allocate_equal_weight(request, config)
    elif request.method == AllocationMethod.RANK_WEIGHTED:
        return allocate_rank_weighted(request, config)
    elif request.method == AllocationMethod.RISK_SCORE_WEIGHTED:
        return allocate_risk_score_weighted(request, config)
    elif request.method == AllocationMethod.VOLATILITY_ADJUSTED:
        return allocate_volatility_adjusted(request, config)
    elif request.method == AllocationMethod.NOTIONAL_FROM_RISK_DECISION:
        return allocate_from_risk_decision_notional(request, config)
    elif request.method == AllocationMethod.HYBRID_BASELINE:
        return allocate_hybrid_baseline(request, config)
    elif request.method == AllocationMethod.ZERO_ALLOCATION:
        return zero_allocation(request, "Zero allocation method requested.")
    else:
        return zero_allocation(request, f"Unknown allocation method: {request.method}")
