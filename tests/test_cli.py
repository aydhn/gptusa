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

def test_comparison_cli_commands():
    from usa_signal_bot.app.cli import cmd_comparison_info, cmd_comparison_summary, cmd_comparison_latest, cmd_comparison_validate
    from collections import namedtuple
    class DummyConfig:
        def __init__(self):
            self.data = namedtuple('Data', ['root_dir'])('/tmp')
            self.comparison = namedtuple('Comp', ['enabled', 'matching_tolerance_bars', 'write_comparison_reports'])(True, 1, True)
    class DummyContext:
        config = DummyConfig()

    class DummyArgs:
        pass

    assert cmd_comparison_info(DummyContext(), DummyArgs()) == 0
    assert cmd_comparison_summary(DummyContext(), DummyArgs()) == 0
    assert cmd_comparison_latest(DummyContext(), DummyArgs()) == 0

    args_validate = DummyArgs()
    args_validate.latest = True
    assert cmd_comparison_validate(DummyContext(), args_validate) in [0, 1] # 1 because missing file
