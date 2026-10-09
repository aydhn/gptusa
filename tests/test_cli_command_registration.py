import argparse

from usa_signal_bot.app import cli


def test_all_registrars_register_without_conflicts():
    parser = cli.setup_parser()
    choices = set()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            choices |= set(action.choices)
    assert "backtest-closure-info" in choices
    assert "optimizer-prototype-info" in choices
    assert "portfolio-risk-info" in choices
    assert len(cli._command_registrars()) == len(set(cli._command_registrars()))


def test_backtest_closure_info_runs(capsys):
    args = cli.setup_parser().parse_args(["backtest-closure-info"])
    args.func(args)
    assert "Phase 152" in capsys.readouterr().out
