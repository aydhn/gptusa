"""Test corporate action loader."""
from pathlib import Path
from usa_signal_bot.corporate_actions.corporate_action_loader import write_example_manual_corporate_actions, load_manual_corporate_actions_from_json

def test_corporate_action_loader(tmp_path):
    p = tmp_path / "actions.json"
    write_example_manual_corporate_actions(p)
    events = load_manual_corporate_actions_from_json(p)
    assert len(events) == 2
