import datetime
from typing import Dict, Any, List
import pandas as pd
from .phase147_models import SimulationClock, SimulationClockKind, create_simulation_clock_id

def build_simulation_clock(price_bars: pd.DataFrame) -> SimulationClock:
    timestamps = sorted(price_bars["timestamp"].unique().tolist())
    return SimulationClock(
        clock_id=create_simulation_clock_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        clock_kind=SimulationClockKind.DAILY_BAR_CLOCK,
        timestamps=timestamps,
        event_count=len(timestamps),
        timezone_policy="UTC",
        deterministic=True,
        clock_valid=True,
        no_scheduler=True,
        no_daemon=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_simulation_clock(clock: SimulationClock) -> List[str]:
    errors = []
    if not clock.deterministic: errors.append("Clock must be deterministic")
    if not clock.no_scheduler: errors.append("no_scheduler must be true")
    if not clock.no_daemon: errors.append("no_daemon must be true")
    return errors

def simulation_clock_summary(clock: SimulationClock) -> Dict[str, Any]:
    return {"event_count": clock.event_count}

def simulation_clock_to_text(clock: SimulationClock, limit: int = 300) -> str:
    return f"SimulationClock {clock.clock_id} with {clock.event_count} events"
