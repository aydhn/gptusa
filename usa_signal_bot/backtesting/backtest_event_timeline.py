from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    BacktestEventTimelineContract,
    create_backtest_event_timeline_contract_id
)
from usa_signal_bot.core.enums import BacktestTimeModelKind, BacktestFoundationRiskFlag

def build_default_backtest_event_timeline() -> BacktestEventTimelineContract:
    return BacktestEventTimelineContract(
        timeline_id=create_backtest_event_timeline_contract_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        time_model_kind=BacktestTimeModelKind.BAR_CLOSE_TO_NEXT_OPEN,
        bar_timestamp_policy="BAR_END_TIME",
        feature_available_time_policy="BAR_END_TIME",
        research_prediction_available_time_policy="BAR_END_TIME_PLUS_COMPUTE_DELAY",
        execution_decision_time_policy="BEFORE_NEXT_BAR_OPEN",
        fill_time_policy="NEXT_BAR_OPEN_OR_LATER",
        prevents_lookahead_bias=True,
        event_order=[
            "load_bar",
            "compute_features_asof",
            "read_research_prediction_asof",
            "form_research_backtest_decision_metadata",
            "apply_execution_assumption",
            "apply_cost_spread_slippage_assumption",
            "record_research_fill_metadata"
        ],
        timeline_valid=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_backtest_event_timeline(timeline: BacktestEventTimelineContract) -> list[str]:
    errors = []
    if not timeline.prevents_lookahead_bias:
        errors.append("prevents_lookahead_bias must be True")
    if not timeline.timeline_valid:
        errors.append("timeline_valid must be True")
    return errors

def backtest_event_timeline_summary(timeline: BacktestEventTimelineContract) -> dict[str, Any]:
    return {"valid": timeline.timeline_valid, "model": timeline.time_model_kind.value}

def backtest_event_timeline_to_text(timeline: BacktestEventTimelineContract, limit: int = 300) -> str:
    return f"EventTimeline(valid={timeline.timeline_valid}, prevents_lookahead={timeline.prevents_lookahead_bias})"
