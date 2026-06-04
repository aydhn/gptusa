import datetime
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    ScenarioReplayResult,
    ScenarioPathPoint,
    ScenarioDrawdownDiagnostic,
    create_scenario_drawdown_diagnostic_id
)

def build_scenario_drawdown_diagnostics(results: list[ScenarioReplayResult]) -> list[ScenarioDrawdownDiagnostic]:
    diags = []
    for r in results:
        min_eq = min([p.stressed_equity for p in r.path_points if p.stressed_equity is not None], default=r.final_stressed_equity)
        dur = estimate_drawdown_duration(r.path_points)
        rec = r.final_stressed_equity is not None and min_eq is not None and r.final_stressed_equity > min_eq * 1.05

        diags.append(ScenarioDrawdownDiagnostic(
            diagnostic_id=create_scenario_drawdown_diagnostic_id(),
            created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
            scenario_id=r.scenario_id,
            max_drawdown=r.stressed_max_drawdown,
            min_equity=min_eq,
            drawdown_duration_approx=dur,
            recovery_detected=rec,
            diagnostic_notes=[],
            diagnostic_valid=True,
            not_investment_advice=True,
            research_data_only=True,
            warnings=[], errors=[], risk_flags=[], metadata={}
        ))
    return diags

def estimate_drawdown_duration(points: list[ScenarioPathPoint]) -> int | None:
    max_dur = 0
    curr_dur = 0
    peak = 0

    for p in points:
        if p.stressed_equity is None:
            continue
        if p.stressed_equity > peak:
            peak = p.stressed_equity
            curr_dur = 0
        else:
            curr_dur += 1
            if curr_dur > max_dur:
                max_dur = curr_dur
    return max_dur
