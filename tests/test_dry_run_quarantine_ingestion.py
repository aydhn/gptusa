import pytest
from usa_signal_bot.paper_dry_run_bridge.quarantine_ingestion import (
    ingest_quarantine_review_payload,
    extract_quarantined_candidate_payload,
    extract_quarantine_candidate_id,
    extract_candidate_status,
    quarantine_supports_dry_run_bridge,
    quarantine_ingestion_warnings,
    quarantine_ingestion_to_text
)
from usa_signal_bot.core.enums import QuarantineCandidateStatus

def test_quarantine_ingestion():
    payload = {
        "candidate": {
            "candidate_id": "cand_123",
            "status": QuarantineCandidateStatus.ENROLLED.value
        }
    }

    assert extract_quarantine_candidate_id(payload) == "cand_123"
    assert extract_candidate_status(payload) == QuarantineCandidateStatus.ENROLLED.value

    supports, _ = quarantine_supports_dry_run_bridge(payload)
    assert supports is True

    payload_blocked = {
        "candidate": {
            "candidate_id": "cand_123",
            "status": QuarantineCandidateStatus.BLOCKED.value
        }
    }
    supports, _ = quarantine_supports_dry_run_bridge(payload_blocked)
    assert supports is False

    assert "cand_123" in quarantine_ingestion_to_text(payload)
