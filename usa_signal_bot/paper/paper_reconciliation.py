from dataclasses import dataclass
from typing import List, Optional
import datetime
import uuid

from usa_signal_bot.core.enums import PaperReconciliationStatus
from usa_signal_bot.paper.paper_models import (
    VirtualAccount, PaperPosition, CashLedgerEntry, PaperEquitySnapshot
)

@dataclass
class PaperReconciliationItem:
    name: str
    status: PaperReconciliationStatus
    expected: Optional[float | str]
    observed: Optional[float | str]
    difference: Optional[float]
    message: str

@dataclass
class PaperReconciliationReport:
    report_id: str
    created_at_utc: str
    account_id: str
    status: PaperReconciliationStatus
    items: List[PaperReconciliationItem]
    warnings: List[str]
    errors: List[str]

def build_paper_reconciliation_report(
    account: VirtualAccount,
    positions: List[PaperPosition],
    cash_ledger: List[CashLedgerEntry],
    equity_snapshots: List[PaperEquitySnapshot]
) -> PaperReconciliationReport:

    items = []
    items.append(reconcile_cash(account, cash_ledger))
    latest_snap = equity_snapshots[-1] if equity_snapshots else None
    items.append(reconcile_equity(account, positions, latest_snap))
    items.append(reconcile_open_positions(positions))

    overall_status = PaperReconciliationStatus.MATCHED
    warnings = []
    errors = []

    for i in items:
        if i.status == PaperReconciliationStatus.MISMATCH:
            overall_status = PaperReconciliationStatus.MISMATCH
            errors.append(i.message)
        elif i.status == PaperReconciliationStatus.WARNING:
            if overall_status != PaperReconciliationStatus.MISMATCH:
                overall_status = PaperReconciliationStatus.WARNING
            warnings.append(i.message)
        elif i.status == PaperReconciliationStatus.FAILED:
            overall_status = PaperReconciliationStatus.FAILED
            errors.append(i.message)

    return PaperReconciliationReport(
        report_id=f"reconciliation_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        account_id=account.account_id,
        status=overall_status,
        items=items,
        warnings=warnings,
        errors=errors
    )

def reconcile_cash(account: VirtualAccount, cash_ledger: List[CashLedgerEntry]) -> PaperReconciliationItem:
    from usa_signal_bot.paper.cash_ledger import calculate_cash_from_ledger
    calc_cash = calculate_cash_from_ledger(cash_ledger)
    diff = abs(account.cash - calc_cash)
    if diff <= 1e-4:
        return PaperReconciliationItem(
            name="cash_reconciliation",
            status=PaperReconciliationStatus.MATCHED,
            expected=calc_cash,
            observed=account.cash,
            difference=diff,
            message="Account cash matches ledger."
        )
    return PaperReconciliationItem(
        name="cash_reconciliation",
        status=PaperReconciliationStatus.MISMATCH,
        expected=calc_cash,
        observed=account.cash,
        difference=diff,
        message=f"Cash mismatch: Account=${account.cash:,.2f}, Ledger=${calc_cash:,.2f}"
    )

def reconcile_equity(
    account: VirtualAccount,
    positions: List[PaperPosition],
    latest_snapshot: Optional[PaperEquitySnapshot]
) -> PaperReconciliationItem:
    from usa_signal_bot.core.enums import PaperPositionSide

    calc_market_value = sum(p.quantity * (p.market_price or p.average_price) for p in positions if p.side != PaperPositionSide.FLAT)
    calc_equity = account.cash + calc_market_value

    observed = latest_snapshot.equity if latest_snapshot else account.equity
    diff = abs(observed - calc_equity)

    if diff <= 1e-4:
        return PaperReconciliationItem(
            name="equity_reconciliation",
            status=PaperReconciliationStatus.MATCHED,
            expected=calc_equity,
            observed=observed,
            difference=diff,
            message="Account equity matches calculated positions value."
        )
    return PaperReconciliationItem(
        name="equity_reconciliation",
        status=PaperReconciliationStatus.MISMATCH,
        expected=calc_equity,
        observed=observed,
        difference=diff,
        message=f"Equity mismatch: Observed=${observed:,.2f}, Calculated=${calc_equity:,.2f}"
    )

def reconcile_open_positions(positions: List[PaperPosition]) -> PaperReconciliationItem:
    from usa_signal_bot.core.enums import PaperPositionSide
    for p in positions:
        if p.side != PaperPositionSide.FLAT and p.quantity < 0:
            return PaperReconciliationItem(
                name="open_positions_reconciliation",
                status=PaperReconciliationStatus.MISMATCH,
                expected="quantity >= 0",
                observed=p.quantity,
                difference=None,
                message=f"Negative quantity found for {p.symbol}"
            )
    return PaperReconciliationItem(
        name="open_positions_reconciliation",
        status=PaperReconciliationStatus.MATCHED,
        expected="Valid Quantities",
        observed="Valid Quantities",
        difference=0.0,
        message="All open position quantities are logically valid."
    )

def paper_reconciliation_report_to_dict(report: PaperReconciliationReport) -> dict:
    from dataclasses import asdict
    d = asdict(report)
    d["status"] = report.status.value if hasattr(report.status, "value") else report.status
    for i in d["items"]:
        i["status"] = i["status"].value if hasattr(i["status"], "value") else i["status"]
    return d

def paper_reconciliation_report_to_text(report: PaperReconciliationReport) -> str:
    lines = [
        "===============================================",
        f"PAPER RECONCILIATION REPORT: {report.status.value if hasattr(report.status, 'value') else report.status}",
        f"Account ID: {report.account_id} | Created: {report.created_at_utc}",
        "==============================================="
    ]

    for i in report.items:
        status = i.status.value if hasattr(i.status, 'value') else i.status
        lines.append(f"[{status}] {i.name}: {i.message} (Diff: {i.difference})")

    lines.append("")
    lines.append("*** DISCLAIMER: LOCAL PAPER TRADING ONLY ***")
    return "\n".join(lines)
