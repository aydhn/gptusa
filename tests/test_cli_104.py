import pytest
from usa_signal_bot.app.cli import lifecycle_info, startup_checks, readiness_gate

# Mock click since it seems cli.py might be using its own
class MockClickEcho:
    def __init__(self):
        self.output = []
    def echo(self, text):
        self.output.append(str(text))

def test_cli_directly(monkeypatch):
    import usa_signal_bot.app.cli as m_cli
    mock_echo = MockClickEcho()
    monkeypatch.setattr(m_cli.click, "echo", mock_echo.echo)

    lifecycle_info()
    assert any("NOT a financial investment advice" in o for o in mock_echo.output)

    mock_echo.output = []
    startup_checks(False)
    assert any("StartupCheckReport" in o for o in mock_echo.output)

    mock_echo.output = []
    readiness_gate(False)
    assert any("Gate Decision" in o for o in mock_echo.output) # More robust check
