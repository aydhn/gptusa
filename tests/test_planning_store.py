from pathlib import Path
from usa_signal_bot.paper_controlled_planning.planning_store import controlled_planning_store_dir, write_controlled_planning_ticket_json
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket

def test_store(tmp_path):
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    file_path = tmp_path / "ticket.json"
    write_controlled_planning_ticket_json(file_path, t)
    assert file_path.exists()
