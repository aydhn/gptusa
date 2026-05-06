from usa_signal_bot.notifications.notification_adapters import alert_context_from_scan_result, alert_context_from_candidate_summary, build_policy_driven_scan_notifications
from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest
from usa_signal_bot.core.enums import RuntimeRunStatus, RuntimeMode, ScanScope, AlertPolicyScope
from usa_signal_bot.strategies.candidate_selection import SelectedCandidate

def get_dummy_scan_result():
    req = MarketScanRequest("test", RuntimeMode.DRY_RUN, ScanScope.SMALL_TEST_SET)
    res = MarketScanResult("run1", "now", req, RuntimeRunStatus.COMPLETED)
    res.candidate_count = 5
    return res

def test_alert_context_from_scan_result():
    res = get_dummy_scan_result()
    ctx = alert_context_from_scan_result(res)
    assert ctx.run_id == "run1"
    assert ctx.scope == AlertPolicyScope.SCAN
    assert ctx.payload["status"].upper() == "COMPLETED"
    assert ctx.payload["candidate_count"] == 5

def test_alert_context_from_candidate_summary():
    cand1 = SelectedCandidate("AAPL", "s1", "cand1", 1.0, 1.0, 100, "now")
    ctx = alert_context_from_candidate_summary("run2", [cand1])
    assert ctx.run_id == "run2"
    assert ctx.scope == AlertPolicyScope.CANDIDATE
    assert ctx.payload["candidate_count"] == 1
    assert "AAPL" in ctx.payload["symbols"]

def test_build_policy_driven_scan_notifications():
    res = get_dummy_scan_result()
    eval_res, msgs = build_policy_driven_scan_notifications(res)
    assert eval_res.run_id == "run1"
    # Even if no messages generated based on defaults, the process shouldn't crash
    assert isinstance(msgs, list)
