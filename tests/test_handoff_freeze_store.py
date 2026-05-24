import pytest
from pathlib import Path
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_store import handoff_freeze_store_dir, write_final_handoff_freeze_gate_json
from usa_signal_bot.pre_paper_handoff_freeze_gate.final_handoff_freeze_gate import build_default_final_handoff_freeze_gate

def test_handoff_freeze_store_write(tmp_path):
    d = handoff_freeze_store_dir(tmp_path)
    assert d.exists()

    gate = build_default_final_handoff_freeze_gate()
    file_path = d / f"{gate.gate_id}.json"
    write_final_handoff_freeze_gate_json(file_path, gate)
    assert file_path.exists()
