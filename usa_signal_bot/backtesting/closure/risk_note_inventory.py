from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestRiskNote, BacktestBandPhase, BacktestRiskNoteKind,
    BacktestClosureRiskFlag
)

def build_default_backtest_risk_notes() -> list[BacktestRiskNote]:
    return [
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.LOOKAHEAD_BIAS_NOTE,
            title="Lookahead Bias Limitation",
            note="Backtest assumes no lookahead bias, but residual risk remains.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.SURVIVORSHIP_BIAS_NOTE,
            title="Survivorship Bias Limitation",
            note="Universe selection may exhibit survivorship bias.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.COST_MODEL_NOTE,
            title="Cost Model Assumption",
            note="Transaction costs and slippage are approximations.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.LIQUIDITY_NOTE,
            title="Liquidity Constraint",
            note="Assumes sufficient market depth which may not hold in live trading.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.WALK_FORWARD_STABILITY_NOTE,
            title="Walk-Forward Stability",
            note="Historical stability does not guarantee future stability.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.STRESS_ROBUSTNESS_NOTE,
            title="Stress Test Limitations",
            note="Stress scenarios cannot cover all possible market shocks.",
            severity="WARNING"
        ),
        BacktestRiskNote(
            note_kind=BacktestRiskNoteKind.HANDOFF_LIMITATION_NOTE,
            title="Research-Only Handoff",
            note="These artifacts are for research only and do not constitute deployment approval or investment advice.",
            severity="CRITICAL"
        )
    ]

def build_backtest_risk_note_inventory(payloads: dict[str, dict[str, Any]]) -> list[BacktestRiskNote]:
    return build_default_backtest_risk_notes()

def validate_backtest_risk_note_inventory(items: list[BacktestRiskNote]) -> list[str]:
    errors = []
    required_notes = ["Lookahead Bias Limitation", "Survivorship Bias Limitation", "Cost Model Assumption", "Liquidity Constraint", "Walk-Forward Stability", "Stress Test Limitations", "Research-Only Handoff"]
    titles = [n.title for n in items]
    for req in required_notes:
        if req not in titles:
            errors.append(f"Missing required risk note: {req}")
    for item in items:
        if not item.not_investment_advice:
            errors.append(f"Risk note {item.title} flagged as investment advice")
    return errors

def risk_note_inventory_summary(items: list[BacktestRiskNote]) -> dict[str, Any]:
    return {"count": len(items)}

def risk_note_inventory_to_text(items: list[BacktestRiskNote], limit: int = 300) -> str:
    return f"Risk Note Inventory: {len(items)} notes"
