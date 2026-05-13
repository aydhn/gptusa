from usa_signal_bot.execution.execution_reporting import execution_limitations_text

def test_reporting():
    text = execution_limitations_text()
    assert "LIMITATIONS" in text
    assert "broker API" in text
