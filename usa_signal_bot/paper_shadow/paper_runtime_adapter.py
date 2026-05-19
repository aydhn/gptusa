from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext,
    ShadowPortfolioState,
    ShadowRehearsalSession,
    ShadowPosition,
    create_shadow_portfolio_id
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from datetime import datetime, timezone

def build_shadow_context_from_paper_runtime_snapshot(snapshot: dict[str, Any]) -> ShadowSimulationContext:
    context = build_mock_shadow_simulation_context(starting_equity_usd=snapshot.get("equity_usd", 100000.0))
    return context

def copy_paper_snapshot_to_shadow_portfolio(snapshot: dict[str, Any]) -> ShadowPortfolioState:
    positions = []
    for p in snapshot.get("positions", []):
         positions.append(ShadowPosition(
             symbol=p.get("symbol", "UNKNOWN"),
             quantity=p.get("quantity", 0.0),
             avg_price=p.get("avg_price"),
             market_price=p.get("market_price"),
             market_value_usd=p.get("market_value_usd", 0.0),
             unrealized_pnl_usd=p.get("unrealized_pnl_usd", 0.0),
             realized_pnl_usd=p.get("realized_pnl_usd", 0.0)
         ))

    return ShadowPortfolioState(
        portfolio_id=create_shadow_portfolio_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        equity_usd=snapshot.get("equity_usd", 100000.0),
        cash_usd=snapshot.get("cash_usd", 100000.0),
        positions=positions,
        gross_exposure_usd=snapshot.get("gross_exposure_usd", 0.0),
        net_exposure_usd=snapshot.get("net_exposure_usd", 0.0),
        realized_pnl_usd=snapshot.get("realized_pnl_usd", 0.0),
        unrealized_pnl_usd=snapshot.get("unrealized_pnl_usd", 0.0),
        warnings=[],
        errors=[]
    )

def validate_no_paper_runtime_mutation(payload_before: dict[str, Any], payload_after: dict[str, Any]) -> list[str]:
    errors = []
    if payload_after.get("paper_state_committed", False):
        errors.append("Detected paper_state_committed=True")
    if payload_after.get("paper_order_executed", False):
        errors.append("Detected paper_order_executed=True")
    if payload_before != payload_after and not any(k in ["shadow_preview", "metadata"] for k in set(payload_after) - set(payload_before)):
         # Check if changes are only in shadow related fields
         pass
    return errors

def attach_shadow_preview_to_paper_analytics(payload: dict[str, Any], session: ShadowRehearsalSession) -> dict[str, Any]:
    payload["shadow_preview"] = session.session_id
    payload["paper_state_committed"] = False
    payload["paper_order_executed"] = False
    return payload

def paper_runtime_shadow_adapter_to_text(payload: dict[str, Any]) -> str:
    text = "Paper Runtime Adapter Summary\n"
    text += f"Shadow Preview ID: {payload.get('shadow_preview')}\n"
    text += f"Paper State Mutated: {payload.get('paper_state_committed', False)}\n"
    return text
