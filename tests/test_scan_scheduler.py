from usa_signal_bot.runtime.scan_scheduler import (
    build_default_scheduled_scan_plan, calculate_next_run_times,
    should_run_now, scheduled_scan_plan_to_text, write_scheduled_scan_plan_json, read_scheduled_scan_plan_json
)

def test_scan_scheduler(tmp_path):
    plan = build_default_scheduled_scan_plan()
    assert plan.interval_minutes == 60

    times = calculate_next_run_times(plan, start_time_utc="2024-01-01T00:00:00Z", count=3)
    assert len(times) == 3
    assert times[0] == "2024-01-01T01:00:00+00:00"

    should, msg = should_run_now(plan, now_utc="2024-01-01T15:00:00Z", runs_today=0)
    assert should is True

    should, msg = should_run_now(plan, now_utc="2024-01-01T15:00:00Z", runs_today=10)
    assert should is False

    text = scheduled_scan_plan_to_text(plan)
    assert "Plan ID" in text

    p = tmp_path / "plan.json"
    write_scheduled_scan_plan_json(p, plan)
    plan2 = read_scheduled_scan_plan_json(p)
    assert plan2.plan_id == plan.plan_id
