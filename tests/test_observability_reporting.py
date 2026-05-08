from usa_signal_bot.observability.observability_reporting import observability_limitations_text

def test_reporting():
    s = observability_limitations_text()
    assert "NOT an investment advice" in s
