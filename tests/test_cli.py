import subprocess
import sys

def test_cli_observation_commands():
    res = subprocess.run([sys.executable, "-m", "usa_signal_bot", "paper-observation-info"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "NOT investment advice" in res.stdout
