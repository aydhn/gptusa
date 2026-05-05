from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.enums import SignalAction, RiskCheckStatus, RiskSeverity, RiskRejectionReason
from usa_signal_bot.risk.risk_models import PositionSizingRequest, RiskCheckResult
from usa_signal_bot.risk.exposure_guard import ExposureSnapshot

@dataclass
class CandidateRiskInput:
    candidate_id: str
    signal_id: str | None
    symbol: str
    timeframe: str
    strategy_name: str | None
    action: SignalAction
    confidence: float
    rank_score: float | None
    price: float | None
    feature_snapshot: dict[str, Any]
    risk_flags: list[Any]
    metadata: dict[str, Any] = field(default_factory=dict)

def candidate_risk_input_from_signal(signal: Any, candidate_id: str | None = None) -> CandidateRiskInput:
    cid = candidate_id or f"cand_{signal.signal_id}"
    return CandidateRiskInput(
        candidate_id=cid,
        signal_id=signal.signal_id,
        symbol=signal.symbol,
        timeframe=signal.timeframe,
        strategy_name=signal.strategy_name,
        action=signal.action,
        confidence=signal.confidence,
        rank_score=None,
        price=infer_price_from_feature_snapshot(signal.feature_snapshot),
        feature_snapshot=signal.feature_snapshot,
        risk_flags=signal.risk_flags,
        metadata={"source": "StrategySignal"}
    )

def candidate_risk_input_from_selected_candidate(candidate: Any) -> CandidateRiskInput:
    return CandidateRiskInput(
        candidate_id=candidate.candidate_id,
        signal_id=candidate.signal_id,
        symbol=candidate.symbol,
        timeframe=candidate.timeframe,
        strategy_name=candidate.strategy_name,
        action=candidate.action,
        confidence=candidate.confidence,
        rank_score=candidate.rank_score,
        price=infer_price_from_feature_snapshot(candidate.feature_snapshot),
        feature_snapshot=candidate.feature_snapshot,
        risk_flags=candidate.risk_flags,
        metadata={"source": "SelectedCandidate"}
    )

def infer_price_from_feature_snapshot(snapshot: dict[str, Any]) -> float | None:
    if not snapshot:
        return None
    for key in ["close", "adjusted_close", "last_price", "price"]:
        if key in snapshot and snapshot[key] is not None:
            try:
                return float(snapshot[key])
            except (ValueError, TypeError):
                pass
    return None

def infer_volatility_from_feature_snapshot(snapshot: dict[str, Any]) -> float | None:
    if not snapshot:
        return None
    for key in ["rolling_volatility", "volatility", "historical_volatility", "normalized_atr"]:
        if key in snapshot and snapshot[key] is not None:
            try:
                return float(snapshot[key])
            except (ValueError, TypeError):
                pass
    return None

def infer_atr_from_feature_snapshot(snapshot: dict[str, Any]) -> float | None:
    if not snapshot:
        return None
    for key in ["atr", "normalized_atr", "average_true_range"]:
        if key in snapshot and snapshot[key] is not None:
            try:
                return float(snapshot[key])
            except (ValueError, TypeError):
                pass
    return None

def build_position_sizing_request(candidate: CandidateRiskInput, snapshot: ExposureSnapshot, default_price: float | None = None) -> PositionSizingRequest:
    price = candidate.price if candidate.price is not None else default_price
    if price is None or price <= 0:
        price = 0.0

    return PositionSizingRequest(
        candidate_id=candidate.candidate_id,
        symbol=candidate.symbol,
        strategy_name=candidate.strategy_name,
        timeframe=candidate.timeframe,
        action=candidate.action,
        confidence=candidate.confidence,
        rank_score=candidate.rank_score,
        price=price,
        portfolio_equity=snapshot.portfolio_equity,
        available_cash=snapshot.available_cash,
        volatility_value=infer_volatility_from_feature_snapshot(candidate.feature_snapshot),
        atr_value=infer_atr_from_feature_snapshot(candidate.feature_snapshot)
    )

def validate_candidate_risk_input(candidate: CandidateRiskInput) -> list[RiskCheckResult]:
    checks = []
    if candidate.price is None or candidate.price <= 0:
        checks.append(RiskCheckResult(
            check_name="missing_price",
            status=RiskCheckStatus.FAILED,
            severity=RiskSeverity.CRITICAL,
            message="Price is missing or invalid",
            rejection_reason=RiskRejectionReason.MISSING_PRICE
        ))
    if candidate.action == SignalAction.SHORT:
        checks.append(RiskCheckResult(
            check_name="short_action_default_check",
            status=RiskCheckStatus.WARNING,
            severity=RiskSeverity.HIGH,
            message="Candidate is SHORT action, requires explicit short approval",
            rejection_reason=RiskRejectionReason.SHORT_NOT_ALLOWED
        ))
    return checks

def candidate_risk_input_to_dict(candidate: CandidateRiskInput) -> dict[str, Any]:
    return {
        "candidate_id": candidate.candidate_id,
        "signal_id": candidate.signal_id,
        "symbol": candidate.symbol,
        "timeframe": candidate.timeframe,
        "strategy_name": candidate.strategy_name,
        "action": candidate.action.value,
        "confidence": candidate.confidence,
        "rank_score": candidate.rank_score,
        "price": candidate.price,
        "feature_snapshot": candidate.feature_snapshot,
        "risk_flags": [str(f) for f in candidate.risk_flags],
        "metadata": candidate.metadata
    }
