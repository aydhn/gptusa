import datetime
import pandas as pd
from typing import Dict, Any, List
from .phase147_models import (
    BacktestRunConfig, SimulatedFillRecord, PriceEventStream,
    ExposureStateRecord, create_exposure_state_record_id, PriceEvent
)

def update_exposure_state(previous_state: ExposureStateRecord | None, fill: SimulatedFillRecord | None, event: PriceEvent, config: BacktestRunConfig) -> ExposureStateRecord:
    qty = previous_state.simulated_quantity if previous_state else 0.0
    cash = previous_state.simulated_cash if previous_state else config.initial_cash

    if fill and fill.simulated_filled_quantity > 0:
        if fill.exposure_side.name == "LONG_ONLY_RESEARCH":
            qty += fill.simulated_filled_quantity
            cash -= fill.simulated_notional_after_costs or 0.0

    mkt_val = qty * (event.close_price or 0.0)
    eq = cash + mkt_val

    return ExposureStateRecord(
        state_id=create_exposure_state_record_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        run_id=config.config_id,
        symbol=event.symbol,
        timestamp=event.timestamp,
        exposure_side=config.exposure_side,
        simulated_quantity=qty,
        simulated_cash=cash,
        simulated_market_value=mkt_val,
        simulated_equity=eq,
        simulated_cost_basis=None,
        simulated_unrealized_return=None,
        state_valid=True,
        not_live_position=True,
        not_portfolio_allocation=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_exposure_timeline(config: BacktestRunConfig, fills: List[SimulatedFillRecord], price_events: PriceEventStream) -> List[ExposureStateRecord]:
    fills_by_time_sym = {(f.symbol, f.fill_timestamp): f for f in fills}

    states = []
    prev_states = {}

    for evt in price_events.events:
        fill = fills_by_time_sym.get((evt.symbol, evt.timestamp))
        prev = prev_states.get(evt.symbol)

        new_state = update_exposure_state(prev, fill, evt, config)
        states.append(new_state)
        prev_states[evt.symbol] = new_state

    return states

def validate_exposure_timeline(items: List[ExposureStateRecord]) -> List[str]:
    return []

def exposure_timeline_to_dataframe(items: List[ExposureStateRecord]) -> pd.DataFrame:
    return pd.DataFrame([s.__dict__ for s in items])

def exposure_timeline_summary(items: List[ExposureStateRecord]) -> Dict[str, Any]:
    return {"state_count": len(items)}
