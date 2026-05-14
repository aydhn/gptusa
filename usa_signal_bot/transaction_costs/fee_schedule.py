from typing import Any
from usa_signal_bot.transaction_costs.cost_models import FeeScheduleProxy, create_fee_schedule_id

def default_zero_commission_equity_fee_schedule() -> FeeScheduleProxy:
    """
    Returns a zero commission fee schedule proxy for US Equities.
    This is NOT an official broker fee schedule, but a local proxy for backtesting.
    """
    return FeeScheduleProxy(
        schedule_id=create_fee_schedule_id("zero_comm_proxy"),
        name="Zero Commission Proxy (US Equities)",
        commission_per_share=0.0,
        min_commission_usd=0.0,
        max_commission_pct_notional=1.0,
        regulatory_fee_bps_sell=0.02,   # SEC fee proxy
        taf_fee_per_share_sell=0.000166, # FINRA TAF proxy
        enabled=True,
        notes=[
            "This is NOT an official broker fee schedule.",
            "This is a local backtest/paper proxy.",
            "Regulatory fees are heuristics and may not match actual billing."
        ]
    )

def conservative_fee_schedule_proxy() -> FeeScheduleProxy:
    """
    Returns a conservative fee schedule proxy that assumes non-zero commissions
    to stress-test strategies.
    """
    return FeeScheduleProxy(
        schedule_id=create_fee_schedule_id("conservative_proxy"),
        name="Conservative Commission Proxy (US Equities)",
        commission_per_share=0.005,
        min_commission_usd=1.0,
        max_commission_pct_notional=1.0,
        regulatory_fee_bps_sell=0.02,
        taf_fee_per_share_sell=0.000166,
        enabled=True,
        notes=[
            "This is NOT an official broker fee schedule.",
            "This is a conservative local backtest/paper proxy.",
            "It deliberately penalizes trades more than typical free brokers."
        ]
    )

def load_fee_schedule_from_config(config_dict: dict[str, Any] | None = None) -> FeeScheduleProxy:
    if not config_dict:
        return default_zero_commission_equity_fee_schedule()

    fee_config = config_dict.get("fee_schedule_proxy", {})
    if not fee_config or not fee_config.get("enabled", True):
        return default_zero_commission_equity_fee_schedule()

    return FeeScheduleProxy(
        schedule_id=create_fee_schedule_id("config_proxy"),
        name="Configured Fee Schedule Proxy",
        commission_per_share=float(fee_config.get("commission_per_share", 0.0)),
        min_commission_usd=float(fee_config.get("min_commission_usd", 0.0)),
        max_commission_pct_notional=float(fee_config.get("max_commission_pct_notional", 1.0)) if fee_config.get("max_commission_pct_notional") is not None else None,
        regulatory_fee_bps_sell=float(fee_config.get("regulatory_fee_bps_sell", 0.02)),
        taf_fee_per_share_sell=float(fee_config.get("taf_fee_per_share_sell", 0.000166)),
        enabled=True,
        notes=[
            "Loaded from configuration.",
            "This is NOT an official broker fee schedule.",
            "This is a local backtest/paper proxy."
        ]
    )

def fee_schedule_to_text(schedule: FeeScheduleProxy) -> str:
    lines = [
        f"Fee Schedule Proxy: {schedule.name} (ID: {schedule.schedule_id})",
        f"  Commission per share: ${schedule.commission_per_share:.4f}",
        f"  Min commission: ${schedule.min_commission_usd:.2f}",
        f"  Max commission % notional: {schedule.max_commission_pct_notional if schedule.max_commission_pct_notional is not None else 'None'}",
        f"  Regulatory fee bps (sell): {schedule.regulatory_fee_bps_sell:.4f}",
        f"  TAF fee per share (sell): ${schedule.taf_fee_per_share_sell:.6f}",
        "  Notes:"
    ]
    for note in schedule.notes:
        lines.append(f"    - {note}")
    return "\n".join(lines)
