from usa_signal_bot.paper_shadow.shadow_reporting import paper_shadow_limitations_text

def test_paper_shadow_limitations_text():
    text = paper_shadow_limitations_text()
    assert "simulated environment only" in text
    assert "NO real orders are sent to any broker" in text
