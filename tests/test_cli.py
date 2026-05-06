from usa_signal_bot.app.cli import cmd_alert_info, cmd_alert_policy_list, cmd_alert_policy_preview
from usa_signal_bot.core.config import load_app_config

class DummyContext:
    def __init__(self):
        self.config = load_app_config()

class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_alert_info():
    ctx = DummyContext()
    assert cmd_alert_info(ctx, DummyArgs()) == 0

def test_alert_policy_list():
    ctx = DummyContext()
    assert cmd_alert_policy_list(ctx, DummyArgs()) == 0

def test_alert_policy_preview():
    ctx = DummyContext()
    assert cmd_alert_policy_preview(ctx, DummyArgs(scope="scan")) == 0
