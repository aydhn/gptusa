from usa_signal_bot.paper.paper_analytics_reporting import paper_analytics_limitations_text

def test_limitations_text():
    text = paper_analytics_limitations_text()
    assert "NOT investment advice" in text
    assert "No live broker orders will be issued" in text
