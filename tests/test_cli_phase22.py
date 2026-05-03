import pytest
import sys
from pathlib import Path
from usa_signal_bot.app.cli import do_signal_quality_summary, do_strategy_run_confluence

# Rather than calling main() which triggers logging / initialization / sys.exit things that
# conflict with pytest environment patching, let's call the newly defined CLI handlers directly.

def test_cli_signal_quality_summary_empty(capsys, tmp_path):
    from usa_signal_bot.core.config import load_app_config
    cfg = load_app_config()
    cfg.data.root_dir = str(tmp_path)

    class Args:
        pass

    do_signal_quality_summary(Args(), cfg)
    out, err = capsys.readouterr()
    assert "Reports directory does not exist" in out or "No reports found" in out

def test_cli_strategy_run_confluence_no_features(capsys, tmp_path):
    from usa_signal_bot.core.config import load_app_config
    cfg = load_app_config()
    cfg.data.root_dir = str(tmp_path)

    class Args:
        strategies = "test_strat"
        symbols = "AAPL"
        timeframes = "1d"
        write = False

    try:
        do_strategy_run_confluence(Args(), cfg)
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert "Running strategies:" in out
