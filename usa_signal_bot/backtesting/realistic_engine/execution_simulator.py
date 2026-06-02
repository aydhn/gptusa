import datetime
import pandas as pd
from typing import Dict, Any, List, Tuple
from .phase147_models import (
    BacktestRunConfig, ResearchDecisionStream, PriceEventStream,
    PriceEvent, ResearchDecisionRecord, SimulatedFillRecord,
    SimulatedFillKind, create_simulated_fill_record_id, ResearchDecisionKind
)

def choose_fill_timestamp(decision_timestamp: str, available_timestamps: List[str]) -> str | None:
    for ts in available_timestamps:
        if ts > decision_timestamp:
            return ts
    return None

def choose_reference_price(event: PriceEvent, config: BacktestRunConfig) -> float | None:
    if config.time_model_kind.name == "BAR_CLOSE_TO_NEXT_OPEN":
        return event.open_price
    return event.close_price

def simulate_fill_for_decision(decision: ResearchDecisionRecord, price_lookup: Dict[Tuple[str, str], PriceEvent], available_timestamps: List[str], config: BacktestRunConfig) -> SimulatedFillRecord:
    fill_ts = choose_fill_timestamp(decision.timestamp, available_timestamps)
    kind = SimulatedFillKind.FULL_SIMULATED_FILL
    price = None
    if not fill_ts:
        kind = SimulatedFillKind.NO_SIMULATED_FILL_MISSING_PRICE
    else:
        evt = price_lookup.get((decision.symbol, fill_ts))
        if evt:
            price = choose_reference_price(evt, config)
            if price is None:
                kind = SimulatedFillKind.NO_SIMULATED_FILL_MISSING_PRICE
        else:
            kind = SimulatedFillKind.NO_SIMULATED_FILL_MISSING_PRICE

    if decision.decision_kind in [ResearchDecisionKind.NO_ACTION_METADATA, ResearchDecisionKind.HOLD_EXPOSURE_METADATA]:
        kind = SimulatedFillKind.NO_SIMULATED_FILL_CONTRACT_ONLY

    return SimulatedFillRecord(
        fill_id=create_simulated_fill_record_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        run_id=config.config_id,
        symbol=decision.symbol,
        decision_timestamp=decision.timestamp,
        fill_timestamp=fill_ts or decision.timestamp,
        fill_kind=kind,
        exposure_side=decision.exposure_side,
        requested_quantity=1.0, # Will be scaled by allocator
        simulated_filled_quantity=1.0 if kind == SimulatedFillKind.FULL_SIMULATED_FILL else 0.0,
        reference_price=price,
        simulated_fill_price_before_costs=price,
        simulated_fill_price_after_costs=price,
        simulated_notional_before_costs=price if price else 0.0,
        simulated_notional_after_costs=price if price else 0.0,
        liquidity_blocked=False,
        missing_price_blocked=(kind == SimulatedFillKind.NO_SIMULATED_FILL_MISSING_PRICE),
        partial_fill=False,
        simulated_only=True,
        real_order_created=False,
        broker_execution_used=False,
        paper_state_mutated=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def run_simulated_execution(config: BacktestRunConfig, decisions: ResearchDecisionStream, price_events: PriceEventStream, market_contract: Dict[str, Any] | None = None) -> List[SimulatedFillRecord]:
    price_lookup = {(e.symbol, e.timestamp): e for e in price_events.events}
    available_timestamps = sorted(list(set(e.timestamp for e in price_events.events)))

    fills = []
    for dec in decisions.records:
        fills.append(simulate_fill_for_decision(dec, price_lookup, available_timestamps, config))
    return fills

def validate_simulated_fills(items: List[SimulatedFillRecord]) -> List[str]:
    errors = []
    for f in items:
        if f.real_order_created: errors.append(f"real_order_created is true for {f.fill_id}")
        if f.broker_execution_used: errors.append(f"broker_execution_used is true for {f.fill_id}")
        if f.paper_state_mutated: errors.append(f"paper_state_mutated is true for {f.fill_id}")
    return errors

def simulated_fills_to_dataframe(items: List[SimulatedFillRecord]) -> pd.DataFrame:
    return pd.DataFrame([f.__dict__ for f in items])
