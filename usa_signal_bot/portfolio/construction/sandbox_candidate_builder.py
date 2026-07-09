import pandas as pd
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioSandboxCandidate,
    create_portfolio_sandbox_candidate_id,
    _now_str,
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag


def build_portfolio_sandbox_candidates(
    sizing_matrix_payload: Dict[str, Any], candidate_df: Optional[pd.DataFrame] = None
) -> List[PortfolioSandboxCandidate]:

    candidates = infer_candidates_from_sizing_matrix(sizing_matrix_payload)
    if candidate_df is not None and not candidate_df.empty:
        candidates = merge_candidate_overrides(candidates, candidate_df)

    return candidates


def infer_candidates_from_sizing_matrix(
    sizing_matrix_payload: Dict[str, Any],
) -> List[PortfolioSandboxCandidate]:
    candidates = []
    matrix = sizing_matrix_payload.get("matrix", {})
    if not isinstance(matrix, dict):
        return candidates

    for symbol, data in matrix.items():
        if not isinstance(data, dict):
            continue

        candidates.append(
            PortfolioSandboxCandidate(
                candidate_id=create_portfolio_sandbox_candidate_id(),
                created_at_utc=_now_str(),
                symbol=str(symbol).upper(),
                candidate_valid=True,
                eligible_for_sandbox=data.get("eligible", True),
                sizing_score=data.get("sizing_score"),
                risk_budget_score=data.get("risk_budget_score"),
                robustness_score=data.get("robustness_score"),
                liquidity_score=data.get("liquidity_score"),
                cost_score=data.get("cost_score"),
                diversification_group=data.get("diversification_group"),
                sandbox_notes=[],
                live_signal=False,
                order_decision=False,
                actual_target_weight=None,
                actual_portfolio_weight=None,
                actual_allocation=None,
                actual_position_size=None,
                order_size=None,
                capital_allocation=None,
                research_data_only=True,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={"inferred_from": "sizing_matrix"},
            )
        )
    return candidates


def merge_candidate_overrides(
    candidates: List[PortfolioSandboxCandidate], candidate_df: pd.DataFrame
) -> List[PortfolioSandboxCandidate]:

    cand_map = {c.symbol: c for c in candidates}

    if "symbol" not in candidate_df.columns:
        return list(cand_map.values())

    for row in candidate_df.itertuples(index=False):
        symbol = str(getattr(row, "symbol")).upper()
        if symbol not in cand_map:
            cand_map[symbol] = PortfolioSandboxCandidate(
                candidate_id=create_portfolio_sandbox_candidate_id(),
                created_at_utc=_now_str(),
                symbol=symbol,
                candidate_valid=True,
                eligible_for_sandbox=True,
                sizing_score=None,
                risk_budget_score=None,
                robustness_score=None,
                liquidity_score=None,
                cost_score=None,
                diversification_group=None,
                sandbox_notes=["Added via overrides"],
                live_signal=False,
                order_decision=False,
                actual_target_weight=None,
                actual_portfolio_weight=None,
                actual_allocation=None,
                actual_position_size=None,
                order_size=None,
                capital_allocation=None,
                research_data_only=True,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={"inferred_from": "dataframe_override"},
            )

        cand = cand_map[symbol]

        if hasattr(row, "eligible_for_sandbox") and not pd.isna(
            getattr(row, "eligible_for_sandbox")
        ):
            cand.eligible_for_sandbox = bool(getattr(row, "eligible_for_sandbox"))
        if hasattr(row, "sizing_score") and not pd.isna(getattr(row, "sizing_score")):
            cand.sizing_score = float(getattr(row, "sizing_score"))
        if hasattr(row, "risk_budget_score") and not pd.isna(
            getattr(row, "risk_budget_score")
        ):
            cand.risk_budget_score = float(getattr(row, "risk_budget_score"))
        if hasattr(row, "robustness_score") and not pd.isna(
            getattr(row, "robustness_score")
        ):
            cand.robustness_score = float(getattr(row, "robustness_score"))
        if hasattr(row, "liquidity_score") and not pd.isna(
            getattr(row, "liquidity_score")
        ):
            cand.liquidity_score = float(getattr(row, "liquidity_score"))
        if hasattr(row, "cost_score") and not pd.isna(getattr(row, "cost_score")):
            cand.cost_score = float(getattr(row, "cost_score"))
        if hasattr(row, "diversification_group") and not pd.isna(
            getattr(row, "diversification_group")
        ):
            cand.diversification_group = str(getattr(row, "diversification_group"))

    return list(cand_map.values())


def validate_portfolio_sandbox_candidates(
    items: List[PortfolioSandboxCandidate],
) -> List[str]:
    errors = []
    if not items:
        errors.append("No sandbox candidates provided.")
        return errors

    symbols = set()
    for item in items:
        if not item.symbol:
            errors.append(f"Candidate {item.candidate_id} missing symbol.")
        if item.symbol in symbols:
            errors.append(f"Duplicate symbol detected: {item.symbol}")
        symbols.add(item.symbol)

        if item.actual_target_weight is not None:
            errors.append(f"Candidate {item.symbol} has actual_target_weight set.")
            item.risk_flags.append(
                PortfolioConstructionRiskFlag.ACTUAL_TARGET_WEIGHT_RISK
            )
        if item.actual_portfolio_weight is not None:
            errors.append(f"Candidate {item.symbol} has actual_portfolio_weight set.")
            item.risk_flags.append(
                PortfolioConstructionRiskFlag.ACTUAL_PORTFOLIO_WEIGHT_RISK
            )
        if item.actual_allocation is not None:
            errors.append(f"Candidate {item.symbol} has actual_allocation set.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_ALLOCATION_RISK)
        if item.actual_position_size is not None:
            errors.append(f"Candidate {item.symbol} has actual_position_size set.")
            item.risk_flags.append(
                PortfolioConstructionRiskFlag.ACTUAL_POSITION_SIZE_RISK
            )
        if item.order_size is not None:
            errors.append(f"Candidate {item.symbol} has order_size set.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ORDER_SIZE_RISK)
        if item.capital_allocation is not None:
            errors.append(f"Candidate {item.symbol} has capital_allocation set.")
            item.risk_flags.append(
                PortfolioConstructionRiskFlag.CAPITAL_DEPLOYMENT_RISK
            )
        if item.live_signal:
            errors.append(f"Candidate {item.symbol} has live_signal set to True.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.LIVE_TRADING_RISK)
        if item.order_decision:
            errors.append(f"Candidate {item.symbol} has order_decision set to True.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.REAL_ORDER_RISK)

    return errors


def portfolio_sandbox_candidates_summary(
    items: List[PortfolioSandboxCandidate],
) -> Dict[str, Any]:
    return {
        "count": len(items),
        "eligible_count": sum(1 for item in items if item.eligible_for_sandbox),
        "symbols": [item.symbol for item in items[:10]]
        + (["..."] if len(items) > 10 else []),
    }


def portfolio_sandbox_candidates_to_text(
    items: List[PortfolioSandboxCandidate], limit: int = 300
) -> str:
    summary = portfolio_sandbox_candidates_summary(items)
    return (
        f"Sandbox Candidates: {summary['count']} total\n"
        f"Eligible: {summary['eligible_count']}\n"
        f"Symbols: {', '.join(summary['symbols'])}"
    )
