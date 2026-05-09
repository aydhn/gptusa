import sys
import subprocess
import pytest

def test_incident_info_cli():
    res = subprocess.run([sys.executable, "-m", "usa_signal_bot", "incident-info"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Incident Response Config" in res.stdout

def test_incident_review_cli():
    res = subprocess.run([sys.executable, "-m", "usa_signal_bot", "incident-review"], capture_output=True, text=True)
    assert res.returncode == 0
