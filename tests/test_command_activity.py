from usa_signal_bot.observability.command_activity import create_command_activity_record, complete_command_activity
from usa_signal_bot.core.enums import OperationalMetricStatus

def test_command_activity():
    c = create_command_activity_record("test")
    complete_command_activity(c, exit_code=0)
    assert c.status == OperationalMetricStatus.OK
    assert c.duration_seconds is not None
