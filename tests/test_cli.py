from click.testing import CliRunner
from usa_signal_bot.app.cli import cli
from pathlib import Path
import tempfile
import pandas as pd

def test_core_indicators_info():
    runner = CliRunner()
    result = runner.invoke(cli, ['core-indicators-info'])
    assert result.exit_code == 0
    assert "NOT activation" in result.output
