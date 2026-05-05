from dataclasses import dataclass, field
from typing import List, Any, Optional

from usa_signal_bot.portfolio.portfolio_models import (
    AllocationRequest,
    AllocationResult,
    PortfolioBasket,
    PortfolioConstructionResult
)
from usa_signal_bot.core.enums import AllocationStatus

@dataclass
class PortfolioValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: List[PortfolioValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_allocation_request_report(request: AllocationRequest) -> PortfolioValidationReport:
    issues = []

    if request.portfolio_equity <= 0:
        issues.append(PortfolioValidationIssue("ERROR", "portfolio_equity", "Must be > 0"))

    if request.available_cash < 0:
        issues.append(PortfolioValidationIssue("ERROR", "available_cash", "Cannot be negative"))

    error_count = sum(1 for i in issues if i.severity == "ERROR")
    warning_count = sum(1 for i in issues if i.severity == "WARNING")

    return PortfolioValidationReport(
        valid=error_count == 0,
        issue_count=len(issues),
        warning_count=warning_count,
        error_count=error_count,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "WARNING"],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_allocation_results_report(results: List[AllocationResult]) -> PortfolioValidationReport:
    issues = []

    total_weight = 0.0
    for r in results:
        if r.target_notional < 0:
            issues.append(PortfolioValidationIssue("ERROR", "target_notional", f"Negative notional for {r.candidate_id}"))
        if r.target_quantity < 0:
            issues.append(PortfolioValidationIssue("ERROR", "target_quantity", f"Negative quantity for {r.candidate_id}"))
        if r.status in [AllocationStatus.REJECTED, AllocationStatus.ZERO]:
            if r.target_notional > 0 or r.target_quantity > 0:
                issues.append(PortfolioValidationIssue("ERROR", "target_notional/quantity", f"Rejected allocation {r.candidate_id} has > 0 notional/qty"))

        if r.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED]:
            total_weight += r.target_weight

    if total_weight > 1.05: # Slight tolerance
        issues.append(PortfolioValidationIssue("WARNING", "total_weight", f"Total target weight > 100%: {total_weight}"))

    error_count = sum(1 for i in issues if i.severity == "ERROR")
    warning_count = sum(1 for i in issues if i.severity == "WARNING")

    return PortfolioValidationReport(
        valid=error_count == 0,
        issue_count=len(issues),
        warning_count=warning_count,
        error_count=error_count,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "WARNING"],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_portfolio_basket_report(basket: PortfolioBasket) -> PortfolioValidationReport:
    issues = []

    if basket.cash_buffer_after_allocation < 0:
        issues.append(PortfolioValidationIssue("ERROR", "cash_buffer_after_allocation", "Negative cash buffer after allocation"))

    error_count = sum(1 for i in issues if i.severity == "ERROR")
    warning_count = sum(1 for i in issues if i.severity == "WARNING")

    return PortfolioValidationReport(
        valid=error_count == 0,
        issue_count=len(issues),
        warning_count=warning_count,
        error_count=error_count,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "WARNING"],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_no_portfolio_optimizer_behavior(result: PortfolioConstructionResult) -> PortfolioValidationReport:
    issues = []

    # Check for optimizer terms in dictionaries or properties if we could serialize it
    from usa_signal_bot.portfolio.portfolio_models import portfolio_construction_result_to_dict
    import json

    try:
        data = json.dumps(portfolio_construction_result_to_dict(result)).lower()
        if "optimal_weights" in data or "recommended_portfolio" in data or "optimizer" in data:
            if not ("not_optimizer" in data or "not_investment_advice" in data):
                # Simple heuristic
                issues.append(PortfolioValidationIssue("ERROR", "result", "Contains optimization or recommendation language."))
    except Exception:
        pass

    error_count = sum(1 for i in issues if i.severity == "ERROR")
    warning_count = sum(1 for i in issues if i.severity == "WARNING")

    return PortfolioValidationReport(
        valid=error_count == 0,
        issue_count=len(issues),
        warning_count=warning_count,
        error_count=error_count,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "WARNING"],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_no_broker_execution_in_portfolio(result: PortfolioConstructionResult) -> PortfolioValidationReport:
    issues = []
    from usa_signal_bot.portfolio.portfolio_models import portfolio_construction_result_to_dict
    import json

    try:
        data = json.dumps(portfolio_construction_result_to_dict(result)).lower()
        if "broker_order" in data or "live_order" in data or "paper_order" in data:
             issues.append(PortfolioValidationIssue("ERROR", "result", "Contains live/broker order instructions."))
    except Exception:
        pass

    error_count = sum(1 for i in issues if i.severity == "ERROR")
    warning_count = sum(1 for i in issues if i.severity == "WARNING")

    return PortfolioValidationReport(
        valid=error_count == 0,
        issue_count=len(issues),
        warning_count=warning_count,
        error_count=error_count,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "WARNING"],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_portfolio_construction_result(result: PortfolioConstructionResult) -> PortfolioValidationReport:
    req_report = validate_allocation_request_report(result.request)
    if not req_report.valid:
        return req_report

    alloc_report = validate_allocation_results_report(result.approved_allocations + result.rejected_allocations)
    if not alloc_report.valid:
        return alloc_report

    if result.basket:
        bask_report = validate_portfolio_basket_report(result.basket)
        if not bask_report.valid:
            return bask_report

    opt_report = validate_no_portfolio_optimizer_behavior(result)
    if not opt_report.valid:
        return opt_report

    brok_report = validate_no_broker_execution_in_portfolio(result)
    if not brok_report.valid:
        return brok_report

    return PortfolioValidationReport(
        valid=True,
        issue_count=0,
        warning_count=0,
        error_count=0,
        issues=[],
        warnings=[],
        errors=[]
    )

def portfolio_validation_report_to_text(report: PortfolioValidationReport) -> str:
    lines = [f"Valid: {report.valid}"]
    if report.issues:
        for i in report.issues:
            lines.append(f"[{i.severity}] {i.field}: {i.message}")
    return "\n".join(lines)

def assert_portfolio_valid(report: PortfolioValidationReport) -> None:
    from usa_signal_bot.core.exceptions import PortfolioValidationError
    if not report.valid:
        raise PortfolioValidationError(f"Portfolio validation failed: {portfolio_validation_report_to_text(report)}")
