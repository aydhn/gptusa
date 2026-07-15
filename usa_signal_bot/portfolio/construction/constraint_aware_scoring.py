from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    ConstraintAwareScore,
    ConstraintAwareScoreKind,
    PortfolioSandboxCandidate,
    PortfolioConstructionPolicy,
    create_constraint_aware_score_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag


def _create_score(symbol: str, score_kind: ConstraintAwareScoreKind, raw_score: float | None, source: str) -> ConstraintAwareScore:
    return ConstraintAwareScore(
        score_id=create_constraint_aware_score_id(),
        created_at_utc=_now_str(),
        symbol=symbol,
        score_kind=score_kind,
        raw_score=raw_score,
        normalized_score=None,
        penalty_applied=None,
        score_valid=True,
        research_data_only=True,
        allocation_sandbox_only=True,
        not_investment_advice=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={"source": source}
    )

def build_constraint_aware_scores(
    candidates: List[PortfolioSandboxCandidate],
    policy: PortfolioConstructionPolicy
) -> List[ConstraintAwareScore]:

    scores = []

    for cand in candidates:
        if not cand.eligible_for_sandbox:
            continue

        scores.append(_create_score(
            cand.symbol,
            ConstraintAwareScoreKind.SIZING_SCORE,
            cand.sizing_score,
            "candidate.sizing_score"
        ))

        scores.append(_create_score(
            cand.symbol,
            ConstraintAwareScoreKind.RISK_BUDGET_SCORE,
            cand.risk_budget_score,
            "candidate.risk_budget_score"
        ))

        scores.append(_create_score(
            cand.symbol,
            ConstraintAwareScoreKind.ROBUSTNESS_SCORE,
            cand.robustness_score,
            "candidate.robustness_score"
        ))

        composite = calculate_candidate_composite_score(cand, policy)
        scores.append(_create_score(
            cand.symbol,
            ConstraintAwareScoreKind.COMPOSITE_SCORE,
            composite,
            "policy_weighted_composite"
        ))

    return normalize_scores(scores)

def calculate_candidate_composite_score(candidate: PortfolioSandboxCandidate, policy: PortfolioConstructionPolicy) -> float | None:
    parts = []
    if candidate.sizing_score is not None and policy.sizing_weight > 0:
        parts.append(candidate.sizing_score * policy.sizing_weight)
    if candidate.risk_budget_score is not None and policy.risk_budget_weight > 0:
        parts.append(candidate.risk_budget_score * policy.risk_budget_weight)
    if candidate.robustness_score is not None and policy.robustness_weight > 0:
        parts.append(candidate.robustness_score * policy.robustness_weight)
    if candidate.liquidity_score is not None and policy.liquidity_weight > 0:
        parts.append(candidate.liquidity_score * policy.liquidity_weight)
    if candidate.cost_score is not None and policy.cost_weight > 0:
        parts.append(candidate.cost_score * policy.cost_weight)

    if not parts:
        return None

    return sum(parts)

def normalize_scores(scores: List[ConstraintAwareScore]) -> List[ConstraintAwareScore]:
    # Group by kind
    groups: Dict[ConstraintAwareScoreKind, List[ConstraintAwareScore]] = {}
    for s in scores:
        if s.score_kind not in groups:
            groups[s.score_kind] = []
        groups[s.score_kind].append(s)

    for kind, group_scores in groups.items():
        total = sum(s.raw_score for s in group_scores if s.raw_score is not None and s.raw_score > 0)

        for s in group_scores:
            if s.raw_score is None or s.raw_score <= 0 or total <= 0:
                s.normalized_score = 0.0
            else:
                s.normalized_score = s.raw_score / total

    return scores

def validate_constraint_aware_scores(items: List[ConstraintAwareScore]) -> List[str]:
    errors = []

    for item in items:
        if item.raw_score is not None and item.normalized_score is not None:
            if item.normalized_score < 0.0:
                errors.append(f"Score {item.score_id} has negative normalized score.")
                item.score_valid = False
                item.risk_flags.append(PortfolioConstructionRiskFlag.CONSTRAINT_SCORE_INVALID)

        if not item.research_data_only or not item.allocation_sandbox_only:
            errors.append(f"Score {item.score_id} is not marked as research/sandbox only.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.CONSTRAINT_SCORE_INVALID)

    return errors

def constraint_aware_scores_summary(items: List[ConstraintAwareScore]) -> Dict[str, Any]:
    kinds = list(set(s.score_kind.value for s in items))
    symbols = list(set(s.symbol for s in items))
    return {
        "count": len(items),
        "kinds": kinds,
        "symbol_count": len(symbols)
    }

def constraint_aware_scores_to_text(items: List[ConstraintAwareScore], limit: int = 300) -> str:
    summary = constraint_aware_scores_summary(items)
    return (
        f"Constraint Aware Scores: {summary['count']} total\n"
        f"Kinds: {', '.join(summary['kinds'])}\n"
        f"Symbols: {summary['symbol_count']}"
    )
