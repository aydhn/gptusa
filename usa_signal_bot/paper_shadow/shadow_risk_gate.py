from typing import Any

from usa_signal_bot.core.enums import ShadowOrderIntentStatus
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowOrderIntent,
    ShadowPortfolioState,
    ShadowSimulationContext,
    ShadowRiskGateStatus
)
from usa_signal_bot.paper_shadow.shadow_order_intent import validate_shadow_order_intents_safe

def evaluate_shadow_order_risk(intent: ShadowOrderIntent, portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> ShadowRiskGateStatus:
    if validate_shadow_order_intents_safe([intent]):
        return ShadowRiskGateStatus.BLOCKED

    if intent.notional_usd <= 0 or intent.quantity <= 0:
        return ShadowRiskGateStatus.INSUFFICIENT_DATA

    pct_equity = (intent.notional_usd / portfolio.equity_usd) * 100 if portfolio.equity_usd > 0 else 100

    if pct_equity > 5.0:
        return ShadowRiskGateStatus.WARNING

    return ShadowRiskGateStatus.PASS

def apply_shadow_risk_gates(intents: list[ShadowOrderIntent], portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> list[ShadowOrderIntent]:
    processed = []
    for intent in intents:
        status = evaluate_shadow_order_risk(intent, portfolio, context)
        if status == ShadowRiskGateStatus.PASS:
            intent.status = ShadowOrderIntentStatus.RISK_APPROVED
        elif status == ShadowRiskGateStatus.WARNING:
            intent.status = ShadowOrderIntentStatus.RISK_APPROVED
            intent.warnings.append("Risk Gate Warning")
        elif status == ShadowRiskGateStatus.BLOCKED:
            intent.status = ShadowOrderIntentStatus.BLOCKED
            intent.errors.append("Blocked by Risk Gate")
        elif status == ShadowRiskGateStatus.FAIL:
            intent.status = ShadowOrderIntentStatus.RISK_REJECTED
            intent.errors.append("Failed Risk Gate")
        elif status == ShadowRiskGateStatus.INSUFFICIENT_DATA:
            intent.status = ShadowOrderIntentStatus.RISK_REJECTED
            intent.errors.append("Insufficient data for Risk Gate")

        processed.append(intent)
    return processed

def shadow_risk_gate_warnings(intent: ShadowOrderIntent, portfolio: ShadowPortfolioState) -> list[str]:
    warnings = []
    pct_equity = (intent.notional_usd / portfolio.equity_usd) * 100 if portfolio.equity_usd > 0 else 100
    if pct_equity > 5.0:
        warnings.append(f"Notional value is > 5% of equity ({pct_equity:.2f}%)")
    return warnings

def shadow_risk_gate_summary(intents: list[ShadowOrderIntent]) -> dict[str, Any]:

    return {
        "total": len(intents),
        "approved": sum(1 for i in intents if i.status == ShadowOrderIntentStatus.RISK_APPROVED),
        "rejected": sum(1 for i in intents if i.status == ShadowOrderIntentStatus.RISK_REJECTED),
        "blocked": sum(1 for i in intents if i.status == ShadowOrderIntentStatus.BLOCKED)
    }

def shadow_risk_gate_to_text(payload: dict[str, Any]) -> str:
    text = "Shadow Risk Gate Summary\n"
    text += f"Total Evaluated: {payload.get('total', 0)}\n"
    text += f"Approved: {payload.get('approved', 0)}\n"
    text += f"Rejected: {payload.get('rejected', 0)}\n"
    text += f"Blocked: {payload.get('blocked', 0)}\n"
    text += "Note: Risk PASS does not constitute live trading approval."
    return text
