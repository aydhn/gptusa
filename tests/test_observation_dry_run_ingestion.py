from usa_signal_bot.paper_observation.dry_run_ingestion import (
    ingest_dry_run_bridge_review, extract_dry_run_sessions, extract_dry_run_session_ids,
    extract_human_checkpoints, extract_bridge_telemetry_events, dry_run_ingestion_warnings, dry_run_ingestion_to_text
)

def test_dry_run_ingestion():
    payload = {
        "sessions": [{"session_id": "s1"}],
        "checkpoints": [{"checkpoint_id": "cp1"}],
        "telemetry_events": [{"event_type": "BLOCKED_OPERATION"}],
        "blocked_operation_count": 1
    }

    res = ingest_dry_run_bridge_review(payload)
    assert len(extract_dry_run_sessions(res)) == 1
    assert "s1" in extract_dry_run_session_ids(res)
    assert len(extract_human_checkpoints(res)) == 1
    assert len(extract_bridge_telemetry_events(res)) == 1

    warnings = dry_run_ingestion_warnings(res)
    assert any("Blocked operations" in w for w in warnings)

    text = dry_run_ingestion_to_text(res)
    assert "Dry-run Bridge Review" in text
