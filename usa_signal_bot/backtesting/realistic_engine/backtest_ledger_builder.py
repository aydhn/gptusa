import datetime
import hashlib
from typing import Dict, Any, List
from .phase147_models import (
    SimulatedFillRecord, CostLedgerRecord, ExposureStateRecord,
    BacktestLedger, create_backtest_ledger_id
)

def compute_backtest_ledger_hash(ledger: BacktestLedger) -> str:
    data = f"{ledger.fill_count}_{ledger.cost_record_count}_{ledger.exposure_state_count}"
    return hashlib.sha256(data.encode()).hexdigest()

def build_backtest_ledger(run_id: str, fills: List[SimulatedFillRecord], costs: List[CostLedgerRecord], exposure_states: List[ExposureStateRecord]) -> BacktestLedger:
    l = BacktestLedger(
        ledger_id=create_backtest_ledger_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        run_id=run_id,
        fills=fills,
        costs=costs,
        exposure_states=exposure_states,
        fill_count=len(fills),
        cost_record_count=len(costs),
        exposure_state_count=len(exposure_states),
        ledger_hash=None,
        ledger_valid=True,
        simulated_only=True,
        real_order_created=False,
        broker_execution_used=False,
        paper_state_mutated=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    l.ledger_hash = compute_backtest_ledger_hash(l)
    return l

def validate_backtest_ledger(ledger: BacktestLedger) -> List[str]:
    errors = []
    if ledger.real_order_created: errors.append("real_order_created must be false")
    if ledger.broker_execution_used: errors.append("broker_execution_used must be false")
    if ledger.paper_state_mutated: errors.append("paper_state_mutated must be false")
    return errors

def backtest_ledger_summary(ledger: BacktestLedger) -> Dict[str, Any]:
    return {"fills": ledger.fill_count, "costs": ledger.cost_record_count, "states": ledger.exposure_state_count}

def backtest_ledger_to_text(ledger: BacktestLedger, limit: int = 300) -> str:
    return f"BacktestLedger {ledger.ledger_id} (fills: {ledger.fill_count}, costs: {ledger.cost_record_count})"
