from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid
import datetime

from usa_signal_bot.core.enums import PaperReportType, PaperReportStatus
from usa_signal_bot.paper.paper_models import (
    VirtualAccount, PaperOrder, PaperFill, PaperPosition,
    CashLedgerEntry, PaperEquitySnapshot, PaperTrade
)

@dataclass
class DailyPaperAccountReport:
    report_id: str
    report_date: str
    created_at_utc: str
    account_id: str
    account_name: str
    report_type: PaperReportType
    status: PaperReportStatus
    starting_cash: float
    ending_cash: float
    starting_equity: Optional[float]
    ending_equity: Optional[float]
    realized_pnl: float
    unrealized_pnl: float
    total_orders: int
    filled_orders: int
    rejected_orders: int
    total_fills: int
    open_positions: int
    closed_trades: int
    open_trades: int
    total_fees: float
    gross_exposure: float
    net_exposure: float
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

def create_daily_paper_account_report(
    account: VirtualAccount,
    orders: List[PaperOrder],
    fills: List[PaperFill],
    positions: List[PaperPosition],
    cash_ledger: List[CashLedgerEntry],
    equity_snapshots: List[PaperEquitySnapshot],
    trades: List[PaperTrade],
    report_date: Optional[str] = None
) -> DailyPaperAccountReport:

    now = datetime.datetime.now(datetime.timezone.utc)
    date_str = report_date or now.strftime("%Y-%m-%d")

    starting_equity = equity_snapshots[0].equity if equity_snapshots else account.starting_cash
    ending_equity = equity_snapshots[-1].equity if equity_snapshots else account.equity

    total_fees = sum(f.fees for f in fills)

    from usa_signal_bot.core.enums import PaperOrderStatus
    filled_orders = sum(1 for o in orders if o.status == PaperOrderStatus.FILLED)
    rejected_orders = sum(1 for o in orders if o.status == PaperOrderStatus.REJECTED)

    from usa_signal_bot.core.enums import PaperPositionSide
    open_positions = sum(1 for p in positions if p.side != PaperPositionSide.FLAT and p.quantity > 0)

    from usa_signal_bot.core.enums import PaperTradeStatus
    closed_trades = sum(1 for t in trades if t.status == PaperTradeStatus.CLOSED)
    open_trades = sum(1 for t in trades if t.status == PaperTradeStatus.OPEN)

    gross_exposure = equity_snapshots[-1].gross_exposure if equity_snapshots else 0.0
    net_exposure = equity_snapshots[-1].net_exposure if equity_snapshots else 0.0

    warnings = []
    if not fills:
        warnings.append("No fills generated during this period.")
    if not trades:
        warnings.append("No trades generated during this period.")

    status = PaperReportStatus.COMPLETED
    if not orders and not fills and not positions:
        status = PaperReportStatus.EMPTY

    report = DailyPaperAccountReport(
        report_id=create_daily_paper_report_id(date_str),
        report_date=date_str,
        created_at_utc=now.isoformat(),
        account_id=account.account_id,
        account_name=account.name,
        report_type=PaperReportType.DAILY_ACCOUNT,
        status=status,
        starting_cash=account.starting_cash,
        ending_cash=account.cash,
        starting_equity=starting_equity,
        ending_equity=ending_equity,
        realized_pnl=account.realized_pnl,
        unrealized_pnl=account.unrealized_pnl,
        total_orders=len(orders),
        filled_orders=filled_orders,
        rejected_orders=rejected_orders,
        total_fills=len(fills),
        open_positions=open_positions,
        closed_trades=closed_trades,
        open_trades=open_trades,
        total_fees=total_fees,
        gross_exposure=gross_exposure,
        net_exposure=net_exposure,
        warnings=warnings,
        errors=[]
    )
    validate_daily_paper_account_report(report)
    return report

def daily_paper_account_report_to_dict(report: DailyPaperAccountReport) -> dict:
    from dataclasses import asdict
    d = asdict(report)
    d["report_type"] = report.report_type.value if hasattr(report.report_type, "value") else report.report_type
    d["status"] = report.status.value if hasattr(report.status, "value") else report.status
    return d

def daily_paper_account_report_to_text(report: DailyPaperAccountReport) -> str:
    lines = [
        "===============================================",
        f"DAILY VIRTUAL ACCOUNT REPORT: {report.report_date}",
        f"Account: {report.account_name} ({report.account_id})",
        "===============================================",
        f"Starting Cash:  ${report.starting_cash:,.2f}",
        f"Ending Cash:    ${report.ending_cash:,.2f}",
        f"Starting Eq:    ${report.starting_equity:,.2f}" if report.starting_equity is not None else "Starting Eq:    N/A",
        f"Ending Eq:      ${report.ending_equity:,.2f}" if report.ending_equity is not None else "Ending Eq:      N/A",
        f"Realized PnL:   ${report.realized_pnl:,.2f}",
        f"Unrealized PnL: ${report.unrealized_pnl:,.2f}",
        f"Total Fees:     ${report.total_fees:,.2f}",
        "--- ACTIVITY ---",
        f"Orders: {report.total_orders} (Filled: {report.filled_orders}, Rejected: {report.rejected_orders})",
        f"Fills:  {report.total_fills}",
        f"Trades: Closed {report.closed_trades}, Open {report.open_trades}",
        f"Open Positions: {report.open_positions}",
        "--- EXPOSURE ---",
        f"Gross: ${report.gross_exposure:,.2f}",
        f"Net:   ${report.net_exposure:,.2f}"
    ]
    if report.warnings:
        lines.append("--- WARNINGS ---")
        for w in report.warnings:
            lines.append(f"  * {w}")
    if report.errors:
        lines.append("--- ERRORS ---")
        for e in report.errors:
            lines.append(f"  ! {e}")

    lines.append("")
    lines.append("*** DISCLAIMER: LOCAL PAPER TRADING ONLY ***")
    lines.append("This is not a real brokerage statement. Not investment advice.")
    return "\n".join(lines)

def validate_daily_paper_account_report(report: DailyPaperAccountReport) -> None:
    pass

def create_daily_paper_report_id(report_date: Optional[str] = None) -> str:
    d = report_date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    return f"daily_report_{d}_{uuid.uuid4().hex[:8]}"
