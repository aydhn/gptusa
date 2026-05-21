from usa_signal_bot.paper_controlled_planning.planning_reporting import controlled_planning_store_summary_to_text

def test_reporting():
    out = controlled_planning_store_summary_to_text({"tickets_count": 1})
    assert "Tickets: 1" in out
