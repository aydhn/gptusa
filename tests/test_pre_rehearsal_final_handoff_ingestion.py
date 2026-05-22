import pytest
from usa_signal_bot.paper_pre_rehearsal.final_handoff_ingestion import (
    final_handoff_supports_pre_paper_rehearsal, extract_final_handoff_candidate_id
)

def test_ingestion_supports():
    payload = {
        "candidate_id": "c1",
        "pre_paper_checkpoint": {"decision": "PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL"},
        "sealed_archive_manifest": {"archive_id": "a1"}
    }
    supports, warnings = final_handoff_supports_pre_paper_rehearsal(payload)
    assert supports is True
    assert len(warnings) == 0

    assert extract_final_handoff_candidate_id(payload) == "c1"
