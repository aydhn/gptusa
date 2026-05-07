from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PaperAccountStatus
from usa_signal_bot.paper.paper_models import (
    VirtualAccount,
    PaperPosition,
    create_virtual_account_id,
    validate_virtual_account
)

def create_virtual_account(name: str = "local_paper", starting_cash: float = 100000.0) -> VirtualAccount:
    now_utc = datetime.now(timezone.utc).isoformat()
    account = VirtualAccount(
        account_id=create_virtual_account_id(),
        name=name,
        status=PaperAccountStatus.ACTIVE,
        starting_cash=starting_cash,
        cash=starting_cash,
        equity=starting_cash,
        realized_pnl=0.0,
        unrealized_pnl=0.0,
        created_at_utc=now_utc
    )
    validate_virtual_account(account)
    return account

def pause_virtual_account(account: VirtualAccount, reason: Optional[str] = None) -> VirtualAccount:
    account.status = PaperAccountStatus.PAUSED
    account.updated_at_utc = datetime.now(timezone.utc).isoformat()
    if reason:
        account.metadata["pause_reason"] = reason
    return account

def resume_virtual_account(account: VirtualAccount) -> VirtualAccount:
    account.status = PaperAccountStatus.ACTIVE
    account.updated_at_utc = datetime.now(timezone.utc).isoformat()
    account.metadata.pop("pause_reason", None)
    return account

def close_virtual_account(account: VirtualAccount) -> VirtualAccount:
    account.status = PaperAccountStatus.CLOSED
    account.updated_at_utc = datetime.now(timezone.utc).isoformat()
    return account

def update_account_equity(account: VirtualAccount, positions: List[PaperPosition], prices: Dict[str, float], timestamp_utc: Optional[str] = None) -> VirtualAccount:
    total_market_value = 0.0
    total_unrealized_pnl = 0.0

    for pos in positions:
        market_price = prices.get(pos.symbol, pos.market_price)
        if market_price is None:
            continue

        pos.market_price = market_price
        pos.market_value = pos.quantity * market_price

        if pos.side == "LONG" or getattr(pos.side, "value", str(pos.side)) == "LONG":
            pos.unrealized_pnl = (market_price - pos.average_price) * pos.quantity

        total_market_value += pos.market_value
        total_unrealized_pnl += pos.unrealized_pnl

    account.unrealized_pnl = total_unrealized_pnl
    account.equity = account.cash + total_market_value
    account.updated_at_utc = timestamp_utc or datetime.now(timezone.utc).isoformat()

    validate_virtual_account(account)
    return account

def apply_cash_delta(account: VirtualAccount, amount: float, allow_negative_cash: bool = False) -> VirtualAccount:
    new_cash = account.cash + amount
    if not allow_negative_cash and new_cash < 0:
        raise ValueError(f"Insufficient cash. Current: {account.cash}, Required: {-amount}")

    account.cash = new_cash
    account.updated_at_utc = datetime.now(timezone.utc).isoformat()

    validate_virtual_account(account)
    return account

def virtual_account_summary(account: VirtualAccount) -> Dict[str, Any]:
    return {
        "account_id": account.account_id,
        "name": account.name,
        "status": account.status.value if hasattr(account.status, 'value') else account.status,
        "cash": round(account.cash, 2),
        "equity": round(account.equity, 2),
        "realized_pnl": round(account.realized_pnl, 2),
        "unrealized_pnl": round(account.unrealized_pnl, 2),
        "updated_at_utc": account.updated_at_utc
    }

def virtual_account_to_text(account: VirtualAccount) -> str:
    lines = [
        "--- VIRTUAL ACCOUNT ---",
        f"ID: {account.account_id} | Name: {account.name}",
        f"Status: {account.status.value if hasattr(account.status, 'value') else account.status}",
        f"Cash: ${account.cash:,.2f}",
        f"Equity: ${account.equity:,.2f}",
        f"Realized PnL: ${account.realized_pnl:,.2f}",
        f"Unrealized PnL: ${account.unrealized_pnl:,.2f}"
    ]
    return "\n".join(lines)
