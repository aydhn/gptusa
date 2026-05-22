import pytest
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_audit import create_pre_paper_audit_entry

def test_audit():
    entry = create_pre_paper_audit_entry("Type", "1", "Act", "Rat")
    assert entry.entity_type == "Type"
