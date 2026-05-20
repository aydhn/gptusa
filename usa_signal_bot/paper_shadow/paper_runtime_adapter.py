from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, ShadowPortfolioState, ShadowRehearsalSession,
    ShadowPosition, create_shadow_portfolio_id, get_utc_now_str
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context

def build_shadow_context_from_paper_runtime_snapshot(snapshot: Dict[str, Any]) -> ShadowSimulationContext:
    context = build_mock_shadow_simulation_context(starting_equity_usd=snapshot.get("equity", 100000.0))
    context.metadata["source"] = "paper_runtime_snapshot"
    return context

def copy_paper_snapshot_to_shadow_portfolio(snapshot: Dict[str, Any]) -> ShadowPortfolioState:
    positions = []
    for p in snapshot.get("positions", []):
        positions.append(ShadowPosition(
            symbol=p.get("symbol", "UNKNOWN"),
            quantity=p.get("quantity", 0.0),
            avg_price=p.get("avg_price", 0.0),
            market_price=p.get("market_price", 0.0),
            market_value_usd=p.get("market_value", 0.0),
            unrealized_pnl_usd=p.get("unrealized_pnl", 0.0),
            realized_pnl_usd=p.get("realized_pnl", 0.0),
            strategy_name=p.get("strategy_name")
        ))

    return ShadowPortfolioState(
        portfolio_id=create_shadow_portfolio_id("copy"),
        created_at_utc=get_utc_now_str(),
        equity_usd=snapshot.get("equity", 0.0),
        cash_usd=snapshot.get("cash", 0.0),
        positions=positions,
        gross_exposure_usd=snapshot.get("gross_exposure", 0.0),
        net_exposure_usd=snapshot.get("net_exposure", 0.0),
        realized_pnl_usd=snapshot.get("realized_pnl", 0.0),
        unrealized_pnl_usd=snapshot.get("unrealized_pnl", 0.0),
        warnings=[],
        errors=[]
    )

def validate_no_paper_runtime_mutation(payload_before: Dict[str, Any], payload_after: Dict[str, Any]) -> List[str]:
    errors = []
    if payload_before != payload_after:
        errors.append("Paper runtime mutation detected.")
    return errors

def attach_shadow_preview_to_paper_analytics(payload: Dict[str, Any], session: ShadowRehearsalSession) -> Dict[str, Any]:
    payload["shadow_preview"] = {
        "session_id": session.session_id,
        "simulated_pnl": session.pnl_snapshots[-1].total_pnl_usd if session.pnl_snapshots else 0.0
    }
    return payload

def paper_runtime_shadow_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"PaperRuntimeAdapter({payload})"
