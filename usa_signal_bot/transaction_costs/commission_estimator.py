from typing import Any
from usa_signal_bot.core.enums import TransactionSide
from usa_signal_bot.transaction_costs.cost_models import FeeScheduleProxy

def estimate_commission_usd(quantity: float | None, notional_usd: float | None, schedule: FeeScheduleProxy) -> float:
    if not quantity or quantity <= 0:
        return schedule.min_commission_usd

    commission = quantity * schedule.commission_per_share
    commission = max(commission, schedule.min_commission_usd)

    if schedule.max_commission_pct_notional is not None and notional_usd and notional_usd > 0:
        max_comm = notional_usd * (schedule.max_commission_pct_notional / 100.0)
        commission = min(commission, max_comm)

    return commission

def estimate_regulatory_fee_proxy_usd(side: TransactionSide, notional_usd: float | None, quantity: float | None, schedule: FeeScheduleProxy) -> float:
    # Regulatory proxy is applied on sells and short covers typically, but for generic proxy we apply on SELL and SHORT
    if side not in [TransactionSide.SELL, TransactionSide.SHORT, TransactionSide.COVER]:
        return 0.0

    fee = 0.0
    if notional_usd and notional_usd > 0:
        # SEC fee proxy based on notional
        sec_fee = notional_usd * (schedule.regulatory_fee_bps_sell / 10000.0)
        fee += sec_fee

    if quantity and quantity > 0:
        # TAF proxy based on shares
        taf_fee = quantity * schedule.taf_fee_per_share_sell
        fee += taf_fee

    return fee

def estimate_total_fee_proxy_usd(side: TransactionSide, quantity: float | None, notional_usd: float | None, schedule: FeeScheduleProxy) -> dict[str, float]:
    if quantity is not None and quantity < 0:
        raise ValueError("Quantity cannot be negative")
    if notional_usd is not None and notional_usd < 0:
        raise ValueError("Notional USD cannot be negative")

    commission = estimate_commission_usd(quantity, notional_usd, schedule)
    regulatory = estimate_regulatory_fee_proxy_usd(side, notional_usd, quantity, schedule)

    return {
        "commission_usd": commission,
        "regulatory_fee_usd": regulatory,
        "total_fee_usd": commission + regulatory
    }

def fee_proxy_to_bps(total_fee_usd: float, notional_usd: float | None) -> float | None:
    if not notional_usd or notional_usd <= 0:
        return None
    return (total_fee_usd / notional_usd) * 10000.0

def commission_estimate_to_text(payload: dict[str, float]) -> str:
    lines = [
        "Fee Proxy Estimate:",
        f"  Commission: ${payload.get('commission_usd', 0.0):.4f}",
        f"  Regulatory Fee Proxy: ${payload.get('regulatory_fee_usd', 0.0):.4f}",
        f"  Total Fee Proxy: ${payload.get('total_fee_usd', 0.0):.4f}"
    ]
    return "\n".join(lines)
