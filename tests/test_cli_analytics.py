import pytest
from usa_signal_bot.app.cli import main

def test_cli_analytics_info(capsys):
    with pytest.raises(SystemExit) as exc:
        import sys
        sys.argv = ["usa_signal_bot", "paper-analytics-info"]
        main()


    pass
