from usa_signal_bot.notifications.notification_adapters import notifications_from_scan_result
from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest
from usa_signal_bot.core.enums import RuntimeMode, ScanScope, RuntimeRunStatus

def test_notifications_from_scan_result():
    req = MarketScanRequest("test", RuntimeMode.DRY_RUN, ScanScope.SMALL_TEST_SET)
    res = MarketScanResult("run1", "now", req, RuntimeRunStatus.COMPLETED)

    msgs = notifications_from_scan_result(res)
    assert len(msgs) == 1
    assert msgs[0].notification_type.value == "SCAN_SUMMARY"
