import pytest
from usa_signal_bot.paper_shadow.sandbox_ingestion import (
    ingest_sandbox_review_payload,
    extract_sandbox_context_payload,
    extract_sandbox_bundle_refs,
    extract_sandbox_preview_outputs,
    sandbox_ingestion_warnings,
    sandbox_ingestion_to_text
)

def test_sandbox_ingestion():
    payload = {
        "sandbox_id": "test_sandbox",
        "bundle_id": "test_bundle",
        "bundle_version": "1.0",
        "context": {"key": "val"},
        "outputs": [{"result": "pass"}]
    }

    ingested = ingest_sandbox_review_payload(payload.copy())
    assert "warnings" not in ingested or not ingested["warnings"]

    ctx = extract_sandbox_context_payload(payload)
    assert ctx == {"key": "val"}

    refs = extract_sandbox_bundle_refs(payload)
    assert refs["source_sandbox_id"] == "test_sandbox"
    assert refs["source_bundle_id"] == "test_bundle"

    outs = extract_sandbox_preview_outputs(payload)
    assert outs == [{"result": "pass"}]

    payload_bad = {"safety_flags": ["UNSAFE_FLAG"]}
    warns = sandbox_ingestion_warnings(payload_bad)
    assert len(warns) == 2 # missing context + unsafe flag

    text = sandbox_ingestion_to_text(payload)
    assert "Sandbox Ingestion Summary" in text
