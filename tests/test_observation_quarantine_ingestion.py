from usa_signal_bot.paper_observation.quarantine_ingestion import (
    ingest_quarantine_payload, extract_candidate_id_from_quarantine, extract_ticket_id_from_quarantine,
    extract_quarantine_status, quarantine_payload_supports_observation, quarantine_ingestion_to_text
)

def test_quarantine_ingestion():
    payload = {
        "candidate_id": "c1",
        "ticket_id": "t1",
        "status": "ENROLLED"
    }
    res = ingest_quarantine_payload(payload)
    assert extract_candidate_id_from_quarantine(res) == "c1"
    assert extract_ticket_id_from_quarantine(res) == "t1"
    assert extract_quarantine_status(res) == "ENROLLED"

    supports, _ = quarantine_payload_supports_observation(res)
    assert supports is True

    text = quarantine_ingestion_to_text(res)
    assert "c1" in text

    payload_blocked = {"status": "BLOCKED"}
    supports, _ = quarantine_payload_supports_observation(payload_blocked)
    assert supports is False
