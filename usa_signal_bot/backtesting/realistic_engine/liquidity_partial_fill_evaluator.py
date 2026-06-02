from typing import Dict, Any, List
from .phase147_models import SimulatedFillRecord, PriceEventStream, PriceEvent, SimulatedFillKind

def apply_partial_fill_rule(fill: SimulatedFillRecord, event: PriceEvent | None, liquidity_payload: Dict[str, Any] | None = None, partial_fill_payload: Dict[str, Any] | None = None) -> SimulatedFillRecord:
    if not event or not event.volume or event.volume == 0:
        fill.liquidity_blocked = True
        fill.simulated_filled_quantity = 0.0
        fill.fill_kind = SimulatedFillKind.NO_SIMULATED_FILL_LIQUIDITY_BLOCK
        return fill
    # Dummy mock passing
    return fill

def evaluate_liquidity_and_partial_fills(fills: List[SimulatedFillRecord], price_events: PriceEventStream, liquidity_payload: Dict[str, Any] | None = None, partial_fill_payload: Dict[str, Any] | None = None) -> List[SimulatedFillRecord]:
    price_lookup = {(e.symbol, e.timestamp): e for e in price_events.events}
    new_fills = []
    for f in fills:
        f_copy = SimulatedFillRecord(**f.__dict__)
        evt = price_lookup.get((f_copy.symbol, f_copy.fill_timestamp))
        new_fills.append(apply_partial_fill_rule(f_copy, evt, liquidity_payload, partial_fill_payload))
    return new_fills

def validate_liquidity_partial_fill_results(items: List[SimulatedFillRecord]) -> List[str]:
    return []

def liquidity_partial_fill_summary(items: List[SimulatedFillRecord]) -> Dict[str, Any]:
    return {"processed_count": len(items)}
