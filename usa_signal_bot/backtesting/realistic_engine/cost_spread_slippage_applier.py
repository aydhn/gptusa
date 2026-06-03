import datetime
import pandas as pd
from typing import Dict, Any, List, Tuple
from .phase147_models import (
    SimulatedFillRecord, CostLedgerRecord, CostApplicationKind,
    create_cost_ledger_record_id, SimulatedFillKind
)

def estimate_total_cost_for_fill(fill: SimulatedFillRecord, transaction_cost_payload: Dict[str, Any] | None = None, commission_payload: Dict[str, Any] | None = None, spread_payload: Dict[str, Any] | None = None, slippage_payload: Dict[str, Any] | None = None) -> CostLedgerRecord:
    notional = fill.simulated_notional_before_costs or 0.0

    # Simple defaults if no payload
    t_cost = notional * 0.0001
    c_cost = 0.0
    sp_cost = notional * 0.0002
    sl_cost = notional * 0.0003

    if fill.fill_kind != SimulatedFillKind.FULL_SIMULATED_FILL and fill.fill_kind != SimulatedFillKind.PARTIAL_SIMULATED_FILL:
        t_cost = c_cost = sp_cost = sl_cost = 0.0

    tot = t_cost + c_cost + sp_cost + sl_cost

    return CostLedgerRecord(
        cost_id=create_cost_ledger_record_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        run_id=fill.run_id,
        fill_id=fill.fill_id,
        symbol=fill.symbol,
        timestamp=fill.fill_timestamp,
        cost_kind=CostApplicationKind.TOTAL_SIMULATED_COST,
        transaction_cost_amount=t_cost,
        commission_amount=c_cost,
        spread_cost_amount=sp_cost,
        slippage_cost_amount=sl_cost,
        total_cost_amount=tot,
        cost_bps_effective=(tot / notional * 10000) if notional > 0 else 0.0,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def apply_cost_spread_slippage_to_fills(fills: List[SimulatedFillRecord], transaction_cost_payload: Dict[str, Any] | None = None, commission_payload: Dict[str, Any] | None = None, spread_payload: Dict[str, Any] | None = None, slippage_payload: Dict[str, Any] | None = None) -> Tuple[List[SimulatedFillRecord], List[CostLedgerRecord]]:
    costs = []
    new_fills = []
    for f in fills:
        c = estimate_total_cost_for_fill(f, transaction_cost_payload, commission_payload, spread_payload, slippage_payload)
        costs.append(c)
        f_copy = SimulatedFillRecord(**f.__dict__)
        if f_copy.simulated_fill_price_before_costs and f_copy.simulated_filled_quantity > 0:
            # simple mock application
            f_copy.simulated_notional_after_costs = f_copy.simulated_notional_before_costs + c.total_cost_amount
            f_copy.simulated_fill_price_after_costs = f_copy.simulated_notional_after_costs / f_copy.simulated_filled_quantity
        new_fills.append(f_copy)
    return new_fills, costs

def validate_cost_ledger(items: List[CostLedgerRecord]) -> List[str]:
    return []

def cost_ledger_to_dataframe(items: List[CostLedgerRecord]) -> pd.DataFrame:
    return pd.DataFrame([c.__dict__ for c in items])

def cost_application_summary(items: List[CostLedgerRecord]) -> Dict[str, Any]:
    return {"cost_record_count": len(items)}
