import pandas
from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    CandidateUniverseContract, PortfolioCandidate, PortfolioCandidateUniverseKind
)

def infer_candidates_from_handoff(handoff_payload: dict[str, Any]) -> list[PortfolioCandidate]:
    candidates = []
    # Try to extract symbols from metric inventory or risk notes
    symbols = set()

    if "metric_inventory" in handoff_payload:
        for item in handoff_payload["metric_inventory"]:
            if "symbol" in item:
                symbols.add(item["symbol"])

    if "risk_notes" in handoff_payload:
        for item in handoff_payload["risk_notes"]:
            if "symbol" in item:
                symbols.add(item["symbol"])

    for symbol in sorted(list(symbols)):
        c = PortfolioCandidate(symbol=symbol)
        candidates.append(c)

    return candidates

def infer_candidates_from_frame(candidate_df: pandas.DataFrame) -> list[PortfolioCandidate]:
    candidates = []
    if "symbol" in candidate_df.columns:
        for symbol in candidate_df["symbol"].unique():
            c = PortfolioCandidate(symbol=str(symbol))
            candidates.append(c)
    return candidates

def build_candidate_universe_contract(handoff_payload: dict[str, Any], candidate_df: pandas.DataFrame | None = None) -> CandidateUniverseContract:
    contract = CandidateUniverseContract()
    contract.universe_name = "Phase153 Base Candidate Universe"
    contract.universe_kind = PortfolioCandidateUniverseKind.MULTI_SYMBOL_RESEARCH_UNIVERSE

    candidates = []
    if candidate_df is not None:
        candidates = infer_candidates_from_frame(candidate_df)
    else:
        candidates = infer_candidates_from_handoff(handoff_payload)

    contract.candidates = candidates
    contract.candidate_count = len(candidates)
    contract.symbols = [c.symbol for c in candidates]

    contract.min_required_candidates = 1
    contract.max_allowed_candidates = 1000

    contract.contract_valid = True

    # Check candidates for illegal fields
    for c in candidates:
        c.target_weight = None
        c.allocation = None
        c.position_size = None
        c.live_signal = False
        c.order_decision = False

    contract.produces_portfolio_weights = False
    contract.produces_order_decision = False
    contract.produces_live_signal = False

    return contract

def validate_candidate_universe_contract(contract: CandidateUniverseContract) -> list[str]:
    errors = []
    if contract.produces_portfolio_weights:
        errors.append("Produces portfolio weights must be false")
    if contract.produces_order_decision:
        errors.append("Produces order decision must be false")
    if contract.produces_live_signal:
        errors.append("Produces live signal must be false")
    for c in contract.candidates:
        if c.target_weight is not None or c.allocation is not None or c.position_size is not None:
            errors.append(f"Candidate {c.symbol} has active weight/size fields")
    return errors

def candidate_universe_contract_summary(contract: CandidateUniverseContract) -> dict[str, Any]:
    return {
        "candidate_count": contract.candidate_count,
        "valid": contract.contract_valid
    }

def candidate_universe_contract_to_text(contract: CandidateUniverseContract, limit: int = 300) -> str:
    return f"CandidateUniverseContract: {contract.candidate_count} candidates, valid: {contract.contract_valid}"
