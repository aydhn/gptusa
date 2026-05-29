import pytest
import argparse
from usa_signal_bot.app.cli import phase126_regime_foundation_info, phase126_regime_taxonomy_info

def test_phase126_regime_foundation_info(capsys):
    phase126_regime_foundation_info(None)
    out, err = capsys.readouterr()
    assert "USA Signal Bot - Phase 126" in out
    assert "NOT an active paper trading phase" in out

def test_phase126_regime_taxonomy_info(capsys):
    class Args:
        write = False
    phase126_regime_taxonomy_info(Args())
    out, err = capsys.readouterr()
    assert "Taxonomy ID" in out
    assert "unknown_regime" in out


def test_phase130_market_behavior_info():
    import sys
    from io import StringIO
    from usa_signal_bot.app.cli import get_parser
    parser = get_parser()
    args = parser.parse_args(["market-behavior-info"])

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        args.func(args)
    finally:
        sys.stdout = old_stdout

    output = mystdout.getvalue()
    assert "Phase 130" in output
    assert "NOT an active paper trading phase" in output
