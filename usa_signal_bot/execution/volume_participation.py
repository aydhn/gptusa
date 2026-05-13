from typing import Optional
from usa_signal_bot.core.enums import ExecutionRiskLevel
from usa_signal_bot.core.config_schema import VolumeParticipationConfig

def calculate_participation_rate_pct(order_notional_usd: float, avg_dollar_volume: float | None) -> float | None:
    if avg_dollar_volume is None or avg_dollar_volume <= 0:
        return None
    return (order_notional_usd / avg_dollar_volume) * 100.0

def classify_participation_risk(
    participation_rate_pct: float | None,
    config: VolumeParticipationConfig | None = None
) -> ExecutionRiskLevel:
    if participation_rate_pct is None:
        return ExecutionRiskLevel.UNKNOWN

    if config is None:
        config = VolumeParticipationConfig()

    if participation_rate_pct > config.critical_participation_pct:
        return ExecutionRiskLevel.CRITICAL
    if participation_rate_pct > config.high_participation_pct:
        return ExecutionRiskLevel.HIGH
    if participation_rate_pct > config.max_participation_pct:
        return ExecutionRiskLevel.MODERATE

    return ExecutionRiskLevel.LOW

def recommended_max_notional_from_adv(
    avg_dollar_volume: float | None,
    max_participation_pct: float = 1.0
) -> float | None:
    if avg_dollar_volume is None or avg_dollar_volume <= 0:
        return None
    return avg_dollar_volume * (max_participation_pct / 100.0)

def volume_participation_to_text(
    order_notional_usd: float,
    avg_dollar_volume: float | None,
    participation_rate_pct: float | None
) -> str:
    lines = [
        "Volume Participation Analysis:",
        f"  Order Notional: ${order_notional_usd:,.2f}",
        f"  ADV (Dollar): ${avg_dollar_volume:,.2f}" if avg_dollar_volume else "  ADV (Dollar): Unknown",
    ]

    if participation_rate_pct is not None:
        lines.append(f"  Participation Rate: {participation_rate_pct:.4f}%")
        risk = classify_participation_risk(participation_rate_pct)
        lines.append(f"  Risk Level: {risk.value}")
    else:
        lines.append("  Participation Rate: INSUFFICIENT DATA")

    lines.append("  Note: This does not guarantee a fill rate or market impact.")
    return "\n".join(lines)
