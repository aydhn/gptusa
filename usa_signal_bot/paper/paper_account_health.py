from dataclasses import dataclass
from typing import List, Optional
import datetime
import uuid

from usa_signal_bot.core.enums import PaperAccountHealthStatus
from usa_signal_bot.paper.paper_models import (
    VirtualAccount, PaperPosition, CashLedgerEntry, PaperEquitySnapshot
)

@dataclass
class PaperAccountHealthCheck:
    name: str
    status: PaperAccountHealthStatus
    severity: str
    message: str
    observed_value: Optional[float | str] = None
    expected_value: Optional[float | str] = None

@dataclass
class PaperAccountHealthReport:
    report_id: str
    created_at_utc: str
    account_id: str
    status: PaperAccountHealthStatus
    checks: List[PaperAccountHealthCheck]
    warning_count: int
    critical_count: int
    warnings: List[str]
    errors: List[str]

def build_paper_account_health_report(
    account: VirtualAccount,
    positions: List[PaperPosition],
    cash_ledger: List[CashLedgerEntry],
    equity_snapshots: List[PaperEquitySnapshot],
    max_drawdown_warning_pct: float = 0.10
) -> PaperAccountHealthReport:

    checks = []
    checks.append(check_cash_non_negative(account))
    checks.append(check_equity_non_negative(account))
    checks.append(check_position_quantities_valid(positions))
    checks.append(check_cash_ledger_consistency(account, cash_ledger))
    checks.append(check_drawdown_warning(equity_snapshots, max_drawdown_warning_pct))

    warning_count = sum(1 for c in checks if c.status == PaperAccountHealthStatus.WARNING)
    critical_count = sum(1 for c in checks if c.status == PaperAccountHealthStatus.CRITICAL)

    overall_status = PaperAccountHealthStatus.HEALTHY
    if critical_count > 0:
        overall_status = PaperAccountHealthStatus.CRITICAL
    elif warning_count > 0:
        overall_status = PaperAccountHealthStatus.WARNING

    warnings = [c.message for c in checks if c.status == PaperAccountHealthStatus.WARNING]
    errors = [c.message for c in checks if c.status == PaperAccountHealthStatus.CRITICAL]

    return PaperAccountHealthReport(
        report_id=f"health_report_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        account_id=account.account_id,
        status=overall_status,
        checks=checks,
        warning_count=warning_count,
        critical_count=critical_count,
        warnings=warnings,
        errors=errors
    )

def check_cash_non_negative(account: VirtualAccount) -> PaperAccountHealthCheck:
    if account.cash < 0:
        return PaperAccountHealthCheck(
            name="cash_non_negative",
            status=PaperAccountHealthStatus.CRITICAL,
            severity="CRITICAL",
            message="Account cash is negative.",
            observed_value=account.cash,
            expected_value=">= 0"
        )
    return PaperAccountHealthCheck(
        name="cash_non_negative",
        status=PaperAccountHealthStatus.HEALTHY,
        severity="INFO",
        message="Account cash is valid.",
        observed_value=account.cash,
        expected_value=">= 0"
    )

def check_equity_non_negative(account: VirtualAccount) -> PaperAccountHealthCheck:
    if account.equity < 0:
        return PaperAccountHealthCheck(
            name="equity_non_negative",
            status=PaperAccountHealthStatus.CRITICAL,
            severity="CRITICAL",
            message="Account equity is negative.",
            observed_value=account.equity,
            expected_value=">= 0"
        )
    return PaperAccountHealthCheck(
        name="equity_non_negative",
        status=PaperAccountHealthStatus.HEALTHY,
        severity="INFO",
        message="Account equity is valid.",
        observed_value=account.equity,
        expected_value=">= 0"
    )

def check_position_quantities_valid(positions: List[PaperPosition]) -> PaperAccountHealthCheck:
    from usa_signal_bot.core.enums import PaperPositionSide
    for p in positions:
        if p.side != PaperPositionSide.FLAT and p.quantity < 0:
            return PaperAccountHealthCheck(
                name="position_quantities_valid",
                status=PaperAccountHealthStatus.CRITICAL,
                severity="CRITICAL",
                message=f"Negative quantity found for {p.symbol}",
                observed_value=p.quantity,
                expected_value=">= 0"
            )
    return PaperAccountHealthCheck(
        name="position_quantities_valid",
        status=PaperAccountHealthStatus.HEALTHY,
        severity="INFO",
        message="All position quantities are valid."
    )

def check_cash_ledger_consistency(account: VirtualAccount, cash_ledger: List[CashLedgerEntry]) -> PaperAccountHealthCheck:
    from usa_signal_bot.paper.cash_ledger import calculate_cash_from_ledger
    calculated_cash = calculate_cash_from_ledger(cash_ledger)
    diff = abs(account.cash - calculated_cash)
    if diff > 1e-4: # Tolerance
        return PaperAccountHealthCheck(
            name="cash_ledger_consistency",
            status=PaperAccountHealthStatus.WARNING,
            severity="WARNING",
            message="Account cash does not match ledger.",
            observed_value=account.cash,
            expected_value=calculated_cash
        )
    return PaperAccountHealthCheck(
        name="cash_ledger_consistency",
        status=PaperAccountHealthStatus.HEALTHY,
        severity="INFO",
        message="Account cash matches ledger."
    )

def check_drawdown_warning(equity_snapshots: List[PaperEquitySnapshot], threshold_pct: float) -> PaperAccountHealthCheck:
    if not equity_snapshots:
        return PaperAccountHealthCheck(
            name="drawdown_warning",
            status=PaperAccountHealthStatus.UNKNOWN,
            severity="INFO",
            message="No equity snapshots to evaluate drawdown."
        )

    max_equity = 0.0
    max_dd = 0.0
    for s in equity_snapshots:
        if s.equity > max_equity:
            max_equity = s.equity
        if max_equity > 0:
            dd = (max_equity - s.equity) / max_equity
            if dd > max_dd:
                max_dd = dd

    if max_dd >= threshold_pct:
        return PaperAccountHealthCheck(
            name="drawdown_warning",
            status=PaperAccountHealthStatus.WARNING,
            severity="WARNING",
            message=f"Max drawdown {max_dd*100:.2f}% exceeds warning threshold {threshold_pct*100:.2f}%",
            observed_value=max_dd,
            expected_value=f"< {threshold_pct}"
        )
    return PaperAccountHealthCheck(
        name="drawdown_warning",
        status=PaperAccountHealthStatus.HEALTHY,
        severity="INFO",
        message=f"Max drawdown {max_dd*100:.2f}% is within acceptable limits.",
        observed_value=max_dd,
        expected_value=f"< {threshold_pct}"
    )

def paper_account_health_report_to_dict(report: PaperAccountHealthReport) -> dict:
    from dataclasses import asdict
    d = asdict(report)
    d["status"] = report.status.value if hasattr(report.status, "value") else report.status
    for c in d["checks"]:
        c["status"] = c["status"].value if hasattr(c["status"], "value") else c["status"]
    return d

def paper_account_health_report_to_text(report: PaperAccountHealthReport) -> str:
    lines = [
        "===============================================",
        f"PAPER ACCOUNT HEALTH REPORT: {report.status.value if hasattr(report.status, 'value') else report.status}",
        f"Account ID: {report.account_id} | Created: {report.created_at_utc}",
        "==============================================="
    ]

    for c in report.checks:
        status = c.status.value if hasattr(c.status, 'value') else c.status
        obs = f"Obs: {c.observed_value}" if c.observed_value is not None else ""
        exp = f"Exp: {c.expected_value}" if c.expected_value is not None else ""
        vals = f"[{obs} | {exp}]" if obs or exp else ""
        lines.append(f"[{status}] {c.name}: {c.message} {vals}")

    lines.append("")
    lines.append("*** DISCLAIMER: LOCAL PAPER TRADING ONLY ***")
    return "\n".join(lines)
