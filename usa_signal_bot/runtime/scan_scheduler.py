import datetime
import json
from pathlib import Path
from typing import List, Optional, Tuple

from usa_signal_bot.core.enums import RuntimeMode, ScanScope
from usa_signal_bot.runtime.runtime_models import (
    ScheduledScanPlan, MarketScanRequest, create_scheduled_scan_plan_id, scheduled_scan_plan_to_dict
)

def build_default_scheduled_scan_plan() -> ScheduledScanPlan:
    request = MarketScanRequest(
        run_name="scheduled_scan_default",
        mode=RuntimeMode.LOCAL_SCAN_LOOP,
        scope=ScanScope.LATEST_ELIGIBLE_UNIVERSE,
    )
    return ScheduledScanPlan(
        plan_id=create_scheduled_scan_plan_id(),
        enabled=True,
        name="default_plan",
        mode=RuntimeMode.SCHEDULE_PLAN_ONLY,
        interval_minutes=60,
        max_runs_per_day=8,
        market_hours_only=False,
        timezone="Europe/Istanbul",
        scan_request_template=request,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

def calculate_next_run_times(plan: ScheduledScanPlan, start_time_utc: Optional[str] = None, count: int = 5) -> List[str]:
    start = datetime.datetime.fromisoformat(start_time_utc) if start_time_utc else datetime.datetime.now(datetime.timezone.utc)
    times = []
    current = start
    for _ in range(count):
        current += datetime.timedelta(minutes=plan.interval_minutes)
        times.append(current.isoformat())
    return times

def should_run_now(plan: ScheduledScanPlan, now_utc: Optional[str] = None, runs_today: int = 0) -> Tuple[bool, str]:
    if not plan.enabled:
        return False, "Plan is disabled"
    if runs_today >= plan.max_runs_per_day:
        return False, f"Max runs per day ({plan.max_runs_per_day}) reached"

    # Very basic placeholder for market hours
    if plan.market_hours_only:
        now = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)
        if now.weekday() >= 5: # Sat, Sun
            return False, "Market is closed on weekends"
        # 14:30 to 21:00 UTC approx US market
        hour = now.hour
        minute = now.minute
        time_val = hour + minute / 60.0
        if time_val < 14.5 or time_val > 21.0:
            return False, "Outside of approximate US market hours (14:30-21:00 UTC)"

    return True, "Conditions met"

def scheduled_scan_plan_to_text(plan: ScheduledScanPlan) -> str:
    lines = [
        f"Plan ID: {plan.plan_id}",
        f"Name: {plan.name}",
        f"Enabled: {plan.enabled}",
        f"Interval: {plan.interval_minutes} minutes",
        f"Max Runs/Day: {plan.max_runs_per_day}",
        f"Market Hours Only: {plan.market_hours_only}",
    ]
    return "\n".join(lines)

def write_scheduled_scan_plan_json(path: Path, plan: ScheduledScanPlan) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(scheduled_scan_plan_to_dict(plan), f, indent=2)
    return path

def read_scheduled_scan_plan_json(path: Path) -> ScheduledScanPlan:
    with open(path, "r") as f:
        data = json.load(f)

    # Manual deserialization mapping
    req_data = data["scan_request_template"]
    request = MarketScanRequest(
        run_name=req_data["run_name"],
        mode=RuntimeMode(req_data["mode"]),
        scope=ScanScope(req_data["scope"]),
        symbols=req_data.get("symbols"),
        timeframes=req_data.get("timeframes", ["1d"]),
        provider_name=req_data.get("provider_name", "yfinance"),
        composite_set_name=req_data.get("composite_set_name", "core"),
        rule_strategy_set_name=req_data.get("rule_strategy_set_name", "basic_rules"),
        max_symbols=req_data.get("max_symbols"),
        refresh_data=req_data.get("refresh_data", False),
        write_outputs=req_data.get("write_outputs", True),
        dry_run=req_data.get("dry_run", False),
    )

    return ScheduledScanPlan(
        plan_id=data["plan_id"],
        enabled=data["enabled"],
        name=data["name"],
        mode=RuntimeMode(data["mode"]),
        interval_minutes=data["interval_minutes"],
        max_runs_per_day=data["max_runs_per_day"],
        market_hours_only=data["market_hours_only"],
        timezone=data["timezone"],
        scan_request_template=request,
        created_at_utc=data["created_at_utc"],
        metadata=data.get("metadata", {})
    )
