import pandas as pd
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSandboxCandidate

def build_optimizer_sandbox_candidates(exposure_table_payload: Dict[str, Any], candidate_df: Optional[pd.DataFrame] = None) -> List[OptimizerSandboxCandidate]:
    candidates = infer_candidates_from_exposure_table(exposure_table_payload)
    if candidate_df is not None:
        candidates = merge_optimizer_candidate_overrides(candidates, candidate_df)
    return candidates

def infer_candidates_from_exposure_table(exposure_table_payload: Dict[str, Any]) -> List[OptimizerSandboxCandidate]:
    candidates = []
    # Simplified mock for inference
    items = exposure_table_payload.get("items", [])
    for item in items:
        sym = item.get("symbol", "UNKNOWN")
        c = OptimizerSandboxCandidate(symbol=sym, candidate_valid=True, eligible_for_optimizer_sandbox=True, research_data_only=True)
        c.sandbox_score = item.get("sandbox_score")
        candidates.append(c)
    return candidates

def merge_optimizer_candidate_overrides(candidates: List[OptimizerSandboxCandidate], candidate_df: Optional[pd.DataFrame] = None) -> List[OptimizerSandboxCandidate]:
    if candidate_df is None or candidate_df.empty: return candidates

    cdict = {c.symbol: c for c in candidates}
    for row in candidate_df.itertuples(index=False):
        sym = getattr(row, "symbol", None)
        if not sym: continue
        if sym not in cdict:
            c = OptimizerSandboxCandidate(symbol=sym, candidate_valid=True, eligible_for_optimizer_sandbox=True, research_data_only=True)
            cdict[sym] = c
        c = cdict[sym]
        c.sandbox_score = getattr(row, "sandbox_score", c.sandbox_score)
        c.risk_budget_score = getattr(row, "risk_budget_score", c.risk_budget_score)
        c.concentration_group = getattr(row, "concentration_group", c.concentration_group)
    return list(cdict.values())

def validate_optimizer_sandbox_candidates(items: List[OptimizerSandboxCandidate]) -> List[str]:
    errs = []
    for c in items:
        if c.actual_target_weight is not None: errs.append(f"{c.symbol}: actual_target_weight not None")
        if c.actual_portfolio_weight is not None: errs.append(f"{c.symbol}: actual_portfolio_weight not None")
        if c.actual_allocation is not None: errs.append(f"{c.symbol}: actual_allocation not None")
        if c.actual_position_size is not None: errs.append(f"{c.symbol}: actual_position_size not None")
        if c.order_size is not None: errs.append(f"{c.symbol}: order_size not None")
        if c.capital_allocation is not None: errs.append(f"{c.symbol}: capital_allocation not None")
        if c.live_signal: errs.append(f"{c.symbol}: live_signal is true")
        if c.order_decision: errs.append(f"{c.symbol}: order_decision is true")
    return errs

def optimizer_sandbox_candidates_summary(items: List[OptimizerSandboxCandidate]) -> Dict[str, Any]:
    return {"count": len(items)}

def optimizer_sandbox_candidates_to_text(items: List[OptimizerSandboxCandidate], limit: int = 300) -> str:
    return str([c.to_dict() for c in items])[:limit]
