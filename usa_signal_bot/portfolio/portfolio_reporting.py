from pathlib import Path
from typing import List, Optional
from usa_signal_bot.portfolio.portfolio_models import (
    PortfolioCandidate,
    AllocationResult,
    PortfolioBasket,
    PortfolioConstructionResult
)
from usa_signal_bot.portfolio.allocation_methods import AllocationConfig
from usa_signal_bot.portfolio.risk_budgeting import RiskBudgetConfig
from usa_signal_bot.portfolio.concentration_guards import ConcentrationGuardConfig
from usa_signal_bot.portfolio.portfolio_validation import PortfolioValidationReport

def allocation_config_to_text(config: AllocationConfig) -> str:
    lines = [
        "Allocation Config:",
        f"  Method: {config.method.value if hasattr(config.method, 'value') else str(config.method)}",
        f"  Max Total Allocation Pct: {config.max_total_allocation_pct:.2f}",
        f"  Max Candidate Weight: {config.max_candidate_weight:.2f}",
        f"  Min Candidate Weight: {config.min_candidate_weight:.2f}",
        f"  Normalize Weights: {config.normalize_weights}"
    ]
    return "\n".join(lines)

def risk_budget_config_to_text(config: RiskBudgetConfig) -> str:
    lines = [
        "Risk Budget Config:",
        f"  Max Total Budget: {config.max_total_budget_pct:.2f}",
        f"  Max Symbol Budget: {config.max_symbol_budget_pct:.2f}",
        f"  Max Strategy Budget: {config.max_strategy_budget_pct:.2f}",
        f"  Enforce Budget: {config.enforce_budget}"
    ]
    return "\n".join(lines)

def concentration_guard_config_to_text(config: ConcentrationGuardConfig) -> str:
    lines = [
        "Concentration Guard Config:",
        f"  Max Symbol Weight: {config.max_symbol_weight:.2f}",
        f"  Max Strategy Weight: {config.max_strategy_weight:.2f}",
        f"  Max Timeframe Weight: {config.max_timeframe_weight:.2f}",
        f"  Max Single Candidate Weight: {config.max_single_candidate_weight:.2f}",
        f"  Cap Breaches: {config.cap_breaches}",
        f"  Reject Breaches: {config.reject_breaches}"
    ]
    return "\n".join(lines)

def portfolio_candidate_to_text(candidate: PortfolioCandidate) -> str:
    return f"{candidate.symbol} ({candidate.timeframe}) [{candidate.status.value if hasattr(candidate.status, 'value') else str(candidate.status)}] - Risk: {candidate.risk_score}"

def allocation_result_to_text(result: AllocationResult) -> str:
    st = result.status.value if hasattr(result.status, "value") else str(result.status)
    return f"{result.symbol} ({result.timeframe}) -> {st} | Target Wt: {result.target_weight:.4f} | Notional: {result.target_notional:.2f} | Capped: {result.capped}"

def allocations_to_text(allocations: List[AllocationResult], limit: int = 30) -> str:
    lines = [f"Allocations ({len(allocations)} total):", "-" * 50]
    for i, a in enumerate(allocations[:limit]):
        lines.append(f"{i+1}. {allocation_result_to_text(a)}")
    if len(allocations) > limit:
        lines.append(f"... and {len(allocations) - limit} more.")
    return "\n".join(lines)

def portfolio_basket_to_text(basket: PortfolioBasket, limit: int = 30) -> str:
    rev_st = basket.review_status.value if hasattr(basket.review_status, "value") else str(basket.review_status)
    method = basket.method.value if hasattr(basket.method, "value") else str(basket.method)

    lines = [
        f"Portfolio Basket [{basket.basket_id}]",
        f"Review Status: {rev_st}",
        f"Method: {method}",
        f"Total Target Wt: {basket.total_target_weight:.4f}",
        f"Total Target Notional: {basket.total_target_notional:.2f}",
        f"Cash Buffer Remaining: {basket.cash_buffer_after_allocation:.2f}",
        "-" * 50,
        allocations_to_text(basket.allocations, limit)
    ]
    return "\n".join(lines)

def portfolio_construction_result_to_text(result: PortfolioConstructionResult, limit: int = 30) -> str:
    st = result.status.value if hasattr(result.status, "value") else str(result.status)

    lines = [
        f"Portfolio Construction Run [{result.run_id}]",
        f"Status: {st}",
        f"Created At: {result.created_at_utc}",
        "-" * 50,
        f"Eligible Candidates Processed: {len(result.request.candidates)}",
        f"Approved Allocations: {len(result.approved_allocations)}",
        f"Rejected/Zero Allocations: {len(result.rejected_allocations)}"
    ]

    if result.basket:
        lines.append("")
        lines.append(portfolio_basket_to_text(result.basket, limit))

    lines.append("")
    lines.append(portfolio_limitations_text())
    return "\n".join(lines)

def portfolio_limitations_text() -> str:
    return (
        "*** PORTFOLIO LIMITATIONS & WARNING ***\n"
        "- This portfolio construction is a LOCAL BASELINE for research and backtesting only.\n"
        "- It is NOT an optimizer (no mean-variance, no Kelly, etc.).\n"
        "- The allocation weights and notionals are NOT investment advice.\n"
        "- NO LIVE BROKER EXECUTION or paper trade routing is performed."
    )

def write_portfolio_report_json(path: Path, result: PortfolioConstructionResult, validation_report: Optional[PortfolioValidationReport] = None) -> Path:
    from usa_signal_bot.portfolio.portfolio_models import portfolio_construction_result_to_dict
    import json
    data = {
        "result": portfolio_construction_result_to_dict(result),
        "limitations": portfolio_limitations_text(),
        "validation": None
    }
    if validation_report:
        from dataclasses import asdict
        data["validation"] = asdict(validation_report)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path
