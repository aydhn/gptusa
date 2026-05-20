from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowOrderIntent, ShadowPortfolioState, ShadowSimulationContext
)
from usa_signal_bot.core.enums import ShadowRiskGateStatus, ShadowOrderIntentStatus

def evaluate_shadow_order_risk(intent: ShadowOrderIntent, portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> ShadowRiskGateStatus:
    if intent.is_real_order or intent.broker_destination is not None:
        return ShadowRiskGateStatus.BLOCKED

    if not intent.symbol or intent.limit_price is None:
        return ShadowRiskGateStatus.INSUFFICIENT_DATA

    if portfolio.equity_usd > 0 and intent.notional_usd > portfolio.equity_usd * 0.05:
        return ShadowRiskGateStatus.WARNING

    return ShadowRiskGateStatus.PASS

def apply_shadow_risk_gates(intents: List[ShadowOrderIntent], portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> List[ShadowOrderIntent]:
    for intent in intents:
        if intent.status in [ShadowOrderIntentStatus.BLOCKED, ShadowOrderIntentStatus.CANCELLED]:
            continue

        risk_status = evaluate_shadow_order_risk(intent, portfolio, context)
        if risk_status == ShadowRiskGateStatus.BLOCKED:
            intent.status = ShadowOrderIntentStatus.BLOCKED
            intent.errors.append("Blocked by risk gate.")
        elif risk_status == ShadowRiskGateStatus.INSUFFICIENT_DATA:
            intent.status = ShadowOrderIntentStatus.RISK_REJECTED
            intent.errors.append("Insufficient data for risk evaluation.")
        elif risk_status == ShadowRiskGateStatus.FAIL:
            intent.status = ShadowOrderIntentStatus.RISK_REJECTED
            intent.errors.append("Failed risk gate.")
        else:
            intent.status = ShadowOrderIntentStatus.RISK_APPROVED
            if risk_status == ShadowRiskGateStatus.WARNING:
                intent.warnings.append("Risk gate warning: oversize.")
    return intents

def shadow_risk_gate_warnings(intent: ShadowOrderIntent, portfolio: ShadowPortfolioState) -> List[str]:
    return intent.warnings

def shadow_risk_gate_summary(intents: List[ShadowOrderIntent]) -> Dict[str, Any]:
    return {
        "approved": sum(1 for i in intents if i.status == ShadowOrderIntentStatus.RISK_APPROVED),
        "rejected": sum(1 for i in intents if i.status == ShadowOrderIntentStatus.RISK_REJECTED),
        "blocked": sum(1 for i in intents if i.status == ShadowOrderIntentStatus.BLOCKED)
    }

def shadow_risk_gate_to_text(payload: Dict[str, Any]) -> str:
    return f"ShadowRiskGate(appr={payload['approved']}, rej={payload['rejected']}, blk={payload['blocked']})"
