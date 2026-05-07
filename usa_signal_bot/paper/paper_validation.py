from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.paper.paper_models import (
    VirtualAccount, PaperOrderIntent, PaperOrder, PaperFill, PaperEngineRunResult
)
from usa_signal_bot.paper.paper_engine import PaperEngineConfig

@dataclass
class PaperValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: List[PaperValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_paper_engine_config(config: PaperEngineConfig) -> PaperValidationReport:
    issues = []

    if config.allow_short:
        issues.append(PaperValidationIssue("WARNING", "allow_short", "allow_short is True but shorts are partially supported"))

    if config.starting_cash <= 0:
        issues.append(PaperValidationIssue("ERROR", "starting_cash", "starting_cash must be positive"))

    if config.max_positions <= 0:
        issues.append(PaperValidationIssue("ERROR", "max_positions", "max_positions must be positive"))

    return _build_report(issues)

def validate_paper_order_intent_report(intent: PaperOrderIntent) -> PaperValidationReport:
    issues = []

    if not intent.symbol:
        issues.append(PaperValidationIssue("ERROR", "symbol", "symbol cannot be empty"))

    if getattr(intent.side, "value", str(intent.side)) in ["BUY", "SELL"] and intent.quantity <= 0:
        issues.append(PaperValidationIssue("ERROR", "quantity", "quantity must be positive for BUY/SELL"))

    return _build_report(issues)

def validate_paper_order_report(order: PaperOrder) -> PaperValidationReport:
    report = validate_paper_order_intent_report(order.intent)
    return report

def validate_paper_fill_report(fill: PaperFill) -> PaperValidationReport:
    issues = []
    if fill.fill_price <= 0:
        issues.append(PaperValidationIssue("ERROR", "fill_price", "fill_price must be positive"))
    if fill.gross_notional < 0:
        issues.append(PaperValidationIssue("ERROR", "gross_notional", "gross_notional cannot be negative"))
    return _build_report(issues)

def validate_virtual_account_report(account: VirtualAccount) -> PaperValidationReport:
    issues = []
    if account.starting_cash <= 0:
        issues.append(PaperValidationIssue("ERROR", "starting_cash", "starting_cash must be positive"))
    if account.cash < 0:
        issues.append(PaperValidationIssue("ERROR", "cash", "cash cannot be negative"))
    if account.equity < 0:
        issues.append(PaperValidationIssue("ERROR", "equity", "equity cannot be negative"))
    return _build_report(issues)

def validate_paper_engine_run_result(result: PaperEngineRunResult) -> PaperValidationReport:
    issues = []

    acct_report = validate_virtual_account_report(result.account)
    issues.extend(acct_report.issues)

    for order in result.orders:
        o_rep = validate_paper_order_report(order)
        issues.extend(o_rep.issues)

    for fill in result.fills:
        f_rep = validate_paper_fill_report(fill)
        issues.extend(f_rep.issues)

    return _build_report(issues)

def validate_no_broker_execution_in_paper(result: Any) -> PaperValidationReport:
    issues = []

    # We must ensure we capture dataclass conversion
    try:
        from dataclasses import asdict
        res_dict = asdict(result)
    except Exception:
        # Fallback to json if asdict fails
        res_dict = json.loads(json.dumps(result, default=str))

    def _search_dict(d: dict, path: str):
        forbidden_keys = ["broker_order", "live_order", "demo_order", "broker_execution"]
        if not isinstance(d, dict):
            return
        for k, v in d.items():
            if k in forbidden_keys:
                issues.append(PaperValidationIssue("ERROR", f"{path}.{k}", "Broker execution field found in paper result!"))
            if isinstance(v, dict):
                _search_dict(v, f"{path}.{k}")
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        _search_dict(item, f"{path}.{k}[{i}]")

    _search_dict(res_dict, "root")
    return _build_report(issues)

def validate_no_live_order_language_in_paper(result: Any) -> PaperValidationReport:
    issues = []
    res_str = json.dumps(result, default=str).lower()

    forbidden_terms = ["live executed", "sent to broker", "live order placed", "real money"]
    for term in forbidden_terms:
        if term in res_str:
            issues.append(PaperValidationIssue("ERROR", "result_content", f"Forbidden live order language found: '{term}'"))

    return _build_report(issues)

def _build_report(issues: List[PaperValidationIssue]) -> PaperValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    return PaperValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def paper_validation_report_to_text(report: PaperValidationReport) -> str:
    lines = ["--- PAPER VALIDATION REPORT ---"]
    lines.append(f"Valid: {report.valid}")
    lines.append(f"Issues: {report.issue_count} ({report.error_count} E, {report.warning_count} W)")

    if report.errors:
        lines.append("Errors:")
        for e in report.errors:
            lines.append(f"  - {e}")

    if report.warnings:
        lines.append("Warnings:")
        for w in report.warnings:
            lines.append(f"  - {w}")

    return "\n".join(lines)

def assert_paper_valid(report: PaperValidationReport) -> None:
    from usa_signal_bot.core.exceptions import PaperValidationError
    if not report.valid:
        raise PaperValidationError(f"Paper validation failed: {report.errors}")
